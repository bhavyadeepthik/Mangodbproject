from flask import Flask

from flask_pymongo import PyMongo

from bson.json_util import dumps

from bson.objectid import ObjectId

from flask import jsonify, request

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "secret_key"

app.config['MONGO_URI'] = "mongodb://localhost:27017/newUsers.movie"

mongo = PyMongo(app)


@app.route('/add', methods=['POST'])
def add_newUser():

    _json = request.json
    _name = _json['name']
    _email = _json['email']

    if _name and _email and request.method == 'POST':

        id = mongo.db.movie.insert({'name': _name, 'email': _email})

        resp = jsonify("user added succesfully")

        resp.status_code = 200

        return resp

    else:
        return not_found()


@app.route('/newUsers')
def newUsers():
    newUsers = mongo.db.movie.find()
    resp = dumps(newUsers)
    return resp


@app.route('/movie/<id>')
def movie(id):
    movie = mongo.db.movie.find_one({'_id': ObjectId(id)})
    resp = dumps(movie)
    return resp


@app.route('/delete/<id>', methods=['DELETE'])
def delete_movie(id):
    mongo.db.movie.delete_one({'_id': ObjectId(id)})
    resp = jsonify("user deleted successfully")

    resp.status_code = 200

    return resp


@app.route('/update/<id>', methods=['PUT'])
def update_movie(id):
    _id = id
    _json = request.json
    _name = json['name']
    _email = json['email']

    if _name and _email and _id and request.method == 'PUT':

        mongo.db.movie.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(
            _id)}, {'$set': {'name': _name, 'email': _email}})
        resp = jsonify("user updated successfully")

        resp.status_code = 200

        return resp
    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'not found' + request.url
    }
    resp = jsonify(message)

    resp.status_code = 404

    return resp


if __name__ == "__main__":
    app.run(debug=True)
