from flask import Flask,jsonify,request
from flask_restful import Api, Resource

import os
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

api=Api(app)

@app.route('/')
def hello_world():
    return jsonify({'msg':"Hello World!"})

#*******************************  DAY 2 Exercise ******************
'''
Activity
1)Registration of a User
2)Each User gets 5 tokens
3)Store a sentence for 1 tokens
4)Retirve his stored sentence on out database for 1 tokens
'''

#************************** Mongo DB Implementation ************

client = MongoClient("mongodb://127.0.0.1:27017/")
db = client.SentencesDatabase
users = db["Users"]

#**********************************************************


def verify_user_and_password(posted_data):
    # user = db.users.find({'username':posted_data.get('username')})
    user_count = db.users.count({'username':posted_data.get('username')})
    print(user_count)
    if user_count > 0:
        user = db.users.find({'username':posted_data.get('username')})[0]

        if bcrypt.checkpw(posted_data.get('password').encode('utf8'),user['password']):
            return (200,"")
        else:
            return (301,"Incorrect Password")
    else:
        return (302,"User has not registered with the API")


def count_tokens(posted_data):
    user = db.users.find({'username':posted_data['username']})[0]
    return user['tokens']


class Register(Resource):

    def post(self):
        posted_data = request.get_json()
        #get the Data
        username = posted_data.get('username')
        password = posted_data.get('password')

        if username and password:
            hashed_pw = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())
            #we don't store password as it is in database we have to use hash password
            #hash(password + salt)

            user_count = db.users.count({'username':username})
            print(str(user_count))

            #Verify that user has not registered with API Application earlier
            if user_count == 0:
                db.users.insert({
                    'username':username,
                    'password':hashed_pw,
                    'sentence':"",
                    'tokens':5
                })
                retmap = {
                    'status_code':200,
                    'message':'sucessfully signed up for the API'
                }
                return jsonify(retmap)
            else:
                return jsonify({
                    'status_code':302,
                    'error':'User has already exit with username '+username
                })
        else:
            return_data = {
                'status_code':301,
                'error':'Invalid entry for Username/Password'
            }
            return jsonify(return_data)


class Sentence(Resource):

    def get(self):
        posted_data = request.get_json()
        username = posted_data.get('username')
        user_count = db.users.count({'username':username})
        if user_count > 0:
            user_detail = db.users.find({'username':username})[0]
            json_data = {'sentence':user_detail.get('sentence'),'status_code':200}
        else:
            json_data = {"ErrorMsg":"Incorrect Username",'status_code':403}
        return jsonify(json_data)

    def post(self):

        posted_data = request.get_json()
        #get the Data
        username = posted_data.get('username')
        password = posted_data.get('password')
        sentence = posted_data.get('sentence')

        #verify that username and password match
        result = verify_user_and_password(posted_data)
        if result[0] != 200:
            return jsonify({
            'status_code':result[0],
            'error':result[1]
            })

        #verify user has enough tokens
        token_count = count_tokens(posted_data)
        if token_count < 1:
            return jsonify({
                'status_code':301,
                'error':'Not enough Tokens'
            })

        #store the sentence
        db.users.update({
            'username':username
            },{
                "$set":
                {
                    "sentence":sentence,'tokens':token_count-1
                    }
               }
        )

        return jsonify({
            'status_code':200,
            'msg':'sentence successfully updated'
        })


api.add_resource(Register,'/register')
api.add_resource(Sentence,'/get_update_sentence')




if __name__ == "__main__":
    app.run(debug=True)
