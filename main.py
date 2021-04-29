from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy  # pip install Flask-SQLAlchemy
import random
import json

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")
    

#  HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def random_cafe():
    # get a random cafe from the database
    all_cafes = db.session.query(Cafe).all()
    rand_cafe = random.choice(all_cafes)
    # Turn the random cafe SQLAlchemy Object into a JSON Response object

    # The original manual dictionary method
    # cafe = {
    #     'id': rand_cafe.id,
    #     'name': rand_cafe.name,
    #     'map_url': rand_cafe.map_url,
    #     'img_url': rand_cafe.img_url,
    #     'location': rand_cafe.location,
    #     'seats': rand_cafe.seats,
    #     'has_toilet': rand_cafe.has_toilet,
    #     'has_wifi': rand_cafe.has_wifi,
    #     'has_sockets': rand_cafe.has_sockets,
    #     'can_take_calls': rand_cafe.can_take_calls,
    #     'coffee_price': rand_cafe.coffee_price,
    # }
    # return jsonify(cafe=cafe)

    # This method saves me having to manually type out the dictionary
    cafe = jsonify(
        # jsonify the dictionary
        cafe=jsonify(
            # jsonify the cafe data
            id=rand_cafe.id,
            name=rand_cafe.name,
            map_url=rand_cafe.map_url,
            img_url=rand_cafe.img_url,
            location=rand_cafe.location,
            seats=rand_cafe.seats,
            has_toilet=rand_cafe.has_toilet,
            has_wifi=rand_cafe.has_wifi,
            has_sockets=rand_cafe.has_sockets,
            can_take_calls=rand_cafe.can_take_calls,
            coffee_price=rand_cafe.coffee_price,
        ).json  # convert the Response object to a dictionary
    )
    return cafe


#  HTTP POST - Create Record

#  HTTP PUT/PATCH - Update Record

#  HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True, port=5006)
