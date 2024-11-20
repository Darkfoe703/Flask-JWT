FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

COPY . .
RUN ls -a
RUN chmod a+x boot.sh

ENV FLASK_APP app.py

EXPOSE 5001
ENTRYPOINT ["./boot.sh"]
