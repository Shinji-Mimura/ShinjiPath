# Import necessary modules
import os

# Define configuration variables
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY', 'my_secret_key')
DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///myapp.db')
