from django.contrib import admin
from .models import User, Category, Recipes, Ingredient

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Recipes)
admin.site.register(Ingredient)
