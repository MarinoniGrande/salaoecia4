from django.db import models
import salaoecia.accounts.models

# Create your models here.


class Salao(models.Model):
    is_caixa_aberto = models.BooleanField(default=False, null=True)
    usr_edicao = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING, null=True)
    dat_edicao = models.DateTimeField(null=True, auto_now=True)


class Servicos(models.Model):
    nome = models.CharField(max_length=200, null=True)
    status = models.BooleanField(default=True, null=True)
    valor = models.DecimalField(max_digits=14, decimal_places=2, null=True)


class Horario(models.Model):
    hora = models.CharField(max_length=200, null=True)
    hora_int = models.IntegerField(null=True)
    status = models.BooleanField(default=True, null=True)


class Agendamento(models.Model):
    cliente = models.ForeignKey(salaoecia.accounts.models.User, on_delete=models.DO_NOTHING, null=True)
    data = models.DateField(null=True)
    horario = models.ForeignKey('Horario', on_delete=models.DO_NOTHING, null=True)
    valor = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    is_pago = models.BooleanField(default=False, null=True)
    funcionario = models.ForeignKey(salaoecia.accounts.models.User, on_delete=models.DO_NOTHING, null=True, related_name='funcionario')
    status = models.BooleanField(default=True, null=True)
    servicos = models.ManyToManyField(through_fields=('agendamento', 'servico'), through='AgendamentoServicos', to='Servicos')
    funcionario_cancelou = models.ForeignKey(salaoecia.accounts.models.User, on_delete=models.DO_NOTHING, null=True, related_name='funcionario_cancelou')
    motivo = models.ForeignKey('MotivosAgendamento', on_delete=models.DO_NOTHING, null=True)


class AgendamentoServicos(models.Model):
    agendamento = models.ForeignKey('Agendamento', on_delete=models.DO_NOTHING, null=True)
    servico = models.ForeignKey('Servicos', on_delete=models.DO_NOTHING, null=True)


class MotivosAgendamento(models.Model):
    nome = models.CharField(max_length=200, null=True)
    status = models.BooleanField(default=True, null=True)


class ProdutoUnidadeComercial(models.Model):
    nome = models.CharField(max_length=200, null=True)
    unidade = models.CharField(max_length=200, null=True)
    status = models.BooleanField(null=True, default=True)


class Produto(models.Model):
    status = models.BooleanField(null=True, default=True)
    dat_insercao = models.DateTimeField(auto_now_add=True)
    ean = models.CharField(max_length=200, null=True)
    descricao = models.CharField(max_length=200, null=True)
    nome = models.CharField(max_length=200, null=True)
    unidade_comercial = models.ForeignKey('ProdutoUnidadeComercial', on_delete=models.DO_NOTHING, null=True)
    estoque_minimo = models.IntegerField(null=True)
    estoque_inicial = models.IntegerField(null=True)
    estoque_atual = models.IntegerField(null=True)
    estoque_atualizado = models.IntegerField(null=True)
    valor_revenda = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    valor_revenda2 = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    tipo = models.CharField('Tipo', max_length=30, default='Tintura', choices=(
        ('Tintura', 'Tintura'),
        ('Escova', 'Escova'),
        ('Lavagem', 'Lavagem'),
        ('Corte', ' Corte'),)

                            )


class Compra(models.Model):
    cliente = models.ForeignKey(salaoecia.accounts.models.User, on_delete=models.DO_NOTHING, null=True)
    pagamento = models.CharField(max_length=200, null=True)
    vlr_total = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    vlr_recebido = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    vlr_troco = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    parcela = models.IntegerField(null=True, default=1)
    vlr_parcelado = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    cpf_na_nota = models.CharField(max_length=200, null=True)


class CompraAgendamento(models.Model):
    agendamento = models.ForeignKey('Agendamento', on_delete=models.DO_NOTHING, null=True)
    compra = models.ForeignKey('Compra', on_delete=models.DO_NOTHING, null=True)


class CompraProduto(models.Model):
    produto = models.ForeignKey('Produto', on_delete=models.DO_NOTHING, null=True)
    compra = models.ForeignKey('Compra', on_delete=models.DO_NOTHING, null=True)