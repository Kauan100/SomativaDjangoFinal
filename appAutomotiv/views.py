from django.shortcuts import render
from .models import *
from .serializers import *
from .customFilters import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAdminUser, IsAuthenticated


def strToDate(strDate):
    return datetime.strptime(strDate, '%Y-%m-%d').date()

class CustomModelViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# Create your views here.

class CategoriaServicoView(CustomModelViewSet):
    queryset = CategoriaServico.objects.all()
    serializer_class = CategoriaServicoSerializer
    permission_classes = (IsAdminUser, )

class ProdutosView(CustomModelViewSet):
    queryset = Produtos.objects.all()
    serializer_class = ProdutosSerializer
    permission_classes = (IsAdminUser, )

class AutomoveisView(CustomModelViewSet):
    queryset = Automoveis.objects.all()
    serializer_class = AutomoveisSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = Automoveis
    ordering_fields = '__all__'
    permission_classes = (IsAdminUser, )

class CustomUserView(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CustomUserFilter
    ordering_fields = '__all__'
    permission_classes = (IsAuthenticated, )
    def get_queryset(self):
        user = self.request.user
        queryset = None
        if user.is_superuser:
            queryset = CustomUser.objects.all()
        else:
            queryset = CustomUser.objects.filter(user__username=user.username)
        return queryset 

class ManutencaoView(CustomModelViewSet): 
    queryset = Manutencao.objects.all()
    serializer_class = ManutencaoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = '__all__'
    permission_classes = (IsAuthenticated, )
    def create(self, request, *args, **kwargs):
        manutencao = request.data
        produto = request.data['produtosFK']
        produtoModel = Produtos.objects.get(id=produto)
        produtoSerializado = ProdutosSerializer(produtoModel)
        produtoSerializado.data['quantidadeEstoque'] = int(produtoSerializado.data['quantidadeEstoque'])-1
        produtoSerializadoPython = ProdutosSerializer(data=produtoSerializado.data,many=False)
        produtoSerializadoPython.save()
        ManutencaoSerializado = ManutencaoSerializer(data=manutencao,many=False)
        ManutencaoSerializado.is_valid(raise_exception=True)
        ManutencaoSerializado.save()
        return Response(ManutencaoSerializado.data)
    
class PagamentoView(CustomModelViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer
    permission_classes = (IsAuthenticated, )
    def get_queryset(self):
        user = self.request.user
        queryset = None
        if user.is_superuser:
            queryset = Pagamento.objects.all()
        else:
            queryset = Pagamento.objects.filter(customUserFK__user__username=user.username)
        return queryset 

class ReservasView(CustomModelViewSet):
    queryset = Reservas.objects.all()
    serializer_class = ReservasSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = '__all__'
    permission_classes = (IsAdminUser, )
    
class ChecaEstoque(APIView):
    def get(self, request):
        produtos = Produtos.objects.filter(quantidadeEstoque__lt=4)
        produtosSerializado = ProdutosSerializer(produtos)
        return Response(produtosSerializado.data)