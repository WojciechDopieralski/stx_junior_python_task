import requests
import pandas as pd


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

def get_book_information(url: str = "https://www.googleapis.com/books/v1/volumes?q=war"):
    """
    TO DO description 
    
    Parameters
    ----------
    
    Returns
    -------
    None.
    """
    
    url_json = get_books_json(url)
    items_list = url_json["items"]
    list_of_wanted_params = ["id", "volumeInfo_authors",  "volumeInfo_title", "volumeInfo_publishedDate", "volumeInfo_categories", "volumeInfo_averageRating", "volumeInfo_ratingsCount", "volumeInfo_imageLinks_thumbnail"]
    parameters_list = []
    
    for item in items_list:
        flatten_df = pd.json_normalize(item, sep='_')
        flatten_dict = flatten_df.to_dict(orient='records')[0]  
        book_params_dict = {key: flatten_dict.get(key) for key in list_of_wanted_params}
        parameters_list.append(book_params_dict)
        
    return parameters_list
        


       