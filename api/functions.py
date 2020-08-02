import requests


def get_books_json(url: str = "https://www.googleapis.com/books/v1/volumes?q=war") -> dict:
    """
    Use GET method for given url to retrive json file.
    
    Parameters
    ----------
    url: str
        link to resources (default: link to volumes with q=war, target of recrutment task)
    
    Returns
    -------
    dict
        json file from given url.
        
    """
    
    #TO DO: ZABEZPIECZ DOBRA WIADOMOSCIA, GDY NIE BEDZIE ZWROTU 200 - WYSWIETL USEROWI NR BLEDU. 
    user_url = url
    r = requests.get(user_url)
    
    return r.json()

