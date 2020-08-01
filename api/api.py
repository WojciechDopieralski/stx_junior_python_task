import flask

app = flask.Flask(__name__)
#app.config["DEBUG"] = True
#nie umiem odczytac w tym errora :/ 





@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

app.run()




#Pobierz json i przetwórz go do odpowiedniej postaci:
# Potrzebe z jsona do zadan sa: id, volumeInfo: authors (cala lista), volumeInfo: publishedDate
# do wyswitlania potrzebne dodatkowa:  volumeInfo: title, volumeInfo: categories, volumeInfo: averageRating, volumeInfo: raitingsCount