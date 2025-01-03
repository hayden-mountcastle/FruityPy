from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("recipe", views.create_recipe, name="recipe"),
    path("your_recipe", views.your_recipe, name="your_recipe"),
    path("fruity_profile", views.fruity_profile, name="fruity_profile"),
    #path('api/fruit/<str:fruit_name>/', views.proxy_fruit_data, name='proxy_fruit_data'),
    path("recipe/<int:recipe_id>/", views.index, name="recipe_detail"),
    path("view_cat", views.view_cat, name="view_cat"),
    path("view_recipe/<int:id>", views.view_recipe, name="view_recipe"),
]
