FROM python:3.8.0-buster
RUN apt update -y && apt install -y bash python3-tk ghostscript
COPY . app/
WORKDIR /app
RUN pip install -r requirements.txt
