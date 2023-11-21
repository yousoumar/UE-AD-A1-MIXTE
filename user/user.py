from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

import grpc
import booking_pb2
import booking_pb2_grpc

app = Flask(__name__)

PORT = 3203
HOST = "0.0.0.0"


with open("{}/data/users.json".format("."), "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=["GET"])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/users", methods=["GET"])
def get_users():
    res = make_response(jsonify(users), 200)
    return res


@app.route("/users/<userid>", methods=["GET"])
def get_user_by_id(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            res = make_response(jsonify(user), 200)
            return res
    return make_response(jsonify({"error": "User not found"}), 400)


@app.route("/users/<userid>/bookings", methods=["GET"])
def get_user_bookings(userid):
    booking = {}
    returnedBooking = {}
    with grpc.insecure_channel("booking:3201") as channel:
        stub = booking_pb2_grpc.BookingStub(channel)
        booking = stub.GetUserBookings(booking_pb2.UserId(userid=userid))

        returnedBooking["userid"] = booking.userid
        returnedBooking["dates"] = []

    for date_item in booking.dates:
        mapped_movies = []
        for movie_id in date_item.movies:
            qurey = """
                {
                    movie_with_id (_id: "%s"){
                        title,
                        id,
                        rating,
                        director
                    }
                }
            """ % (
                movie_id
            )
            res = requests.post(url="http://movie:3200/graphql", json={"query": qurey})
            movie = res.json()
            mapped_movies.append(movie["data"]["movie_with_id"])

        returnedBooking["dates"].append(
            {"date": date_item.date, "movies": mapped_movies}
        )

    return make_response(jsonify(returnedBooking), 200)


@app.route("/users/<userid>/bookings", methods=["POST"])
def book_for_user(userid):
    data = request.get_json()

    with grpc.insecure_channel("booking:3201") as channel:
        stub = booking_pb2_grpc.BookingStub(channel)
        try:
            stub.AddToUserBookings(
                booking_pb2.BookingPayload(
                    userid=userid, date=data["date"], movieid=data["movieid"]
                )
            )
            return make_response(jsonify({"message": "booking added successfully"}))
        except Exception as e:
            return make_response(
                jsonify(
                    {
                        "error": "the date or the movieid is not correct, make sure the date is in the showtime table, that the movie is part of it, and that's not already reserved"
                    }
                ),
                400,
            )


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
