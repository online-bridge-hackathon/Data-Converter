FROM python:3.7-stretch

RUN apt-get update && mkdir -p /app

COPY requirements.txt /app/

COPY /src/ /app/

WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt

#ENV FLASK_APP "api.py"

CMD [ "python3.7", "api.py"]

