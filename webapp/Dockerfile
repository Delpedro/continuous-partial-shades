FROM python:3.4

RUN pip install flask redis

COPY . /code
WORKDIR /code

CMD ["python", "webapp.py"]
