FROM python:3.8-alpine
WORKDIR /app
COPY requirements.txt /app
ADD . /app/
RUN pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I=./protos --python_out=. --grpc_python_out=. showtime.proto
CMD ["python","-u","showtime.py"]
