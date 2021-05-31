from applications.users.functions import CodRegister
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.urls.base import reverse
from django.core.mail import send_mail


from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
from django.views.generic import (
    View,
    CreateView
)
from django.views.generic.edit import (
    FormView
)

from .forms import *

from .models import User




class UserRegisterView(FormView):
    template_name = "users/register.html"
    form_class = UsersRegisterForm
    success_url = '/'
    
    def form_valid(self, form):
        #generar codigo
        codigo = CodRegister()

        #registro user
        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres = form.cleaned_data['nombres'],
            apellidos = form.cleaned_data['apellidos'],
            genero = form.cleaned_data['genero'],
            codregistro = codigo,
        )
        #enviar el codigo de correo al usuario
        asunto = 'confirmacion  de email'
        mensaje = 'codigo de verificacion: ' + codigo
        email_remitente = 'ibarra.jhonatann@gmail.com'

        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email'],])
        #redirigir pantalla de validacion
        return HttpResponseRedirect(
            reverse(
                'user_app:verificacion',
                kwargs={'pk': usuario.id}
            )
        )


class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')

    # def form_valid(self, form):
    #     user = authenticate(
    #         username=form.cleaned_data['username'],
    #         password=form.cleaned_data['password'],
    #     )
    #     login(self.request, user)
    #     return super(LoginUser, self).form_valid(form)

class logoutView(View):
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'user_app:login'
            )
        )


class UpdatePasswordView(LoginRequiredMixin,FormView):
    template_name = "users/update.html"
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('user_app:login')
    login_url = reverse_lazy('user_app:login')
    
    def form_valid(self, form):
        #recuperar un usuario activo
        usuario = self.request.user
        # autenticacion de contrseña
        user = authenticate(
            username=usuario.username,
            password=form.cleaned_data['password1'],
        )
        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()
        
        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)


class CodVerificacionView(FormView):
    template_name = 'users/verifications.html'
    form_class =VerificationForm
    success_url: reverse_lazy('user_app:login')

    def get_form_kwargs(self):
        kwargs = super(CodVerificacionView, self).get_form_kwargs()
        kwargs.update({
            'pk':self.kwargs['pk']
        })
        return kwargs

    def form_valid(self, form):
       
        return super(CodVerificacionView, self).form_valid(form)
