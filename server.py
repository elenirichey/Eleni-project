
from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db
import crud
from datetime import datetime

from jinja2 import StrictUndefined
import requests
from pprint import pprint


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """View homepage."""
    # user = crud.get_user_by_email(session['email'])
    return render_template("homepage.html")


@app.route("/all_users")
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template("all_users.html", users=users)

# @app.route("/parks")


@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")
    display_name = request.form.get("display_name")
    zipcode = request.form.get("zipcode")
    print(zipcode)
    zipp = crud.zip_in_database(zipcode)
    print(zipp)

    if not zipp:

        zipcode_info = requests.get(f'https://www.zipcodeapi.com/rest/WDYLG229vLjY9yvVfANO5TACiqVVZbT1ADaOhjnSKNFQWUNKebQbBatoIJbaQAra/info.json/{zipcode}/degrees', verify=False).json()

        city = zipcode_info['city']
        state = zipcode_info['state'] 
        url_city = city.replace(' ', '+')

        new_region = crud.create_region(region_name = city, state = state) # return your newly created region object from your db <Region>
        # new_zipcode = Zipcode(zipcode=userLocation, region=new_region)

        zipcodes_in_city = requests.get(f'https://www.zipcodeapi.com/rest/fuRLOSEI0hS9FnSFYExsRgXqXqxXJsSI5uRuN9GA2mJCcwQqTe06YCVkc87N2sQZ/city-zips.json/{url_city}/{state}').json()
        for zipp in zipcodes_in_city:
            zipcode = crud.create_zipcode(zipp, new_region.region_id)
        # new_region = crud.create_region(region_name = city, state = state)


    user = crud.get_user_by_email(email)

    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, password, display_name, zipcode)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")



@app.route("/message_board")



@app.route("/message_board/<region_id>")
def show_homeboard(region_id):
    """show user's home message board"""
    # user=session.get("")

    display_name=session.get("name")

    region_id = session.get("region_id")

    # print(session['zipcode'])
    # region_id = crud.get_region_by_zipcode(zipcode)
    # crud.create_Message(datetime.now(), 1, None, 1, "hello there")
    homeboard = crud.get_message_by_region(region_id)
    has_messages = len(homeboard)

    user = crud.get_user_by_email(session['email'])

    return render_template("message_board.html", homeboard=homeboard, user=user, has_messages=has_messages)



@app.route("/new_message", methods = ["POST"])
def add_new_message_to_homeboard():

   
    user = crud.get_user_by_email(session['email'])

    message = request.form.get("new-message")
    user_id = user.user_id
    park_id = None
    # request.form.get("park_id")
    region_id = user.region_id
    

    new_message = crud.create_message(timestamp=datetime.now(), user_id=user_id, park_id = park_id, region_id = region_id, message = message)
    
    
    return redirect (f"/message_board/{user.region_id}")

# @app.route("/delete_message", methods = ["POST"])
# def delete_user_message():
#     message = request.form.get("selected-message")
    #comes from clicking on the delete button in the message - so clicking that button should send the info of the message id


@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""
    user_id = session.get("user_id")
    user = crud.get_user_by_id(user_id)
    messages = crud.get_message_by_user(user_id)
    user_children = crud.get_child_by_user(user_id)

    return render_template("user_details.html", user=user, user_id=user_id, messages=messages, user_children=user_children)

@app.route("/users/<user_id>/children")
def show_user_children(user_id):
    user_id=session.get("user_id")
    user = crud.get_user_by_id(user_id)
    user_children = crud.get_child_by_user(user_id)
    for child in user_children:
        child_age = crud.get_child_by_age(child)
        return child_age



@app.route("/users/<region_id>")
def show_users(region_id):
    """show all users in particular region"""

    users_in_region = crud.get_users_by_region(region_id)

    return render_template("users_in_region.html", users = users_in_region)


#get first region id by zipcode and create user with region id

@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")
    display_name = request.form.get("display_name")


    user = crud.get_user_by_email(email)

    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        return redirect("/")
    else:
        # Log in user by storing the user's email in session
        # session["user"] = user
        session["email"] = user.email
        session["name"] = user.display_name
        session["region_id"] = user.region_id
        session["user_id"] = user.user_id
        
        flash(f"Welcome back, {user.display_name} ({user.email})!")

    return redirect(f"/message_board/{user.region_id}")


@app.route("/map/parkmap", methods = ["POST"])
def view_parkmap():

    zipcode = request.form.get('zipcode')


    return render_template("parkmap.html", zipcode=zipcode)



@app.route("/local/parks", methods=["POST"])
def google():
    userLocation = request.json.get('loc')
    zipcode = str(request.json.get('zipcode'))
    print(userLocation, 'line 195')
    print(zipcode, 'line 196')

    lat=userLocation['lat']
    lng=userLocation['lng']
    #Dynanmic so you can put variables in string
    # url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat}%2C{lng}&radius=7500&type=park&keyword={keyword}&key=AIzaSyCBAi6UglC70WempK9I8qLUHiHKkNuWBy0'
    # url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query=playground+{lat}+{lng}&key=AIzaSyCBAi6UglC70WempK9I8qLUHiHKkNuWBy0'
    # url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={keyword}&location={lat},{lng}&radius=10&key=AIzaSyCBAi6UglC70WempK9I8qLUHiHKkNuWBy0'
    url_parks = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query=park&location={lat},{lng}&radius=500&key=AIzaSyCBAi6UglC70WempK9I8qLUHiHKkNuWBy0'
    url_playgrounds = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query=playground&location={lat},{lng}&radius=500&key=AIzaSyCBAi6UglC70WempK9I8qLUHiHKkNuWBy0'
    
    park_data = requests.get(url_parks).json()
    playground_data = requests.get(url_playgrounds).json()

    data = park_data['results']
    data.extend(playground_data['results'])

    zipp = crud.zip_in_database(zipcode)
    region_id = 0

    if not zipp:

        zipcode_info = requests.get(f'https://www.zipcodeapi.com/rest/WDYLG229vLjY9yvVfANO5TACiqVVZbT1ADaOhjnSKNFQWUNKebQbBatoIJbaQAra/info.json/{zipcode}/degrees', verify=False).json()

        city = zipcode_info['city']
        state = zipcode_info['state'] 
        url_city = city.replace(' ', '+')

        new_region = crud.create_region(region_name = city, state = state) # return your newly created region object from your db <Region>
        # new_zipcode = Zipcode(zipcode=userLocation, region=new_region)
        region_id =  new_region.region_id

        zipcodes_in_city = requests.get(f'https://www.zipcodeapi.com/rest/fuRLOSEI0hS9FnSFYExsRgXqXqxXJsSI5uRuN9GA2mJCcwQqTe06YCVkc87N2sQZ/city-zips.json/{url_city}/{state}').json()
        
        for zipp in zipcodes_in_city:
            zipcode = crud.create_zipcode(zipp, new_region.region_id)

    else:
        region_id = zipp.region_id
    # if not region_id:
        #     city = data[0]['formatted_address'].split(',')[-3].strip(" ")
        #     state = data[0]['formatted_address'].split(',')[-2][1:3]
        # regioN = crud.get_regions_by_state(state, city) # endregion
        #     if region:
        #         region_id = region.region_id
        #     else:
        #         new_reg = crud.create_region(city, state)
        #         new_zip = crud.create_zipcode(zipcode, new_reg.region_id)
        #         region_id = new_zip.region_id

    all_park_names = set(crud.all_parknames_by_region(region_id))
    all_zipcodes = crud.return_all_zipcodes()

    for park in data:
        park_name = park['name']
        park_address = park['formatted_address']
        longitude = float(park['geometry']['location']['lng'])
        latitude = float(park['geometry']['location']['lat'])      
        # hours=park['opening_hours']
        #park_hours? park amenities? should i add them to my model as optional?
        if park_name not in all_park_names:
            crud.create_park(park_name=park_name, park_address = park_address, latitude = latitude, longitude=longitude, region_id=region_id )
#can i combine two calls for the data?? to get both park and playground?
#or to use both my db data and google data? do i need to jsonify the data before the loop?
    return jsonify(data)
# once its in db i cld query db for it

    # print(data)
#     for park in data['results']:
#         park_name = park['name']
#         # park_address = park['vicinity']
#         park_address = park['formatted_address']
#         longitude = float(park['geometry']['location']['lng'])
#         latitude = float(park['geometry']['location']['lat'])
#         region_id = crud.get_region_by_zipcode(zipcode)
#         print(region_id, 'line 211')
#         # hours=park['opening_hours']
#         #park_hours? park amenities? should i add them to my model as optional?
#         if park not in crud.get_all_parks_by_region(region_id):
#             crud.create_park(park_name=park_name, park_address = park_address, latitude = latitude, longitude=longitude, region_id=region_id )
# #can i combine two calls for the data?? to get both park and playground?
# #or to use both my db data and google data? do i need to jsonify the data before the loop?
#     return jsonify(data['results'])
# once its in db i cld query db for it


@app.route("/new_region", methods=["POST"])
def new_region():
    # userLocation=request.json.get('loc')

    # lat=userLocation['lat']
    # lng=userLocation['lng']

    zipcode = request.form.get('zipcode')

    # location = f'https://maps.googleapis.com/maps/api/geocode/json?address={zipcode}&key=AIzaSyCBAi6UglC70WempK9I8qLUHiHKkNuWBy0'


    # zipcode_radius = f'https://www.zipcodeapi.com/rest/fuRLOSEI0hS9FnSFYExsRgXqXqxXJsSI5uRuN9GA2mJCcwQqTe06YCVkc87N2sQZ/radius.json/{zipcode}/5/mile'
    if not crud.zip_in_database(zipcode):
        zipcode_info = f'https://www.zipcodeapi.com/rest/fuRLOSEI0hS9FnSFYExsRgXqXqxXJsSI5uRuN9GA2mJCcwQqTe06YCVkc87N2sQZ/info.json/{zipcode}/degrees'

        city = zipcode_info['city']
        state = zipcode_info['state']

# create a region for city, state if one doesn't already exist
        new_region = crud.create_region(region_name = city, state = state) # return your newly created region object from your db <Region>
# new_zipcode = Zipcode(zipcode=userLocation, region=new_region)

        zipcodes_in_city = f'https://www.zipcodeapi.com/rest/fuRLOSEI0hS9FnSFYExsRgXqXqxXJsSI5uRuN9GA2mJCcwQqTe06YCVkc87N2sQZ/city-zips.json/{city}/{state}'
        for zip in zipcodes_in_city:
            zipcode = crud.create_zipcode(zip, new_region.region_id)

#create region using city, then take zipcode user input and create zipcode
#new_region = crud.create_region(city, state)
#zipcode = crud.create_zipcode(zipcode, region_id)


@app.route("/parks")
def parks_in_region():
    region_id = session['region_id']
    print(region_id)
    parks = crud.get_all_parks_by_region(region_id)

    return render_template("all_parks.html", parks = parks)
#     # email = request.form.get("email")
#     # user = crud.get_user_by_email(email)
#     # region_id = crud.get_user_region(user)
#     parks = []

#     for park in crud.get_all_parks_by_region(region_id):
#             parks.append({
#             "id": park.park_id,
#             "park name": park.park_name,
#             "address": park.park_address,   
# #add all messages by park?
# #be able to click on park and take to a park page?
#         }) 
#     return parks
app.route("/parks/<park_id>")
def show_park_info(park):
#need event listener for click on park link?
    park = crud.get_park_by_id(park.park_id)
    
    return render_template("park_details.html", park = park)


@app.route("/add_park")
def view_add_park():

    return render_template("add_park.html")

@app.route("/new_park", methods = ["GET", "POST"])
def process_add_park():
    park_name = request.form.get("park_name")
    park_address = request.form.get("park_address")
    zipcode = request.form.get("park_zipcode")
    # request.json.get - api request call api request for that address
    # latitude = 
    # longitude = 
    region_id = crud.get_region_by_zipcode(zipcode)
 # address city/state/etc
#  https://maps.googleapis.com/maps/api/geocode/json?address={zipcode}&key=AIzaSyCBAi6UglC70WempK9I8qLUHiHKkNuWBy0'
    crud.create_park(park_name = park_name, park_address = park_address, zipcode=zipcode, region_id=region_id )
   #don't know park address? enter info you have and we will look it up?
    flash(f"Success! you have added {park_name} at {park_address} to our list of parks!")
    
    return redirect ("/all_parks")#render_template ("add_park.html", park_name = park_name, park_address = park_address, park_zipcode = zipcode) #return redirect ("/all_parks") - update all parks
   
#    methods = ["GET", "POST"]
connect_to_db(app)
app.run()
host="0.0.0.0",
use_reloader=True,
use_debugger=True,

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
    print("connected to database")