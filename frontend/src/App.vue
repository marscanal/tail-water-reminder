<template>
  <div style="max-width:640px;margin:30px auto;font-family:Helvetica, Arial;">
    <h2>喝水提醒小助手</h2>
    <ReminderStatus :status="status" />
    <WaterProgress :status="status" @change="fetchStatus" />
    <SettingsForm :settings="status" @update="onSettingsUpdate" />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import api from './api'
import WaterProgress from './components/WaterProgress.vue'
import SettingsForm from './components/SettingsForm.vue'
import ReminderStatus from './components/ReminderStatus.vue'

const status = ref({})
let waterTimer = null
let standTimer = null

async function fetchStatus() {
  try {
    const res = await api.getStatus()
    status.value = res.data
  } catch (e) { console.error(e) }
}

function startWaterReminder() {
  clearInterval(waterTimer)
  if (!status.value.reminder_interval_minutes) return
  const intervalMs = status.value.reminder_interval_minutes * 60 * 1000
  waterTimer = setInterval(() => {
    showNotification('喝水提醒', '该喝水啦！')
    if (status.value.stand_enabled) {
      startStandCountdown()
    }
  }, intervalMs)
}

function startStandCountdown() {
  clearTimeout(standTimer)
  const standMs = (status.value.stand_duration_minutes || 3) * 60 * 1000
  console.log(`开始站立计时 ${standMs/60000} 分钟`)
  standTimer = setTimeout(() => {
    console.log('可以坐下休息了')
    showNotification('站立结束', '可以坐下休息了')
  }, standMs)
}

function showNotification(title, body) {
  if (Notification.permission === 'granted') {
    new Notification(title, { body })
  } else if (Notification.permission !== 'denied') {
    Notification.requestPermission().then((permission) => {
      if (permission === 'granted') {
        new Notification(title, { body })
      }
    })
  }
}

function onSettingsUpdate() {
  fetchStatus().then(() => {
    startWaterReminder()
  })
}

onMounted(() => {
  fetchStatus().then(() => {
    startWaterReminder()
  })
})

onBeforeUnmount(() => {
  clearInterval(waterTimer)
  clearTimeout(standTimer)
})
</script>

