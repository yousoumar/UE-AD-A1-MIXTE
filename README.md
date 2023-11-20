# UE-AD-A1-MIXTE## Overview

As part of our Distributed System course at IMT Atlantique, this project is about the implementation of REST, gRPC, and GraphQL APIs in the context of a movie booking system with 4 microservices.

The four services are: `movie` (a GraphQL server), `booking` (a gRPC server and client), `showtime` (a gRPC server), and `user` (a REST server, and a GraphQL and gRPC client):

![Architecture illustration](./architecture.png)

We used `Python`, `Flask`, `Docker` and `Docker Compose`



## Running it locally

You should have Docker and Docker Compose installed. After that, it's as simple as cloning this repository, opening a terminal window in the project root folder, and running:

```sh
docker-compose up
```

The user service can be accessed on `http://localhost:3203`, the showtime on `http://localhost:3202`, the booking on `http://localhost:3201`, and the movie on `http://localhost:3200`.

