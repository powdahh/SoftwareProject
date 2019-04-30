from app.api import api
from app import Database
import json
from flask import request

#Syed Review / Comments Code DATABASE PORTION

@api.route('/get_comment', methods=["GET"])
def get_comment(movie_id):
    data = json.loads(movie_id)
    search = data["titleID"]

    myDB = Database.dbConnection()
    print(myDB)
    sqlString = "Select user, review from Comments where movie_id = '234'"
    result = Database.selectStatement(myDB, sqlString)
    cast_fetch = result.fetchall()
    completeInfo = {}
    for row in cast_fetch:
        completeInfo[row[0]] = {
            "movie_id": row[1],
            "comment_id": row[2],
            "user": row[4]

        }

    return json.dumps(movie_id)#cast_fetch)

@api.route('/insert_comment', methods=["POST"])
def insert_comment():
    if request.method == 'POST':
        movie_id = request.form.get('movie_id', None)
        comment = request.form.get('text', None)
        user_id = request.form.get('user', None)

@api.route('/submit_comment', methods=["POST"])
def create_comment():
    if request.method == 'POST':
        movie_id = request.form.get('movie_id', None)
        comment = request.form.get('text', None)
        user_id = request.form.get('user_id', None)
        user = request.form.get('user', None)

        myDB = Database.dbConnection()
        print(myDB)
        print(movie_id)
        sqlString = "Select * from Comments where movie_id = '234', user_id = '2'"
        result = Database.selectStatement(myDB, sqlString)
        cast_fetch = result.fethcall()

        if cast_fetch is None:
            sqlString = "Insert into Comments (review, user_id, movie_id, user) " \
                        "values ({comment}, {user_id}, {movie_id}, {user})".format(comment=comment, user_id=user_id,
                                                                                   movie_id=movie_id, user=user)
            # create new entry into table
            result = Database.selectStatement(myDB, sqlString)
            res = {"res": "successful"}

            return json.dumps(res)
        else:
            res = {"res": "Comment already made"}

    return json.dumps(movie_id)

#End Code Syed for Review
