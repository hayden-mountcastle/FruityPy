from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Count, Sum  

from .models import User, Category, Recipes, Ingredient
import requests
import os
import  json


def index(request):
    return render(request, "fruity/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "fruity/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "fruity/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "fruity/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "fruity/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "fruity/register.html")




def index(request):
        return render(request, "fruity/index.html",{
        "active_categories": Category.objects.all(),
        "current_recipes":  Recipes.objects.all()
    })

def view_cat(request):
    if request.method == "POST":
        new_category = request.POST['category']
        category_filter = Category.objects.get(categoryName=new_category)
        return render(request, "fruity/index.html",{
        "active_categories": Category.objects.all(),
        "current_recipes":  Recipes.objects.filter(category=category_filter)
    })


#Add a recipe

def create_recipe(request):
    if request.method == "GET":


                # URL of the API
        url = "https://www.fruityvice.com/api/fruit/all/"

        try:
            # Send GET request to the API
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful

            # Parse the JSON response
            fruits = response.json()
            anti_fruit = ["GreenApple", "Japanese Persimmon", "Horned Melon","Ceylon Gooseberry"]
            # Extract and print the fruit names
            fruit_names = [fruit["name"] for fruit in fruits if fruit["name"] not in anti_fruit]
        

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

        # Fetch all categories to display in the form
        allCategories = Category.objects.all()
        return render(request, "fruity/recipe.html", {
            "categories": allCategories,
            "fruit_names": fruit_names
        })


        
    elif request.method == "POST":



        # Get data from the form
        title = request.POST["title"]
        description = request.POST["description"]
        image_url = request.POST.get("imageUrl", "https://img.freepik.com/premium-vector/cute-dizzy-lemon-character-funny-confused-lemon-fruit-cartoon-emoticon-flat-style_841552-205.jpg?w=1480")
        category_id = request.POST.get("category")
        ingredients_data = request.POST.getlist("ingredients[]")  # List of ingredient names
        sugars = request.POST.getlist("sugars[]")
        calories = request.POST.getlist("calories[]")
        fats = request.POST.getlist("fats[]")
        fibers = request.POST.getlist("fibers[]")
        proteins = request.POST.getlist("proteins[]")
        quantity = request.POST.get("quantity[]")
        quantity = int(quantity) #ensure this is an interger

        # Current user
        current_user = request.user

        # Find the category or set it to None if not provided
        category = Category.objects.filter(id=category_id).first() if category_id else None

        # Create a new recipe
        new_recipe = Recipes(
            title=title,
            description=description,
            imageUrl=image_url,
            owner=current_user,
            category=category
        )
        new_recipe.save()

        # Initialize total values
        total_sugar = total_calories = total_fat = total_fiber = total_protein = 0
        

        # Add ingredients to the recipe
        for i in range(len(ingredients_data)):
            ingredient_name = ingredients_data[i]
            sugar = float(sugars[i])*quantity
            calorie = float(calories[i])*quantity
            fat = float(fats[i])*quantity
            fiber = float(fibers[i])*quantity
            protein = float(proteins[i])*quantity

            # Create ingredient
            ingredient = Ingredient(
                name=ingredient_name,
                fruit_owner=current_user,
                sugar=sugar,
                calories=calorie,
                fat=fat,
                fiber=fiber,
                protein=protein,
                recipe=new_recipe,
                quantity = quantity
            )
            ingredient.save()

            # Accumulate totals
            total_sugar += sugar
            total_calories += calorie
            total_fat += fat
            total_fiber += fiber
            total_protein += protein

        # Update the recipe's total nutritional values
        new_recipe.total_sugar = total_sugar
        new_recipe.total_calories = total_calories
        new_recipe.total_fat = total_fat
        new_recipe.total_fiber = total_fiber
        new_recipe.total_protein = total_protein
        new_recipe.category = category
        new_recipe.save()

        # Redirect to a success page or the recipe detail page
        #return redirect("index", recipe_id=new_recipe.id)
       # return redirect("index")
        return HttpResponseRedirect(reverse("index"),
                                    {"quantity": quantity,
                                     "test": request.POST.getlist("quantity[]")})



def your_recipe(request):
    # Filter recipes where the current user is the owner
    recipes = Recipes.objects.filter(owner=request.user)



    return render(request, "fruity/your_recipe.html", {
        "your_recipes": recipes
    })



def fruity_profile(request):
    # Get the ingredients associated with the current user
    your_ingredients = Ingredient.objects.filter(fruit_owner=request.user)
    
    # Count the occurrences of each ingredient and order by most used
    ingredient_count = your_ingredients.values('name').annotate(count=Count('name')).order_by('-count')

    ingredient_totals = your_ingredients.values('name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')

    most_used_fruit = ingredient_count.first()
    most_quantity_fruit = ingredient_totals.first()

    profile = None

    user_recipes = Recipes.objects.filter(owner=request.user)
    # Path to the JSON file (ensure this path is correct) 
    path = os.path.expanduser("~/Desktop/Hayden/CS-33a/Final_Project/fruitsaladpy/FruityProfiles_4.json")

    if not user_recipes:
        return render(request, "fruity/fruity_profile.html", {
        "current_recipes":  Recipes.objects.filter(owner=request.user)
    })


    elif most_used_fruit:
        fruit_name = most_used_fruit["name"].capitalize()
        fruit_name_quantity = most_quantity_fruit["name"].capitalize()
        print(f"Most used fruit: {fruit_name}")

        # Open and load the JSON file
        with open(path, 'r') as file:
            fruity_profiles = json.load(file)

        # Debug: Print the loaded profiles
        #print(f"Loaded fruit profiles: {fruity_profiles}")

        # Find the profile of the most used fruit (case insensitive comparison)
        for fruit in fruity_profiles:
            #print(f"Checking fruit: {fruit['fruit_name']}")  # Debug each fruit
            if fruit["Fruit"] == fruit_name:
                profile = fruit["Profile"]
                snapshot = fruit["Snapshot"]
            
            if fruit["Fruit"] == fruit_name_quantity:
                profile_quantity = fruit["Profile"]
                snapshot_quantity = fruit["Snapshot"]
    # Render the result to the template, passing the most used ingredient and its profile
    return render(request, "fruity/fruity_profile.html", {

        "most_used_fruit": most_used_fruit,
        "most_quantity_fruit": most_quantity_fruit,
        "fruit_name": fruit_name,
        "fruit_profile": profile,
        "fruit_snapshot": snapshot,
        "fruit_name_quantity": fruit_name_quantity,
        "fruit_profile_quantity": profile_quantity,
        "fruit_snapshot_quantity": snapshot_quantity,
        "current_recipes":  Recipes.objects.filter(owner=request.user)
    })
    


def view_recipe(request, id):
    current_recipe = Recipes.objects.get(pk=id)
    current_ingredients = Ingredient.objects.filter(recipe=current_recipe)  
    
    return render(request, "fruity/view_recipe.html", {
        "click_recipe": current_recipe,
        "current_ingredients": current_ingredients
        
    })

