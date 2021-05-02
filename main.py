from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy  # pip install Flask-SQLAlchemy
import random
import json
import os


FILE_URL = 'sqlite:///database/cafes.db'
app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = FILE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    __tablename__ = "Cafes"

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

    # Angela's method: Convert database record to a dictionary
    def to_dict(self):
        # # Method 1.
        # dictionary = {}
        # # Loop through each column in the data record
        # for column in self.__table__.columns:
        #     # Create a new dictionary entry;
        #     # where the key is the name of the column
        #     # and the value is the value of the column
        #     dictionary[column.name] = getattr(self, column.name)
        # return dictionary

        # Method 2. Alternatively use Dictionary Comprehension to do the same thing.
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# Create the database file and tables
if not os.path.isfile(FILE_URL):
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")
    

#  HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def get_random_cafe():
    # get a random cafe from the database
    all_cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(all_cafes)
    # Turn the random cafe SQLAlchemy Object into a JSON Response object

    # # The original manual dictionary method
    # cafe = {
    #     'id': rand_cafe.id,
    #     'name': random_cafe.name,
    #     'map_url': random_cafe.map_url,
    #     'img_url': random_cafe.img_url,
    #     'location': random_cafe.location,
    #     'seats': random_cafe.seats,
    #     'has_toilet': random_cafe.has_toilet,
    #     'has_wifi': random_cafe.has_wifi,
    #     'has_sockets': random_cafe.has_sockets,
    #     'can_take_calls': random_cafe.can_take_calls,
    #     'coffee_price': random_cafe.coffee_price,
    # }
    # return jsonify(cafe=cafe)

    # # This method saves me having to manually type out the dictionary
    # cafe = jsonify(
    #     # jsonify the dictionary
    #     cafe=jsonify(
    #         # jsonify the cafe data
    #         id=random_cafe.id,
    #         name=random_cafe.name,
    #         map_url=random_cafe.map_url,
    #         img_url=random_cafe.img_url,
    #         location=random_cafe.location,
    #         seats=random_cafe.seats,
    #         has_toilet=random_cafe.has_toilet,
    #         has_wifi=random_cafe.has_wifi,
    #         has_sockets=random_cafe.has_sockets,
    #         can_take_calls=random_cafe.can_take_calls,
    #         coffee_price=random_cafe.coffee_price,
    #     ).json  # convert the Response object to a dictionary
    # )
    # return cafe

    # Even better solution from Angela: add to_dict() function to the class
    # Simply convert the random_cafe data record to a dictionary of key-value pairs.
    return jsonify(cafes=random_cafe.to_dict())


@app.route("/all", methods=["GET"])
def get_all_cafes():
    # get all cafes from the database
    all_cafes = db.session.query(Cafe).all()
    # combine into a list of dictionaries
    all_cafes_dict = [cafe.to_dict() for cafe in all_cafes]
    """
    {
      "all_cafes": [
        {
          "can_take_calls": true, 
          "coffee_price": "\u00a32.40", 
          "has_sockets": true, 
          "has_toilet": true, 
          "has_wifi": false, 
          "id": 1, 
          "img_url": "https://atlondonbridge.com/wp-content/uploads/2019/02/Pano_9758_9761-Edit-190918_LTS_Science_Gallery-Medium-Crop-V2.jpg", 
          "location": "London Bridge", 
          "map_url": "https://g.page/scigallerylon?share", 
          "name": "Science Gallery London", 
          "seats": "50+"
        }, 
        ...
      ]
    }
    """
    return jsonify(cafes=all_cafes_dict)


@app.route("/search", methods=["GET"])
def find_cafes():
    # Get value from URL query string e.g. http://127.0.0.1:5006/search?loc=Peckham
    # https://flask.palletsprojects.com/en/1.1.x/api/#flask.Request.args
    location = request.args.get('loc')
    found_cafes = db.session.query(Cafe).filter_by(location=location).all()
    if not found_cafes:
        found_cafes_dict = {"Not Found": "Sorry, we don't have a cafe at that location."}
    else:
        # combine into a list of dictionaries
        found_cafes_dict = [cafe.to_dict() for cafe in found_cafes]
    return jsonify(cafes=found_cafes_dict)


#  HTTP POST - Create Record

#  HTTP PUT/PATCH - Update Record

#  HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True, port=5006)
