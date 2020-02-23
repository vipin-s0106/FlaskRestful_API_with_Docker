from flask import Flask,jsonify,request
from flask_restful import Api, Resource

import os
from pymongo import MongoClient

app = Flask(__name__)

api=Api(app)

'''
*******************************************
                Day1 Exercise
*******************************************
Notes

1)install flask using pip or pip3
'''



@app.route('/')
def hello_world():
    return "Hello World!"

@app.route("/hithere")
def hi_there_everyone():
    return "I just hit hi there Link"


@app.route('/add_two_nums',methods=['POST'])
def addition():
    print("Coming to function")
    json_data = request.get_json()
    if 'a' not in json_data or 'b' not in json_data:
        return jsonify({
            "error":"some error occured"
        })
    a = json_data['a']
    b = json_data['b']
    result={
        "sum":a+b,
        "status code":200
    }
    return jsonify(result)

@app.route("/bye")
def bye1():
    c = 2*534
    s = str(c)
    json_data = {
        "a":1,
        "b":2

    }
    return jsonify(json_data)


'''
*******************************************
                Day1 Exercise
*******************************************

Notes-
1)install - pip install flask-restful

'''

#function to check the validated json_data
def validate_posted_data(operation,posted_data):
    if 'x' not in posted_data or 'y' not in posted_data:
        return 301
    elif int(posted_data['y']) == 0 and operation == "division":
        return 304
    else:
        return 200


class Add(Resource):
    def post(self):
        posted_data = request.get_json()

        status_code = validate_posted_data("add",posted_data)

        if status_code != 200:
            return jsonify({
                "Status Code":status_code,
                "Error Message":"An Error occured"
            })

        #execute below steps when status code is 200
        x = int(posted_data['x'])
        y = int(posted_data['y'])

        ret = x+y

        retmap = {
            "sum":ret,
            "Status Code":200
        }
        return jsonify(retmap)


    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

class Subtract(Resource):
    def post(self):
        posted_data = request.get_json()

        status_code = validate_posted_data("subtract",posted_data)

        if status_code != 200:
            return jsonify({
                "Status Code":status_code,
                "Error Message":"An Error occured"
            })

        #execute below steps when status code is 200
        x = int(posted_data['x'])
        y = int(posted_data['y'])

        ret = x-y

        retmap = {
            "subtract":ret,
            "Status Code":200
        }
        return jsonify(retmap)

class Multiply(Resource):
    def post(self):
        posted_data = request.get_json()

        status_code = validate_posted_data("multiply",posted_data)

        if status_code != 200:
            return jsonify({
                "Status Code":status_code,
                "Error Message":"An Error occured"
            })

        #execute below steps when status code is 200
        x = int(posted_data['x'])
        y = int(posted_data['y'])

        ret = x*y

        retmap = {
            "multiplication":ret,
            "Status Code":200
        }
        return jsonify(retmap)

class Divide(Resource):
    def post(self):
        posted_data = request.get_json()

        status_code = validate_posted_data("division",posted_data)

        if status_code != 200:
            if status_code == 304:
                return jsonify({
                    "Status Code":status_code,
                    "Error Message":"Zero Division Error"
                })
            else:
                return jsonify({
                    "Status Code":status_code,
                    "Error Message":"An Error occured"
                })


        #execute below steps when status code is 200
        x = int(posted_data['x'])
        y = int(posted_data['y'])

        ret = x/y

        retmap = {
            "Division":ret,
            "Status Code":200
        }
        return jsonify(retmap)


#************************** Mongo DB Exercise ************

client = MongoClient("mongodb://db:27017")
db = client.aNewDB
UserNum = db["UserNum"]

UserNum.insert({
    'num_of_users':0
})

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['num_of_users']
        new_num = prev_num + 1
        UserNum.update({},{"$set":{'num_of_users':new_num}})
        return str("Hello User" + str(new_num))

#**********************************************************


api.add_resource(Add,"/add")
api.add_resource(Subtract,"/subtract")
api.add_resource(Divide,"/divide")
api.add_resource(Multiply,"/multiply")
api.add_resource(Visit,"/hello")

#https://github.com/vipin-s0106/FlaskRestful_API_with_Docker.git
if __name__ == "__main__":
    app.run(host='0.0.0.0')
