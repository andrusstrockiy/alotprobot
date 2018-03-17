from peewee import *
database = SqliteDatabase('alotpro.db')


class CallRecords(Model):
    uploadedby = CharField(max_length=120)
    recid = AutoField()
    address = CharField(max_length=255)
    phone = CharField(max_length=32)
    name = CharField(max_length=140)
    zip = CharField(max_length=10)
    employees = CharField(null=True)
    city = CharField()
    state = CharField(max_length=40,null=True)
    status = CharField(null=True)
    business = CharField(null=True)
    products = CharField(null=True)
    epsbizid = CharField()
    callowner = CharField(default='NULL')
    telespend = CharField(null=True)
    rec_imp_date = TimeField()
    description = CharField(null=True)
    filename = CharField()

    class Meta:
        database = database




class Users(Model):
    chat_id = IntegerField()
    nickname = CharField(max_length=255)
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    lang = CharField(max_length=255)
    contact = CharField(max_length=255)
    device = CharField(max_length=255)
    device_model = CharField(max_length=255)
    fault = CharField(max_length=255)
    first_step_lang = CharField(max_length=255)
    second_step_choose = CharField(max_length=255)
    what_bad = CharField(max_length=255)

    class Meta:
        database = database

class Person(Model):
    name = CharField()
    birthday = DateField()
    is_relative = BooleanField()

    class Meta:
        database = database


