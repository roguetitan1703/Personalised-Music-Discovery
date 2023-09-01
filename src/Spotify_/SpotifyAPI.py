# Importing modules to handle requests, server and encoding
import requests, webbrowser, http.server, socketserver, threading
import base64, json
from urllib.parse import urlencode

# Importing modules for paths and environment file
import os, sys
from dotenv import load_dotenv, set_key

# Importing logging module
import logging, colorlog

# Adding the project's root directory to the path
project_root = os.getcwd()
sys.path.append(f'{project_root}/data')
sys.path.append(f'{project_root}/src')

# Importing local modules
from helpers_.json_helper import read_file

# Initialising the paths for data files
spotify_data_path = f'{project_root}/src/data/Spotify_/'
log_data_path = f'{project_root}/src/data/logs/'

# Loading the .env file
env_file = f'{spotify_data_path}/.env'
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
access_scopes = read_file(f'{spotify_data_path}/modify_scopes.json')
scope = ' '.join(access_scopes['MODIFY_PLAYBACK_LISTENING_PLUS'])

# Urls for getting data from Spotify API
recommendations_url = os.getenv('GET_RECOMMENDATIONS_URL')

# Implenting a logger function for seperate module logging
class Logger:
    def __init__(self, log_name, log_file, log_to_console=False, debug_mode=None):
        # Name of the logger to differentiate later
        self.log_name = log_name
        # The log file where the log statements are to be saved
        self.log_file = log_file
        # Whether to log to console or not (only needed when debugging through console)
        self.log_to_console = log_to_console
        # Whether to log in debug mode or not
        self.debug_mode = debug_mode
        
        # Initialising the logger
        self.logger = colorlog.getLogger(self.log_name)
        # Setting the logger to the lowest level DEBUG-> INFO-> WARNING-> ERROR -> CRITICAL, a logger only logs statements which are on or above it's level
        self.logger.setLevel(logging.DEBUG)
        # Managing all the handlers
        self.handlers = {}        
        # Setting up a custom color formatter for better visuals of the log and easy readability
        self.color_formatter = colorlog.ColoredFormatter(
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
        
        # Setting up the loggers handlers
        self.setup_handlers()
        
        
    # Function to setup the file handler which will log to the specified log file 
    def setup_file_handler(self):
        file_handler = logging.FileHandler(self.log_file)
        # Set the level to DEBUG to allow all the logs
        file_handler.setLevel(logging.DEBUG)
        # Add the handler to the handlers dictionary
        self.handlers['file_handler'] = file_handler

        # Add the file handler to the logger
        self.logger.addHandler(file_handler)
        
        # Set the formatter to the color_formatter for the file handler
        file_handler.setFormatter(self.color_formatter)
    
    # Function to setup the console handler which will log to the console, and will be usef for immediate feedback during development
    def setup_console_handler(self):
        console_handler = logging.StreamHandler()
        # Set the level to CRITICAL if log_to_console if False making the console_logger to only log statements to console if they are CRITICAL
        console_handler.setLevel(logging.CRITICAL if not self.log_to_console else logging.DEBUG)
        # Add the handler to the handlers dictionary
        self.handlers['console_handler'] = console_handler
        
        # Add the console_handler to the logger
        self.logger.addHandler(console_handler)
        
        # Set the formatter to the color_formatter for the file handler
        console_handler.setFormatter(self.color_formatter)
        

    # Setup all the handlers at once
    def setup_handlers(self):
        self.setup_file_handler()
        self.setup_console_handler() 

        # If a log file is opened to be read, it makes sure the contents are not cleared and vice versa   
        if not self.debug_mode:
            self.clear_log_file()
            # self.log_message('info', 'Starting Program')
        
        
    # Enable console logging if it was disabled previously
    def enable_console_logging(self):
        self.log_to_console = True
        if self.handlers['console_handler'] in self.logger.handlers:
            # Check for the console handler and set its level to DEBUG to allow all logs to log through console 
            self.handlers['console_handler'].setLevel(logging.DEBUG)    
    
    # Disable console logging if it was enabled previously or default
    def disable_console_logging(self):
        self.log_to_console = False
        if self.handlers['console_handler'] in self.logger.handlers:
            # Check for the console handler and set its level to CRITICAL to only log to console if they are CRITICAL
            self.handlers['console_handler'].setLevel(logging.CRITICAL)
            
            
    # Remove a handler from the logger permanently
    def remove_handler(self, handler):
        # Deleting the handler from the handlers dictionary
        del self.handlers[handler]
        # Check if the handler is present in the logger's handlers
        for handler_ in self.logger.handlers:
            if handler_ == handler:
                # Remove the handler from the logger permanently
                self.logger.removeHandler(handler_)
                break
            
    # Custom log message function which logs the message through all the handlers, It then depends on the handler's level if the log message will pass through
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
        

    # Read and display the contents of the log file line by line
    def read_log_file(self):
        with open(self.log_file, 'r') as file:
            for line in file:
                line = line.strip()  # To remove any leading/trailing whitespace
                print(line)

    # Clear log file in case of unwanted log statements filling up the log file
    def clear_log_file(self):
        with open(self.log_file, 'w') as file:
            # Opening the file in 'w' mode truncates it, effectively clearing its contents.
            pass


# The Spotify API Helper to manage tokens and authorization seemlessly
class SpotifyAPIHelper:
    
    # A local server to catch the OAuth2 redirection when retrieving the auth token
    # Defining classmethod as the function does not depend on the instance bound values
    # Using keyword cls is just a measure to differentiate self from cls, any keyword can be used  
    @classmethod
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

            # It handles the incoming redirection from the OAuth2 provider
            def do_GET(self):
                # Extract the URL when the user is redirected back after authorization
                redirected_url = self.path

                # Extract the authorization code from the URL
                auth_code = redirected_url.split('?code=')[1]
                logger.log_message('info', f"From {cls.start_local_server.__name__} : Authorization code captured successfully, Auth Code: {auth_code}")

                # Store the authorization code in the environment configuration
                set_key(env_file, 'AUTHORIZATION_CODE', auth_code)
                logger.log_message('info', f"From {cls.start_local_server.__name__} : Authorization code saved in the environment configuration file")
    
                # Respond to the user's browser with a success message
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Authorization code captured successfully. You can now close this window.')
                

        # Start the local web server on the specified port which listens for incoming connections.
        with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
            # Print a message indicating that the server is running
            print("Local web server started on port", PORT)

            # Log that the server has started and is waiting for the authorization code
            logger.log_message('info', f'From {cls.start_local_server.__name__} : Local web server started. Waiting for the authorization code.')

            # Open the browser to initiate the OAuth2 authorization process
            cls.get_authorization_code()

            # Create a separate thread to handle incoming requests and wait with a timeout //refer documentation for explanation
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
                logger.log_message('error', f'From {cls.start_local_server.__name__} : Server request timed out.')

                # Return status_code 500 if the server request timed out
                return {
                    'status_code': 500
                }
            
            else:
                # Return status_code 200 if it's successfull
                return {
                    'status_code': 200
                }
                

    # A unified function which handles the fetching of tokens, if the access_token is expired, it will refresh the access_token through refresh_token
    # and if the refresh_token is expired it will get a new auth_token through authorization
    @classmethod
    def refresh_or_get_new_tokens(cls):
        logger.log_message('debug',f'From {cls.refresh_or_get_new_tokens.__name__} : Refreshing or getting new tokens')
        
        # Try to refresh the access token only if the token values are not none:
        if auth_code and refresh_token:
            token = cls.refresh_access_token()
                
            # If refresh_access_token is returning an error, it means expired access token or invalid refresh token 
            if token.get('error') == 'invalid_grant':  
                logger.log_message('error', f"From {cls.refresh_or_get_new_tokens.__name__} : Refresh token is invalid or expired. Need to get new authorization code.")
                
                # Getting new tokens, first we have to renew auth code
                # Start the local web server to capture the authorization code
                response = cls.start_local_server()

                # Checking if the auth code fetching was successfull
                if response['status_code'] == 200:
                    # Now we can proceed to get the access token
                    token = cls.get_access_and_refresh_tokens()
                    
                    # There is another error occuring even after a valid auth code 
                    if token.get('error') == 'invalid_grant':
                        logger.log_message('error', f"From {cls.refresh_or_get_new_tokens.__name__} : {token.get('error_description')}")
                
                    # If the token is not returning an error, it means the tokens were successfully generated
                    else:
                        # Updating the env file with new tokens
                        cls.update_tokens(token)
                
                # If the status_code was not 200, it means the local server request timed out
                elif response['status_code'] == 500:
                    logger.log_message('error', f"From {cls.refresh_or_get_new_tokens.__name__} : Local server request timed out.")
                
                # Unexpected error occured 
                else:
                    logger.log_message('warning', f"From {cls.refresh_or_get_new_tokens.__name__} : Unexpected error occured")
                    
            
            # refresh_access_token is returning a valid token, means the fetch was successfull 
            else:
                # Updating the env file with new access token
                cls.update_tokens(token, refresh=False)
        
        # If token or auth code values are none refreshing everything to avoid errors 
        elif not auth_code or not refresh_token:
            
            # Getting auth code
            response = cls.start_local_server()
            
            # Checking if the auth code fetching was successfull
            if response.get('status_code') == 200:
                
                # Now we can proceed to get the tokens
                token = cls.get_access_and_refresh_tokens()
                
                # There is another error occuring even after a valid auth code 
                if token.get('error') == 'invalid_grant':
                    logger.log_message('error', f"From {cls.refresh_or_get_new_tokens.__name__} : {token.get('error_description')}")
            
                # If the token is not returning an error, it means the tokens were successfully generated
                else:
                    # Updating the env file with new tokens
                    cls.update_tokens(token)
            
            # If the status_code was not 200, it means the local server request timed out
            elif response.get('status_code') == 500:
                logger.log_message('error', f"From {cls.refresh_or_get_new_tokens.__name__} : Local server request timed out.")
            
            # Unexpected error occured 
            else:
                logger.log_message('warning', f"From {cls.refresh_or_get_new_tokens.__name__} : Unexpected error occured")
                
        
    # To get the authorization code by opening the browser and redirecting the user to the spotify authorization page
    @classmethod
    def get_authorization_code(cls):
        url = auth_code_url
        headers = {
            'client_id': client_id,
            'response_type': 'code',
            'redirect_uri': redirect_uri,
            'scope': scope
        }
        post_url = url + urlencode(headers)
        # Open the browser with the post method to the authorization page
        webbrowser.open(post_url)
    
    
    # To get the access token and refersh token from the authorization code
    @classmethod
    def get_access_and_refresh_tokens(cls):
        response = requests.post(
            access_token_url,
            data={
                'code': auth_code,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code'
            },
            headers={
                'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode('utf-8')).decode('utf-8')
            }
        )
        
        # If the response is 200, it means the token was successfully generated
        if response.status_code == 200:
            json_resp = response.json()
            access_token = json_resp['access_token']
            refresh_token = json_resp['refresh_token']
            
            # Return the token values
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'error': None
            }
        
        # If the response is not 200, it means the token was not successfully generated
        else:
            response_dict = json.loads(response.text)
            # Return the response for the calling function to handle the error
            return response_dict


    # To refresh the access token through refresh token
    @classmethod
    def refresh_access_token(cls):
        response = requests.post(
            access_token_url,
            data={
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            },
            headers={
                'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode('ascii')).decode('ascii')
            }
        )

        # If the response is 200, it means the access token was successfully refreshed
        if response.status_code == 200:
            resp_json = response.json()
            access_token = resp_json['access_token']
            return {
                'access_token': access_token,
                'error': None
                    }
            
        # If the response is not 200, it means that there was an error in refreshing the access token
        else:
            response_dict = json.loads(response.text)
            # Return the response for the calling function to handle the error
            return response_dict


    # To update the access token and refresh token in the env file
    @classmethod
    def update_tokens(cls, token, access=True, refresh=True):
        global access_token, refresh_token
        
        if token:
            # If instructions are to set access token then update it
            if access:
                access_token = token['access_token']
                logger.log_message('info', f'{"From " + cls.update_tokens.__name__} : Access token is set.')
                set_key(env_file, 'ACCESS_TOKEN', access_token)
            
            # If instructions are to set refresh token then update it
            if refresh:
                refresh_token = token['refresh_token']
                logger.log_message('info', f'{"From " + cls.update_tokens.__name__} : Refresh token is set.')
                set_key(env_file, 'REFRESH_TOKEN', refresh_token) 


    # To retrieve the any variable from the env file in real time
    @classmethod
    def get(cls, key):
        if key == 'ACCESS_TOKEN':
            cls.refresh_or_get_new_tokens()
            return os.getenv(key)
        else:
            return os.getenv(key)

if __name__ == '__main__':
    logger = Logger('SpotifyAPI', f'{log_data_path}SpotifyAPI.log', log_to_console=False, debug_mode=False)
    SAH = SpotifyAPIHelper
    # print(SAH.get('ACCESS_TOKEN'))
    # print(SAH.get('REFRESH_TOKEN'))
    # print(SAH.get('AUTHORIZATION_CODE'))
    
    