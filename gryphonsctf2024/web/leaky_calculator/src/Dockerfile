FROM python:3.11-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER nobody 

EXPOSE 1337

ENTRYPOINT ["python", "-u", "app.py"]