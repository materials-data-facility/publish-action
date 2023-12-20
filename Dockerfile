FROM python:3.10

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pwd ; ls -R

ENTRYPOINT ["python", "/app/main.py"]