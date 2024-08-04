const http = require('http');
const fs = require('fs');
const path = require('path');
const WebSocket = require('ws');

const server = http.createServer((req, res) => {
    if (req.method === 'GET' && req.url === '/') {
        fs.readFile(path.join(__dirname, 'index.html'), (err, data) => {
            if (err) {
                res.writeHead(500);
                res.end();
            } else {
                res.writeHead(200, { 'Content-Type': 'text/html' });
                res.end(data);
            }
        });
    } else {
        res.writeHead(404);
        res.end('Not Found');
    }
});

const wss = new WebSocket.Server({ server });

const clients = new Map();

wss.on('connection', (ws) => {
    const clientData = {
        spins: 0,
        cumulativeAngle: 0,
        lastAngle: null,
        touchedPoints: []
    };

    clients.set(ws, clientData);

    ws.on('message', (message) => {
        const data = JSON.parse(message);
        const client = clients.get(ws);

        if (client) {
            const { x, y, centerX, centerY } = data;

            if (client.touchedPoints.some(point => point.x === x && point.y === y)) {
                return;
            }

            client.touchedPoints.push({ x, y });

            const currentAngle = Math.atan2(y - centerY, x - centerX) * (180 / Math.PI);

            if (client.lastAngle !== null) {
                let delta = currentAngle - client.lastAngle;
                if (delta > 180) delta -= 360;
                if (delta < -180) delta += 360;
                client.cumulativeAngle += delta;

                while (Math.abs(client.cumulativeAngle) >= 360) {
                    client.cumulativeAngle -= 360 * Math.sign(client.cumulativeAngle);
                    client.spins += 1;
                }

                ws.send(JSON.stringify({ spins: client.spins }));

                if (client.spins >= 9999) {
                    ws.send(JSON.stringify({ message: process.env.FLAG ?? "vsctf{test_flag}" }));
                    client.spins = 0;
                }
            }

            client.lastAngle = currentAngle;
        }
    });

    ws.on('close', () => {
        clients.delete(ws);
    });
});

const PORT = process.env.PORT || 8080;
server.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
