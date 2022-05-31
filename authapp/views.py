import os
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, CreateView, UpdateView

from authapp.forms import CustomUserCreationForm, CustomUserChangeForm
from authapp.models import User


class CustomLoginView(LoginView):
    template_name = 'authapp/login.html'
    extra_context = {
        'title': 'Вход пользователя'
    }

    def form_valid(self, form):
        ret = super().form_valid(form)

        message = ("Login success!<br>Hi, %(username)s") % {
            "username": self.request.user.get_full_name()
            if self.request.user.get_full_name()
            else self.request.user.get_username()
        }
        messages.add_message(self.request, messages.INFO, mark_safe(message))
        return ret

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, 'Неправильно имя пользователя или пароль!')
        return self.render_to_response(self.get_context_data(form=form))


class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('authapp:login')


# class RegisterView(TemplateView):
#     template_name = 'authapp/register.html'
#     extra_context = {
#         'title': 'Регистрация пользователя'
#     }
#
#     def post(self, request, *args, **kwargs):
#         try:
#             if all(
#                     (
#                             request.POST.get('username'),
#                             request.POST.get('password1'),
#                             request.POST.get('password2'),
#                             request.POST.get('first_name'),
#                             request.POST.get('last_name'),
#                             request.POST.get('email'),
#                             request.POST.get('password1') == request.POST.get('password2'),
#                     )
#             ):
#                 new_user = User.objects.create(
#                     username=request.POST.get('username'),
#                     first_name=request.POST.get('first_name'),
#                     last_name=request.POST.get('last_name'),
#                     email=request.POST.get('email'),
#                     age=request.POST.get('age') if request.POST.get('age') else 0,
#                     avatar=request.FILES.get('avatar')
#                 )
#                 new_user.set_password(request.POST.get('password1'))
#                 new_user.save()
#                 messages.add_message(request, messages.INFO, 'Реистрация успешна')
#                 return HttpResponseRedirect(reverse('authapp:login'))
#             else:
#                 messages.add_message(request, messages.WARNING, 'Что-то не получилось')
#                 return HttpResponseRedirect(reverse('authapp:register'))
#         except Exception as ex:
#             messages.add_message(request, messages.WARNING, f'Что-то не получилось {ex}')
#             return HttpResponseRedirect(reverse('authapp:register'))


# class EditView(CreateView):
#     model = User
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('authapp:login')


class EditView(UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'authapp/edit.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('authapp:edit', args=[self.request.user.pk])


# class EditView(TemplateView):
#     template_name = 'authapp/edit.html'
#     extra_context = {
#         'title': 'Изменение пользователя'
#     }
#
#     def post(self, request, *args, **kwargs):
#         try:
#             if request.POST.get("username"):
#                 request.user.username = request.POST.get("username")
#             if request.POST.get("first_name"):
#                 request.user.first_name = request.POST.get("first_name")
#             if request.POST.get("last_name"):
#                 request.user.last_name = request.POST.get("last_name")
#             if request.POST.get("age"):
#                 request.user.age = request.POST.get("age")
#             if request.POST.get("email"):
#                 request.user.email = request.POST.get("email")
#             if request.FILES.get("avatar"):
#                 if request.user.avatar and os.path.exists(request.user.avatar.path):
#                     os.remove(request.user.avatar.path)
#                 request.user.avatar = request.FILES.get("avatar")
#             request.user.save()
#             messages.add_message(request, messages.INFO, ("Saved!"))
#         except Exception as exp:
#             messages.add_message(
#                 request,
#                 messages.WARNING,
#                 mark_safe(f"Something goes worng:<br>{exp}"),
#             )
#         return HttpResponseRedirect(reverse("authapp:edit"))


class CustomLogoutView(LogoutView):
    template_name = 'mainapp/index.html'
