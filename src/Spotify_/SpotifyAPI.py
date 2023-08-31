# Importing modules to handle requests, server and encoding
import requests, webbrowser, http.server, socketserver, threading
import base64
from urllib.parse import urlencode

# Importing modules for paths and environment file
import os, sys
from dotenv import load_dotenv, set_key

# Importing logging module
import logging, colorlog

# Importing local modules
from ..helpers_.json_helper import read_file

# Adding the project's root directory to the path
project_root = os.getcwd()
sys.path.append(f'{project_root}/data')

# Initialising the paths
spotify_path = f'{project_root}/data/Spotify_/'
log_path = f'{project_root}/data/logs/'

# Loading the .env file
env_file = f'{project_root}/.env'
load_dotenv(env_file)

# Loading environment variables 

# Variables dealing with authorization and tokens
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')  
redirect_uri = os.getenv('REDIRECT_URI')
auth_code_url = os.getenv('GET_AUTHORIZATION_CODE_URL')
auth_code = os.getenv('AUTHORIZATION_CODE')
access_token_url = os.getenv('GET_ACCESS_TOKEN_URL')

# Tokens
refresh_token = os.getenv('REFRESH_TOKEN')
access_token = os.getenv('ACCESS_TOKEN')

# Access scopes for modifying user's data or reading it 
access_scopes = read_file(f'{spotify_path}/modify_scopes.json')
scope = ' '.join(access_scopes['MODIFY_PLAYBACK_LISTENING_PLUS'])

# Urls for getting data from Spotify API
recommendations_url = os.getenv('GET_RECOMMENDATIONS_URL')

# Implenting a logger function for seperate module logging
class Logger:
    def __init__(self, log_name, log_file_path, log_to_console=False):
        self.log_to_console = log_to_console
        self.log_name = log_name
        self.log_file_path = log_file_path
        self.logger = colorlog.getLogger(self.log_name)
        self.logger.setLevel(logging.DEBUG)
                
            
        self.setup_file_handler()
        
    
    def setup_file_handler(self):
        # Create a FileHandler to save log messages into a .log file
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)

        # Create a console handler for immediate feedback during development
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO if not self.log_to_console else logging.DEBUG)
        
        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        if self.log_to_console:
            self.logger.addHandler(console_handler)
        
        # Create a formatter for the file handler
        formatter = colorlog.ColoredFormatter(
            '%(asctime)s - %(log_color)s%(levelname)-8s%(reset)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
    
    
    # Enable console logging
    def enable_console_logging(self):
        self.log_to_console = True
        for handler in self.logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                handler.setLevel(logging.DEBUG)
                break
    
    
    # Disable console logging
    def disable_console_logging(self):
        self.log_to_console = False
        for handler in self.logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                handler.setLevel(logging.INFO)
                break
    
    
    def log_message(self, log_level, message):
        # Validate the log level provided by the user
        log_level = log_level.upper()
        if log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            raise ValueError("Invalid log level. Expected one of: DEBUG, INFO, WARNING, ERROR, CRITICAL")

        # Mapping log levels to corresponding logging methods
        log_level_mapping = {
            'DEBUG': self.logger.debug,
            'INFO': self.logger.info,
            'WARNING': self.logger.warning,
            'ERROR': self.logger.error,
            'CRITICAL': self.logger.critical
        }

        # Log the message with the specified log level using the mapped logging method
        log_level_mapping[log_level](message)
        
        
class SpotifyAPIHelper:

    def start_local_server(cls):
        global auth_code
        # Set the port number for the local server
        PORT = 8000

        # Use the built-in SimpleHTTPRequestHandler as the base handler
        Handler = http.server.SimpleHTTPRequestHandler

        # Create a custom handler by inheriting from SimpleHTTPRequestHandler
        class CustomHandler(Handler):
            # Override log_request method to disable logging of incoming requests
            def log_request(self, code='-', size='-'):
                pass

            # Handle incoming GET requests
            def do_GET(self):
                # Extract the URL when the user is redirected back after authorization
                redirected_url = self.path

                # Extract the authorization code from the URL
                auth_code = redirected_url.split('?code=')[1]

                # Store the authorization code in the environment configuration
                set_key(env_file, 'AUTHORIZATION_CODE', auth_code)

                # Respond to the user's browser with a success message
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Authorization code captured successfully. You can now close this window.')

        # Start the local web server on the specified port
        with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
            # Print a message indicating that the server is running
            print("Local web server started on port", PORT)

            # Log that the server has started and is waiting for the authorization code
            cls.logger_api.log_message('info', 'Local web server started. Waiting for the authorization code.')

            # Open the browser to initiate the OAuth2 authorization process
            cls.get_authorization_code()

            # Create a separate thread to handle incoming requests and wait with a timeout
            httpd_thread = threading.Thread(target=httpd.handle_request)
            httpd_thread.start()
            httpd_thread.join(timeout=30)  # Set the timeout to 30 seconds

            # If the thread is still alive after the timeout, handle the timeout
            if httpd_thread.is_alive():
                # Shut down the server
                httpd.shutdown()

                # Print a message indicating that the server request timed out
                print("Server request timed out.")

                # Log an error message about the server request timing out
                cls.logger_api.log_message('error', 'Server request timed out.')

                # Handle the error and proceed with the authentication process accordingly
                # For example, you can retry or display an error message to the user.


if __name__ == '__main__':
    logger = Logger('SpotifyAPI', f'{spotify_path}SpotifyAPI.log', True)
    logger.log_message("INFO", "This is info")
    logger.log_message("WARNING", "This is warning")
    logger.log_message("ERROR", "This is error")
    logger.log_message("CRITICAL", "This is critical")
    
    