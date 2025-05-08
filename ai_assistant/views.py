from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from openai import OpenAI
from django.conf import settings
from products.models import Product
from difflib import SequenceMatcher
from products.serializers import ProductSerializer

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def is_similar(a, b, threshold=0.5):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() >= threshold

class AIQueryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        query = request.data.get('query', '')
        if not query:
            return Response({"error": "Query not provided"}, status=400)

        products = Product.objects.select_related('brand', 'subcategory').prefetch_related('attributes').all()
        descriptions = [f"{p.name} - {p.description}" for p in products if p.description]

        openai_messages = [
            {
                "role": "system",
                "content": (
                    "You are Medzy AI, a medical assistant that understands a user's symptoms "
                    "and recommends suitable medicines from the database provided."
                ),
            },
            {
                "role": "user",
                "content": f"User said: {query}\n\nHere is the product database:\n{chr(10).join(descriptions)}",
            },
        ]

        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=openai_messages,
                temperature=0.2,
            )
            answer = response.choices[0].message.content.strip()

            recommended_products = []
            response_lower = answer.lower()

            for product in products:
                if product.name.lower() in response_lower:
                    recommended_products.append(
                        ProductSerializer(product, context={'request': request}).data
                    )

            return Response({
                "response": answer,
                "recommended_products": recommended_products
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)
