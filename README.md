# stx_junior_python_task

### API is available online at: https://stxtaskbooksapi.herokuapp.com/

### If you would like to test this API locally you have to: 
1. Fork and clone repo.
2. Run `pip3 install -r requirements.txt` to install all libraries 
3. Change relative import (by removing dots) to absolute one.
4. This API uses MongoDB. It would be best to create your own free DB at: https://cloud.mongodb.com
5. You will need to change uri parameter inside "dbconn.py" to your own uri (generated from your MongoDB)
6. inside api folder create pickled file named "pass.p". It should contain pickled string. I attached "pass_example.p".
7. If you would like to put your project online use heroku not pythonanywhere. Pythonanywhere doesn't support MongoDB as free account package. 

### Substantiation of some methods:

- Why MongoDB? It was well suited for this task. In SQL DB there would be a problem with authors, because in the API they're given by many different names. There also could be a problem with categories. I prepared SQL schema for this task, it is available here: https://dbdiagram.io/d/5f2684d27543d301bf5d8f07
- Created additional filed in DB called PublishedYear. This filed is int value of year from PublishedDate. Why? I think that it is important to keep all the data, and for future analysis it good to keep them in original shape. That's why I decided not to turn PublishedDate into date object. 

This API is part of recruitment process for junior python developer at STX. 
