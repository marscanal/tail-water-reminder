<script setup>
import { ref, onMounted } from 'vue';
import { initNotificationListener, setReminderInterval } from './services/notify';
import { sendNotification, requestPermission, isPermissionGranted } from '@tauri-apps/api/notification';

const minutes = ref(30);

function updateInterval() {
  setReminderInterval(minutes.value);
}

async function sendTestNotification() {
  let permissionGranted = await isPermissionGranted();
  if (!permissionGranted) {
    const permissionResult = await requestPermission();
    permissionGranted = permissionResult === 'granted';
  }

  if (permissionGranted) {
    sendNotification({
      title: "测试通知",
      body: "这是一条来自 Tauri 的测试消息！",
    });
  } else {
    alert("你必须先允许通知权限！");
  }
}

onMounted(() => {
  // For desktop, we listen for notifications from the backend
  initNotificationListener();
});
</script>

<template>
  <div>
    <h1>喝水提醒</h1>
    <div>
      <label>提醒间隔（分钟）：</label>
      <input type="number" v-model="minutes" />
      <button @click="updateInterval">更新间隔</button>
    </div>
    <div style="margin-top: 20px;">
      <button @click="sendTestNotification">发送测试通知</button>
    </div>
  </div>
</template>