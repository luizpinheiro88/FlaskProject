from flask import Flask
from models.bookModel import db
from controllers.bookController import book_blueprint

app = Flask(__name__, template_folder="views")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(book_blueprint, url_prefix='/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
