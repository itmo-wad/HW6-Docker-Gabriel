from flask import Flask, render_template, request
import pymongo
from pymongo import MongoClient

import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'app/static/img/uploads'
app.config['SECRET_KEY'] = 'donteventhinkaboutit'

def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017, 
                         username='root', 
                         password='pass',
                        authSource="admin")
    db = client["animal_db"]
    return db



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == "POST":
        if request.files:
            image = request.files['image']
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
            return render_template('success.html')
        else:
            return render_template('failed.html')
    return render_template('form.html')

@app.route('/animals')
def get_stored_animals():
    db=""
    try:
        db = get_db()
        _animals = db.animal_tb.find()
        animals = [{"id": animal["id"], "name": animal["name"], "type": animal["type"]} for animal in _animals]
        return jsonify({"animals": animals})
    except:
        pass
    finally:
        if type(db)==MongoClient:
            db.close()



if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)