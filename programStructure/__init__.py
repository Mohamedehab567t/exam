from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '0af460ece0df65g4df65g4d56h65gbe45788c981fc2a0564gdf6ggh54'
log = LoginManager(app)
log.login_view = 'login'
log.login_message = 'You Must Login First'
Setting_ID = 945269278489
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024




from programStructure import urls

