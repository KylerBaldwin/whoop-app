import json
from os import getenv
import secrets

from flask import Blueprint, request, jsonify, session, redirect
from flask_login import login_required, current_user

from . import db
from .models import WhoopAuth
from .whoop import Whoop

routes = Blueprint('routes', __name__)

whoop = Whoop(client_id=getenv('CLIENT_ID'),
                        client_secret=getenv('CLIENT_SECRET'))

# Redirect to Whoop Authorization endpoint
@routes.route("/whoop/auth", methods=['GET'])
@login_required
def whoop_auth():
    # Get the user_id from the query parameter
    user_id = request.args.get('userid')
    if not user_id:
        return "Missing userid", 400

    # Generate a secure state parameter
    state = secrets.token_urlsafe(16)

    # Save the state in the session
    session['oauth_state'] = state
    session['user_id'] = user_id

    return redirect(f'{whoop.authorization_url}&{state}')

# Authorize whoop client and fetch tokens
@routes.route("/oauth2_callback", methods=['GET'])
def callback():
    state = request.args.get('state')
    code = request.args.get('code')

    # Validate state to prevent CSRF
    if not state or state != session.get('oauth_state'):
        return jsonify({'message': 'Invalid state'}), 400

    try:
        # Exchange code for access token
        token_response = whoop.get_access_token(authorization_code=code)
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve access token from Whoop', 'error': str(e)}), 500

    refresh_token = token_response.get('refresh_token')

    # Check if we have the tokens
    if not refresh_token:
        return jsonify({'message': 'Refresh token missing'}), 400

    whoopAuth = WhoopAuth.query.where(user_id=session.get('user_id'))
    if not whoopAuth:
        return jsonify({'message': 'User not found'}), 404

    whoopAuth.refresh_token = refresh_token
    db.session.commit()

    # Redirect the user to a success page in the frontend
    return redirect("https://kylerbaldwin.com/whoop/success?status=ok")