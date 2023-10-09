from flask import Flask, render_template, url_for, redirect, request
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = "ab53722c39ed18bc6c6e507be09bfe6e"

recipes = [
    {
        'name': 'Rice Cake',
        'ingredients': ['milk', 'eggs', 'rice'],
        'image': 'cauliflower.jpg'
    },
    {
        'name': 'Omelet',
        'ingredients': ['onion', 'eggs'],
        'image': 'pumpkin.jpg'
    },
    {
        'name': 'Grilled Carrot',
        'ingredients': ['carrot'],
        'image': 'cauliflower.jpg'
    },
    {
        'name': 'Salad',
        'ingredients': ['carrot', 'onion'],
        'image': 'pumpkin.jpg'
    },
    {
        'name': 'Scrambled Eggs',
        'ingredients': ['eggs'],
        'image': 'cauliflower.jpg'
    },
    {
        'name': 'Rice Balls',
        'ingredients': ['rice'],
        'image': 'pumpkin.jpg'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home_page.html', recipes = recipes, title = 'Home')


@app.route("/cauliflower")
def recipe():
    return render_template('cauliflower.html', title = 'Recipe')

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login")
def login(): 
    form = LoginForm()
    return render_template('login.html', form = form, title = 'Login')


if __name__ == '__main__':
    app.run(debug=True)