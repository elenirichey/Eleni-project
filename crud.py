"""CRUD operations"""

from model import db, Region, User, Park, Zipcode, Child, Message, connect_to_db

from datetime import datetime

def create_region(region_name, state):
    """create a region"""
    region = Region(region_name=region_name, state=state)
    db.session.add(region)
    db.session.commit()
    return region


def get_regions():
    """return all regions"""
    return Region.query.all()


def return_all_zipcodes():
    zip_set = set()
    zips = Zipcode.query.all()
    for z in zips:
        zip_set.add(z.zipcode)
    return zip_set

def all_parknames_by_region(region):
    park_names = []
    parks = db.session.query(Park).filter_by(region_id=region).all()
    for park in parks:
        park_names.append(park.park_name)
    return park_names

def get_regions_by_state(state):
    """return all regions by state"""
    regions_by_state = db.session.query(Region).filter_by(state = state)
    return regions_by_state


def get_region_by_zipcode(zipcode):
    region_by_zip = db.session.query(Zipcode).filter_by(zipcode=zipcode).first()
    if region_by_zip:
        return region_by_zip.region_id
       

def create_user(email, password, display_name, zipcode):
    """create a user"""
    
    region_id = get_region_by_zipcode(zipcode)
    
    if region_id:
        user = User(email=email, password=password, display_name=display_name, region_id=region_id)
        db.session.add(user)
        db.session.commit()

    

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
    
    users_in_region = db.session.query(User).filter_by(region_id = region_id)
    return users_in_region


def get_user_region(user):
    """get a user's region"""
    
    return user.region_id





def create_park(park_name, park_address, latitude, longitude, region_id):
    """create a park"""

    
    park=Park(park_name=park_name, park_address=park_address, latitude=latitude, longitude=longitude, region_id=region_id)
    print(park, 'lin')
    db.session.add(park)
    db.session.commit()
    
    return park


def get_all_parks_by_region(region_id):
    """get all parks in a region"""
    parks_in_region = db.session.query(Park).filter_by(region_id = Park.region_id).all()
    return parks_in_region




def get_park_by_id(park_id):
    "return a park by park id"
    return Park.query.get(park_id)

def create_zipcode(zipcode, region_id):
   """create a zipcode"""

   zipcode = Zipcode(zipcode=zipcode, region_id=region_id)

   db.session.add(zipcode)
   db.session.commit()

   return zipcode


def get_zipcode_by_region(region_id):
    """get all zipcodes in region"""
    

    zips_in_region = db.session.query(Zipcode).filter_by(region_id = region_id)
    return zips_in_region




def zip_in_database(zipcode):

    zip =  db.session.query(Zipcode).filter_by(zipcode=zipcode).first()
    return zip


def create_child(birthdate, user_id):

    child = Child(birthdate=birthdate, user_id=user_id)
    """create a child"""
    db.session.add(child)
    db.session.commit()
    return child


def get_child_by_user(user_id):
    """get a user's children"""
    
    user_children = db.session.query(Child).filter_by(user_id =user_id).all()
    
    return user_children

def get_child_by_age(child):
    child_id = child.child_id
    kid= Child.query.get(child)

    birthdate = kid.birthdate
    child_age= (datetime.now().date - birthdate)
    return child_age




def create_message(timestamp, user_id, park_id, region_id, message):
    "create a message"

    message = Message(timestamp=timestamp, user_id=user_id, park_id=park_id, region_id=region_id, message=message)
    db.session.add(message)
    db.session.commit()
    return message


def get_message_by_user(user_id):
    """get all messages by a certain user"""
    user_messages = db.session.query(Message).filter_by(user_id = user_id)

    return user_messages


def get_message_by_region(region_id):
    """THIS IS HOW TO CREATE MESSAGE BOARDS""" 
    

    homeboard = db.session.query(Message).filter_by(region_id = region_id).all()
    return homeboard



def get_message_by_park_id(park_id):
    """get all posts referencing a specific park(id)"""
    park_messages = db.session.query(Message).filter_by(park_id = Park.park_id)
    return park_messages






if __name__ == "__main__":
    from server import app

    connect_to_db(app)