# bluebutton-callback-handler
simple server to handle callback from bluebutton sandbox using OAuth2.0

Based on the following code examples:

- http://requests-oauthlib.readthedocs.io/en/latest/examples/real_world_example.html
- https://gist.github.com/ib-lundgren/6507798

## Install

Create a virtualenv and install libraries:

    mkdir demo
    cd demo
    python -m venv ./virtualenv
    # activate the virtualenv
    source ./virtualenv/bin/activate
    git clone https://github.com/ekivemark/bluebutton-callback-handler.git
    cd ./bluebutton-callback-handler
    # install supporting libraries
    pip install -r requirements.txt
    
    
## Register an app in the sandbox

- Login to sandbox.bluebutton.cms.gov
- Register your application
  - Authorization Grant Type: authorization_code
  - Client Type: confidential
  - Redirect_Uri: http://localhost:8000/callback

## edit callback.py

- add your client_id and client_secret to the code.

## Run the handler

    python callback.py

## Open a browser

    http://localhost:8000

- Login to Medicare
- Authorize your app
