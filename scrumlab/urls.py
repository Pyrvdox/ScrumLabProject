"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views import View

from django.urls import path
from django.contrib import admin


from jedzonko.views import IndexView,PlanModifyView,ContactView,  AboutView, PlanAddView, MainPageView, DashboardView, PlanAddRecipe, RecipeListView, PlanListVIew, RecipeDetailsView, RecipeAddView, RecipeModifyView, PlanDetailsView, PlanAddView



from django.views.decorators.csrf import csrf_exempt

app_name = 'jedzonko'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', IndexView.as_view()),
    path('', MainPageView.as_view()),
    path('main/', DashboardView.as_view(), name='dashboard'),
    path('recipe/<int:id>', RecipeDetailsView.as_view(), name='recipe-details'),
    path('recipe/list/', RecipeListView.as_view(), name='recipe-list'),
    path('recipe/add/', RecipeAddView.as_view() , name='recipe-add'),
    path('recipe/modify/<int:id>/', RecipeModifyView.as_view(), name='recipe-modify'),
    path('plan/<int:id>/', PlanDetailsView.as_view(), name='plan-details'),
    path('plan/add/', PlanAddView.as_view() , name='plan-add'),
    path('plan/<int:id>/details/', PlanDetailsView.as_view(), name="plan_details"),
    path('plan/add-recipe/', PlanAddRecipe.as_view(), name='add_recipe'),
    path('plan/list/', PlanListVIew.as_view(), name='plan-list'),
    path('plan/modify/<int:id>', PlanModifyView.as_view(), name='plan-modify'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact')
    ]


