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

model.connect_to_db(server.app)
model.db.create_all()

#need to put user/region etc data in json file!! 
with open("data/regions.json") as f:
    region_data = json.loads(f.read())


# //if zipcode in zipinregion - user - zipcode - message - park - child --> park and child are optional
# //region is what makes the message board -->  i create message boards, users create user
# //and get assigned a region board based on their zipcode"""

# create regions, store in list so we can create fake users and messages
#do i need to account for zipcodes in each region?
regions_in_db = []
for region in region_data:
    region_name, state = (
        region["region_name"],
        region["state"]
        
    )
    # print(region_name)
    # print(state)

    db_region = crud.create_region(region_name, state)
    # print(db_region)
    regions_in_db.append(db_region)
# print(regions_in_db)
model.db.session.add_all(regions_in_db)
model.db.session.commit()

#     release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")

#     db_movie = crud.create_movie(title, overview, release_date, poster_path)
#     movies_in_db.append(db_movie)










# Create 5 users; each user will make 5 messages
for n in range(5):
    email = f"user{n}@test.com"  # Voila! A unique email!
    password = "test"
    display_name = f"user {n}"

    region_id = randint(1,2)
    # choice(region.region_id)
    # randint(1,5)# or? #

    user = crud.create_user(email, password, display_name, region_id)
    model.db.session.add(user)
    model.db.session.commit()


#     for _ in range(10):
#         random_movie = choice(movies_in_db)
#         score = randint(1, 5)

#         rating = crud.create_rating(user, random_movie, score)
#         model.db.session.add(rating)

# model.db.session.commit()