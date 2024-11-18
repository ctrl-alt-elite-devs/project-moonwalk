from square.client import Client
import os
from dotenv import load_dotenv
from django.conf import settings

load_dotenv()

#sqaure api auth
access_token = os.getenv("SQUARE_ACCESS_TOKEN")
environment = os.getenv("SQUARE_ENVIRONMENT")
sandbox = True

client = Client(
    access_token=access_token,
    environment=environment
)