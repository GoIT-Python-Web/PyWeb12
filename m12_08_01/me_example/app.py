import argparse

from mongoengine import *

connect(db="web12", host="mongodb+srv://userweb12:*****@krabaton.5mlpr.gcp.mongodb.net/?retryWrites=true&w=majority")

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


class Cat(Document):
    name = StringField(max_length=120, required=True)
    age = IntField(min_value=1, max_value=20)
    features = ListField(StringField(max_length=30))
    meta = {'collection': 'cats'}


def create(name, age, features):
    cat = Cat(name=name, age=age, features=features)
    cat.save()
    return cat


def find():
    # cats = Cat.objects.as_pymongo()
    cats = Cat.objects.all()
    return cats


def find_by_id(pk):
    try:
        cat = Cat.objects.get(id=pk)
        return cat
    except DoesNotExist:
        return "Немає такого кота"


def update(pk, name, age, features):
    cat = Cat.objects(id=pk).first()  # None якщо не існує
    if cat:
        cat.update(name=name, age=age, features=features)
        cat.reload()
    return cat


def remove(pk):
    cat = Cat.objects.get(id=pk)
    cat.delete()
    return cat


def main():
    match action:
        case 'create':
            result = create(name, age, features)
            print(result.to_mongo().to_dict())
        case 'find':
            result = find()
            # print(result)
            [print(r.to_mongo().to_dict()) for r in result]
        case 'update':
            result = update(_id, name, age, features)
            print(result.to_mongo().to_dict())
        case 'remove':
            result = remove(_id)
            print(result.to_mongo().to_dict())
        case _:
            print("Unknown command")


if __name__ == '__main__':
    main()
    # print(find_by_id("649b1a8bc48b832dfb7146f8"))
