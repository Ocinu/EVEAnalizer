from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView, TemplateView

from .forms import PersonCreationForm, PersonLoginForm
from .models import News


class NewsView(ListView):
    model = News
    context_object_name = "news_list"
    template_name = "index.html"
    paginate_by = 2


class RegisterView(View):
    form_class = PersonCreationForm
    template_name = "main/register.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration complete!")
            return redirect("home")
        else:
            messages.error(request, "Registration error")
            return render(request, self.template_name, {"form": form})


class LoginView(View):
    form_class = PersonLoginForm
    template_name = "main/login.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
        else:
            return render(request, self.template_name, {"form": form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("home")


class AboutView(TemplateView):
    template_name = "main/about.html"
