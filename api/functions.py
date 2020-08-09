import requests
import pandas as pd
import datetime
import pymongo

def get_books_json(url: str, headers: dict = None) -> dict:
    """
    Use GET method for given url to retrive json file.
    
    Parameters
    ----------
    url: str
        link to resources (default: link to volumes with q=war, target of recrutment task)
    headers: dict
        dict with params for requests.get method. It should contain key and value matched for given url.  
    
    Returns
    -------
    dict:
        json file from given url.
        
    """ 
    user_url = url
    r = requests.get(user_url, headers)
    if r.status_code != 200:
        return "wrong status code: {}".format(r.status_code)
    
    return r.json()

def get_books_information(url: str, headers: dict = None) -> list:
    """
    Create list that contains dicts of cleaned data from google book API. 
    
    Parameters
    ----------
    url: str
        link to resources (default: link to volumes with q=war, target of recrutment task)
    headers: dict
        dict with params for requests.get method. It should contain key and value matched for given url.
        
    Returns
    -------
    books_list: list
        List containing dict with chosen values.     
    """
    
    url_json = get_books_json(url, headers)
    items_list = url_json["items"]
    list_of_wanted_params = ["id", "volumeInfo_authors",  "volumeInfo_title", "volumeInfo_publishedDate", "volumeInfo_categories", "volumeInfo_averageRating", "volumeInfo_ratingsCount", "volumeInfo_imageLinks_thumbnail"]
    parameters_list = []
    
    for item in items_list:
        flatten_df = pd.json_normalize(item, sep='_')
        flatten_dict = flatten_df.to_dict(orient='records')[0]  
        book_params_dict = {key.rsplit("_", 1)[-1]: flatten_dict.get(key) for key in list_of_wanted_params}
        book_params_dict["_id"] = book_params_dict.pop("id")
        book_date = book_params_dict['publishedDate']   
        if "-" in book_date:
            date_time_obj = datetime.datetime.strptime(book_date, '%Y-%m-%d')
            book_re_year = int(date_time_obj.year)
            book_params_dict['publishedYear'] = book_re_year
        else:
            book_re_year = int(book_date)
            book_params_dict['publishedYear'] = book_re_year
            
        parameters_list.append(book_params_dict)
        
    return parameters_list
        

def create_output_json(cursor: pymongo.cursor.Cursor) -> list:
    """
    Create list that contains result of pymongo query
    
    Parameters
    ----------
    cursor: pymongo.cursor.Cursor
        cursor with query created by pymongo
        
    Returns
    -------
    books_list: list
        List containing dict with values after query to DB.  
    """
    books_list = []
    for book in cursor:
        [book.pop(param) for param in ['_id', "publishedYear"]]
        books_list.append(book)
    return books_list

