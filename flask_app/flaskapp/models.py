from flaskapp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    recipes = db.relationship('Recipe', backref = 'author', lazy = True)
    favorites = db.Column(db.Text, nullable = False)
    saved_ingr = db.Column(db.Text, nullable = False)

    def __repr__(self):
        return f"User('{self.username}', '{self.username}')"


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    #required ingredients
    req_ingr = db.Column(db.Text, nullable = False)
    req_ingr_attributes = db.Column(db.Text, nullable = False)
    #additional ingredients
    ad_ingr = db.Column(db.Text, nullable = True)
    ad_ingr_attributes = db.Column(db.Text, nullable = True)

    cook_time = db.Column(db.Integer, nullable = False)
    calories = db.Column(db.Integer, nullable = False)
    instructions = db.Column(db.Text, nullable = False)

    image = db.Column(db.Text, nullable = True)

    def __repr__(self):
        return f"Recipe('{self.name}')"
