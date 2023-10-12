from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
import random


from .models import Recipe, Plan, Dayname, Recipeplan
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import Recipeplan

class MainPageView(View):
    def get(self, request):
        
        recipes = list(Recipe.objects.all())
        random.shuffle(recipes)
        
        carousel_recipes1 = recipes[0]
        carousel_recipes2 = recipes[1]
        carousel_recipes3 = recipes[2]
        return render(request, "index.html", context={'cr1': carousel_recipes1, 'cr2': carousel_recipes2, 'cr3': carousel_recipes3})

class DashboardView(View):
    def get(self, request):

        plans_number = Plan.objects.count()
        recipes_number = Recipe.objects.count()
        recipe_ids = Recipe.objects.values_list('id', flat=True)
        
        latest_plan = Plan.objects.latest('created')
        plan_name = latest_plan.name
        recipeplans = latest_plan.recipeplan_set.select_related('day_name').order_by('day_name__order')
        

        context = {
            'liczba_planów': plans_number,
            'liczba_przepisów': recipes_number,
            'recipe_ids':recipe_ids,
            'latest_plan': latest_plan,
            'recipeplans': recipeplans,
            'plan_name': plan_name
        }

        return render(request, 'dashboard.html', context)

class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)



class RecipeDetailsView(View):
    def get(self, request, id):
        
        return render(request, "app-recipe-details.html")
class RecipeListView(View):
    def get(self, request):
        all_recipes = Recipe.objects.all().order_by('-votes', '-created')
        paginator = Paginator(all_recipes, 50)
        page_number = request.GET.get('page')
        recipes = paginator.get_page(page_number)
        return render(request, 'app-recipes.html', {'recipes': recipes})

class RecipeAddView(View):
    def get(self, request):
        return render(request, "app-add-recipe.html")
    
    def post(self,request):
        name = request.POST.get('recipeName')
        description = request.POST.get('recipeDescription')
        preparation_time = request.POST.get("recipeTime")
        ingredients = request.POST.get('recipeIngredients')

        if (name and description and preparation_time and ingredients):
            Recipe.objects.create(name=name,
                                  description=description,
                                  ingredients=ingredients,

                                  preparation_time=preparation_time,
                                  votes=0)
            return redirect('recipe-list')
        else:
            return render(request, template_name='app-add-recipe.html',
                          context={'error': 'Wszystkie pola muszą zostać uzupełnione'}
                          )

class RecipeModifyView(View):
    def get(self, request, id):
        recipe = Recipe.objects.get(id=id)
        return render(request, "app-edit-recipe.html", context={'recipe':recipe})
    @csrf_exempt
    def post(self, request, id):
        recipe = Recipe.objects.get(id=id)
        nameNew = request.POST.get("recipeName")
        ingredientsNew = request.POST.get("recipeIngredients")
        descriptionNew = request.POST.get("recipeDescription")
        preparation_timeNew = request.POST.get("recipePreparation_time")
        if 'edit' in request.POST:
            recipe.name = nameNew
            recipe.description = descriptionNew
            recipe.ingredients = ingredientsNew
            recipe.preparation_time = preparation_timeNew
            recipe.save()
            return redirect('recipe-list')
        elif 'add' in request.POST:
            recipeNew = Recipe.objects.create(name=nameNew, ingredients=ingredientsNew, description=descriptionNew, preparation_time=preparation_timeNew)
            recipeNew.save()
            return redirect('recipe-list')
        return redirect('recipe-list')
    
class PlanDetailsView(View):
    def get(self, request, id):
        return render(request, "app-details-schedules.html")

class PlanAddRecipe(View):
    def get(self,request):
        
        plans = Plan.objects.order_by('name')
        recipes = Recipe.objects.order_by('name')
        days = Dayname.objects.order_by('order')
        return render(request, 'app-schedules-meal-recipe.html', context={'plans': plans,
                                                                          'recipes': recipes,
                                                                          'days': days,
                                                                          })
    
    @csrf_exempt
    def post(self, request):
        plan_name = request.POST.get('choosePlan')
        meal_name = request.POST.get('name')
        order = request.POST.get('number')
        recipe_name = request.POST.get('recipe')
        day_name = request.POST.get('day')
        print(f"plan name: {plan_name}, meal name: {meal_name}, order: {order},recipe:  {recipe_name},day: {day_name}")
        recipe = Recipe.objects.get(id=recipe_name)
        day = Dayname.objects.get(id=day_name)
        plan = Plan.objects.get(id=plan_name)

        try:
            recipe_plan = Recipeplan.objects.create(
                meal_name=meal_name,
                order=order,
                recipe=recipe,
                plan=plan,
                day_name=day
            )
            recipe_plan.save()

            return redirect('plan-list')
        except:
            return render(request,'app-schedules-meal-recipe.html' ,context={'error': 'Wszystkie pola muszą zostać uzupełnione'})
        
        
        
        

class PlanListVIew(View):
    def get(self, request):
        all_plans = Plan.objects.all().order_by('name', 'description')
        paginator = Paginator(all_plans, 50)
        page_number = request.GET.get('page')
        plans = paginator.get_page(page_number)

        

        return render(request, "app-schedules.html", {'plans': plans})
      
class PlanAddView(View):
    def get(self, request):
        return render(request, "app-add-schedules.html")
    def post(self, request):
        planName = request.POST.get('planName')
        planDesc = request.POST.get('planDescription')


        if not planName or not planDesc:  
            return render(request, "app-add-schedules.html", context={'error': 'Wszystkie pola muszą zostać uzupełnione'})
        else:
            newPlan = Plan.objects.create(name=planName, description=planDesc)
            return redirect('plan_details', id=newPlan.id)

class PlanDetailsView(View):
    def get(self, request, id):
        plan = Plan.objects.get(id=id)
        recipeplans = plan.recipeplan_set.select_related('day_name').order_by('day_name__order')
        return render(request, 'app-details-schedules.html', {'plan': plan, 'recipeplans': recipeplans})
    def post(self,request):
        return render(request, template_name="app-details-schedules.html")


class RecipeDetailsView(View):
    def get(self, request, id):
        recipe = Recipe.objects.get(id=id)
        return render(request, 'app-recipe-details.html', {'recipe': recipe})
    def post(self, request, id):
        recipe = Recipe.objects.get(id=id)
        if "Like" in request.POST:
            recipe.votes +=1
            recipe.save()
            return render(request, 'app-recipe-details.html', {'recipe': recipe})
        elif "Dislike" in request.POST:
            recipe.votes -=1
            recipe.save()
            return render(request, 'app-recipe-details.html', {'recipe': recipe})
        return render(request, 'app-recipe-details.html', {'recipe': recipe})


class PlanModifyView(View):
    def get(self, request, id):
        plan = Plan.objects.get(id=id)
        return render(request, 'app-edit-schedules.html', {'plan':plan})
    @csrf_exempt
    def post(self, request, id):
        plan = Plan.objects.get(id=id)
        nameNew = request.POST.get('planName')
        descNew = request.POST.get("planDescription")
        print(nameNew, descNew)
        if 'save' in request.POST :
            plan.name = nameNew
            plan.description = descNew
            plan.save()
            return redirect('plan-list')
        elif 'add' in request.POST :
            planNew = Plan.objects.create(name=nameNew, description=descNew)
            planNew.save()
            return redirect('plan-list')
        return redirect('plan-list')
    


class AboutView(View):
    def get(self, request):
        return render(request, template_name='about.html')
    

class ContactView(View):
    def get(self, request):
        return render(request, template_name='contact.html')