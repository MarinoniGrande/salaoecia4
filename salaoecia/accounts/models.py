import re
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, UserManager)
from django.core import validators
from django.conf import settings


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Nome de Usuário', max_length=30, unique=True,
                                validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'), 'Nome de usuário inválido', 'invalid')])
    email = models.EmailField('E-mail', unique=True)
    name = models.CharField('Nome completo', max_length=100, blank=True)
    birth = models.DateField('Data de nascimento', null=True)
    is_active = models.BooleanField('Está ativo?', blank=True, default=True)
    is_staff = models.BooleanField('É admin?', blank=True, default=False)
    is_admin = models.BooleanField('Administrador do sistema', blank=True, default=False)
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)

    tentativas_login = models.IntegerField(null=True)
    is_bloqueado = models.BooleanField(null=True, default=True)
    perc_comissao = models.DecimalField(max_digits=14, decimal_places=2, null=True)

    address = models.CharField('Endereço', max_length=50, null=True)
    number = models.CharField('Número', max_length=5, null=True)
    complement = models.CharField('Complemento', max_length=30, null=True)
    neighborhood = models.CharField('Bairro', max_length=30, null=True)
    zip_code = models.CharField('CEP', max_length=20, null=True)
    city = models.CharField('Cidade', max_length=30, null=True)
    state = models.CharField('Estado',
                             max_length=2,
                             default='PR',
                             null=True,
                             choices=(
                                 ('AC', 'Acre'),
                                 ('AL', 'Alagoas'),
                                 ('AP', 'Amapá'),
                                 ('AM', 'Amazonas'),
                                 ('BA', 'Bahia'),
                                 ('CE', 'Ceará'),
                                 ('DF', 'Distrito Federal'),
                                 ('ES', 'Espírito Santo'),
                                 ('GO', 'Goiás'),
                                 ('MA', 'Maranhão'),
                                 ('MT', 'Mato Grosso'),
                                 ('MS', 'Mato Grosso do Sul'),
                                 ('MG', 'Minas Gerais'),
                                 ('PA', 'Pará'),
                                 ('PB', 'Paraíba'),
                                 ('PR', 'Paraná'),
                                 ('PE', 'Pernambuco'),
                                 ('PI', 'Piauí'),
                                 ('RJ', 'Rio de Janeiro'),
                                 ('RN', 'Rio Grande do Norte'),
                                 ('RS', 'Rio Grande do Sul'),
                                 ('RO', 'Rondônia'),
                                 ('RR', 'Roraima'),
                                 ('SC', 'Santa Catarina'),
                                 ('SP', 'São Paulo'),
                                 ('SE', 'Sergipe'),
                                 ('TO', 'Tocantins'),)
                             )
    fx_salario = models.CharField('Faixa salario', max_length=30, default='Faixa 1', choices=(
        ('Faixa 1', '0-1000'),
        ('Faixa 2', '1001-3000'),
        ('Faixa 3', '3001-5000'),
        ('Faixa 4', '> 5000'),)

                                  )

    sexo = models.CharField('Sexo', max_length=1, default='M', null=True, choices=(
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),)
                            )
    cpf = models.CharField(max_length=20, blank=True, null=True)

    telefone = models.CharField(max_length=200, blank=True, null=True)
    tipo_telefone = models.CharField(max_length=15, blank=True, null=True)
    confirmacao_agendamentos = models.IntegerField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.name or self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return str(self)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


class Funcionario(models.Model):
    matricula = models.CharField(max_length=200, null=True)
    cargo = models.ForeignKey('Cargo', on_delete=models.DO_NOTHING, null=True)
    contrato_trabalho = models.ForeignKey('TipoContrato', on_delete=models.DO_NOTHING, null=True)
    data_ini = models.DateField(null=True)
    tempo_contrato = models.ForeignKey('TempoContrato', on_delete=models.DO_NOTHING, null=True)
    usuario = models.OneToOneField('User', on_delete=models.DO_NOTHING, null=True, related_name='usuario')
    valor_contrato = models.DecimalField(max_digits=14, decimal_places=2, null=True)


class TempoContrato(models.Model):
    nome = models.CharField(max_length=200, null=True)
    dias = models.IntegerField(null=True)


class TipoContrato(models.Model):
    nome = models.CharField(max_length=200, null=True)


class PasswordReset(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=models.DO_NOTHING,
                             related_name='resets')
    key = models.CharField('Chave', max_length=100, unique=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    confirmed = models.BooleanField('Confirmado?', default=False, blank=True)

    def __str__(self):
        return '{0} em {1}'.format(self.user, self.created_at)

    class Meta:
        verbose_name = 'Nova Senha'
        verbose_name_plural = 'Novas Senhas'
        ordering = ['-created_at']


class Cargo(models.Model):
    nome = models.CharField(max_length=200, null=True)
