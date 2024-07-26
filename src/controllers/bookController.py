from flask import Blueprint, render_template, request, redirect, abort
from models.bookModel import BookModel, db

book_blueprint = Blueprint('book', __name__)

@book_blueprint.route('/')
def index():
    return render_template('mainpage.html')

@book_blueprint.route('/create', methods=["GET", "POST"])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        name = request.form['name']
        year = request.form['year']
        author = request.form['author']
        book = BookModel(name=name, year=year, author=author)

        db.session.add(book)
        db.session.commit()
        return redirect('/data')

@book_blueprint.route('/data')
def DataView():
    books = BookModel.query.all()
    return render_template('datalist.html', books=books)

@book_blueprint.route('/data/<int:id>')
def findBook(id):
    book = BookModel.query.filter_by(id=id).first()
    if book:
        return render_template("data.html", book=book)
    return f"Livro com id={id} não existe", 404


@book_blueprint.route('/data/<int:id>/update', methods=["GET", "POST"])
def update(id):
    book = BookModel.query.get(id)
    if not book:
        return f"Livro com id={id} não existe", 404

    if request.method == 'POST':
        book.name = request.form["name"]
        book.year = request.form["year"]
        book.author = request.form["author"]
        db.session.commit()
        return redirect('/data')  # Redireciona para a lista de livros

    return render_template("update.html", book=book)


@book_blueprint.route('/data/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    book = BookModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if book:
            db.session.delete(book)
            db.session.commit()
            return redirect('/data')  # Redireciona para a lista de livros
        abort(404)
    return render_template('delete.html', book=book)

