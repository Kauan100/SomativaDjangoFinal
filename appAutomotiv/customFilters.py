from rest_framework import filters
import django_filters
from .models import *

class CustomUserFilter(django_filters.FilterSet):
  type = django_filters.CharFilter(lookup_expr='icontains')
  taxId = django_filters.CharFilter(lookup_expr='iexact')
  class Meta:
    model = CustomUser
    fields = ['type','taxId']
    
class ProdutosFilter(django_filters.FilterSet):
  quantidadeEstoque = django_filters.RangeFilter()
  valorCompra = django_filters.RangeFilter()
  valorVenda = django_filters.RangeFilter()
  class Meta:
    model = Produtos
    fields = ['quantidadeEstoque','valorCompra','valorVenda']

class AutomoveisFilter(django_filters.FilterSet):
  marca = django_filters.CharFilter(lookup_expr='icontains')
  modelo = django_filters.CharFilter(lookup_expr='icontains')
  class Meta:
    model = Automoveis
    fields = ['marca','modelo']