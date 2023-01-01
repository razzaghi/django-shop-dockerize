FROM python:3.7

ENV PYTHONUNBUFFERED 1
RUN mkdir /app

RUN apt update && apt install -y default-libmysqlclient-dev build-essential

WORKDIR /app

COPY requirements.txt /app/

RUN pip3 install -r requirements.txt
COPY start.sh /app/
COPY gunicorn.py /app/
COPY . /app/

EXPOSE 8000

RUN chmod +x start.sh
CMD ["./start.sh"]
