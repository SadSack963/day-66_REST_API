import flask.json
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy  # pip install Flask-SQLAlchemy
import random
import json
import os

# The API documentation is viewable at https://documenter.getpostman.com/view/15623189/TzRNEV41


API_KEY = "MySecretAPIKey"
FILE_URL = 'sqlite:///database/cafes.db'
app = Flask(__name__)

"""
    DEFAULT FLASK APP CONFIGURATION
    ===============================
    default_config = {
        'APPLICATION_ROOT': '/',
        'DEBUG': None,
        'ENV': None,
        'EXPLAIN_TEMPLATE_LOADING': False,
        'JSONIFY_MIMETYPE': 'application/json',
        'JSONIFY_PRETTYPRINT_REGULAR': False,
        'JSON_AS_ASCII': True,
        'JSON_SORT_KEYS': True,
        'MAX_CONTENT_LENGTH': None,
        'MAX_COOKIE_SIZE': 4093,
        'PERMANENT_SESSION_LIFETIME': datetime.timedelta(days = 31),
        'PREFERRED_URL_SCHEME': 'http',
        'PRESERVE_CONTEXT_ON_EXCEPTION': None,
        'PROPAGATE_EXCEPTIONS': None,
        'SECRET_KEY': None,
        'SEND_FILE_MAX_AGE_DEFAULT': None,
        'SERVER_NAME': None,
        'SESSION_COOKIE_DOMAIN': None,
        'SESSION_COOKIE_HTTPONLY': True,
        'SESSION_COOKIE_NAME': 'session',
        'SESSION_COOKIE_PATH': None,
        'SESSION_COOKIE_SAMESITE': None,
        'SESSION_COOKIE_SECURE': False,
        'SESSION_REFRESH_EACH_REQUEST': True,
        'TEMPLATES_AUTO_RELOAD': None,
        'TESTING': False,
        'TRAP_BAD_REQUEST_ERRORS': None,
        'TRAP_HTTP_EXCEPTIONS': False,
        'USE_X_SENDFILE': False
    }
"""

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


# HOME PAGE

@app.route("/")
def home():
    return render_template("index.html")
    

#  HTTP GET - Read Records

@app.route("/random", methods=["GET"])
def get_random_cafe():
    # get a random cafe from the database
    # Select all results from the search <class 'flask_sqlalchemy.BaseQuery'>
    all_cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(all_cafes)
    # Turn the random cafe SQLAlchemy Object into a JSON Response object

    # # The original manual dictionary method
    # cafe = {
    #     'id': random_cafe.id,
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
    # 200 	OK 	Action completed successfully
    return jsonify(cafes=random_cafe.to_dict()), 200


@app.route("/all", methods=["GET"])
def get_all_cafes():
    # get all cafes from the database
    # Select all results from the search <class 'flask_sqlalchemy.BaseQuery'>
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
    # 200 	OK 	Action completed successfully
    return jsonify(cafes=all_cafes_dict), 200


@app.route("/search", methods=["GET"])
def find_cafes():
    # Get value from URL query string e.g. http://127.0.0.1:5006/search?loc=Peckham
    # https://flask.palletsprojects.com/en/1.1.x/api/#flask.Request.args
    location = request.args.get('loc')
    # Select all results from the search <class 'flask_sqlalchemy.BaseQuery'>
    found_cafes = db.session.query(Cafe).filter_by(location=location).all()
    if found_cafes:
        # combine into a list of dictionaries
        # 200 	OK 	Action completed successfully
        return jsonify(cafes=[cafe.to_dict() for cafe in found_cafes]), 200
    else:
        # 404 	Not Found 	Requested file was not found
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404


#  HTTP POST - Create Record

@app.route("/add", methods=["POST"])
def add_cafe():
    def check_bool(value):
        return 1 if value == '1' or value.lower() == 'true' else 0

    # Get field values from request body and create a new Cafe object
    # request.form returns an immutable dictionary (ImmutableMultiDict)
    # the boolean values must be blank, 0 or 1
    data = request.form
    new_cafe = Cafe(
        name=data['name'],
        map_url=data['map_url'],
        img_url=data['img_url'],
        location=data['location'],
        seats=data['seats'],
        has_toilet=check_bool(data['has_toilet']),
        has_wifi=check_bool(data['has_wifi']),
        has_sockets=check_bool(data['has_sockets']),
        can_take_calls=check_bool(data['can_take_calls']),
        coffee_price=data['coffee_price'],
    )
    # Check if cafe is already in the database
    # Select all results from the search <class 'flask_sqlalchemy.BaseQuery'>
    search_cafe = db.session.query(Cafe).filter_by(
        name=new_cafe.name,
        location=new_cafe.location
    ).all()
    if search_cafe:
        # 400 	Bad Request
        # Request had bad syntax or was impossible to fulfill
        return jsonify(error={"exists": "Cafe already exists."}), 400
    else:
        # Add cafe to database
        db.session.add(new_cafe)
        db.session.commit()
        # 200 	OK 	Action completed successfully
        return jsonify(response={"success": "Successfully added the new cafe."}), 200


#  HTTP PUT/PATCH - Update Record

@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    # Get value from URL query string e.g. http://127.0.0.1:5006/search?loc=Peckham
    # https://flask.palletsprojects.com/en/1.1.x/api/#flask.Request.args
    new_price = request.args.get('new-price')
    # Select the first match from the search: <class 'flask_sqlalchemy.BaseQuery'>
    cafe = db.session.query(Cafe).filter_by(
        id=int(cafe_id),
    ).first()
    # Angela used:
    # cafe = db.session.query(Cafe).get(cafe_id)
    if cafe:
        # print("cafe =", cafe, type(cafe))  # >>> cafe = <Cafe 22> <class '__main__.Cafe'>
        cafe.coffee_price = new_price
        db.session.commit()
        # 200 	OK 	Action completed successfully
        return jsonify(response={"success": f"Price updated to {cafe.coffee_price} for {cafe.name}."}), 200
    else:
        # 404 	Not Found 	Requested file was not found
        return jsonify(error={"Not Found": f"A cafe with ID={cafe_id} was not found."}), 404


#  HTTP DELETE - Delete Record

@app.route("/report-closed/<cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    key_data = request.form['api-key']
    if key_data == API_KEY:
        # delete the entry
        cafe = db.session.query(Cafe).get(cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            # 200 	OK 	Action completed successfully
            return jsonify(response={"success": f"Cafe {cafe.name} removed from database."}), 200
        else:
            # 404 	Not Found 	Requested file was not found
            return jsonify(error={"Not Found": f"A cafe with ID={cafe_id} was not found."}), 404
    else:
        # 403 	Forbidden
        # Request does not specify the file name, or the directory
        # or the file does not have the permission that allows the pages to be viewed from the web
        return jsonify(error={"Forbidden": "Not Authorized to delete a cafe."}), 403
    pass


if __name__ == '__main__':
    app.run(debug=True, port=5006)
