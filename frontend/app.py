from flask import Flask,request,render_template,redirect
import requests
import json 

from flask import Flask
import pika

# connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', heartbeat=600, blocked_connection_timeout=300))
# channel = connection.channel()
import psycopg2
def publish(method, body):
    properties = pika.BasicProperties(method)
    # channel.basic_publish(exchange='', routing_key='blog', body=json.dumps(body), properties=properties)

class Review(object):
    def __init__(self,name,review):
        self.name = name
        self.review = review

app = Flask(__name__)

DB_USER = 'odoo'
DB_PASSWORD = 'odoo'
DB = 'docker_test'
DB_HOST = 'localhost'


@app.route("/",methods=["POST","GET"])
def index():

    if request.method == "POST":
        name = request.form["name"]
        review = request.form["review"]

        conn = psycopg2.connect(host=DB_HOST, database=DB, user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()

        # Execute SQL INSERT statement
        insert_query = "INSERT INTO REVIEWS (name, review) VALUES (%s, %s)"
        cursor.execute(insert_query, (name, review))

        # Commit the transaction and close the connection
        conn.commit()
        cursor.close()
        conn.close()

        # res = requests.post("http://172.16.227.164:5000//reviews/add",data={"name":name,"review":review})
        # # res = {"name": name,
        # #         "review": review}
        # print(res)
        # publish('add',res)
        return redirect("/reviews")

    return render_template("index.html")


@app.route("/reviews",methods=["GET"])
def reviews():

    LOAD_REVIEW = "SELECT * from REVIEWS"
    conn = psycopg2.connect(
        host=DB_HOST, database=DB, user=DB_USER, password=DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute(LOAD_REVIEW)
    results = cursor.fetchall()

    # res = requests.post("http://172.16.227.164:5000//reviews/list").json()
    # print(res)
    reviews = []

    for review in results:
        reviews.append(Review(review[0],review[1]))
    return render_template("reviews.html",reviews=reviews)

app.run(host="0.0.0.0",port=5000)
