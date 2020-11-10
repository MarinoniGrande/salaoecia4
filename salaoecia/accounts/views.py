from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.views import View
import salaoecia.utils.utils
from .forms import RegisterForm, EditAccountForm, PasswordResetForm
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from .models import PasswordReset

import copy

User = get_user_model()


@login_required()
def dashboard(request):
    template_name = 'accounts/edit_bs.html'
    return render(request, template_name)


@login_required()
def edit(request):
    template_name = 'accounts/edit_bs.html'
    context = {}
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Os dados da sua conta foram alterados com sucesso.')
            return redirect('dashboard')
    else:
        form = EditAccountForm(instance=request.user)
    context['form'] = form
    return render(request, template_name, context)


def register(request):
    carrinho = copy.deepcopy(request.session.get('carrinho', {}))
    template_name = 'accounts/register.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)

            request.session['carrinho'] = carrinho
            request.session.save()

            messages.success(
                request,
                'Seu cadastro foi criado com sucesso e você já está logado. Bora agendar!'
            )

            return redirect('http://127.0.0.1:8000/')
    else:
        form = RegisterForm()
    context = {
        'form': form
    }

    return render(request, template_name, context)


def password_reset(request):
    template_name = 'accounts/password_reset.html'
    form = PasswordResetForm(request.POST or None)
    context = {}
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, template_name, context)


def password_reset_confirm(request, key):
    template_name = 'accounts/password_reset_confirm.html'
    context = {}
    reset = get_object_or_404(PasswordReset, key=key)
    form = SetPasswordForm(user=reset.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, template_name, context)


@login_required()
def edit_password(request):
    template_name = 'accounts/edit_password_bs.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            context['success'] = True
    else:
        form = PasswordChangeForm(user=request.user)
        context['form'] = form
    return render(request, template_name, context)



class DesativarContaView(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("salao.agendamento"))

        self.request.user.is_active = False
        logout(self.request)
        template_name = 'accounts/register.html'

        form = RegisterForm()

        context = {
            'form': form
        }

        return render(self.request, template_name, context)
