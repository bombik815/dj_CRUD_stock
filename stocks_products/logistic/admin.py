from django.contrib import admin
from logistic.models import Product, Stock, StockProduct
from django.forms import BaseInlineFormSet
# Register your models here.


class StockProductInline(admin.TabularInline):
    model = StockProduct
    extra = 0


@admin.register(Product)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'description')
    list_display_links = ('id','title')

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('id','address', )
    list_display_links = ('id','address')
    inlines = (StockProductInline,)

@admin.register(StockProduct)
class StockProductInline(admin.ModelAdmin):
    list_display = ('stock', 'product', 'quantity', 'price')
