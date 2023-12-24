
from flask_sqlalchemy import SQLAlchemy
#import logging as lg


# We create a "Database Connection Object" and will use "LATER" its .init_app() method to associate it to our API
# That way it will be possible to have Python code TRANSLATED into SQL language TO "MANIPULATE a DB containing info needed by the API"
#************VIA SQLALCHEMY_DATABASE_URI IN "CONFIG" FILE: WE MUST TELL SQLAlchemy THE FILE NAME where store the DB actual values***********
db = SQLAlchemy()


# Declare here as a Python "Class" Object the "STRUCTURE OF THE ONLY DB TABLE CALLED": Dataset_photos_names
# If you instantiate 2 objects of this class, only the last one committed into the DB will be in it!!!
# It is designed to inherit the property of the db.Model class!!
#class Table_datasetphotos_names(db.Model):
class Table_datasetphotos_names(db.Model):

    def __init__(self, photo_file_names):

        self.photo_file_names = photo_file_names
        # The method below is ran each time we associate an API to this connection Object via .init_app()
        #self.init_db()
        return

    # Primary Key is by DEFAULT integer.....MAY be able to make it a different type?
    id_for_this_table = db.Column(db.Integer, primary_key=True)

    # Here only 1 column is needed
    photo_file_names = db.Column(db.String(200), nullable=False)


# CANNOT POPULATE THE DB NOW B/C REQUIRES AN "ACTIVE API CONTEXT" (i.e. "associate" an EXISTING API with the DB Object Connector)
# But the API is NOT defined YET as it use the Table created to query it!!!!