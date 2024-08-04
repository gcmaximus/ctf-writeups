FROM python:slim AS app
RUN pip install --no-cache-dir progress

FROM pwn.red/jail
COPY --from=app / /srv
COPY chall.py /srv/app/run
RUN chmod +x /srv/app/run
COPY exec_utils.py /srv/app/exec_utils.py
COPY flag.txt /srv/flag.txt
# apparently im bad at docker so i stole this from kmh
RUN chmod 444 /srv/flag.txt && mv /srv/flag.txt /srv/flag.`tr -dc A-Za-z0-9 < /dev/urandom | head -c 20`.txt
ENV JAIL_MEM=20M
