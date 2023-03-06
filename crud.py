"""CRUD operations"""

from model import db, Region, User, Park, Zipcode, Child, Message, connect_to_db

def create_region(region_name, state):
    """create a region"""

    region = Region(region_name=region_name, state=state)

    return region


def get_regions():
    """return all regions"""
    return Region.query.all()


def get_regions_by_state(state):
    """return all regions by state"""
    regions_by_state = db.session.query(Region).filter_by(state = state)
    return regions_by_state

# get regions by zipcode? within ____ miles? //get zipcodes in region
def get_region_by_zipcode(zipcode):
    region_by_zip = db.session.query(Region).filter_by(zipcode in Region.zipcodes)
    # .filter_by(zipcodes = zipcode)
    return region_by_zip
#pass as a region id in create user function
#before creating user, run function get region by zipcode and get region id and create user with this region id


def create_user(email, password, display_name, zipcode):
    """create a user"""
    region_id = (get_region_by_zipcode(zipcode))
    print(region_id)
    user = User(email=email, password=password, display_name=display_name, region_id=region_id)

    return user

def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def get_users_by_region(region_id):
    """get all users in region"""
    #return User.query.all(where region =)
    users_in_region = db.session.query(User).filter_by(region_id = region_id)
    return users_in_region
# get all users with/by zipcode?
#get user's children
#get users with children of a specified age







def create_park(park_name, park_address, latitude, longitude, region_id):
    """create a park"""

    park=Park(park_name=park_name, park_address=park_address, latitude=latitude, longitude=longitude, region_id=region_id)

    return park


def get_all_parks_by_region(region_id):
    """get all parks in a region"""
    parks_in_region = db.session.query(Park).filter_by(region_id = Park.region_id)
    return parks_in_region
    # return Park.query.all() #where park zipcode in zip_in_region
#get all parks by zipcode? by region?
#get all parks by message ie have a message abt them? by playgroup? by users?
#is that necessary if we have it by region ie message boards








def create_zipcode(zipcode, region_id):
   """create a zipcode"""

   zipcode = Zipcode(zipcode=zipcode, region_id=region_id)

   return zipcode


def get_zipcode_by_region(region_id):
    """get all zipcodes in region"""
    # return Zipcode.query.all()#where zipcode in zip_in_region

    zips_in_region = db.session.query(Zipcode).filter_by(region_id = region_id)
    return zips_in_region
#get zipcode by region





def create_child(birthdate, user_id):

    child = Child(birthdate=birthdate, user_id=user_id)
    """create a child"""

    return child


def get_child_by_user(user_id):
    """get a user's children"""
    user_children = db.session.query(Child).filter_by(user_id =user_id)
    return user_children


def get_child_by_age():
    """get users with children of specified age"""
# ???




def create_Message(timestamp, user_id, park_id, region_id, message):
    "create a message"
#how do i signal that the parkid is optional?
    message = Message(timestamp=timestamp, user_id=user_id, park_id=park_id, region_id=region_id, message=message)

    return message


def get_message_by_user(user_id):
    """get all messages by a certain user"""
    user_messages = db.session.query(Message).filter_by(user_id = user_id)
    return user_messages


def get_message_by_region(region_id):
    """THIS IS HOW TO CREATE MESSAGE BOARDS""" 
    #should i call it create_message_board?
    message_board = db.session.query(Message).filter_by(region_id = Region.region_id)
    return message_board



def get_message_by_park_id(park_id):
    """get all posts referencing a specific park(id)"""
    park_messages = db.session.query(Message).filter_by(park_id = Park.park_id)
    return park_messages

#get message by day? to look for playdates in area on specific day? idk




if __name__ == "__main__":
    from server import app

    connect_to_db(app)