import os
import dotenv

thisDir = os.path.abspath(os.path.dirname(__file__))
dotenv.load_dotenv(os.path.join(thisDir,'.env'))

DEBUG = True
Threaded = True
FLASK_ENV = 'development'

STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')