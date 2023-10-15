from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','is_superuser','first_name','last_login')
        many = True

class CustomUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = '__all__'
        many = True

class CategoriaServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaServico
        fields = '__all__'
        many = True

class ProdutosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produtos
        fields = '__all__'
        many = True

class AutomoveisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Automoveis
        fields = '__all__'
        many = True

class ManutencaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manutencao
        fields = '__all__'
        many = True

class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = '__all__'
        many = True

class ReservasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservas
        fields = '__all__'
        many = True