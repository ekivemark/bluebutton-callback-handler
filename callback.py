#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
Project: bluebutton-callback-handler
App: .
FILE: callback
Created: 6/14/18 5:33 PM

Created by: '@ekivemark'

based on:
http://requests-oauthlib.readthedocs.io/en/latest/examples/real_world_example.html
and this gist:
https://gist.github.com/ib-lundgren/6507798

"""

from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import os

app = Flask(__name__)


# This information is obtained upon registration of a new GitHub OAuth
# application here: https://github.com/settings/applications/new
client_id = "GC68JoIs7VhXevfwSJ8uizaaOmetV7qq5iZh5iLl"
client_secret = "BYlusC8jFFh6DEpGWH67LP2Dlrexdg1hyGSB0prbLb8HLyEIAGyiY5rfHLsZPBlN9jWb5IH2d894vRRcx2uL9GjkcXOukqdQ6U5empY2QVmBIU9sCP8YBxI3tlxug9ml"
authorization_base_url = 'https://sandbox.bluebutton.cms.gov/v1/o/authorize/'
token_url = 'https://sandbox.bluebutton.cms.gov/v1/o/token/'
base_url = "https://sandbox.bluebutton.cms.gov"


@app.route("/")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Blue Button sandbox)
    using an URL with a few key OAuth parameters.
    """
    bluebutton = OAuth2Session(client_id)


    if 'oauth_state' in session:
        print("Assigning saved state [%s] to state" % session['oauth_state'])
        saved_state = session['oauth_state']
    else:
        saved_state = None

    authorization_url, state = bluebutton.authorization_url(authorization_base_url, state=saved_state)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    print("State:%s" % state)
    print("Auth URL:%s" % authorization_url)
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.

@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """
    print("Callback GET:%s" % request.args.get)
    print("Session State:%s" % session['oauth_state'])
    print("New State:%s" % request.args.get('state'))

    if session['oauth_state'] != request.args.get('state'):
        print('\n========================================\n'
              'WARNING: Saved State [%s] NOT returned via '
              'callback [%s]\n'
              '=========================================='
              '\n' % (session['oauth_state'],
                      request.args.get('state')))

        session['previous_state'] = session['oauth_state']
        print("Saving previous State:%s" % session['previous_state'])
        session['oauth_state'] = request.args.get('state')
        print("Updated oauth_state:%s" % session['oauth_state'])

    bluebutton = OAuth2Session(client_id, state=session['oauth_state'])

    print("blubutton:%s" % bluebutton)
    token = bluebutton.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    session['oauth_token'] = token

    print("Token:%s" % token)

    print("Grab the Access token: %s" % token['access_token'])

    call_strings = {"oauth_token": token}
    call_strings['curl_patient_url'] = "curl -s --header 'Authorization: " \
                                       "Bearer %s' " \
                                       "'%s/v1/fhir/Patient/%s'" % (token['access_token'],
                                                                    base_url,
                                                                    token['patient'])
    call_strings['curl_coverage_url'] = "curl -s --header 'Authorization: " \
                                        "Bearer %s' " \
                                        "'%s/v1/fhir/Coverage' " % (token['access_token'],
                                                                    base_url)
    call_strings['curl_eob'] = "curl -s --header 'Authorization: " \
                               "Bearer %s' " \
                               "'%s/v1/fhir/ExplanationOfBenefit' " % (token['access_token'],
                                                                       base_url)
    return jsonify(call_strings)


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

    app.secret_key = os.urandom(24)
    app.run(debug=True, port=8000)