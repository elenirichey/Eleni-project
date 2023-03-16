import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb Playdates")
print("dbdropped")
os.system("createdb Playdates")
print("dbcreated")

model.connect_to_db(server.app)
model.db.create_all()

#need to put user/region etc data in json file!! 
with open("data/regions.json") as f:
    region_data = json.loads(f.read())

# zipcodes_in_db=[]
# for zip in zip_in_region:
#     zipcode[]
# //if zipcode in zipinregion - user - zipcode - message - park - child --> park and child are optional
# //region is what makes the message board -->  i create message boards, users create user
# //and get assigned a region board based on their zipcode"""

# create regions, store in list so we can create fake users and messages
#do i need to account for zipcodes in each region?
# regions_in_db = []
for region in region_data:
    region_name, state, zip_in_region = (
        region["region_name"],
        region["state"],
        region["zip_in_region"]
        
    )
    # print(region_name)
    # print(state)

    db_region = crud.create_region(region_name, state)

    # zbr=[]

    for zip in zip_in_region:
        zipcode = crud.create_zipcode(zip, db_region.region_id)

        # print(zipcode)
#not sure which indent is appropriate
        # zbr.append(zipcode)
    # print(db_region)
    # regions_in_db.append(db_region)
    # print (zbr)
# print(regions_in_db)
# model.db.session.add_all(regions_in_db)
# model.db.session.commit()

#     release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")

#     db_movie = crud.create_movie(title, overview, release_date, poster_path)
#     movies_in_db.append(db_movie)











# Create 5 users; 
zipcodes = model.Zipcode.query.all()
print(zipcodes, 'line 76')

for n in range(5):
    email = f"user{n}@test.com"  # Voila! A unique email!
    password = "test"
    display_name = f"user {n}"
    # for region in region_data:
    #     zip_in_region = (region["zip_in_region"])

    zipcode = choice(zipcodes)
    # choice(region.region_id)
    # randint(1,5)# or? #

    user = crud.create_user(email, password, display_name, zipcode.zipcode)
    # model.db.session.add(user)
    # model.db.session.commit()

users= model.User.query.all()
test_messages=["Reese", "Rowan", "Ayan", "Anand", "Eleni", "Jude", "Maeve", "Avi"]
# each user will make 5 messages
for user in users:
    for n in range(5):
        test_message = choice(test_messages)

        message = crud.create_message(user_id=user.user_id, timestamp=datetime.now(), park_id = None, region_id = user.region_id, message = test_message)

#     for _ in range(10):
#         random_movie = choice(movies_in_db)
#         score = randint(1, 5) // user message userid park id

#         message = crud.create_message(user, random_movie, score)
#         model.db.session.add(rating)

# model.db.session.commit()