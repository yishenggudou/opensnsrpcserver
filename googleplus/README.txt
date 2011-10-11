# Google+ Python Command-line Starter #

VITAL!

For installation, you also need the Google API Python Client, found at:

http://code.google.com/p/google-api-python-client

For a quick run, you can add something like this to your path:

export PYTHONPATH=$PYTHONPATH:[path to checkout]/google-api-python-client

Otherwise, you can copy the contents of that directory into your
python directory, or be picky and just copy:

httplib2
oauth2client
apiclient
gflags*.py
uritemplate


## Setup Authentication ##

Visit https://code.google.com/apis/console/ to register your application.
 - From the "Project Home" screen, activate access to "Google+ API".
 - Click on "API Access" in the left column
 - Click the button labeled "Create an OAuth2 client ID"
 - Give your application a name and click "Next"
 - Select "Web Application" as the "Application type"
 - Under "Your Site or Hostname" select http:// as the protocol and enter
   "localhost" for the domain name
 - click "Create client ID"
 - click "Edit..." for your new client ID
 - Add "http://localhost:8080" as one of the permitted callback URLs on a 
   separate line

[If you already have something running on 8080, you may get a callback
error when authenticating, as the CLI will attempt to run a server on
port 8080, then 8090, etc.]

Edit the settings.py file and enter the values for the following
properties that you retrieved from the API Console:

- CLIENT_ID
- CLIENT_SECRET
- API_KEY 

## Running the Sample ##

% python plus_cli.py
