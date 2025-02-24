from .app import app
import os.path
def mkpath(p):
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            p))
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///' + mkpath('../testdb.db'))
app.url_map.strict_slashes = False
app.config['SECRET_KEY'] = 'e9767196-4490-415a-8d42-1b16d2ad2a24'
app.config['SECURITY_DEFAULT_REMEMBER_ME'] = False
app.config['SECURITY_REGISTERABLE'] = False
app.config['SECURITY_RECOVERABLE'] = False
app.config['SECURITY_TRACKABLE'] = False
app.config['SECURITY_CONFIRMABLE'] = False
app.config['SECURITY_CHANGEABLE'] = False
app.config['BOOTSTRAP_SERVE_LOCAL'] = True