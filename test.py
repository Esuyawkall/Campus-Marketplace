import yaml
from pathlib import Path
import pymysql
import datetime
from user import user
from product import product
from order import order
from message import message
from favorite import favorite
from image import image

# Repo Github link (text url)
# -Zip file (file upload)
# -Project repo with
# - readme.md
#   - Group member names
#   - Narrative on app purpose
#   - User table with roles, purpose and example user credentials
#   - Relational Schema
#   - analytical queries
#   - getting started / setup
# - .gitignore
# - config file
# - csv / data files
# - sql init
# - Omit credentials file config.yml
# - Example credentials file config.example.py
# Grading:

#  -Application does not have Python errors

#  -Test, Test, Test

#  -Framework usage

#  -Each class has a table

#  -Endpoints should be grouped / predicable

#  -Readme is complete ^^^

#  -Complexity

#  -SQL queries