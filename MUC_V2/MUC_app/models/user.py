from MUC_app.config.mysqlconnection import connectToMySQL
from MUC_app.models import car
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    #attributes

    def __init__(self, data):#constructor : DATA expected to be a dictionary 
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.cars = []
        
    #Methods
    @classmethod
    def get_all(cls): #when we pull from the database, we expect a list of DICTS 
        #query
        query = 'SELECT * FROM users;' 
        #actually query the database
        results = connectToMySQL('cars_db').query_db(query)
        #new list to append objects to
        users = []
        #for loop
        for user in results:
        # turn DICTS into objects 
            users.append(cls(user))
        #return new list of objects
        return users

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, NOW(), NOW());'
        return connectToMySQL('cars_db').query_db(query, data)

    @classmethod
    def get_one_complete(cls, data):
        query = 'SELECT * FROM users LEFT JOIN cars ON cars.user_id = users.id WHERE users.id = %(id)s;' 
        #NOTE User is the one, cars are the many. a user can exist without a car. so if we run this with a regular JOIN, when we run this, if a user doesnt have a car, it will break out code because we will be left with an empty list for self.cars = []. SO WE USE A LEFT JOIN.
        results = connectToMySQL('cars_db').query_db(query, data)
        user = (cls(results[0]))

        if results[0]['cars.id'] == None: 
            #NOTE: since a user can exist without a car, we have to check if the user even has a car. if they do not, we just return the results of the query.
            return (cls(results[0]))
        else:
            #NOTE since one user can have many cars, we will get back a list of cars, in order to look through a list we need a for loop
            for car_dict in results:
                car_data = { 
                    'id' : car_dict['cars.id'], 
                    'color' : car_dict['color'],
                    'year' : car_dict['year'],
                    'created_at' : car_dict['cars.created_at'],
                    'updated_at' : car_dict['cars.updated_at'],
                }
                user.cars.append(car.Car.get_one_complete(car_data))
        return user

    @classmethod
    def get_one(cls,data):
        query = 'SELECT * FROM users WHERE users.id = %(id)s;'
        results = connectToMySQL('cars_db').query_db(query, data)
        return (cls(results[0]))

    @classmethod
    def update(cls, data):
        query = 'UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = NOW() WHERE users.id = %(id)s;'
        return connectToMySQL('cars_db').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM users WHERE users.id = %(id)s;'
        return connectToMySQL('cars_db').query_db(query, data)

    @staticmethod
    def validate(data):
        is_valid = True

        if not data['first_name'].isalpha():
            flash('First Names are made with letters...duh!')
            is_valid = False
        if len(data['first_name']) < 3:
            flash('First Names must be 3 characters long. Doy.')
            is_valid = False
        if not data['last_name'].isalpha():
            flash('Last Names are made with letters...duh!')
            is_valid = False
        if len(data['last_name']) < 3:
            flash('Last Names must be 3 characters long. Doy.')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid Email, must contain (@) and (.)')
            is_valid = False

        return is_valid 