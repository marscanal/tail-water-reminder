const express = require('express');
const cors = require('cors');
const cron = require('node-cron');
const WebSocket = require('ws');
const app = express();
app.use(cors());
app.use(express.json());
let intervalMinutes = 30;
const server = app.listen(3000, () => {
  console.log('Backend running on port 3000');
});
const wss = new WebSocket.Server({ server });
let clients = [];
wss.on('connection', (ws) => {
  clients.push(ws);
  ws.on('close', () => {
    clients = clients.filter(client => client !== ws);
  });
});
function sendNotification(title, message) {
  clients.forEach(ws => {
    ws.send(JSON.stringify({ type: 'notify', title, message }));
  });
}
cron.schedule(`*/${intervalMinutes} * * * *`, () => {
  sendNotification('喝水提醒', '该喝水啦！');
});
app.post('/set-interval', (req, res) => {
  const { minutes } = req.body;
  if (minutes && Number(minutes) > 0) {
    intervalMinutes = Number(minutes);
    res.json({ success: true });
  } else {
    res.status(400).json({ error: 'Invalid minutes' });
  }
});