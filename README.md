# Flask_oauthlib-client
A really simplistic FLASK_OAUTHLIB client exmaple for folks wishes to use this library.

## Contact
Tyler Worman - tsworman@novaslp.net

## Python Oauth Client/Provider Project
This is part 1 of 4 of my project examples showing functional FLASK/Python Oauth usage.
This is an attemp to undo the damage/frustration done by crappy documentation. 
Along the way we've completed 'tricky bits' and 'exercise left to reader' that I've found in many
'tutorials'

### Four projects
* Flask_oauthLib-client - This project. 
* Flask_oauthlib-provider - A full featured FLASK provider application 
* Flask-authlib-provider - A full featured Flask AuthLib based provider
* Flask-authlib-client - A authlib based client.


## Supported providers
All the common ones (Github, Faceobook, Google, etc)
Included are instructions for running against both FLASK_OAUTHLIB and AUTHLIB providers.

## Security considerations
As the documentation for FLASK_OAUTHLIB now states, you shouldn't use FLASK_OAUTHLIB.

The largest risk is that the exmaples store the access token in FLASK session which is
stored in a cookie on the client side. You do not want to expose the access token to an 
end user. A work around for this is moving to server side session storage and multiple 
FLASK plugins are available to do this.

The library itself seems unmaintained and not updated, but existing clients can 
use the information contained here when moving to AUTHLIB providers.

## Testing
This was hand tested against both FLASK_OAUTHLIB and AUTHLIB providers.

## OAUTH Workflows
This uses the authorization_code workflow designed for traditional
web app usage. 

This is not for SPA web apps, unless you have a backend you control.
In those cases it's possible to use the authorization_code workflow between
the backend and OAUTH provider and expose the methods needed to the client
through proxy functions on the backend. This complicates testing and requires
significantly more mocking for proper testing. For SPA you should look into 
using the implicit flow.

## OAUTH provider configuration

## FLASK_OAUTHLIB provider setup
* Create a client_id/secret. 
* _redirect_uris should contain space delimited URLs that are valid
  for redirection. For this example just use https://localhost:5000/authorized
* For _default_scopes setup space delimited scopes. 
  This example needs at lease "email roles" in the scope field.

## AUTHLIB provider setup
* Create client_id/client_secret
* Token_endpoint_auth_method = client_secret_post
* Grant_type = authorization_code
* Response_type = code
* scopes "email roles" space delimited
* Redirect_URI 'https://localhost:5000/authorized' these are new line delimited.

## Setup
Copy env_sample to .env
`cp env_sample .env`

Edit .env to hold your specific OAUTH provider settings

Create a virtual environment
`python3 -m venv venv`

Start your virtual environment
`source venv/bin/activate`

Install pip packages.
`pip install requirements.txt`

## Running
Start virtual environment
`source venv/bin/activate`

Source your .env.
`source .env`

Run the flask app
`flask run`

Navigate in web browser to http://127.0.0.1/ and begin the flow.
