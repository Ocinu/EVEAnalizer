from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, FormView

from .forms import RegionRouteForm
from .models import (Article, Category, Constellation, Group, Region,
                     SolarSystem)


class UniverseView(FormView):
    template_name = "universe/universe.html"
    form_class = RegionRouteForm

    def get_initial(self):
        return {"sec_status": Region.StatusChoices.LOW_SEC}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["regions"] = Region.objects.all()
        context["categories"] = Category.objects.all()
        context["trade_region"] = Region.objects.filter(trade_rout="hi_sec")
        return context

    def post(self, request, *args, **kwargs):
        region = get_object_or_404(Region, pk=request.POST.get("region"))
        region.trade_rout = request.POST.get("sec_status")
        region.save()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ArticleView(DetailView):
    model = Article
    template_name = "universe/article.html"

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        return context


class CategoryView(DetailView):
    model = Category
    template_name = "universe/category.html"


class GroupView(DetailView):
    model = Group
    template_name = "universe/group.html"


class SystemView(DetailView):
    model = SolarSystem
    template_name = "universe/system.html"


class ConstellationView(DetailView):
    model = Constellation
    template_name = "universe/constellation.html"


class RegionView(DetailView):
    model = Region
    template_name = "universe/region.html"
