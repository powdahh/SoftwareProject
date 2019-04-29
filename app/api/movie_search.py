from app.api import api
from app import Database
import json
from flask import request

@api.route('/search_movie', methods=["GET"])
def search_movie(search_criteria):
    data = json.loads(search_criteria)
    search = data["search"]

    myDb = Database.dbConnection()
    print(myDb)
    sqlString = "SELECT * FROM titles WHERE primaryTitle LIKE " + "'" + search + "%'" + "AND titleType = 'movie'"
    result = Database.selectStatement(myDb, sqlString)
    fetch = result.fetchall()
    info = {}
    for row in fetch:
        info[row[0]] = {
            "movieID": row[0],
            "title": row[3],
            "isAdult": row[4],
            "startYear": row[5],
            "runtime": row[7],
            "genres": row[8]
        }

    return json.dumps(info)


@api.route('/get_movieID', methods=["GET"])
def get_movieID(movie_title):
    data = json.loads(movie_title)
    search = data["movieTitle"]

    myDb = Database.dbConnection()
    print(myDb)
    sqlString = "SELECT tconst FROM titles WHERE primaryTitle = " "'" + search + "'" + "AND titleType = 'movie'"
    result = Database.selectStatement(myDb, sqlString)
    fetch = result.fetchone()[0]
    info = {
        "titleID": fetch
    }

    return json.dumps(info)

@api.route('/get_cast', methods=["GET"])
def get_cast(movie_id):
    data = json.loads(movie_id)
    search = data["titleID"]

    myDb = Database.dbConnection()
    print(myDb)
    sqlString = "Select a.nconst, a.primaryName, b.category, b.job, b.characters FROM moviedb.name_basic a, moviedb.cast b WHERE a.nconst = b.nconst AND b.tconst = " "'" + search + "'"
    result = Database.selectStatement(myDb, sqlString)
    cast_fetch = result.fetchall()
    completeInfo = {}
    for row in cast_fetch:
        completeInfo[row[0]] = {
            "name": row[1],
            "category": row[2],
            "job": row[3],
            "characters": row[4]
        }
    return json.dumps(completeInfo)

#Syed Review / Comments Code DATABASE PORTION

#@api.route('/get_comment', methods=["GET"])
#def get_comment(movie_id):
#    data = json.loads(movie_id)
 #   search = data["titleID"]

 #   myDB = Database.dbConnection()
 #   print(myDb)
 #   sqlString = "Select user, review from Comments where movie_id = '234'"
 #   result = Database.selectStatement(myDb, sqlString)
 #   cast_fetch = result.fetchall()
 #   completeInfo = {}
  #  for row in cast_fetch:
   #     completeInfo[row[0]] = {
    #        "movie_id": row[1],
     #       "comment_id": row[2],
      #      "user": row[4]

      #  }

  #  return json.dumps(cast_fetch)


#@api.route('/submit_comment', methods=["POST"])
#def create_comment():
    #if request.method == 'POST':
     #   movie_id = request.form.get('movie_id', None)
      #  comment = request.form.get('text', None)
       # user_id = request.form.get('user_id', None)
        #user = request.form.get('user', None)

        #myDB = Database.dbConnection()
       # print(myDB)
        #sqlString = "Select * from Comments where movie_id = '234', user_id = '2'"
    #    result = Database.selectStatement(myDb, sqlString)
     #   cast_fetch = result.fethcall()

        #if cast_fetch is None:
           # sqlString = "Insert into Comments (review, user_id, movie_id, user) " \
              #        "values ({comment}, {user_id}, {movie_id}, {user})".format(comment=comment, user_id=user_id,  movie_id=movie_id, user=user)
            # create new entry into table
           # result = Database.selectStatement(myDB, sqlString)
           # res = {"res": "successful"}

           # return json.dumps(res)
        #else:
         #   res = {"res": "Comment already made"}

            #return json.dumps(res)

#End Code Syed for Review

@api.route('/get_names', methods=["GET"])
def get_names(name_id):
    data = json.loads(name_id)
    search = data["nameID"]

    myDb = Database.dbConnection()
    print(myDb)
    sqlString = "SELECT primaryName FROM name_basic WHERE nconst = " "'" + search + "'"
    result = Database.selectStatement(myDb, sqlString)
    fetch = result.fetchone()
    info = {
        "name": fetch
    }

    return json.dumps(info)


