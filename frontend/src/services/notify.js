import { sendNotification, requestPermission, isPermissionGranted } from '@tauri-apps/api/notification';

export async function initNotificationListener() {
  let permissionGranted = await isPermissionGranted();
  if (!permissionGranted) {
    const permissionResult = await requestPermission();
    permissionGranted = permissionResult === 'granted';
  }

  if (permissionGranted) {
    const ws = new WebSocket('ws://localhost:3000');
    ws.onmessage = async (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'notify') {
        sendNotification({ title: data.title, body: data.message });
      }
    };
  }
}

export async function setReminderInterval(minutes) {
  await fetch('http://localhost:3000/set-interval', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ minutes }),
  });
}