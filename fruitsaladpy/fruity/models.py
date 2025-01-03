from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    categoryName = models.CharField(max_length  = 50)

    def __str__(self):
        return self.categoryName


class Recipes(models.Model): #Same as listing
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete= models.CASCADE, blank = True, null = True, related_name = "user")


    imageUrl = models.CharField(max_length = 1000, default="https://img.freepik.com/premium-vector/cute-dizzy-lemon-character-funny-confused-lemon-fruit-cartoon-emoticon-flat-style_841552-205.jpg")
    description = models.CharField(max_length=1000, default="No description provided")


    total_sugar = models.FloatField(default=0)
    total_calories = models.FloatField(default=0)
    total_fat = models.FloatField(default=0)
    total_fiber = models.FloatField(default=0)
    total_protein = models.FloatField(default=0)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name= "category" )
    
    def __str__(self):
        return self.title


class Ingredient(models.Model):
    name = models.CharField(max_length=100)  # Generic name for the fruit ingredient 
    fruit_owner = models.ForeignKey(User, on_delete= models.CASCADE, blank = True, null = True, related_name = "fruit_user")
    quantity = models.IntegerField(default = 1) #Quantity to multiply nutrition
    sugar = models.FloatField(default=0)  # Sugar content of the ingredient
    calories = models.FloatField(default=0)  # Calories content of the ingredient
    fat = models.FloatField(default=0)
    fiber = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE, related_name="ingredients")  # Linking ingredient to recipe

    def __str__(self):
        return self.name


