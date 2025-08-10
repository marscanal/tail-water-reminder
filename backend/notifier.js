const { exec } = require('child_process');
// 检测当前运行环境
const isTauri = !!process.env.TAURI_ENV; // 可以在打包时设置
const isAndroid = process.platform === 'android';
// 桌面端通知（Windows / macOS / Linux）
function desktopNotify(title, message) {
  // Windows + Tauri 推荐用 tauri-plugin-notification
  exec(`powershell -command "New-BurntToastNotification -Text '${title}', '${message}'"`);
}
// 安卓端通知（需要 Capacitor 插件或 Termux 等环境）
function androidNotify(title, message) {
  // 这里用 adb/termux-toast 仅作示例
  exec(`termux-notification --title "${title}" --content "${message}"`);
}
function sendNotification(title, message) {
  if (isAndroid) {
    androidNotify(title, message);
  } else {
    desktopNotify(title, message);
  }
}
module.exports = { sendNotification };