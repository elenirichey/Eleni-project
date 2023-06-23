
from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db
import crud
from sqlalchemy import cast, Date
from datetime import datetime, date

from jinja2 import StrictUndefined
import requests
from pprint import pprint


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """View homepage."""
    
    return render_template("homepage.html")


@app.route("/all_users")
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template("all_users.html", users=users)




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

        new_region = crud.create_region(region_name = city, state = state) 

        zipcodes_in_city = requests.get(f'https://www.zipcodeapi.com/rest/fuRLOSEI0hS9FnSFYExsRgXqXqxXJsSI5uRuN9GA2mJCcwQqTe06YCVkc87N2sQZ/city-zips.json/{url_city}/{state}').json()
        for zipp in zipcodes_in_city:
            zipcode = crud.create_zipcode(zipp, new_region.region_id)
        
    else:
        region_id= crud.get_region_by_zipcode(zipcode)

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
    while session:
   

        display_name=session.get("name")

        region_id = session.get("region_id")


        
        homeboard = crud.get_message_by_region(region_id)
        has_messages = len(homeboard)

        user = crud.get_user_by_email(session['email'])
        user_id =session.get("user_id")
        children = crud.get_child_by_user(user_id)

        

        return render_template("message_board.html", homeboard=homeboard, user=user, has_messages=has_messages, children=children)
    
    else:
        return redirect("/")


@app.route("/new_message", methods = ["POST"])
def add_new_message_to_homeboard():

   
    user = crud.get_user_by_email(session['email'])

    message = request.form.get("new-message")
    user_id = user.user_id
    park_id = None
    
    region_id = user.region_id
    

    new_message = crud.create_message(timestamp=(datetime.now()).strftime("%Y-%m-%d %H:%M:%S"), user_id=user_id, park_id = park_id, region_id = region_id, message = message)
    
    
    return redirect (f"/message_board/{user.region_id}")

# TODO: @app.route("/delete_message", methods = ["POST"])
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




@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")
    display_name = request.form.get("display_name")


    user = crud.get_user_by_email(email)
   
    if not user:
        flash("No such email address")
        return redirect("/")
    if user.password != password:
        flash("incorrect password")
        return redirect("/")
    


        # Log in user by storing the user's email in session
        # session["user"] = user
    session["logged_in"] = True
    session["email"] = user.email
    session["name"] = user.display_name
    session["region_id"] = user.region_id
    session["user_id"] = user.user_id
   
        
    flash(f"Welcome back, {user.display_name} ({user.email})!")
    print(session)
    return redirect(f"/message_board/{user.region_id}")

@app.route("/logout")
def process_logout():
    """Log user out."""
    
    
    del session["email"]
    del session["name"]
    del session["region_id"]
    del session["user_id"]
    del session["logged_in"]
    
   

    flash(f"Logged out.")
    return redirect("/")

@app.route("/map/parkmap", methods = ["POST"])
def view_parkmap():

    zipcode = request.form.get('zipcode')
#maybe eventually i can add the zipcodes in radius feature??

    return render_template("parkmap.html", zipcode=zipcode)


@app.route("/add_child", methods=["POST"])
def add_child():
    user_id=session.get("user_id")
    # birthdate = (cast(request.form.get("birthdate"), Date))
    birthdate= request.form.get("birthdate")
    
    # print (datetime.strptime(birthdate, '%m-%d-%Y'))
    user= crud.get_user_by_id(user_id)
    # print (datetime.strptime(birthdate,"%Y-%m-%d").strftime("%m/%d/%Y"))
    region_id = user.region_id
     
    child = crud.create_child(birthdate= birthdate, user_id=user_id)

    flash(f"Congratulations! You have added a child with a birthdate of {birthdate} to your profile")
   
    return redirect (f"/message_board/{user.region_id}")



@app.route("/local/parks", methods=["POST"])
def google():
    userLocation = request.json.get('loc')
    zipcode = str(request.json.get('zipcode'))
    print(userLocation, 'line 195')
    print(zipcode, 'line 196')
    #maybe eventually i can add the zipcodes in radius feature??
    lat=userLocation['lat']
    lng=userLocation['lng']
    
    url_parks = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query=park&location={lat},{lng}&radius=100&key=AIzaSyCBAi6UglC70WempK9I8qLUHiHKkNuWBy0'
    url_playgrounds = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query=playground&location={lat},{lng}&radius=100&key=AIzaSyCBAi6UglC70WempK9I8qLUHiHKkNuWBy0'
    
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

        new_region = crud.create_region(region_name = city, state = state) 
        region_id =  new_region.region_id

        zipcodes_in_city = requests.get(f'https://www.zipcodeapi.com/rest/fuRLOSEI0hS9FnSFYExsRgXqXqxXJsSI5uRuN9GA2mJCcwQqTe06YCVkc87N2sQZ/city-zips.json/{url_city}/{state}').json()
        
        for zipp in zipcodes_in_city:
            zipcode = crud.create_zipcode(zipp, new_region.region_id)

    else:
        region_id = zipp.region_id
   

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

    return jsonify(data)
# once its in db i cld query db for it



@app.route("/new_region", methods=["POST"])
def new_region():
   

    zipcode = request.form.get('zipcode')

    
    if not crud.zip_in_database(zipcode):
        zipcode_info = f'https://www.zipcodeapi.com/rest/fuRLOSEI0hS9FnSFYExsRgXqXqxXJsSI5uRuN9GA2mJCcwQqTe06YCVkc87N2sQZ/info.json/{zipcode}/degrees'

        city = zipcode_info['city']
        state = zipcode_info['state']

# create a region for city, state if one doesn't already exist
        new_region = crud.create_region(region_name = city, state = state) 

        zipcodes_in_city = f'https://www.zipcodeapi.com/rest/fuRLOSEI0hS9FnSFYExsRgXqXqxXJsSI5uRuN9GA2mJCcwQqTe06YCVkc87N2sQZ/city-zips.json/{city}/{state}'
        for zip in zipcodes_in_city:
            zipcode = crud.create_zipcode(zip, new_region.region_id)




@app.route("/parks")
def parks_in_region():
    if session:
        region_id = session['region_id']
        
        parks = crud.get_all_parks_by_region(region_id)

        return render_template("all_parks.html", parks = parks)
   
    else:
        return redirect("/")
@app.route("/parks/<park_id>")
def show_park_info(park_id):

    park = crud.get_park_by_id(park_id)
    
    return render_template("park_details.html", park = park)

@app.route("/signup")
def sign_up():
    return render_template("signup.html")

@app.route("/add_park")
def view_add_park():

    return render_template("add_park.html")

@app.route("/new_park", methods = ["GET", "POST"])
def process_add_park():
    park_name = request.form.get("park_name")
    park_address = request.form.get("park_address")
    zipcode = request.form.get("park_zipcode")
    zipcode_info = requests.get(f'https://www.zipcodeapi.com/rest/WDYLG229vLjY9yvVfANO5TACiqVVZbT1ADaOhjnSKNFQWUNKebQbBatoIJbaQAra/info.json/{zipcode}/degrees', verify=False).json()
    latitude = zipcode_info['lat']
    longitude = zipcode_info['lng']
    
    region_id = crud.get_region_by_zipcode(zipcode)
 
    crud.create_park(park_name = park_name, park_address = park_address, latitude = latitude, longitude = longitude, region_id=region_id ) 
   #don't know park address? enter info you have and we will look it up?
    flash(f"Success! you have added {park_name} at {park_address} to our list of parks!")
    
    return redirect ("/all_parks")


connect_to_db(app)
app.run()
host="0.0.0.0",
use_reloader=True,
use_debugger=True,

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
    print("connected to database")