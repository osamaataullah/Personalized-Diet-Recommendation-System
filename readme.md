# Personalized Diet Recommendation System
The app helps its users choose the right food they should consume based on their personal information (PI), such as age, height, activity level, and personal favorites. Using this data, it computes health-related parameters like daily calorie intake requirements using [equation.](https://www.omnicalculator.com/health/bmr-harris-benedict-equation#:~:text=It%20needs%20your%20age%2C%20weight,%2D%20(6.75%20*%20age)%20.)
Then it prompts users to input their favorite preferences such as cuisine, allergies, etc. and uses this information to further narrow down the recipes from the recipe repository extracted from [RecipeDB](https://cosylab.iiitd.edu.in/recipedb/) - a structured compilation of recipes, ingredients, and nutrition profiles interlinked with flavor profiles and health associations.


## Features
1) Login/Sign up - Hosted on firebase
2) Fully responsive UI 
3) Based on Python-Flask
4) Generates personalized health recommendations based on users health parameters.

## Requirements
```bash
pip install pyrebase4
pip install flask
```



## Additional Info
The server starts by default on http://127.0.0.1:5000/

## Screenshots
