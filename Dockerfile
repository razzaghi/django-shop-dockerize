FROM python:3.8

ENV PYTHONUNBUFFERED 1
RUN mkdir /code

WORKDIR /code
COPY requirements.txt /code/

RUN pip install -r requirements.txt
COPY start.sh /code/start.sh
COPY . /code/

RUN chmod +x start.sh
CMD ["bash start.sh"]