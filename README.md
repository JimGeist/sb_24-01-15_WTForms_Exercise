# sb_24-01-15_WTForms_Exercise - Pet Adoption


## Assignment Details
Assignment involved creation of a Pet Adoption application using Flask, Python, SQL Alchemy, and WTForms. WTForms was used to create an add pet and edit pet form. The landing page used manual methods to create the elements. The WTForm validations on the Add and Edit for valid photo_url and age range between 0 and 30.

WTForms does not seem to show the True/False yes/no on a form -- the value is always 'y' in view source and inspect elements even value is clearly False.

unittests were created in tests_models.py for tests of functions in the models.py and tests_app.py includes the route and form validation tests. 

Models.py includes all database related functions, especially ones that make database changes.

Flask toolbar debugging statements
``` from flask_debugtoolbar import DebugToolbarExtension```
```  . . . .```
``` debug = DebugToolbarExtension(app)```
``` app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False```
are in app.py and are also referenced in tests_app.py and tests_models.py.

A seed file, seed.py, is included with 4 test pets. The database name is ```pet_adoptions```


### ENHANCEMENTS
- species table and model added. Species choices on the WTForms come from the database dynamically, so that handled the choices for pet species. And also taught me that what you see is not what you get - a tuple looks the same as an sqlalchemy.engine.row.Row.
- some color on the landing page 
- try / except included for adds. Specific errors were not included on the except.
- update only when data changes
- flash messages for update and add results


### DIFFICULTIES 
- using a species table for the species choices, 
- not reading and thoroughly comprehending error messages and changing the wrong things that I though were related to using a table for species
- testing - query.filter and filter_by were not working for me in test scripts. It seemed silly to hard-code an id instead of finding the value from a filter(Pet.name=='x')
- testing in general seems to be a genuine time-burner for me.
