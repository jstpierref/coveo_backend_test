import os
import unittest

from flask_script import Manager

from app.main import create_app
from app.blueprint import blueprint

from dotenv import load_dotenv
load_dotenv()

app = create_app(os.getenv("APP_SETTINGS") or "prod")
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

@manager.command
def run():
    # on Heroku, port is defined in env. variables, but locally we run on 5000.
    port = os.getenv("PORT", 5000)
    app.run(host="0.0.0.0", port=port)

@manager.command
def test():
    #Runs the unit tests.
    tests = unittest.TestLoader().discover("app/test", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == "__main__":
    manager.run()
