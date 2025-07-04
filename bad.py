import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

SUKH = getenv("SUKH", "mongodb+srv://pusers:nycreation@nycreation.pd4klp1.mongodb.net/?retryWrites=true&w=majority&appName=NYCREATION")
