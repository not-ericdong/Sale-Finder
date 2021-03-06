"""
I was going to use pymongo but I wanted this app to be easily accessable
So I used a text file to store the values from the user so they don't have to install
mongoDB to use this program
"""

import json
import os

file_name = "product_data.txt"
sale_dict = {}


def is_empty():
    return os.stat(file_name).st_size == 0


# write to database using json.dump so I can use
# json.loads to get the text back as a dictionary later
def write_db(data):
    db = open(file_name, "a")
    db.write(json.dumps(data) + '\n')
    db.close()


# reads the text file db and returns a dictionary key=url value=dictionary
def read_db():
    db = open(file_name, "r")
    for line in db:
        data = json.loads(line)
        sale_dict[data['url']] = data
    # print(sale_dict)
    db.close()
    return sale_dict


# deletes any line that contains 'item' - I pass the url as item
def delete_db(item):
    lines = []
    with open(file_name, "r") as db:
        try:
            for line in db:
                lines.append(json.loads(line))
        except ValueError:
            print("Unwanted value in database, please try again")
    with open(file_name, "w") as db:
        for line in lines:
            if item not in str(line):
                db.write(json.dumps(line) + '\n')
    db.close()
