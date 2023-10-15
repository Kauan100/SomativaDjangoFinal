from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path
urlpatterns = [
  path('estoque', ChecaEstoque.as_view())
]
router = DefaultRouter()
router.register(r'categoriaservico',CategoriaServicoView)
router.register(r'produtos',ProdutosView)
router.register(r'automoveis',AutomoveisView)
router.register(r'customUser',CustomUserView)
router.register(r'manutencao',ManutencaoView)
router.register(r'pagamento',PagamentoView)
router.register(r'reservas',ReservasView)

urlpatterns += router.urls