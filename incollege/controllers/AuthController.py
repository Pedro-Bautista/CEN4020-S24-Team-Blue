# Authentication Controller
# Handles sign in and sign up requests

import incollege.services.AuthService as AuthService

def login(username, password):
    return AuthService.login(username, password)

def signup(username, password):
    return AuthService.signup(username, password)
