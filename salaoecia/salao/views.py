import datetime

from django.db.models import Count
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils import timezone
from django.views.generic.base import View
from django.http import JsonResponse, HttpResponseRedirect
import salaoecia.accounts.models
import salaoecia.salao.models
from salaoecia import salao
import json
#from datetime import datetime


class AgendamentoView(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_staff:
            return HttpResponseRedirect(reverse("salao.gerenciar.agendamento"))

        current_user = 'valor novo'
        funcionarios = salaoecia.accounts.models.User.objects.all().filter(is_staff=True).order_by('name')
        servicos = salaoecia.salao.models.Servicos.objects.all().filter(status=True).order_by('nome')
        horarios = salaoecia.salao.models.Horario.objects.all().filter(status=True).order_by('hora_int')
        todos_agendamentos = salaoecia.salao.models.Agendamento.objects.all().filter(status=True).filter(cliente_id=self.request.user.id)
        context = {
            'servicos': servicos,
            'horarios': horarios,
            'funcionarios': funcionarios,
            'current_user': current_user,
            'cadastro': False,
            'todos_agendamentos': todos_agendamentos
        }
        return render(self.request, 'salao/agendamento.html', context)

    def post(self, *args, **kwargs):
        erro = False
        descricao = None
        funcionario = self.request.POST.get('profissional-agendamento')
        servicos_selecionados = self.request.POST.getlist('servicos-agendamento')
        if len(servicos_selecionados) == 0:
            erro, descricao = True, 'servicos'
        horario = self.request.POST.get('horarios-agendamento')
        if horario in ['', None]:
            erro, descricao = True, 'horario'
        dia = self.request.POST.get('data-agendamento-input')
        if dia in ['', None]:
            erro, descricao = True, 'dia'

        if not erro:
            novo_agendamento = salaoecia.salao.models.Agendamento()
            novo_agendamento.funcionario_id = funcionario if funcionario not in ['', None] else None
            novo_agendamento.horario_id = horario
            novo_agendamento.data = datetime.datetime.strptime(dia, "%d/%m/%Y").date()
            novo_agendamento.cliente = self.request.user
            novo_agendamento.save()

            novos_servicos = []
            servicos_cobrados = salaoecia.salao.models.Servicos.objects.all().filter(status=True).filter(id__in=[int(x) for x in servicos_selecionados]).order_by('nome')
            valor = 0
            for s in servicos_cobrados:
                valor += s.valor if s.valor is not None else 0
                novo_servico = salaoecia.salao.models.AgendamentoServicos(
                    agendamento_id=novo_agendamento.id,
                    servico_id=s.id
                )
                novos_servicos.append(novo_servico)
            salaoecia.salao.models.AgendamentoServicos.objects.bulk_create(novos_servicos)
            novo_agendamento.valor = valor
            novo_agendamento.save()
            return HttpResponseRedirect(reverse("salao.agendamento"))

        funcionarios = salaoecia.accounts.models.User.objects.all().filter(is_staff=True).order_by('name')
        servicos = salaoecia.salao.models.Servicos.objects.all().filter(status=True).order_by('nome')
        horarios = salaoecia.salao.models.Horario.objects.all().filter(status=True).order_by('hora_int')
        todos_agendamentos = salaoecia.salao.models.Agendamento.objects.all().filter(status=True)
        context = {
            'erro': erro,
            'descricao': descricao,
            'funcionario_selecionado': funcionario,
            'servicos_selecionados': servicos_selecionados,
            'horario_selecionado': horario,
            'dia_selecionado': dia,
            'servicos': servicos,
            'horarios': horarios,
            'funcionarios': funcionarios,
            'todos_agendamentos': todos_agendamentos,
            'cadastro': True
        }
        return render(self.request, 'salao/agendamento.html', context)


class CaixaView(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseRedirect(reverse("salao.agendamento"))

        caixa = salaoecia.salao.models.Salao.objects.all().order_by('-id').first()

        context = {
            'caixa': caixa
        }
        return render(self.request, 'salao/caixa.html', context)


class GerenciarAgendamentoView(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseRedirect(reverse("salao.agendamento"))

        funcionarios = salaoecia.accounts.models.User.objects.all().filter(is_staff=True).order_by('name')
        servicos = salaoecia.salao.models.Servicos.objects.all().filter(status=True).order_by('nome')
        horarios = salaoecia.salao.models.Horario.objects.all().filter(status=True).order_by('hora_int')
        motivos = salaoecia.salao.models.MotivosAgendamento.objects.all().filter(status=True).order_by('nome')
        context = {
            'servicos': servicos,
            'horarios': horarios,
            'funcionarios': funcionarios,
            'motivos': motivos,
            'cadastro': False,
        }

        return render(self.request, 'salao/gerenciar_agendamentos.html', context)

    def post(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseRedirect(reverse("salao.agendamento"))
        erro = False
        descricao = None
        funcionario = self.request.POST.get('profissional-agendamento')
        if funcionario in ['', None]:
            erro, descricao = True, 'funcionario'
        servicos_selecionados = self.request.POST.getlist('servicos-agendamento')
        if len(servicos_selecionados) == 0:
            erro, descricao = True, 'servicos'
        horario = self.request.POST.get('horarios-agendamento')
        if horario in ['', None]:
            erro, descricao = True, 'horario'
        dia = self.request.POST.get('data-agendamento-selecionado')
        if dia in ['', None]:
            erro, descricao = True, 'dia'

        if not erro:
            salaoecia.salao.models.AgendamentoServicos.objects.all().filter(agendamento_id=self.request.POST.get('id-agendamento-input')).delete()
            novo_agendamento = salaoecia.salao.models.Agendamento.objects.filter(id=self.request.POST.get('id-agendamento-input')).first()
            novo_agendamento.funcionario_id = funcionario
            novo_agendamento.horario_id = horario
            novo_agendamento.data = datetime.datetime.strptime(dia, "%Y-%m-%d").date()
            novo_agendamento.cliente = self.request.user
            novo_agendamento.save()

            novos_servicos = []
            servicos_cobrados = salaoecia.salao.models.Servicos.objects.all().filter(status=True).filter(id__in=[int(x) for x in servicos_selecionados]).order_by('nome')
            valor = 0
            for s in servicos_cobrados:
                valor += s.valor if s.valor is not None else 0
                novo_servico = salaoecia.salao.models.AgendamentoServicos(
                    agendamento_id=novo_agendamento.id,
                    servico_id=s.id
                )
                novos_servicos.append(novo_servico)
            salaoecia.salao.models.AgendamentoServicos.objects.bulk_create(novos_servicos)
            novo_agendamento.valor = valor
            novo_agendamento.save()
            return HttpResponseRedirect(reverse("salao.gerenciar.agendamento"))

        funcionarios = salaoecia.accounts.models.User.objects.all().filter(is_staff=True).order_by('name')
        servicos = salaoecia.salao.models.Servicos.objects.all().filter(status=True).order_by('nome')
        horarios = salaoecia.salao.models.Horario.objects.all().filter(status=True).order_by('hora_int')
        motivos = salaoecia.salao.models.MotivosAgendamento.objects.all().filter(status=True).order_by('nome')
        context = {
            'erro': erro,
            'descricao': descricao,
            'funcionario_selecionado': funcionario,
            'servicos_selecionados': servicos_selecionados,
            'horario_selecionado': horario,
            'dia_selecionado': dia,
            'servicos': servicos,
            'horarios': horarios,
            'funcionarios': funcionarios,
            'motivos': motivos,
            'cadastro': True
        }
        return render(self.request, 'salao/agendamento.html', context)


class AtualizarAgendamentoView(View):
    def post(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseRedirect(reverse("salao.agendamento"))

        data = datetime.datetime.strptime(self.request.POST.get('data'), "%Y-%m-%d").date()
        agendamentos = list(salaoecia.salao.models.Agendamento.objects.all().filter(status=True, data=data))
        context = {
            'agendamentos': agendamentos
        }
        return render(self.request, 'salao/tabela.html', context=context)


class PegarAgendamentoView(View):
    def post(self, *args, **kwargs):

        agendamento_id = self.request.POST.get('agendamento_id')
        agendamento = salaoecia.salao.models.Agendamento.objects.values('horario_id', 'funcionario_id', 'data', 'id').filter(status=True, id=agendamento_id).first()
        servicos = list(salaoecia.salao.models.AgendamentoServicos.objects.values('servico_id').filter(agendamento_id=agendamento_id))
        context = {
            'agendamento': agendamento,
            'servicos': servicos
        }
        return JsonResponse(context, safe=False)


class CancelarAgendamentoView(View):
    def post(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseRedirect(reverse("salao.agendamento"))

        agendamento_id = self.request.POST.get('agendamento_id')
        motivo_id = self.request.POST.get('motivo_id')
        agendamento = salaoecia.salao.models.Agendamento.objects.all().filter(status=True, id=agendamento_id).first()
        agendamento.status = False
        agendamento.motivo_id = motivo_id
        agendamento.funcionario_cancelou = self.request.user
        agendamento.save()
        context = {
            'status': True
        }
        return JsonResponse(context, safe=False)


class GestaoEstoqueView(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseRedirect(reverse("salao.agendamento"))

        produtos = salaoecia.salao.models.Produto.objects.values('estoque_atual', 'ean', 'dat_insercao', 'nome', 'id', 'status').order_by('nome')
        context = {
            'produtos': produtos
        }
        return render(self.request, 'salao/estoque.html', context)


class GestaoEstoqueLeituraView(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseRedirect(reverse("salao.agendamento"))
        produtos = salaoecia.salao.models.Produto.objects.values('estoque_atual', 'ean', 'dat_insercao', 'nome', 'tipo', 'valor_revenda').order_by('nome')
        context = {
            'produtos': produtos
        }
        return render(self.request, 'salao/estoque_leitura.html', context)


class CadastroProdutoView(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseRedirect(reverse("salao.agendamento"))
        produtos = salaoecia.salao.models.Produto.objects.values('nome', 'id').filter(status=True).order_by('nome')
        unidades = salaoecia.salao.models.ProdutoUnidadeComercial.objects.values('unidade', 'nome', 'id').filter(status=True).order_by('nome')
        context = {
            'produtos': produtos,
            'unidades': unidades
        }
        return render(self.request, 'salao/produto.html', context)

    def post(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseRedirect(reverse("salao.agendamento"))
        operacao = self.request.POST.get('operacao')
        if operacao == 'alterar' or operacao == 'desativar':
            id_produto = self.request.POST.get('select-produto')
            produto_atualizar = salaoecia.salao.models.Produto.objects.all().filter(id=id_produto).first()
            if produto_atualizar is None:
                produtos = salaoecia.salao.models.Produto.objects.values('nome', 'id').filter(status=True).order_by('nome')
                unidades = salaoecia.salao.models.ProdutoUnidadeComercial.objects.values('unidade', 'nome', 'id').filter(status=True).order_by('nome')
                context = {
                    'produtos': produtos,
                    'unidades': unidades,
                    'erro': True,
                    'descricao': 'select-produto'
                }
                return render(self.request, 'salao/produto.html', context)
        else:
            produto_atualizar = salaoecia.salao.models.Produto()
            produto_atualizar.dat_insercao = timezone.now() + timezone.timedelta(hours=-3)

        if operacao == 'desativar':
            produto_atualizar.status = False
            produto_atualizar.save()
            return HttpResponseRedirect(reverse("salao.alterar.produto"))

        produto_atualizar.ean = self.request.POST.get('ean')
        produto_atualizar.nome = self.request.POST.get('nome')
        produto_atualizar.descricao = self.request.POST.get('descricao')
        produto_atualizar.unidade_comercial_id = self.request.POST.get('select-unidade-comercial')
        produto_atualizar.estoque_minimo = self.request.POST.get('estoque-minimo')
        produto_atualizar.estoque_atual = self.request.POST.get('estoque-atual')
        produto_atualizar.valor_revenda2 = self.request.POST.get('valor-revenda')
        produto_atualizar.save()
        if operacao != 'alterar':
            produto_atualizar.dat_insercao = timezone.now() + timezone.timedelta(hours=-3)
        produto_atualizar.save()
        return HttpResponseRedirect(reverse("salao.alterar.produto"))


class AtualizarEstoqueView(View):
    def post(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseRedirect(reverse("salao.agendamento"))
        valores = self.request.POST.get('novos_valores')
        valores = json.loads(valores)
        lista_ids = list(valores.keys())
        produtos = salaoecia.salao.models.Produto.objects.all().filter(status=True, id__in=lista_ids)
        for p in produtos:
            p.estoque_atual = valores[str(p.id)]
            p.save()
        return JsonResponse({}, safe=False)


class CarregarProdutoView(View):
    def post(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseRedirect(reverse("salao.agendamento"))

        produto_id = self.request.POST.get('produto_id')
        produto = salaoecia.salao.models.Produto.objects.values().filter(id=produto_id).first()
        return JsonResponse({'produto': produto}, safe=False)


class CadastroFuncionarioView(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseRedirect(reverse("salao.agendamento"))

        if not self.request.user.is_admin:
            return HttpResponseRedirect(reverse("salao.gerenciar.agendamento"))

        tipos_contratos = list(salaoecia.accounts.models.TipoContrato.objects.values('nome', 'id').order_by('nome'))
        cargos = list(salaoecia.accounts.models.Cargo.objects.values('nome', 'id').order_by('nome'))
        tempos_contratos = list(salaoecia.accounts.models.TempoContrato.objects.values('nome', 'id').order_by('dias'))
        context = {
            'tipos_contratos': tipos_contratos,
            'cargos': cargos,
            'tempos_contratos': tempos_contratos
        }
        return render(self.request, 'salao/funcionario.html', context)

    def post(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseRedirect(reverse("salao.agendamento"))

        if not self.request.user.is_admin:
            return HttpResponseRedirect(reverse("salao.gerenciar.agendamento"))

        is_criar = False
        novo_usuario = salaoecia.accounts.models.User.objects.all().filter(email=self.request.POST.get('email')).first()
        if novo_usuario is None:
            is_criar = True
            novo_usuario = salaoecia.accounts.models.User()

        if is_criar and self.request.POST.get('username') in list(salaoecia.accounts.models.User.objects.values_list('username', flat=True)):
            tipos_contratos = list(salaoecia.accounts.models.TipoContrato.objects.values('nome', 'id').order_by('nome'))
            cargos = list(salaoecia.accounts.models.Cargo.objects.values('nome', 'id').order_by('nome'))
            tempos_contratos = list(salaoecia.accounts.models.TempoContrato.objects.values('nome', 'id').order_by('dias'))
            context = {
                'tipos_contratos': tipos_contratos,
                'cargos': cargos,
                'tempos_contratos': tempos_contratos,
                'erro': True,
                'descricao': 'Já existe um usuário com esse username!'
            }
            return render(self.request, 'salao/funcionario.html', context)

        novo_usuario.email = self.request.POST.get('email')
        novo_usuario.username = self.request.POST.get('username')
        novo_usuario.name = self.request.POST.get('nome')
        novo_usuario.birth = datetime.datetime.strptime(self.request.POST.get('data-nasc'), '%Y-%m-%d')
        novo_usuario.is_active = True
        novo_usuario.is_staff = True
        novo_usuario.is_admin = False
        novo_usuario.address = self.request.POST.get('rua_endereco_form')
        novo_usuario.number = self.request.POST.get('numero')
        novo_usuario.neighborhood = self.request.POST.get('bairro_endereco_form')
        novo_usuario.zip_code = self.request.POST.get('cep')
        novo_usuario.city = self.request.POST.get('cidade-hidden')
        novo_usuario.sexo = self.request.POST.get('select-sexo')
        novo_usuario.cpf = self.request.POST.get('cpf')
        novo_usuario.telefone = self.request.POST.get('telefone')
        novo_usuario.tipo_telefone = self.request.POST.get('select-tipo')
        novo_usuario.confirmacao_agendamentos = self.request.POST.get('confirmacao')
        novo_usuario.state = self.request.POST.get('estado-hidden')

        novo_usuario.save()
        if novo_usuario.password is None:
            novo_usuario.set_password(raw_password=self.request.POST.get('cpf'))
            novo_usuario.save()
        try:
            novo_funcionario = salaoecia.accounts.models.Funcionario(
                matricula=self.request.POST.get('matricula'),
                cargo_id=self.request.POST.get('select-cargo'),
                contrato_trabalho_id=self.request.POST.get('select-tipo-contrato'),
                data_ini=datetime.datetime.strptime(self.request.POST.get('data-ini'), '%Y-%m-%d'),
                tempo_contrato_id=self.request.POST.get('select-tempo'),
                usuario_id=novo_usuario.id,
                valor_contrato=float(self.request.POST.get('valor').replace('.', '').replace(',', '.'))
            )
            novo_funcionario.save()
        except:
            tipos_contratos = list(salaoecia.accounts.models.TipoContrato.objects.values('nome', 'id').order_by('nome'))
            cargos = list(salaoecia.accounts.models.Cargo.objects.values('nome', 'id').order_by('nome'))
            tempos_contratos = list(salaoecia.accounts.models.TempoContrato.objects.values('nome', 'id').order_by('dias'))
            context = {
                'tipos_contratos': tipos_contratos,
                'cargos': cargos,
                'tempos_contratos': tempos_contratos,
                'erro': True,
                'descricao': 'Erro ao criar o funcionário!'
            }
        return HttpResponseRedirect(reverse("salao.quadro.funcionarios"))


class QuadroFuncionarioView(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseRedirect(reverse("salao.agendamento"))

        if not self.request.user.is_admin:
            return HttpResponseRedirect(reverse("salao.gerenciar.agendamento"))

        funcionarios = salaoecia.accounts.models.Funcionario.objects.values('matricula', 'usuario__name', 'data_ini',
                                                                              'cargo__nome', 'contrato_trabalho__nome',
                                                                              'tempo_contrato__nome', 'usuario__cpf', 'usuario__state',
                                                                              'usuario__address', 'usuario__city', 'usuario__zip_code', 'usuario__number', 'usuario__neighborhood'
                                                                            ).order_by(
            'usuario__name')
        context = {
            'funcionarios': funcionarios
        }
        return render(self.request, 'salao/quadro_funcionarios.html', context)


class PegarClientesView(View):
    def post(self, *args, **kwargs):
        return JsonResponse({'clientes': list(salaoecia.accounts.models.User.objects.values('id', 'username', 'cpf', 'name').order_by('name'))}, safe=False)


class PegarInformacoesView(View):
    def post(self, *args, **kwargs):
        cliente_id = self.request.POST.get('cliente_id')
        context = {
            'cliente': salaoecia.accounts.models.User.objects.values('id', 'username', 'cpf', 'name').filter(id=cliente_id).first(),
            'itens': list(salaoecia.salao.models.AgendamentoServicos.objects.values('servico__nome', 'servico__valor').order_by('servico__nome').filter(agendamento__cliente_id=cliente_id, agendamento__is_pago=False, agendamento__status=True))
        }
        return JsonResponse(context, safe=False)


class PegarProdutoView(View):
    def post(self, *args, **kwargs):
        ean = self.request.POST.get('ean')
        context = {
            'produto': salaoecia.salao.models.Produto.objects.values('ean', 'nome', 'valor_revenda2', 'id').filter(ean=ean).first()
        }

        return JsonResponse(context, safe=False)


class FinalizarCompraView(View):
    def post(self, *args, **kwargs):
        produtos = self.request.POST.getlist('produtos_add[]')
        forma_pagamento = self.request.POST.get('forma_pag')
        vlr_total = self.request.POST.get('vlr_total')
        vlr_recebido = self.request.POST.get('vlr_recebido')
        vlr_troco = self.request.POST.get('vlr_troco')
        cliente_id = self.request.POST.get('cliente_id')
        cpf_na_nota = self.request.POST.get('cpf_na_nota')

        try:
            parcela = int(self.request.POST.get('qtd_parcela'))
            vlr_parcelado = vlr_total / parcela
        except:
            parcela = 1
            vlr_parcelado = vlr_total

        nova_compra = salaoecia.salao.models.Compra()
        nova_compra.pagamento = forma_pagamento
        nova_compra.vlr_total = vlr_total
        nova_compra.vlr_recebido = vlr_recebido
        nova_compra.vlr_troco = vlr_troco
        nova_compra.cliente_id = cliente_id
        nova_compra.cpf_na_nota = cpf_na_nota
        nova_compra.parcela = parcela
        nova_compra.vlr_parcelado = vlr_parcelado
        nova_compra.save()

        for agendamento in list(salaoecia.salao.models.Agendamento.objects.all().filter(is_pago=False, status=True, cliente_id=cliente_id)):
            agendamento.is_pago = True
            agendamento.save()
            nova_compraagendamento = salaoecia.salao.models.CompraAgendamento(
                agendamento=agendamento,
                compra=nova_compra
            )
            nova_compraagendamento.save()

        for produto in produtos:
            nova_compraproduto = salaoecia.salao.models.CompraProduto(
                produto_id=produto,
                compra=nova_compra
            )
            nova_compraproduto.save()

        context = {
            'status': True
        }

        return JsonResponse(context, safe=False)


class AbrirCaixaView(View):
    def post(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseRedirect(reverse("salao.agendamento"))

        if not self.request.user.is_admin:
            return HttpResponseRedirect(reverse("salao.gerenciar.agendamento"))

        caixa = salaoecia.salao.models.Salao.objects.all().order_by('-id').first()
        if caixa is not None:
            caixa.is_caixa_aberto = not caixa.is_caixa_aberto if caixa.is_caixa_aberto is not None else True
        caixa.save()
        return JsonResponse({'status': caixa.is_caixa_aberto}, safe=False)


class DashboardView(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_staff:
            template_name = 'salao/dash_funcionario.html'
            informacoes = {
                'agendamentos_hoje': list(salao.models.Agendamento.objects.all().filter(data=timezone.now().date()).order_by('id')),
                'agendamentos_mes': list(salao.models.Agendamento.objects.all().filter(data__gte=timezone.now().date().replace(day=1)).order_by('data')),
                'agendamentos_prestador': list(salao.models.Agendamento.objects.values('funcionario__name').filter(is_pago=True).annotate(qtd=Count('funcionario__name')).order_by('-qtd')),
                'agendamentos_sexo': list(salao.models.Agendamento.objects.values('cliente__sexo').filter(is_pago=True).annotate(qtd=Count('cliente__sexo')).order_by('-qtd')),
                'agendamentos_faixa_etaria': list(salao.models.Agendamento.objects.values('cliente__birth').filter(is_pago=True).annotate(qtd=Count('cliente__birth')).order_by('-qtd')),
                'agendamentos_prestador_futuros': list(salao.models.Agendamento.objects.values('funcionario__name').filter(data__gte=timezone.now().date()).annotate(qtd=Count('funcionario__name')).order_by('-qtd')),
                'clientes_previstos': list(salao.models.Agendamento.objects.values('cliente__name').filter(data__gte=timezone.now().date()).order_by('cliente__name').distinct()),
            }
        else:
            template_name = 'salao/dash_cliente.html'
            informacoes = {
                'ultimo_servico': salao.models.AgendamentoServicos.objects.values('servico__nome').filter(agendamento__cliente_id=self.request.user).order_by('-agendamento__id').first(),
                'agendamentos_futuros': list(salao.models.Agendamento.objects.values().filter(cliente_id=self.request.user, is_pago=False, data__gte=timezone.now().date()).order_by('id'))
            }

        context = {
            'ultimo_login': self.request.user.last_login + timezone.timedelta(hours=-3),
            **informacoes
        }
        return render(self.request, template_name, context=context)

    def post(self, *args, **kwargs):
        dias = self.request.POST.get('dias')
        if dias is None:
            dias = 7
        else:
            dias = int(dias)
        data = timezone.now() + timezone.timedelta(days=-dias)
        quantidade_agendamentos = salao.models.AgendamentoServicos.objects.values('servico__nome').filter(agendamento__cliente_id=self.request.user, agendamento__data__gte=data).count()

        ultimos_servicos = list(salao.models.AgendamentoServicos.objects.values('servico__nome').filter(agendamento__cliente_id=self.request.user, agendamento__data__gte=data).annotate(Count('servico__nome')))

        return JsonResponse({'qtd_agendamentos': quantidade_agendamentos, 'ultimos_servicos': ultimos_servicos}, safe=False)


class RelatorioAgendamentos(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseRedirect(reverse("salao.agendamento"))

        template_name = 'salao/relatorio_agendamentos.html'
        context = {
            'dados': list(salaoecia.accounts.models.User.objects.values('name', 'sexo', 'email', 'birth', 'telefone').order_by('name'))
        }
        return render(self.request, template_name, context=context)


class RelatorioCaixa(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseRedirect(reverse("salao.agendamento"))

        template_name = 'salao/relatorio_caixa.html'
        context = {
            'dados': list(salao.models.Agendamento.objects.all())
        }
        return render(self.request, template_name, context=context)


class RelatorioCliente(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseRedirect(reverse("salao.agendamento"))

        template_name = 'salao/relatorio_clientes.html'
        context = {
            'dados': list(salaoecia.accounts.models.User.objects.values('name', 'sexo', 'email', 'birth', 'telefone').exclude(is_staff=True).annotate(qtd_visita=Count('agendamento')).order_by('name'))
        }
        return render(self.request, template_name, context=context)


class RelatorioFuncionario(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_staff:
            return HttpResponseRedirect(reverse("salao.agendamento"))

        template_name = 'salao/relatorio_funcionario.html'
        context = {
            'dados': list(salaoecia.accounts.models.User.objects.values('name', 'sexo', 'email', 'birth', 'telefone').filter(is_staff=True).order_by('name'))
        }
        return render(self.request, template_name, context=context)
