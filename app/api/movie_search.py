from app.api import api
from app import Database
import json
from flask import request


def sql_fetch(sqlString):
    myDb = Database.dbConnection()
    result = Database.selectStatement(myDb, sqlString)
    fetch = result.fetchall()
    print(len(fetch))
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

#GenreSearch

@api.route('/search_movie', methods=["GET"])
def search_movie(search_criteria):
    data = json.loads(search_criteria)
    search = str(data["search"])

    ##default to title search
    sqlString = "SELECT * FROM titles WHERE primaryTitle LIKE " + "'" + search + "%'" + "AND titleType = 'movie';"
    if "genre:" in search:
        search = search.replace(" ", "")
        genre = search.rsplit(":")[-1]
        sqlString = "SELECT * FROM titles WHERE genres LIKE \'{}\' and titleType = \'movie\' limit 1000".format(genre)
    elif "year:" in search:
        search = search.replace(" ", "")
        year = search.rsplit(":")[-1]
        sqlString = "SELECT * FROM titles WHERE startYear LIKE \'{}\' and titleType = \'movie\' limit 1000".format(year)

    return sql_fetch(sqlString)



#GenreSearch end


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


