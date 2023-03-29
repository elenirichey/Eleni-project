"""CRUD operations"""

from model import db, Region, User, Park, Zipcode, Child, Message, connect_to_db

from datetime import datetime

def create_region(region_name, state):
    """create a region"""
    region = Region(region_name=region_name, state=state)
    db.session.add(region)
    db.session.commit()
    return region
#add zip to region??

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

# get regions by zipcode? within ____ miles? //get zipcodes in region
def get_region_by_zipcode(zipcode):
    region_by_zip = db.session.query(Zipcode).filter_by(zipcode=zipcode).first()
    if region_by_zip:
        return region_by_zip.region_id
        # return region_by_zip.region_id #or region.name?
    # .filter_by(zipcodes = zipcode)
    
#pass as a region id in create user function
#before creating user, run function get region by zipcode and get region id and create user with this region id


def create_user(email, password, display_name, zipcode):
    """create a user"""
    # if zipcode:
    region_id = get_region_by_zipcode(zipcode)
    # else:
    #     zipcode=create_zipcode(zipcode, region_id)
    # print(region_id)
    if region_id:
        user = User(email=email, password=password, display_name=display_name, region_id=region_id)
        db.session.add(user)
        db.session.commit()

    # else: 
    #     zipcode_info = f'https://www.zipcodeapi.com/rest/fuRLOSEI0hS9FnSFYExsRgXqXqxXJsSI5uRuN9GA2mJCcwQqTe06YCVkc87N2sQZ/info.json/{zipcode}/degrees'
    #     # city = zipcode_info['city']
    #     city = zipcode_info['city']
    #     state = zipcode_info['state'] 

    #     new_region = create_region(region_name = city, state = state)
    #     region_id= new_region.region_id

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

def get_user_region(user):
    """get a user's region"""
    
    return user.region_id


#crud add park to db?


def create_park(park_name, park_address, latitude, longitude, region_id):
    """create a park"""

    # print(park_name, park_address, latitude, longitude, region_id, 'line 98')
    park=Park(park_name=park_name, park_address=park_address, latitude=latitude, longitude=longitude, region_id=region_id)
    print(park, 'lin')
    db.session.add(park)
    db.session.commit()
    # print(park.park_id, 'line 100')
    return park


def get_all_parks_by_region(region_id):
    """get all parks in a region"""
    parks_in_region = db.session.query(Park).filter_by(region_id = Park.region_id)
    return parks_in_region
    # return Park.query.all() #where park zipcode in zip_in_region
#get all parks by zipcode? by region?
#get all parks by message ie have a message abt them? by playgroup? by users?
#is that necessary if we have it by region ie message boards


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
    # return Zipcode.query.all()#where zipcode in zip_in_region

    zips_in_region = db.session.query(Zipcode).filter_by(region_id = region_id)
    return zips_in_region
#get zipcode by region

#if zipcode in Region.zipcodes #Region.region_id.zipcodes?

def zip_in_database(zipcode):
#    if db.session.query(Zipcode).filter_by(zipcode=zipcode):
#     return True
    zip =  db.session.query(Zipcode).filter_by(zipcode=zipcode).first()
    return zip


def create_child(birthdate, user_id):

    child = Child(birthdate=birthdate, user_id=user_id)
    """create a child"""

    return child


def get_child_by_user(user_id):
    """get a user's children"""
    
    user_children = db.session.query(Child).filter_by(user_id =user_id)
    
    return user_children


def get_child_by_age(child):
    child_age= (datetime.now() - child.birthdate)
    """get users with children of specified age"""
# ???
    return child_age

# def get_child_age(child):
#     user_id = 
#     user_children = db.session.query(Child).filter_by(user_id =user_id)



def create_message(timestamp, user_id, park_id, region_id, message):
    "create a message"
#how do i signal that the parkid is optional?
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
    #should i call it create_message_board? message_board # region.messages?

    homeboard = db.session.query(Message).filter_by(region_id = region_id).all()
    return homeboard



def get_message_by_park_id(park_id):
    """get all posts referencing a specific park(id)"""
    park_messages = db.session.query(Message).filter_by(park_id = Park.park_id)
    return park_messages

#get message by day? to look for playdates in area on specific day? idk




if __name__ == "__main__":
    from server import app

    connect_to_db(app)