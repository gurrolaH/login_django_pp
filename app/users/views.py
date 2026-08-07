from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')  # En lugar de regresar al login, se va al home.

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # Iniciar sesión automáticamente.
        messages.success(self.request, 'Cuenta creada correctamente. Has iniciado sesión y ya puedes continuar.')
        return response


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home_view(request):
    from django.shortcuts import render
    return render(request, 'users/home.html')