# app.py
from flask import Flask, request, jsonify, g
import sqlite3

#BASIC APP CODE

app = Flask(__name__)

#EXAMPLE OF GET

@app.route('/getecho/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    echo = request.args.get("echo", None)

    # For debugging
    print(f"got string {echo}")

    response = {}

    # Check if user sent a name at all
    if not echo:
        response["ERROR"] = "no string found, please send a string."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"The server echoes: {echo}"

    # Return the response in json format
    return jsonify(response)


#EXAMPLE OF POST

@app.route('/postecho/', methods=['POST'])
def post_something():
    param = request.form.get('echo')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Server got via POST, the message: {param}",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no string found, please send a string."
        })

#-------------------------------------------------------------

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)


#-------------------------------------------------------------

#API ROUTES

@app.route('/testdatabase/', methods=['GET'])
def respondtest():
    cur = get_db().execute("SELECT * FROM User;")
    userinfo = cur.fetchall()
    cur.close()

    response = {}

    # Check if user sent a name at all
    if not userinfo[0]:
        response["ERROR"] = "test database, found 0 users"
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"The server found: {userinfo[0]}"

    # Return the response in json format
    return jsonify(response)

@app.route('/contests/', methods=['GET'])
def contests():

    # Retrieve url parameters
    status = request.args.get("status", None)
    page = request.args.get("page", None)

    response = {}

    #CODE
    #if (status[0] and page[0]):
        #do code for it



    return jsonify(response)

@app.route('/zoos/recommended/', methods=['GET'])
def zoosRecommended():

    response = {}

    #CODE

    return jsonify(response)

@app.route('/contests/<int:contest_id>', methods=['GET'])
def getContest(contest_id):

    #CODE

    response = {}
    response["MESSAGE"] = f"The server found: {contest_id}"


    return jsonify(response)
#-------------------------------------------------------------

#DATABASE ACCESS CODE

DATABASE = 'ikemengori.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

