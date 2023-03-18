
from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud
from datetime import datetime

from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")


@app.route("/users")
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

        session["email"] = user.email
        session["name"] = user.display_name
        session["region_id"] = user.region_id
        session["user_id"] = user.user_id
        
        flash(f"Welcome back, {user.display_name} ({user.email})!")

    return redirect(f"/message_board/{user.region_id}")

@app.route("/map/parkmap", methods = ["POST"])
def view_parkmap():

    zipcode = request.form.get('zipcode')

    """Demo of basic map-related code.

    - Programmatically adding markers, info windows, and event handlers to a
      Google Map
    - Showing polylines, directions, etc.
    requests.form.get('zipcode')
    """

    return render_template("parkmap.html", zipcode=zipcode)

if __name__ == "__main__":
    connect_to_db(app)
    app.run()
    host="0.0.0.0",
    use_reloader=True,
    use_debugger=True,