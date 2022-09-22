from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, BaseFilterBackend
from logistic.models import Product, Stock, StockProduct
from logistic.serializers import ProductSerializer, StockSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend


class CategoryPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 5



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CategoryPagination
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    pagination_class = CategoryPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_fields = ['positions']
    search_fields = ['address']

    def get_queryset(self):
        qs = super().get_queryset()
        query_set = self.request.query_params.get('product')
        qs = Stock.objects.filter(positions__product__title__contains=query_set)
        return qs

