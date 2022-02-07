 
from MUC_app.config.mysqlconnection import connectToMySQL
from MUC_app.models import maker, user
from flask import flash

class Car:
    #attributes

    def __init__(self, data):#constructor : DATA expected to be a dictionary 
        self.id = data['id']
        self.color = data['color']
        self.year = data['year']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.maker = None
        self.user = None
        
        
    #Methods
    @classmethod
    def get_all(cls): #when we pull from the database, we expect a list of DICTS 
        #query
        query = 'SELECT * FROM cars;' 
        #actually query the database
        results = connectToMySQL('cars_db').query_db(query)
        #new list to append objects to
        cars = []
        #for loop
        for car in results:
        # turn DICTS into objects 
            cars.append(cls(car))
        #return new list of objects
        return cars

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO cars (color, year, created_at, updated_at, user_id, maker_id ) VALUES (%(color)s, %(year)s, NOW(), NOW(), %(user_id)s, %(maker_id)s);'
        return connectToMySQL('cars_db').query_db(query, data)

    @classmethod
    def get_one(cls, data): 
        query = 'SELECT * FROM cars WHERE cars.id = %(id)s;'  # since we need a variable for %(id)s, we will need to pass thru data, which will come from car.py
        results = connectToMySQL('cars_db').query_db(query, data)  # since our results will be a list, we can call the index position of that list to get back a value.        
        return (cls(results[0])) #then we simply return this as an object of car. 

    @classmethod
    def get_one_with_maker(cls, data): 
        #for this we will need to user JOIN and we are looking to make a makers object so we can chain OOP. such as: car.maker.name to return tesla
        # cars is the many, maker is the one. 
        query = 'SELECT * FROM cars JOIN makers ON cars.maker_id = makers.id WHERE cars.id = %(id)s;'
        results = connectToMySQL('cars_db').query_db(query, data) # this always returns a list of dicts 
        car = (cls(results[0]))
        # if we are going to create a maker object, we will need to call its constructor, which takes in a dict. so we will make that. 

        makers_data = { #NOTE: this is copied from maker.py, then edited to fit what we need. 
            'id' : results[0]['makers.id'], # NOTE, again we are specifying to the computer that when you see this key 'id', we want the results at index[0] from the list of dicts. NOTE: Since we are joining, we have to then specify where data is coming from on DATA that is repeated. ID is on users and makers. so we specify.
            'name' : results[0]['name'],
            'created_at' : results[0]['makers.created_at'],
            'updated_at' : results[0]['makers.updated_at'],
        } #NOTE: additionally, we have to import the MAKER file, NOT the CLASS Maker! to avoid circular imports. 

        car.maker = maker.Maker(makers_data) #in the above note, we set car.maker = (self.maker from constructor) maker.Maker(makers_data) (filename.CLASSNAME)(data we created)
        return car 

    @classmethod
    def get_one_with_user(cls, data): 
        query = 'SELECT * FROM cars JOIN users ON cars.user_id = users.id WHERE cars.id = %(id)s;'
        results = connectToMySQL('cars_db').query_db(query, data) # this always returns a list of dicts 
        car = (cls(results[0]))
        users_data = { 
            'id' : results[0]['users.id'], 
            'first_name' : results[0]['first_name'],
            'last_name' : results[0]['last_name'],
            'email': results[0]['email'],
            'created_at' : results[0]['users.created_at'],
            'updated_at' : results[0]['users.updated_at'],
        } 
        car.user = user.User(users_data)
        return car 

    @classmethod
    def get_one_complete(cls, data):
        query = 'SELECT * FROM cars JOIN users ON cars.user_id = users.id JOIN makers ON cars.maker_id = makers.id WHERE cars.id = %(id)s;'
        #NOTE we just copied our join statement from get_one_with_user, then added JOIN from get_one_with_maker.
        results = connectToMySQL('cars_db').query_db(query, data)
        car = (cls(results[0]))
        #add user to car.user
        users_data = { 
            'id' : results[0]['users.id'], 
            'first_name' : results[0]['first_name'],
            'last_name' : results[0]['last_name'],
            'email': results[0]['email'],
            'created_at' : results[0]['users.created_at'],
            'updated_at' : results[0]['users.updated_at'],
        }
        car.user = user.User(users_data)
        #add maker to car.maker
        makers_data = {
            'id' : results[0]['makers.id'],
            'name' : results[0]['name'],
            'created_at' : results[0]['makers.created_at'],
            'updated_at' : results[0]['makers.updated_at'],
        }

        car.maker = maker.Maker(makers_data)

        return car

    @classmethod
    def update(cls, data):
        query = 'UPDATE cars SET color = %(color)s, year = %(year)s, updated_at = NOW() WHERE cars.id = %(id)s;'
        return connectToMySQL('cars_db').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM cars WHERE cars.id = %(id)s;'
        return connectToMySQL('cars_db').query_db(query, data)


## example of flash message method
    @staticmethod
    def validate(data):
        is_valid = True

        if not data['color'].isalpha():
            flash('Colors are made with letters...duh!')
            is_valid = False
        if len(data['color']) < 3:
            flash('Colors must be 3 characters long. Doy.')
            is_valid = False
        if len(data['year']) < 4:
            flash('Year must be 4 characters')
            is_valid = False
        if len(data['year']) > 4: 
            flash('What year are you living in? years are 4 digits')
            is_valid = False

        #NOTE: believe this will only work, @ /cars/new, I dont allow them to create a car and select the model. 
        #NOTE: it is returning: TypeError: object of type 'bool' has no len(), so I think the validation check is incorrect.
        # query = 'SELECT * FROM makers WHERE makers.id = %(makers_id)s;'
        # results = connectToMySQL('cars_db').query_db(query, data)
        # if not len(results) == 1:
        #     is_valid = False
        #     flash('Invalid Maker')

        return is_valid 