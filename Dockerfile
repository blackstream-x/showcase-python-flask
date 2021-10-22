FROM python:3.6-alpine

WORKDIR usr/src/flask_app
RUN python -m pip install --upgrade pip
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ADD . .
RUN python ./init_db.py
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:8000", "app:app"]
