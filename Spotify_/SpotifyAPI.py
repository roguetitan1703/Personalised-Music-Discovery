from dotenv import load_dotenv, set_key
import base64
import requests
import json
import time
import os, sys
from urllib.parse import urlencode
import webbrowser
import http.server
import socketserver, threading

# Adding the project's root directory to the path
project_root = os.getcwd()
sys.path.append(f'{project_root}/data')

spotify_path = f'{project_root}/data/Spotify_/'

# Loading the .env file
env_file = f'{project_root}/.env'
load_dotenv(env_file)

# Loading environment variables 