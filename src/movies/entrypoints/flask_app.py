from flask import Flask, request, jsonify
from movies import models
import csv
import movie_fetcher
import models
from manage import users

app = Flask(__name__)
models.start_mappers()

@app.route("/<string:user>/recommendations/<string:rec_type>/<int:pref1>/<int:pref2>/<int:pref3>", methods=["GET"])                             # NORMAL ROUTE
@app.route("/<string:user>/recommendations/<string:rec_type>/<int:pref1>/<int:pref2>/<int:pref3>/<int:size>", methods=["GET"])                  # WITH SIZE
@app.route("/<string:user>/recommendations/<string:rec_type>/<int:pref1>/<int:pref2>/<int:pref3>/<string:rating>", methods=["GET"])             # WITH RATING ORDER
@app.route("/<string:user>/recommendations/<string:rec_type>/<int:pref1>/<int:pref2>/<int:pref3>/<int:size>/<string:rating>", methods=["GET"])  # WITH SIZE AND RATING ORDER
def get_recomendations(user, rec_type, pref1, pref2, pref3, size=10, rating=True):

    calc = pref1 * pref2 * pref3
    calc = (calc % 5) + 1

    rec_list = models.User(user).create_list(rec_type.lower())

    if (rec_list == None):
        return 'Only supports film recommendations', 400
    if(rec_list == 400):
         return 'User not authorized', 400
    
    movie_fetcher.main(rating)
    rec_list.readCSV(size, calc)
    

    return jsonify(rec_list.getList()), 200

