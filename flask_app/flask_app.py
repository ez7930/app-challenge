from flask import Flask, render_template, url_for
app = Flask(__name__)

recipes = [
    {
        'name': 'Rice Cake',
        'ingredients': ['milk', 'eggs', 'rice'],
        'image': 'cauliflower.jpg'
    },
    {
        'name': 'Omelet',
        'ingredients': ['onions', 'eggs'],
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
    return render_template('home_page.html', recipes = recipes)


@app.route("/cauliflower")
def about():
    return render_template('cauliflower.html')


if __name__ == '__main__':
    app.run(debug=True)