FROM python:3.11-slim-bookworm

WORKDIR /app

COPY src/requirements.txt ./
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt --no-cache-dir

COPY src /app

CMD [ "python", "main.py" ]
