# Consumer loan app
Simple REST API in Python, built with Flask.

## Packages used
* Flask
* Flask-sqlalchemy
* marshmallow
* Click
    
## Usage
1. Clone the repository
2. Open terminal/cmd in dir
3. Install virtualenv
    ~~~sh
    > py -m pip install virtualenv
    ~~~
4. Create and activate a new virtual environment
    ~~~sh
    > py -m venv env
    > env\Scripts\activate
    ~~~
5. Install requirements
    ~~~sh
    > py -m pip install -r requirements.txt
    ~~~
6. Set environment variables
    ~~~sh
    > set FLASK_APP=app:create_app("dev")
    > set FLASK_ENV=development
    ~~~
7. Run
    * a. Tests
        ~~~sh
        > python -m unittest discover
        ~~~
    * b. Application
        ~~~sh
        > flask init-db [--seed] # first init DB and seed it if wanted
        > flask run
        ~~~

## API Schema

|Method|Route|Description
|-|-|-|
| GET    | /api/loan/<borrower_id>                      | List all loans by a borrower
| POST   | /api/loan/                                   | Apply for a loan

## Unittest coverage
~~~sh
Name                         Stmts   Miss  Cover
------------------------------------------------
app\__init__.py                 20      0   100%
app\api\loan.py                 46      1    98%
app\config.py                   12      0   100%
app\db_init.py                  36     14    61%
app\models\blacklist.py          5      0   100%
app\models\client.py             7      0   100%
app\models\loan.py              11      0   100%
app\schemas\loan_schema.py      13      1    92%
test\__init__.py                 0      0   100%
test\test.py                    40      1    98%
------------------------------------------------
TOTAL                          190     17    91%
~~~