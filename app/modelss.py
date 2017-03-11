import logging

from google.appengine.ext import ndb
from datetime import datetime
from functools import wraps
from .sticky_notes import add_notes
from flask_login import current_user
from uuid import uuid1
