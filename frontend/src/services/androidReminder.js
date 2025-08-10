import { LocalNotifications } from '@capacitor/local-notifications';
let intervalId = null;
export async function startReminder(intervalMinutes = 30) {
  await LocalNotifications.requestPermissions();
  if (intervalId) clearInterval(intervalId);
  intervalId = setInterval(async () => {
    await LocalNotifications.schedule({
      notifications: [{
        title: '喝水提醒',
        body: '该喝水啦！',
        id: Date.now(),
      }],
    });
  }, intervalMinutes * 60 * 1000);
}
export function stopReminder() {
  if (intervalId) {
    clearInterval(intervalId);
    intervalId = null;
  }
}