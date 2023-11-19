FROM python:3.8-alpine
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
ADD . /app/
RUN python -m grpc_tools.protoc -I=./protos --python_out=. --grpc_python_out=. booking.proto
CMD ["python","-u","user.py"]
