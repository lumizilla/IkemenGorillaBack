# app.py
from flask import Flask, request, jsonify, g
import sqlite3
import sys

app = Flask(__name__)

#DATABASE ACCESS CODE

DATABASE = 'ikemengori.db'

def get_db():
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#-------------------------------------------------------------

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

#DATABASE ACCESS EXAMPLE

@app.route('/testdatabase/', methods=['GET'])
def testdatabase():
    cur = get_db().execute("SELECT * FROM User;")
    userinfo = cur.fetchall()
    cur.close()

    response = {}

    #example of printing on logs
    print("example of printing on logs")
    sys.stdout.flush()

    # Check if user sent a name at all
    if not userinfo[0]:
        response["ERROR"] = "test database, found 0 users"
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"The server found: {userinfo[0]}"

    # Return the response in json format
    return jsonify(response)


#-------------------------------------------------------------

#API ROUTES

"""
#YAMADA
@app.route('/contests/', methods=['GET'])
def contests():

    # Retrieve url parameters
    status = request.args.get("status", None)
    page = request.args.get("page", None)

    response = []

    cur = get_db().execute("SELECT * FROM Contest LIMIT 8;")
    columns = [column[0] for column in cur.description]
    for row in cur.fetchall():
        response.append(dict(zip(columns, row)))
    cur.close()
    
    #response["MESSAGE"] = "this is where you have to save the server answer"
    #if not contestinfo[0]:
    #    response["ERROR"] = "test database, found 0 contests"

    return jsonify(response)
"""


@app.route('/zoos/recommended/', methods=['GET'])
def zoosRecommended():
    response = []

    #Getting random 8 zoos in a optimized manner
    cur = get_db().execute("SELECT * FROM Zoo WHERE ID IN (SELECT ID FROM Zoo ORDER BY RANDOM() LIMIT 8);")
    columns = [column[0] for column in cur.description]

    for row in cur.fetchall():
        response.append(dict(zip(columns, row)))
    
    cur.close()

    return jsonify(response)

"""
# YAMADA 
@app.route('/contests/<int:contest_id>', methods=['GET'])
def getContest(contest_id):
    response = []
    #TODO
    return jsonify(response)
"""

@app.route('/contests/<int:contest_id>/sponsors', methods=['GET'])
def getContestSponsors(contest_id):
    response = []
    sponsorIDs = []

    #getting sponsor IDs based on contest id
    cur = get_db().execute("SELECT sponsorID FROM Support WHERE contestID = "+str(contest_id)+";")
    columns = [column[0] for column in cur.description]
    for row in cur.fetchall():
        sponsorIDs.append(row["sponsorID"])
    
    cur.close()
    
    #getting all information about each sponsor
    cur = get_db().execute("SELECT * FROM Sponsor WHERE ID IN ("+str(sponsorIDs).strip('[]')+");")
    columns = [column[0] for column in cur.description]

    for row in cur.fetchall():
        response.append(dict(zip(columns, row)))
   
    cur.close()

    return jsonify(response)

@app.route('/contests/<int:contest_id>/posts', methods=['GET'])
def getContestPosts(contest_id):
        
        response = []
        entries = []

        #selecting entries according to contest_id
        cur = get_db().execute( \
            "SELECT e.created AS created_at, e.ID AS id, e.placement, e.animalID AS animal_id, a.name AS animal_name, \
            a.image_url AS animal_icon_url, a.description, a.zooID AS zoo_id, z.name AS zoo_name \
                FROM Entry e, Zoo z, Animal a WHERE e.animalID = a.ID AND a.zooID = z.ID AND e.contestID = "+str(contest_id)+";")
        
        columns = [column[0] for column in cur.description]
        for row in cur.fetchall():
            post = []
            post = dict(zip(columns, row))

            #adding other animal pictures other than profile
            pictures = []
            cur2 = get_db().execute( \
                    "SELECT Picture.image_url FROM Picture WHERE Picture.animalID = "+str(post["animal_id"])+";") 
            for row in cur2.fetchall():
                pictures.append(row["image_url"])

            post["image_urls"] = pictures
            
            entries.append(post)

        cur.close()

        return jsonify(entries)


@app.route('/zoos/<int:zoo_id>', methods=['GET'])
def zooByID(zoo_id):
    response = []

    cur = get_db().execute("SELECT * FROM Zoo WHERE ID = "+str(zoo_id)+";")
    columns = [column[0] for column in cur.description]

    for row in cur.fetchall():
        response.append(dict(zip(columns, row)))
    
    cur.close()

    return jsonify(response)


@app.route('/createuser', methods=['GET'])
def createUser():
    response = []
    newuser = {}

    cur = get_db().execute("INSERT INTO 'User' ('name', 'image_url', 'profile') VALUES ('','','');")
    get_db().commit()

    newuser["id"] = cur.lastrowid
    newuser["name"] = ""
    newuser["image_url"] = ""
    newuser["profile"] = ""

    response.append(newuser)

    cur.close()

    return jsonify(response)

@app.route('/users/<int:user_id>', methods=['POST'])
def editUser(user_id):
    
    updateduser = {}
    #proper way to receive parameters in POST
    name = request.form.get('name')
    icon = request.form.get('icon_url')

    cur = get_db().execute("UPDATE 'User' SET name = '"+str(name)+"', 'image_url' = '"+str(icon)+"' WHERE ID = "+str(user_id)+";")
    get_db().commit()

    updateduser["id"] = user_id
    updateduser["name"] = name
    updateduser["icon_url"] = icon
    updateduser["profile"] = ""

    cur.close()

    response = []
    response.append(updateduser)

    return jsonify(response)

@app.route('/contests/<int:contest_id>/vote', methods=['POST'])
def vote(contest_id):
    
    response = {}

    #proper way to receive parameters in POST
    user = request.form.get('user_id')
    animal = request.form.get('animal_id')
    
    if(user == None or user=="" or animal =="" or animal == None):
        response["result"] = "error: user id or animal id missing."
        return jsonify(response)

    #selecting the Entry related to the vote
    cur = get_db().execute("SELECT * FROM 'Entry' WHERE contestID="+str(contest_id)+" AND animalID="+str(animal)+";")
    entry = cur.fetchone()

    if(entry != None):
        #see if user already voted
        cur1 = get_db().execute("SELECT * FROM 'Vote' WHERE entryID="+str(entry["ID"])+" AND userID="+str(user)+";")
        vote = cur1.fetchone()

        if( vote == None):
            #insert in table Vote
            cur2 = get_db().execute("INSERT INTO 'Vote'('entryID', 'userID') VALUES ('"+str(entry["ID"])+"','"+str(user)+"');")
            get_db().commit()
            cur2.close()
            response["result"] = "ok"
        else:
            response["result"] = "error: user already voted for this animal in this contest"
        cur1.close()

    else:
        response["result"] = "error: entry related to this vote doesnt exist"
    cur.close()

    return jsonify(response)

@app.route('/zoos/<int:zoo_id>/favorite', methods=['POST'])
def favoriteZoo(zoo_id):
    
    response = {}

    #proper way to receive parameters in POST
    user = request.form.get('user_id')
    cur = get_db().execute("SELECT * FROM 'UserFanZoo' WHERE userID="+str(user)+" AND zooID="+str(zoo_id)+";")
    fan = cur.fetchone()
    if(fan == None):
        cur = get_db().execute("INSERT INTO 'UserFanZoo'('userID', 'zooID') VALUES ("+str(user)+", "+str(zoo_id)+");")
        get_db().commit()

        if(cur.lastrowid == "" or cur.lastrowid == None):
            response["error"] = "Insert in table failed."
            cur.close()
            return jsonify(response)
        else:
            response["result"] = "ok"
            cur.close()
            return jsonify(response)
    else:
        response["error"] = "User is already fan of this zoo."
        return jsonify(response)

#-------------------------------------------------------------

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our IkemenGorilla server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)



