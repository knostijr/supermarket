from rest_framework import serializers
from supermarket.models import Market, Seller

#Er wandelt Django-Objekte (z. B. Model-Instanzen) in JSON um, 
#damit sie über eine API ausgeliefert werden können.

#Der Serializer prüft:
#Datentypen
#Pflichtfelder
#Längen
#Eigene Geschäftslogik


# fehler validierung, außerhalb der Klasse, da flexibler
def validate_no_x(value):
        errors = []
    
        if 'X' in value:
            errors.append('no x in location')
        if 'Y' in value:
            errors.append('no y in location')
        if errors:
            raise serializers.ValidationError(errors)
        return value

class MarketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255, validators=[validate_no_x])
    description = serializers.CharField()
    net_worth = serializers.DecimalField(max_digits=100, decimal_places=2)
    
    #dynamische Datenuebergabe
    def create(self, validated_data):
        return Market.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get('location', instance.location)
        instance.description = validated_data.get('description', instance.description)
        instance.net_worth = validated_data.get('net_worth', instance.net_worth)
        instance.save()
        return instance
    
class SellerDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    markets = MarketSerializer(many=True, read_only=True)
    
class SellerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    markets = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    
    def validate_markets(self, value):
        markets = Market.objects.filter(id_in=value)
        if(markets) != len(value):
            raise serializers.ValidationError("one or more markets ids not found")
        return 
    
    def create(self, validated_data):
        market_id = validated_data.pop('markets')
        seller = Seller.objects.create(**validated_data)
        markets = Market.objects.filter(id_in=market_id)
        seller.market.set(markets)
        return seller