from blogger import create_app
from blogger.models import User, Post, db
import os
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

migrate = Migrate(app, db, render_as_batch=True)

if __name__ == '__main__':
    app.run(debug=True)
