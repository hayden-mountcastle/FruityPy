FruityPy!

Hayden Mountcastle

12-15-2024


This is an app that accesses the https://www.fruityvice.com/ API which is a free API with about 50 different fruit and their nutritional content. You can see an example json exports from this API here (for Kiwi)

https://www.fruityvice.com/api/fruit/kiwi/

You can view all fruit here available here. 

https://www.fruityvice.com/api/fruit/all/


A. PURPOSE:

1. The purpose of this app is to pull from the fruityvice API to get the nutritional content of fruits. Users can then add these to recipes and specify the quantity of each fruit. Users can then save their recipes and filter based on Smoothie, Fruit Salad, Sorbet, of Fruit Pop. 

2. Finally, users can then see their "Fruity Profiles" based off of calculated criteria from their recipes. First is their primary profile which calculates their fruity profile based on the number of times the user used fruits in their recipes. If it's just one, that fruit will be random. Then there is the secondary profile which is calculated based on the quantity in grams the user uses a certain fruit. For example, if a user used Strawberry in 5 of their recipes at 100g, but Kiwi one time at 1000g their secondary profile will be Kiwi. If Strawberry was the most used fruit, this will be their primary profile. 

FUNCTIONALITY: 

1. ADDING RECIPES
Fruity vice apis are called using Javascript fetch command in recipe.html. When "Look up fruit" is clicked, the API will be called and the below items will be autofilled with the selected fruit's sugar, fat, fiber (calculated from carbohydrates - sugar), protein, and calories. When adding another fruit, the function will be called again with the new fruits nutritional information. The total nutrition will sum all looked up fruits together. The list of fruits is calculated via the https://www.fruityvice.com/api/fruit/all/ API (accessed using python) which is then made into a list based off of "name". Fruits  names of more than one word (eg Horned Melon) are removed as this confused the API. 

Below will be the "Create a New Fruity Recipe" option where details about the recipe can be added. Recipe title, description, and category are required; a pop up will occur if they are not filled out at the time of pressing "Create Recipe". An image URL is optional. 

In the ingredients section, the quantity of fruit can be entered. The fruit nutrition will auto populate in the appropriate cells so the user does not have to do this. 

Users are able to add fruit to their recipes, as well as remove fruit. This command is also done through Javascript where it duplicates the previous child. Unfortunately, this leads to a small bug where the quantity is duplicated and users will have to manually edit this. 


2. INDEX/VIEW RECIPES

The index of the website is the "Fruit Recipes" page where users (authenticated or not) can see recipes made by other users. They are presented as clickable cards of 3 rows that display the title, creator, total calories, total sugar, total fat, total fiber, total protein, and category. Animations occur as the mouse hovers over the recipe. Users can click anywhere on the card to view the full recipe/nutritional content. 

In Index (Fruit Recipes), users are able to filter recipes based off of their selected category. This is calculated via a lift of the categories specified by the admin. There is no way to add categories apart from through the admin.  If authenticated and there is no available recipe for a category, the user will be invited to add a recipe. If not authenticated, the user will be encourage to register for an account. 


When clicked, users are brought to the specific recipes page as "view_recipes/recipe.id". The layout is designed such that users are greeted with the title and large photo of the recipe, with the description as the caption. Total nutrition is below in apparent text, with calories bolded. Finally below this, ingredients are listed with their quantities and total nutritional contributions to the recipe per gram. The instructions are simple, merely "Blend, mix, chop, or freeze these up for a delicious fruity snack!" as this is only fruit based. 


3. FRUITY PROFILES

Fruity profiles are a unique feature of this app. There are two profiles: primary and secondary. The primary profile is the "times used profile" which calculated how many times a particular fruit was used for an individuals recipes. For example, if in all a users recipes, they used strawberry 5 times, guava 3 times, and mango 1 time, their primary profile will be "Strawberry". Alternatively, the secondary profile is calculated based on a users total sum in grams of a certain ingredient. In the same example, even if strawberry is used 5 times at 100 grams each (total = 500g), but mango is used one time at 1000grams, the secondary profile will be mango. These will automatically update as users add more recipes with different fruits.

How fruity profiles are given:
I made a JSON file for each fruit with a unique "Snapshot" and "Profile". The most_used_fruits and most_quantity_fruits are calculated and then fed into a search function in the JSON. It pulls out the corresponding "Snapshot" and "Profile" and appends it to the page for the user to see. These profiles were generated by ChatGPT, not by my own writing. I did this as it is only fun writing, outside the scope of this course. 


4. LOGIN/REGISTRATION 

Login and registration was taken from "Commerce", as the needed functionality was similar. Many functions were also modified from Project 2 to fit this app (such as viewing and filtering recipes). 

5. Bugs in the program
Unfortunately there are still some bugs in the program regarding "creating recipes". Most of these have to do with the Javascript auto-population. While the ingredients auto-populate with the correct nutritional information, it only captures the first quantity provided, and uses this for all fruits in a recipe. I tried many ways around this including a proteins = request.POST.getlist("quantity[]"), which works for the other categories. However, when using multiplying the nutritional content for the ingredient against said quantity, I would get a "list of out range error" that I was not able to resolve. 

Additionally, when adding a new container to enter new ingredients, the information from the previous child remains (including quantity) and only updates when adding the new fruit. I would have liked this to be empty initially, but failed to do so. 

6. Future avenues
I would like to create a function that matches users with their profiles, but did not have time to do so. For example, if two users are "Strawberries", I would like for them to be able to match with the idea that they can bond over their mutual love of strawberries and similar "strawberry" personalities. 


I hope you enjoy FruityPy!

Please reach out to me at haydenmountcastle@gmail.com with any questions. 

You can view the video demonstrating functionality at the following link:

https://www.loom.com/share/9c2f7b726a87420ca3783f3964b628b5?sid=3a330103-a5bd-4be2-8cba-ef3b96207f6e







