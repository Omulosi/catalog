"""
app.api.v1.common.utils
~~~~~~~~~~~~~~~~~~~~~~~~

some common utility functions
"""
import re
import string
from flask import jsonify
from app import jwt
from app.helpers import is_token_revoked

EMAIL_PATTERN = re.compile(r".+@[\w]+\.[\w]")


def valid_item_name(name):
    if name:
        name = name.strip()
    return name if name else None

def valid_category(category):
    if category:
        category = category.strip()
    return category if category else None

def valid_description(description):
    if description:
        description = description.strip()
    return description if description else None

def valid_email(email):
    if EMAIL_PATTERN.match(email):
        return email

def valid_password(password):
    special_char_present = False
    for char in password:
        if char in string.punctuation:
            special_char_present = special_char_present or True
    digit_present = False
    for char in password:
        digit_present = digit_present or char.isdigit()

    if special_char_present and digit_present:
        if len(password) >= 5:
            return True

# Define our callback function to check if a token has been revoked or not
@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)
