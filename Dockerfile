FROM python:3.9
WORKDIR /app
COPY . /app
ENV FLASK_APP='task_2_2:app'
RUN pip install --no-cache gunicorn -r requirements.txt
ENTRYPOINT flask run --host=0.0.0.0

