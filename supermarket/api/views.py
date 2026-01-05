from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MarketSerializer
from supermarket.models import Market

@api_view(['GET', 'POST'])
def markets_view(request):
    if request.method == 'GET':
        markets = Market.objects.all()
        serializer = MarketSerializer(markets, many=True)
        return Response(serializer.data)
    
    
    if request.method == 'POST':
        try:
            msg = request.data['message']
            return Response({"your_message": msg}, status=status.HTTP_201_CREATED)
        except:    
            return Response({"your_message": "error"},status=status.HTTP_400_BAD_REQUEST)
        

            
