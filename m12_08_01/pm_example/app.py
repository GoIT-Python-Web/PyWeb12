import argparse

from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://userweb12:*****@krabaton.5mlpr.gcp.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.web12

parser = argparse.ArgumentParser(description='Cats APP')
parser.add_argument('--action', help='Command: create, update, find, remove')
parser.add_argument('--id')
parser.add_argument('--name')
parser.add_argument('--age')
parser.add_argument('--features', nargs='+')

arguments = parser.parse_args()
my_arg = vars(arguments)

action = my_arg.get('action')
name = my_arg.get('name')
age = my_arg.get('age')
_id = my_arg.get('id')
features = my_arg.get('features')


def create(name, age, features):
    result = db.cats.insert_one({
        "name": name,
        "age": age,
        "features": features
    })
    return result


def find():
    return db.cats.find()


def find_by_id(pk):
    return db.cats.find_one({"_id": ObjectId(pk)})


def update(pk, name, age, features):
    result = db.cats.update_one({"_id": ObjectId(pk)}, {
        "$set": {
            "name": name,
            "age": age,
            "features": features
        }
    })
    return result


def remove(pk):
    return db.cats.delete_one({"_id": ObjectId(pk)})


def main():
    match action:
        case 'create':
            result = create(name, age, features)
            print(result)
        case 'find':
            result = find()
            [print(el) for el in result]
        case 'update':
            result = update(_id, name, age, features)
            print(result)
        case 'remove':
            result = remove(_id)
            print(result)
        case _:
            print("Unknown command")


if __name__ == '__main__':
    main()
    # print(find_by_id("649b1a8bc48b832dfb7146f8"))
