# docker build -t so-many-flags . && docker run -p 1337:1337 -t so-many-flags
FROM node:20-buster-slim

# Install Google Chrome
RUN apt-get update \
    && apt-get install -y wget gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf libxss1 libx11-xcb1 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# install killall
RUN apt-get update && apt-get install -y psmisc

COPY package.json server.js /app/

ARG FLAG=GPNCTF{fake_flag}
RUN echo "$FLAG" > /flag.txt

WORKDIR /app

RUN npm i
RUN mkdir /app/uploads

COPY flags.txt /app/

CMD node server.js
# CMD bash
EXPOSE 1337
