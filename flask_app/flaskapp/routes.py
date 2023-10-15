from flask import render_template, url_for, flash, request, redirect, abort
from flaskapp import app, db, bcrypt
from flaskapp.forms import RegistrationForm, LoginForm, RecipeForm
from flaskapp.models import User, Recipe
from flask_login import login_user, current_user, logout_user, login_required


with app.app_context():
    db.create_all()


# recipes = [
#     {
#         'name': 'Rice Cake',
#         'ingredients': ['milk', 'eggs', 'rice'],
#         'image': 'cauliflower.jpg',
#         'id': 1
#     },
#     {
#         'name': 'Omelet',
#         'ingredients': ['onion', 'eggs'],
#         'image': 'pumpkin.jpg',
#         'id': 2
#     },
#     {
#         'name': 'Grilled Carrot',
#         'ingredients': ['carrot'],
#         'image': 'cauliflower.jpg',
#         'id': 3
#     },
#     {
#         'name': 'Salad',
#         'ingredients': ['carrot', 'onion'],
#         'image': 'pumpkin.jpg',
#         'id': 4
#     },
#     {
#         'name': 'Scrambled Eggs',
#         'ingredients': ['eggs'],
#         'image': 'cauliflower.jpg',
#         'id': 5
#     },
#     {
#         'name': 'Rice Balls',
#         'ingredients': ['rice'],
#         'image': 'pumpkin.jpg',
#         'id': 6
#     }
# ]

@app.route("/")
@app.route("/home")
def home():
    #remove dummy data once finished with data model
    recipes = Recipe.query.all()
    return render_template('home_page.html', recipes = recipes, title = 'Home')


# @app.route("/cauliflower")
# def recipe():
#     return render_template('cauliflower.html', title = 'Recipe')

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
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


@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html', title = 'Profile')

@app.route("/post/new", methods = ['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        req_ingr_data = form.required_ingredients.data
        req_ingr = ""
        req_ingr_attributes = ""
        ad_ingr_data = form.additional_ingredients.data
        ad_ingr = ""
        ad_ingr_attributes = ""

        for line in req_ingr_data.splitlines():
            words = line.split()
            req_ingr += words.pop() + "\n"
            for word in words:
                req_ingr_attributes += word
            req_ingr_attributes += "\n"
        
        for line in ad_ingr_data.splitlines():
            words = line.split()
            ad_ingr += words.pop() + "\n"
            for word in words:
                ad_ingr_attributes += word
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
    return render_template('recipe.html', title=recipe.name, recipe = recipe)

@app.route("/post/<int:recipe_id>/update", methods = ['GET', 'POST'])
@login_required
def update_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if(recipe.author != current_user):
        abort(403)
    form = RecipeForm()
    #needs the other data columns in Recipe not just name
    if form.validate_on_submit():
        recipe.name = form.name.data
        db.session.commit()
        flash('Your recipe was updated!', 'success')
        return redirect(url_for('recipe', recipe_id=recipe.id))
    elif request.method == 'GET':    
        form.name.data = form.name
    return render_template('create_recipe.html', title = "Update Recipe", 
                           form = form, legend='Update Post')

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