FROM python:3.9

WORKDIR /app
COPY . /app

RUN pip install --no-cache -r requirements.txt
RUN pip install tox
CMD flask run