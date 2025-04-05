FROM node:22-alpine

WORKDIR /app

COPY package.json package-lock.json server.js ./
RUN npm install --only=production

EXPOSE 3000

CMD ["node", "server.js"]
