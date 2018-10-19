FROM python:2.7.15-jessie

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

WORKDIR /app
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:80", "app:app"]
