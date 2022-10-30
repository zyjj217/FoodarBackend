from flask import Flask, request, session
import pymysql.cursors


app = Flask(__name__)

conn = pymysql.connect(host = 'localhost',
                       user = 'root',
                       password = 'password',
                       db = 'Takeouttest',
                       charset = 'utf8mb4',
                       cursorclass = pymysql.cursors.DictCursor)

#simple query testing
@app.route("/", methods = ['POST', 'GET'])
def testing():
    #db stufff
    cursor = conn.cursor()
    query = 'SELECT * from users where userID = 0'
    cursor.execute(query)
    data = cursor.fetchall()
    #json stuff
    username = request.json.get('username')
    password = request.json.get('password')

    return data


#auth and register
@app.route("/gate/userAuth", methods = ['POST', 'GET'])
def userAuth():
    username = request.json.get('username')
    password = request.json.get('password')


    #db connect
    cursor = conn.cursor()
    query = 'SELECT * from users WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
    data = cursor.fetchone()
    cursor.close()
    error = None

    if(data):
        session['username'] = username
        session['userID'] = data['userID']
        session['mode'] = 0
        return 'true'
    else:
        error = 'Credentials Wrong'
        return 'false'


@app.route("/gate/driverAuth", methods = ['POST', 'GET'])
def driverAuth():
    username = request.json.get('username')
    password = request.json.get('password')


    #db connect
    cursor = conn.cursor()
    query = 'SELECT * from drivers WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
    data = cursor.fetchone()
    cursor.close()
    error = None

#once logged in store sessiondata
    if(data):
        session['username'] = username
        session['driverID'] = data['driverID']
        session['mode'] = "1"
        session['myOrders'] = {}
        return 'true'
    else:
        error = 'Credentials Wrong'
        return 'false'




@app.route("/gate/shopAuth", methods = ['POST','GET'])
def shopAuth():
    username = request.json.get('username')
    password = request.json.get('password')


    #db connect
    cursor = conn.cursor()
    query = 'SELECT * from shops WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
    data = cursor.fetchone()
    cursor.close()
    error = None

    if(data):
        session['username'] = username
        session['shopID'] = data['shopID']
        session['mode'] = 2
        return 'true'
    else:
        error = 'Credentials Wrong'
        return 'false'



@app.route("/gate/userReg")
def userReg():
    return "userReg"

@app.route("/gate/driverReg")
def driverReg():
    return "driverReg"

@app.route("/gate/shopReg")
def shopReg():
    return "shopReg"



#user actions
    #get orderlist
# @app.route("/user/getOrderlist", methods = ('POST', 'GET'))
# def getOrderlist():
#
#     cursor = conn.cursor()
#     query = 'SELECT * from orders WHERE userID = %s'
#     cursor.execute(query, userID)

    #get shoplist
    #get itemslist from shops
    #create order





#driver actions
#get orderlist
@app.route("/driver/getOrderlist", methods = ["POST", 'GET'])
def driverGetOrderlist():
    driverID = session['driverID']
    cursor = conn.cursor()
    query = 'SELECT * from orders WHERE driverID = %s'
    cursor.execute(query, driverID)
    data = cursor.fetchall()
    return data

    #accept order

#experimental
@app.route("/driver/acceptOrder", methods = ["POST", "GET"])
def driverAcceptOrder():

    orderID = request.json.get('orderID')
    status = 'Accepted'
    driverID = session['driverID']


    cursor = conn.cursor()
    query = 'UPDATE orders SET status = %s, driverID = %s WHERE orders.orderID = %s'
    cursor.execute(query, (status, driverID, orderID))
    conn.commit()
    cursor.close()

    return "Success"


#finish order
@app.route("/driver/finishOrder", methods = ["POST", "GET"])
def driverFinishOrder():
    orderID = request.json.get('orderID')
    status = 'Delivered'
    driverID = session['driverID']


    cursor = conn.cursor()
    query = 'UPDATE orders SET status = %s, driverID = %s WHERE orders.orderID = %s'
    cursor.execute(query, (status, driverID, orderID))
    conn.commit()
    cursor.close()

    return "Success"



#shop actions
#get itemslist
#post item
#put item
#delete item
#get orderlist
#accept order change status

#global methods
@app.route('/global/getOrders', methods = ['POST','GET'])
def getOrders():
    cursor = conn.cursor()
    query = 'SELECT * from orders'
    cursor.execute(query)
    data = cursor.fetchall()
    return data




app.secret_key = 'some key that you will never guess'
if __name__ == "__main__":
    app.run()
