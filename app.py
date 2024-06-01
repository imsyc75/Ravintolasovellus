from flask import Flask # type: ignore
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes # type: ignore