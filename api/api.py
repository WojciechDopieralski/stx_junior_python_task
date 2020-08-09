import flask
from .dbconn import db
from .functions import get_books_information, create_output_json


app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():  
    return """<center><h1> Welcome to small book API. You can do following things here: </h1><br/>
<h2>- /books => get all books in DB. You can filter by ?published_date (in fact published year) and sort by it. You can also filter by authors. <br/>
- /books/bookid => get information about book with given id. <br/>
- /db => Post method. You need to send JSON with key "q", and some value (for example "war") to add new books to DB or update existing ones. </h2><br/> 
"""

@app.route('/books', methods=['GET'])
def get_book_list():
    books_colection = db.books
    cursor = books_colection.find()
        
    if 'published_date' in flask.request.args:
        year = int(flask.request.args['published_date'])
        cursor = books_colection.find({"publishedYear" : {"$eq": year}})
    
    if 'sort' in flask.request.args:
        sort_value = str(flask.request.args['sort'])
        if sort_value == "published_date":
            cursor = books_colection.find().sort([("publishedYear", 1), ("publishedDate" , 1)])
        elif sort_value == "-published_date":
            cursor = books_colection.find().sort([("publishedYear",-1), ("publishedDate", -1)])
  
    if 'author' in flask.request.args:
        query_parameters = flask.request.args.to_dict(flat=False)
        authors = query_parameters.get('author')
        authors = [s.replace('"', '') for s in authors]
            
        books_with_auth_filter = []
        for author in authors:
            cursor = db.books.find({ "authors": author })
            for book in cursor:
                [book.pop(param) for param in ['_id', "publishedYear"]]
                books_with_auth_filter.append(book)
         
        return flask.jsonify(books_with_auth_filter)
    
    books_list = create_output_json(cursor)     
    return flask.jsonify(books_list)

@app.route('/books/<string:book_id>', methods=['GET'])   
def show_book_by_id(book_id):
    cursor = db.books.find({"_id": book_id})
    books_by_id = create_output_json(cursor)   
    return flask.jsonify(books_by_id)

@app.route('/db', methods=['POST'])
def post_db():
    post_json = flask.request.json
    q_tag_keys = list(post_json.keys())
        
    if all(element == 'q' for element in q_tag_keys):
        new_books_json = get_books_information("https://www.googleapis.com/books/v1/volumes", post_json)
    
        for books in new_books_json:
            db.books.update({"_id": books['_id']}, books, upsert = True)
        resp = flask.jsonify('books added and updated successfully')
        resp.status_code = 200
    else: 
        resp = flask.jsonify('json should contain 1 key named "q" and some value (for example: {"q" : "war"})')
        resp.status_code = 400
    
    return resp
    
if __name__ == '__main__':
    app.run()

