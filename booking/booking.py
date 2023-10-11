import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import json
import showtime_pb2
import showtime_pb2_grpc


class BookingServicer(booking_pb2_grpc.BookingServicer):
    def __init__(self):
        with open("{}/data/bookings.json".format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    def GetUserBookings(self, request, context):
        for booking in self.db:
            if request.userid == booking["userid"]:
                return booking_pb2.BookingData(
                    userid=booking["userid"], dates=booking["dates"]
                )

    def AddToUserBookings(self, request, context):
        schedule = []
        with grpc.insecure_channel("showtime:3202") as channel:
            stub = showtime_pb2_grpc.ShowtimeStub(channel)
            schedule = stub.GetShwotime(showtime_pb2.Empty()).schedule

        for schedule_item in schedule:
            if (
                schedule_item.date == request.date
                and request.movieid in schedule_item.movies
            ):
                for booking in self.db:
                    if booking["userid"] == request.userid:
                        for item in booking["dates"]:
                            if item["date"] == request.date:
                                if request.movieid not in item["movies"]:
                                    item["movies"].append(request.movieid)
                                else:
                                    return
                            else:
                                booking["dates"].append(
                                    {
                                        "date": request.date,
                                        "movies": [request.movieid],
                                    }
                                )
                        return booking_pb2.BookingData(
                            userid=booking["userid"], dates=booking["dates"]
                        )
                # As of now we assume the userid is valid
                self.db.append(
                    {
                        "userid": userid,
                        "dates": [{"date": request.date, "movies": [request.movieid]}],
                    }
                )
                return booking_pb2.BookingData(
                    userid=self.db[-1]["userid"], dates=self.db[-1]["dates"]
                )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port("[::]:3201")
    server.start()
    print("gRPC server started ")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
