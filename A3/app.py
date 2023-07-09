from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# RDS config
DB_HOST = "krishnadb.c8thzzafkvni.us-east-1.rds.amazonaws.com"
DB_PORT = 3306
DB_USER = "admin"
DB_PASSWORD = "admin123"
DB_NAME = "krishnadb"

# Connect to the  database
def get_db_connection():
    connection = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    return connection

#end point to store products
@app.route('/store-products', methods=['POST'])
def store_products():
    data = request.get_json()
    #open db connection
    conndb = get_db_connection()
    dbcur = conndb.cursor()
    #insert products into db
    for product in data['products']:
            name = product.get('name')
            price = product.get('price')
            availability = product.get('availability')
            #insert query
            insert_query = "INSERT INTO products (name, price, availability) VALUES (%s, %s, %s)"
            dbcur.execute(insert_query, (name, price, availability))
    #commit and close db connection
    conndb.commit()
    dbcur.close()
    conndb.close()
    #return message
    return jsonify({'message': 'Success.'}), 200

        
#end point to list products
@app.route('/list-products', methods=['GET'])
def list_products():
    #connect db
    conndb = get_db_connection()
    dbcur = conndb.cursor()
    #select statement
    select_query = "SELECT name, price, availability FROM products"
    dbcur.execute(select_query)
    #get all products
    products = dbcur.fetchall()
    #end db connection
    dbcur.close()
    conndb.close()
    #make a list of products
    product_list = []
    for product in products:
        name, price, availability = product
        product_list.append({'name': name, 'price': price, 'availability': availability})
    #return products
    return jsonify({'products': product_list}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
