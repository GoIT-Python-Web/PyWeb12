from mongoengine import Document, connect, BooleanField, StringField

connect(db='web12', host="mongodb+srv://userweb12:****@krabaton.5mlpr.gcp.mongodb.net/?retryWrites=true&w=majority")


class Task(Document):
    completed = BooleanField(default=False)
    consumer = StringField()
