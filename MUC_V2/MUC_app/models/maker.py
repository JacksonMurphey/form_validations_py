
from MUC_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Maker:
    #attributes

    def __init__(self, data):#constructor : DATA expected to be a dictionary 
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    #Methods
    @classmethod
    def get_all(cls): #when we pull from the database, we expect a list of DICTS 
        #query
        query = 'SELECT * FROM makers;' 
        #actually query the database
        results = connectToMySQL('cars_db').query_db(query)
        #new list to append objects to
        makers = []
        #for loop
        for maker in results:
        # turn DICTS into objects 
            makers.append(cls(maker))
        #return new list of objects
        return makers

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO makers (name, created_at, updated_at) VALUES (%(name)s, NOW(), NOW());'
        return connectToMySQL('cars_db').query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = 'SELECT * FROM makers WHERE makers.id = %(id)s;'
        results = connectToMySQL('cars_db').query_db(query, data)
        return (cls(results[0]))

    @classmethod
    def update(cls, data):
        query = 'UPDATE makers SET name = %(name)s, updated_at = NOW() WHERE makers.id = %(id)s;'
        return connectToMySQL('cars_db').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM makers WHERE makers.id = %(id)s;'
        return connectToMySQL('cars_db').query_db(query, data)

    @staticmethod
    def validate(data):
        is_valid = True

        if not data['name'].isalpha():
            flash('Names are made with letters...duh!')
            is_valid = False
        if len(data['name']) < 3:
            flash('Names must be 3 characters long. Doy.')
            is_valid = False

        return is_valid 