# syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /home/mykola/Desktop/Testing

COPY requirements.txt /home/mykola/Desktop/Testing/requirements.txt
RUN pip freeze > requirements.txt
RUN pip3 install flask
RUN pip3 install --upgrade pip -r requirements.txt

COPY . /home/mykola/Desktop/Testing

EXPOSE 5000

CMD [ "python3", "main.py"]
