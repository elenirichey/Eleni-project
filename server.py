
from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud

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
    user=session.get("user")
    display_name=session.get("user_display_name")
    # region_id = session.get("region_id")
    zipcode = request.args.get("zipcode")

    region_id = crud.get_region_by_zipcode(zipcode)
    homeboard = crud.get_message_by_region(region_id)

    return render_template("message_board.html", homeboard=homeboard, user=user, region_id=region_id, display_name=display_name)







@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)




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
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        session["user_display_name"] = user.display_name
        session["user_region_id"] = user.region_id
        
        flash(f"Welcome back, {user.email}, {user.display_name}!")

    return redirect(f"/message_board/{user.region_id}")



if __name__ == "__main__":
    connect_to_db(app)
    app.run()
    host="0.0.0.0",
    use_reloader=True,
    use_debugger=True,