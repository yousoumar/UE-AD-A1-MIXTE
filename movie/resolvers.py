import json


def get_all_movies(_, info):
    with open("{}/data/movies.json".format("."), "r") as file:
        movies = json.load(file)
        return movies["movies"]


def movie_with_id(_, info, _id):
    with open("{}/data/movies.json".format("."), "r") as file:
        movies = json.load(file)
        for movie in movies["movies"]:
            if movie["id"] == _id:
                return movie


def actor_with_id(_, info, _id):
    with open("{}/data/actors.json".format("."), "r") as file:
        movies = json.load(file)
        for movie in movies["actors"]:
            if movie["id"] == _id:
                return movie


def update_movie_rate(_, info, _id, _rate):
    newmovies = {}
    newmovie = {}
    with open("{}/data/movies.json".format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies["movies"]:
            if movie["id"] == _id:
                movie["rating"] = _rate
                newmovie = movie
                newmovies = movies
    with open("{}/data/movies.json".format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie


def resolve_actors_in_movie(movie, info):
    with open("{}/data/actors.json".format("."), "r") as file:
        data = json.load(file)
        actors = [actor for actor in data["actors"] if movie["id"] in actor["films"]]
        return actors
