from flask import render_template, url_for, flash, request, redirect, abort
from flaskapp import app, db, bcrypt
from flaskapp.forms import RegistrationForm, LoginForm, RecipeForm
from flaskapp.models import User, Recipe
from flask_login import login_user, current_user, logout_user, login_required

ingredients_data = {
    'vegetables': ['Bell Pepper', 'Celery', 'Onion', 'Carrot'],
    'proteins': ['Eggs', 'Chicken Breast', 'Chicken Thigh', 'Ground Beef', 'Bacon'],
    'carbs': ['Sliced Bread', 'Noodle', 'Tortilla', 'Bagel'],
    'other': ['Butter', 'Milk', 'Shredded Cheese', 'Sliced Cheese']
}
with app.app_context():
    db.create_all()

@app.route("/")
@app.route("/home")
def home():
    #remove dummy data once finished with data model
    recipes = Recipe.query.all()
    favorited_recipes = []
    saved_ingr_li = []
    if current_user.is_authenticated:
        favorited_recipes = [int(r) for r in current_user.favorites.splitlines()]
        #Gets a list of the saved ingredients
        for ingr in current_user.saved_ingr.splitlines():
            saved_ingr_li.append(ingr)

    return render_template('home_page.html', recipes = recipes, favorited_recipes = favorited_recipes, title = 'Home', filter_ingr = ingredients_data, saved_ingr=saved_ingr_li)

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password, favorites = "", saved_ingr = "")
        db.session.add(user)
        db.session.commit()
        flash(f'Successfully created account for {form.username.data}', 'success')
        return redirect(url_for('login'))
    

    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods = ['GET', 'POST'])
def login(): 
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit(): 
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login Successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if  next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form = form, title = 'Login')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/profile", methods = ['GET', 'POST'])
@login_required
def profile():
    favorited_recipes = []
    favorited_recipes_id = [int(r) for r in current_user.favorites.splitlines()]
    for id in favorited_recipes_id:
        favorited_recipes.append(Recipe.query.get(id))

    #Submits checked ingredients to User model
    if request.method == 'POST':
        checked_ingr = request.form.getlist('ingr_checkbox')

        astring = ""
        for ingr in checked_ingr:
            astring += ingr + "\n"

        current_user.saved_ingr = astring
        db.session.commit()
        flash(f'Updated Your Saved Ingredients!', 'success')

    #Gets a list of the saved ingredients
    saved_ingr_li = []
    for ingr in current_user.saved_ingr.splitlines():
        saved_ingr_li.append(ingr)
    
    return render_template('profile.html', title = 'Profile', favorited_recipes = favorited_recipes, filter_ingr = ingredients_data, saved_ingr = saved_ingr_li)

@app.route("/post/new", methods = ['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        #Gets all the content
        req_ingr_data = form.required_ingredients.data
        req_ingr = ""
        req_ingr_attributes = ""
        ad_ingr_data = form.additional_ingredients.data
        ad_ingr = ""
        ad_ingr_attributes = ""

        for line in req_ingr_data.splitlines():
            words = line.split()
            req_ingr += words.pop().replace("-", " ") + "\n"
            for word in words:
                req_ingr_attributes += word + " "
            req_ingr_attributes += "\n"
        
        for line in ad_ingr_data.splitlines():
            words = line.split()
            ad_ingr += words.pop().replace("-", " ") + "\n"
            for word in words:
                ad_ingr_attributes += word + " "
            ad_ingr_attributes += "\n"

        recipe = Recipe(name=form.name.data, description=form.description.data, author=current_user,
                         req_ingr=req_ingr, req_ingr_attributes=req_ingr_attributes,
                         ad_ingr=ad_ingr, ad_ingr_attributes=ad_ingr_attributes,
                         cook_time=form.cook_time.data, calories=form.calories.data, 
                         instructions=form.instructions.data, image=form.image.data)
        
        db.session.add(recipe)
        db.session.commit()
        flash('Your recipe has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_recipe.html', title = "New Recipe",
                           form = form, legend='New Recipe')

@app.route("/post/<int:recipe_id>")
def recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    complete_req_ingr = []
    complete_ad_ingr = []
    for attribute, ingr in zip(recipe.req_ingr_attributes.splitlines(), recipe.req_ingr.splitlines()):
        complete_req_ingr.append(attribute+ingr)
    for attribute, ingr in zip(recipe.ad_ingr_attributes.splitlines(), recipe.ad_ingr.splitlines()):
        complete_ad_ingr.append(attribute+ingr)
    return render_template('recipe.html', title=recipe.name, recipe = recipe, req_ingr=complete_req_ingr, ad_ingr=complete_ad_ingr)

@app.route("/post/<int:recipe_id>/update", methods=['GET', 'POST'])
@login_required
def update_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author != current_user:
        abort(403)
    form = RecipeForm()
    if form.validate_on_submit():

        #Adds in the data from form
        req_ingr_data = form.required_ingredients.data
        req_ingr = ""
        req_ingr_attributes = ""
        ad_ingr_data = form.additional_ingredients.data
        ad_ingr = ""
        ad_ingr_attributes = ""

        for line in req_ingr_data.splitlines():
            words = line.split()
            req_ingr += words.pop().replace("-", " ") + "\n"
            for word in words:
                req_ingr_attributes += word + " "
            req_ingr_attributes += "\n"
        
        for line in ad_ingr_data.splitlines():
            words = line.split()
            ad_ingr += words.pop().replace("-", " ") + "\n"
            for word in words:
                ad_ingr_attributes += word + " "
            ad_ingr_attributes += "\n"

        recipe.name=form.name.data
        recipe.description=form.description.data
        recipe.req_ingr=req_ingr
        recipe.req_ingr_attributes=req_ingr_attributes
        recipe.ad_ingr=ad_ingr
        recipe.ad_ingr_attributes=ad_ingr_attributes
        recipe.cook_time=form.cook_time.data
        recipe.calories=form.calories.data
        recipe.instructions=form.instructions.data
        recipe.image=form.image.data

        db.session.commit()
        flash('Your recipe has been updated!', 'success')
        return redirect(url_for('recipe', recipe_id=recipe.id))
    elif request.method == 'GET':
        #fills in previously entered data
        form.name.data=recipe.name
        form.description.data=recipe.description
        #Combine columns for ingredient list
        complete_req_ingr = ""
        complete_ad_ingr = ""
        for attribute, ingr in zip(recipe.req_ingr_attributes.splitlines(), recipe.req_ingr.splitlines()):
            complete_req_ingr += attribute + ingr + "\n"
        for attribute, ingr in zip(recipe.ad_ingr_attributes.splitlines(), recipe.ad_ingr.splitlines()):
            complete_ad_ingr += attribute + ingr + "\n"
        form.required_ingredients.data=complete_req_ingr
        form.additional_ingredients.data=complete_ad_ingr
        form.cook_time.data=recipe.cook_time
        form.calories.data=recipe.calories
        form.instructions.data=recipe.instructions
        form.image.data=recipe.image
    return render_template('create_recipe.html', title='Update Recipe',
                           form=form, legend='Update Recipe')

@app.route("/post/<int:recipe_id>/delete", methods = ['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if(recipe.author != current_user):
        abort(403)
    db.session.delete(recipe)
    db.session.commit()
    flash('Your recipe was deleted', 'success')
    return redirect(url_for('home'))

@app.route("/favorite/<int:recipe_id>", methods = ['POST'])
@login_required
def favorite_recipe(recipe_id):
    current_user.favorites += str(recipe_id) + "\n"
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/unfavorite/<int:recipe_id>", methods = ['POST'])
@login_required
def unfavorite_recipe(recipe_id):
    #creates list
    new_favorites = current_user.favorites.splitlines()
    new_favorites.remove(str(recipe_id))

    astring = ""
    for f in new_favorites:
        astring += f + "\n"

    current_user.favorites = astring
    db.session.commit()
    return redirect(url_for('home'))
