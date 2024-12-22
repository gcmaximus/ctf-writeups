FROM python:3.12-slim-bookworm

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt && \
    chown -R root:root /app

USER nobody 

EXPOSE 1337

ENTRYPOINT ["python", "-u", "app.py"]