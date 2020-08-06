import flask
from dbconn import db
import datetime
from flask_rest_jsonapi import Api



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
        author = query_parameters.get('author')
        #Z tym mozna dalej dzialac by sprawdzic czy dany autor cos pisal ;) 
        
        return 
        
    return flask.jsonify(books_list)




app.run()


api = Api(app)




