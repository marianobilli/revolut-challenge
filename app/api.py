import flask
import logging 
import os
import sys
from db import Db
from flask import request, make_response, jsonify
from datetime import datetime,date

app = flask.Flask(__name__)

@app.route('/hello/status', methods=['GET'])
def get_status():
    '''
    Returns 200 if the application is up
    
    Returns
    -------
    (str, int)
        (Response message, HTTP status)
    '''
    try:
        get_db().read_databases()
        return make_response("Database up and running...",200)
    except Exception as e:
        return make_response(str(e),500)


@app.route('/hello/<username>', methods=['GET'])
def get_user(username:str):
    '''
    Handles GET /hello/<username> request. 

    Returns the message for the user.

    Parameters
    ----------
    username
    
    Returns
    -------
    (str, int)
        (Response message, HTTP status)
    '''
    try:
        username, dateOfBirth = get_db().read_user(username=username)
        response = make_response(jsonify({"message":f"Hello, {username}! {birthday_message(dateOfBirth)}"}), 200)
        get_log().info(str(response))
        return response
    except Exception as e:
        return make_response(str(e),400)
        

@app.route('/hello/<username>', methods=['PUT'])
def put_user(username:str):
    '''
    Handles POST /hello/<username> request. 

    Stores the user in the db

    Parameters
    ----------
    username

    request-data
        should be a json lile this -> { “dateOfBirth”: “YYYY-MM-DD” }
    
    Returns
    -------
    (str, int)
        (Response message, HTTP status)
    '''
    try:
        validate_request(username)
    except Exception as e:
        return make_response(str(e), 400)

    try:
        get_db().write_user(username=username, dateOfBirth=request.json.get("dateOfBirth"))
        response = make_response("",204)
        get_log().info(str(response))
        return response
    except Exception as e:
        return make_response(str(e), 500)


def get_log():
    '''
    Returns log object, it aims to work as a singleton

    Returns
    -------
    log
        an object wich is an abastraction of the database and users table
    '''
    global log
    try:
        return log
    except:
        if 'LOG_LEVEL' in os.environ:
            log_level = os.environ['LOG_LEVEL']
        else:
            log_level = 'INFO'
        logging.basicConfig(level=log_level,stream=sys.stdout,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log = logging.getLogger("API")
        return log


def get_db() -> Db:
    '''
    Returns db object, it aims to work as a singleton

    Returns
    -------
    Db
        an object wich is an abastraction of the database and users table
    '''
    global db
    try:
        return db
    except:
        db = Db(host=os.environ['DB_HOST'], port=os.environ['DB_PORT'], username=os.environ['DB_USERNAME'], password=os.environ['DB_PASSWORD'], name='revolut', schema='revolut')
        return db


def validate_request(username:str) -> None:
    '''
    Basic validations for the PUT request

    Parameters
    ----------
    username: str
    '''
    if len(username) > 25:
        raise Exception("username is longer than 25 characters")

    if not request.is_json:
        raise Exception("request body is not json")

    if "dateOfBirth" not in request.json:
        raise Exception("Field 'dateOfBirth' not found in request body")
    
    try:  
        date.fromisoformat(request.json.get("dateOfBirth"))
    except ValueError:
        raise Exception("date is not in format YYYY-MM-DD")


def days_till_birthday(dateOfBirth: date) -> int:
    '''
    Calculates days until next birthday

    Parameters
    ----------
    dateOfBirth: date
        the user's date of birth
    
    Returns
    -------
    int
        days until next birthday

    '''
    today = datetime.now().date()
    if dateOfBirth.replace(year=today.year) < today:
        return (dateOfBirth.replace(year=today.year+1)-today).days
    else:
        return (dateOfBirth.replace(year=today.year) - today).days


def birthday_message(dateOfBirth:date) -> str:
    '''
    Returns a either a happy birthday message or days until next birthday message
    Parameters
    ----------
    dateOfBirth: date
        the user's date of birth
    
    Returns
    -------
    str
        birthday message 
    '''
    days = days_till_birthday(dateOfBirth) 
    if days == 0:
        return "Happy birthday!"
    else:
        return f"Your birthday is in {days} day(s)"
    