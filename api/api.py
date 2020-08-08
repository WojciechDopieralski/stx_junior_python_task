import flask
from dbconn import db
import datetime
from functions import get_book_information


app = flask.Flask(__name__)
#app.config["DEBUG"] = True
#nie umiem odczytac w tym errora :/ 


@app.route('/', methods=['GET'])
def home():
    
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/books', methods=['GET'])
def get_book_list():
    books_colection = db.books
    books_bonson = books_colection.find()
    books_list = []
    for book in books_bonson:
        book.pop('_id')
        books_list.append(book)
        
    if 'published_date' in flask.request.args:
        year = int(flask.request.args['published_date'])
        year_filter_book_list = []
        for book in books_list:
            book_date = book['publishedDate']
            if "-" in book_date:
                date_time_obj = datetime.datetime.strptime(book_date, '%Y-%m-%d')
                book_re_year = int(date_time_obj.year)
            else:
                book_re_year = int(book['publishedDate'])
            
            if  book_re_year == year:
                year_filter_book_list.append(book)
        return flask.jsonify(year_filter_book_list)
    
    if 'sort' in flask.request.args:
        sort_value = str(flask.request.args['sort'])
        correct_date_list = []
        for book in books_list:
            book_date = book['publishedDate']
            if "-" in book_date:
                date_time_obj = datetime.datetime.strptime(book_date, '%Y-%m-%d')
                book_re_year = int(date_time_obj.year)
            else:
                book_re_year = int(book['publishedDate'])
            book['publishedDate'] = book_re_year
            correct_date_list.append(book)
            
        if sort_value == "published_date":
            sorted_list = sorted(correct_date_list, key = lambda i: i['publishedDate'])
        elif sort_value == "-published_date":
            sorted_list = sorted(correct_date_list, key = lambda i: i['publishedDate'], reverse=True)
            
        return flask.jsonify(sorted_list)
    
    if 'author' in flask.request.args:
        query_parameters = flask.request.args.to_dict(flat=False)
        authors = query_parameters.get('author')
        authors = [s.replace('"', '') for s in authors]
            
        books_with_auth_filter = []
        for author in authors:
            cursor = db.books.find({ "authors": author })
            for book in cursor:
                book.pop('_id')
                books_with_auth_filter.append(book)
         
        return flask.jsonify(books_with_auth_filter)
        
    return flask.jsonify(books_list)


@app.route('/books/<string:book_id>', methods=['GET'])   
def show_book_by_id(book_id):
    books_bonson = db.books.find({"id": book_id})
    books_list = []
    for book in books_bonson:
        book.pop('_id')
        books_list.append(book)
    
    return flask.jsonify(books_list)


@app.route('/db', methods=['POST'])
def post_db():
    
    post_json = flask.request.json
    q_tag_keys = list(post_json.keys())
        
    if all(element == 'q' for element in q_tag_keys):
        new_books_json = get_book_information("https://www.googleapis.com/books/v1/volumes", post_json)
    
        for books in new_books_json:
            db.books.update({"_id": books['_id']} , books, upsert = True)
        resp = flask.jsonify('books added and updated successfully')
        resp.status_code = 200
    else: 
        resp = flask.jsonify('json should contain 1 key named "q" and some value (for example: {"q" : "war"})')
        
    
    return resp
    
    



app.run()

