"""
app.api.v1.common.utils
~~~~~~~~~~~~~~~~~~~~~~~~

some common utility functions
"""

import re
from flask import jsonify

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
