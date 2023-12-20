FROM python:3.10

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN pwd ; ls -R

ENTRYPOINT ["python", "/app/main.py"]