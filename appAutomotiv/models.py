from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
import datetime
# Create your models here.

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=500)
    taxId = models.CharField(max_length=30)
    cellphone = models.CharField(max_length=30)
    is_customer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_user_custom(sender, instance, created, **kwargs):
    if created:
        CustomUser.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_custom(sender, instance, created, **kwargs):
    instance.customuser.save()

class CategoriaServico(models.Model):
    name = models.CharField(max_length=200)
    valorMaoObra = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.name
    
class Produtos(models.Model):
    name = models.CharField(max_length=200)
    quantidadeEstoque = models.IntegerField
    codigoFabricante = models.CharField(max_length=200)
    nomeFabricante = models.CharField(max_length=200)
    valorCompra = models.DecimalField(max_digits=10,decimal_places=2)
    valorVenda = models.DecimalField(max_digits=10,decimal_places=2)
    
    def __str__(self):
        return self.name
    

class Automoveis (models.Model):
    categoria = models.CharField(max_length=200)
    marca = models.CharField(max_length=200)
    modelo = models.CharField(max_length=200)
    ano = models.DateField
    
    def __str__(self):
        return self.categoria
    
class Manutencao (models.Model):
    automoveisFK = models.ForeignKey(Automoveis, related_name='automoveisFKManutencao', on_delete=models.CASCADE)
    categoriaservicoFK = models.ForeignKey(CategoriaServico, related_name='categoriaservicoFKManutencao', on_delete=models.CASCADE)
    produtosFK = models.ForeignKey(Produtos, related_name='produtosFKManutencao', on_delete=models.CASCADE)
    valorTotal =  models.DecimalField(max_digits=10, decimal_places=2)
    customUserFK = models.ForeignKey(CustomUser, related_name='customUserFKManutencao', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.valorTotal
    
    def __save__(self, *args, **kwargs):
        self.valorTotal = self.categoriaservicoFK__valorMaoObra + self.produtosFK__valorVenda
        super(Manutencao, self).save(*args, **kwargs)
    
class Pagamento(models.Model) :
    Fpagamento = (
    ('pix', 'pix'),
    ('boleto', 'boleto'),
    ('cartão de crédito', 'cartão de crédito'),
    ('cartão de débito', 'cartão de débito'),
    ('Dinheiro em espécie', 'Dinheiro em espécie'),
    ('Transferência bancária', 'Transferência bancária'),
)
    formaPagamento = models.CharField(max_length=100, choices=Fpagamento)
    customUserFK = models.ForeignKey(CustomUser, related_name='customUserFKPagamento', on_delete=models.CASCADE)
    manutencaoFK = models.ForeignKey(Manutencao, related_name='manutencaoFKPagamento', on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)
    numeroNota = models.CharField(max_length=500, null=False)
    status = (
    ('pendente', 'pendente'),
    ('aprovado', 'aprovado'),
    ('recusado', 'recusado'),
)
    status = models.CharField(max_length=100, choices=status)
    valorDesconto = models.DecimalField(max_digits=10,decimal_places=2)
    valorFinal =  models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.numeroNota
    
    def __save__(self, *args, **kwargs):
        self.valorFinal = self.manutencaoFK__valorTotal - self.valorDesconto
        super(Pagamento, self).save(*args, **kwargs)
    
class Reservas(models.Model) :
    customUserFK = models.ForeignKey(CustomUser, related_name='customUserFKReservas', on_delete=models.CASCADE)
    data = models.DateField(default=datetime.date.today())
    manutencaoFK = models.ForeignKey(Manutencao, related_name='manutencaoFKReservas', on_delete=models.CASCADE)
    
    postoTrabalho = (
    ('posto1', 'posto1'),
    ('posto2', 'posto2'),
)
    postoTrabalho = models.CharField(max_length=100, choices=postoTrabalho)
    
    def __str__(self):
        return self.data
    
    
    
    