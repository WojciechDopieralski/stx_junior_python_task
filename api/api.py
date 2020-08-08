import flask
from dbconn import db
from functions import get_book_information


app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    
    return ""

@app.route('/books', methods=['GET'])
def get_book_list():
    books_colection = db.books
    books_bonson_querry = books_colection.find()
        
    if 'published_date' in flask.request.args:
        year = int(flask.request.args['published_date'])
        books_bonson_querry = books_colection.find({"publishedYear" : {"$eq": year}})
    
    if 'sort' in flask.request.args:
        sort_value = str(flask.request.args['sort'])
        if sort_value == "published_date":
            books_bonson_querry = books_colection.find().sort("publishedYear", 1)
        elif sort_value == "-published_date":
            books_bonson_querry = books_colection.find().sort("publishedYear",-1)
  
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
    
    books_list = []
    for book in books_bonson_querry:
        book.pop('_id')
        books_list.append(book)
        
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

