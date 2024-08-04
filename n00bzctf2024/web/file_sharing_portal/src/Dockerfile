FROM python:3.9-slim
RUN apt-get update && \
    apt-get install -y cron && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt server.py /app/
COPY templates/ /app/templates/
COPY uploads/ /app/uploads/
COPY REDACTED.txt /app/
# The flag file is redacted on purpose
RUN pip install --no-cache-dir -r requirements.txt
# Add the cron job to the crontab
RUN mkdir /etc/cron.custom
RUN echo "*/5 * * * * root rm -rf /app/uploads/*" > /etc/cron.custom/cleanup-cron
RUN echo "* * * * * root cd / && run-parts --report /etc/cron.custom" | tee -a /etc/crontab
# Give execution rights on the cron job
RUN chmod +x /etc/cron.custom/cleanup-cron
RUN crontab /etc/cron.custom/cleanup-cron
RUN crontab /etc/crontab
CMD ["sh", "-c", "cron && python server.py"]
