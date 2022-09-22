from rest_framework import serializers
from logistic.models import Product, StockProduct, Stock

class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=60)
    description = serializers.CharField()
    # настройте сериализатор для продукта
    class Meta:
        model = Product
        fields = '__all__'


class StockProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    quantity = serializers.IntegerField(default=1)
    price = serializers.DecimalField(max_digits=18, decimal_places=2)
    class Meta:
        model = StockProduct
        fields =['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = StockProductSerializer(many=True)

    class Meta:
        model = Stock
        fields =  ['address', 'positions']

    def create(self, validated_data):

        positions_data = validated_data.pop('positions')
        stock = Stock.objects.create(**validated_data)
        for position in positions_data:
            StockProduct.objects.create(stock=stock, **position)
        return stock


    def update(self, instance, validated_data):

        positions_data = validated_data.pop('positions')
        instance = super(StockSerializer, self).update(instance, validated_data)

        for position_new in positions_data:
            position_instance =  StockProduct.objects.filter(stock_id=instance.id, product_id=position_new['product'].id)
            if  position_instance.exists():
                positions_old = position_instance.first()
                positions_old.price = position_new['price']
                positions_old.quantity = position_new['quantity']
                positions_old.product_id = position_new['product'].id
                positions_old.save()
            else:
                positions = StockProduct.objects.create(**position_new)

        instance.save()
        return instance

