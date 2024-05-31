from flask import Flask

app = Flask(__name__)
app.secret_key = '5364d23940c3ec8d93a8a07bd8a423f4'

import routes