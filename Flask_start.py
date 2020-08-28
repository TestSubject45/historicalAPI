from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>This is the homepage. You shouldn't be here.</h1>"

@app.route("/api/storedcoins/")
def getCoins():
    """
    Returns all the coins we currently have data for.
    """
    outArray = []
    conn = create_connection("historical_data.db")
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")

    tables = [
        v[0] for v in cur.fetchall()
        if v[0] != "sqlite_sequence"
    ]
    cur.close()
    
    for table in tables:
        outArray.append(table)

    payload = {'data':outArray}

    return payload

@app.route("/api/coindata/<coin>")
def getCoinData(coin):
    """
    Returns all the coins we currently have data for.
    :param conn: the Connection object
    """
    outDict = {}
    conn = create_connection("historical_data.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM "+coin.replace(" ","_")+";")

    for item in cur.fetchall():
    	outDict[item[0]] = {'price':item[1],'percent_change_1h':item[2],'percent_change_24h':item[3],'percent_change_7d':item[4]}

    payload = {"data":outDict}
    return payload

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

if __name__ == "__main__":
    app.run(host='0.0.0.0')