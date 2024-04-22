from flask import Flask, redirect,url_for, render_template, request
from pymongo import MongoClient
from bson import ObjectId # untuk ngambil object dari idnya

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    fruits = list(db.fruits.find({}))
    return render_template("dashboard.html", fruits=fruits)

@app.route('/fruit', methods=['GET', 'POST'])
def fruit():
    fruits = list(db.fruits.find({}))
    return render_template("index.html", fruits=fruits)

@app.route('/addFruit', methods=['GET', 'POST'])
def addFruit():
    if request.method == 'POST':
        # untuk request.form() sesuaikan nama didalam html
        name = request.form['name']
        price = request.form['price']
        # jika tipenya file maka request file
        image = request.files['image']
        description = request.form['description']
        
        if image :
            nameFile = image.filename
            nameFileImage = nameFile.split('/')[-1]
            filePath = f'static/assets/imgFruits/{nameFileImage}'
            image.save(filePath)
        else:
            image = None
        doc = {
            'name' : name,
            'price' : price,
            'description' : description,
            'image' : nameFileImage
        }
        db.fruits.insert_one(doc)
        # untuk menampilkan templates lain ketika berhasil 
        # dengan memasukan function route yg ingin dituju
        return redirect(url_for('fruit'))
    return render_template("AddFruit.html")

@app.route('/editFruit/<_id>', methods=['GET', 'POST'])
def editFruit(_id):
    if request.method == 'POST':
        # untuk request.form() sesuaikan nama didalam html
        id = request.form['id']
        name = request.form['name']
        price = request.form['price']
        # jika tipenya file maka request file
        image = request.files['image']
        description = request.form['description']
        doc = {
            'name' : name,
            'price' : price,
            'description' : description
        }
        if image :
            nameFile = image.filename
            nameFileImage = nameFile.split('/')[-1]
            filePath = f'static/assets/imgFruits/{nameFileImage}'
            image.save(filePath)
            doc['image'] = nameFileImage
        
        db.fruits.update_one({'_id': ObjectId(id)}, {'$set':doc})
        # untuk menampilkan templates lain ketika berhasil 
        # dengan memasukan function route yg ingin dituju
        return redirect(url_for('fruit'))
    id = ObjectId(_id)
    data = list(db.fruits.find({'_id': id}))
    return render_template("EditFruit.html", data=data)

@app.route('/deleteFruit/<_id>', methods=['GET', 'POSTY'])
def deleteFruit(_id):
    db.fruits.delete_one({'_id': ObjectId(_id)})
    # untuk menampilkan templates lain ketika berhasil 
    # dengan memasukan function route yg ingin dituju
    return redirect(url_for('fruit'))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)