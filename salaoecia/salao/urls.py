from django.contrib.auth.decorators import login_required
from django.urls import re_path
from salaoecia.salao.views import AgendamentoView, GerenciarAgendamentoView, AtualizarAgendamentoView, PegarAgendamentoView, CancelarAgendamentoView, GestaoEstoqueLeituraView, GestaoEstoqueView, CadastroProdutoView, \
    AtualizarEstoqueView, CarregarProdutoView, CadastroFuncionarioView, QuadroFuncionarioView, CaixaView, PegarClientesView, PegarInformacoesView, PegarProdutoView, FinalizarCompraView, AbrirCaixaView, DashboardView

urlpatterns = [
    re_path(r'cadastrar/agendamentos$', login_required(AgendamentoView.as_view()), name='salao.agendamento'),
    re_path(r'gerenciar/agendamentos$', login_required(GerenciarAgendamentoView.as_view()), name='salao.gerenciar.agendamento'),
    re_path(r'abrir/caixa$', login_required(AbrirCaixaView.as_view()), name='salao.abrir_caixa'),
    re_path(r'caixa$', login_required(CaixaView.as_view()), name='salao.caixa'),
    re_path(r'pegar/clientes$', login_required(PegarClientesView.as_view()), name="salao.pegar_clientes"),
    re_path(r'pegar/produto$', login_required(PegarProdutoView.as_view()), name="salao.pegar_produto"),
    re_path(r'pegar/informacoes$', login_required(PegarInformacoesView.as_view()), name="salao.pegar_informacoes"),
    re_path(r'finalizar/compra$', login_required(FinalizarCompraView.as_view()), name="salao.finalizar_compra"),
    re_path(r'atualizar/agendamentos$', login_required(AtualizarAgendamentoView.as_view()), name='salao.atualizar.agendamento'),
    re_path(r'cancelar/agendamentos$', login_required(CancelarAgendamentoView.as_view()), name='salao.cancelar.agendamento'),
    re_path(r'pegar/agendamentos$', login_required(PegarAgendamentoView.as_view()), name='salao.pegar.agendamento'),
    re_path(r'visualizar/estoque$', login_required(GestaoEstoqueLeituraView.as_view()), name="salao.visualizar.estoque"),
    re_path(r'alterar/estoque$', login_required(GestaoEstoqueView.as_view()), name="salao.alterar.estoque"),
    re_path(r'alterar/produto$', login_required(CadastroProdutoView.as_view()), name="salao.alterar.produto"),
    re_path(r'atualizar/estoque$', login_required(AtualizarEstoqueView.as_view()), name="salao.atualizar.estoque"),
    re_path(r'cadastrar/funcionario$', login_required(CadastroFuncionarioView.as_view()), name="salao.cadastrar.funcionario"),
    re_path(r'carregar/produto$', login_required(CarregarProdutoView.as_view()), name="salao.carregar.produto"),
    re_path(r'quadro/funcionarios$', login_required(QuadroFuncionarioView.as_view()), name="salao.quadro.funcionarios"),
    re_path(r'$', login_required(DashboardView.as_view()), name='salao.dashboard'),
]
