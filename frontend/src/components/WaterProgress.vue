<template>
  <div style="padding:16px;border:1px solid #eee;border-radius:8px;margin-bottom:12px;">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <div>
        <div style="font-weight:600">今日饮水</div>
        <div style="font-size:14px;color:#555">{{ status.water_ml || 0 }} / {{ status.goal_ml_full || 1500 }} ml</div>
      </div>
      <div>
        <button @click="modify(100)">+100 ml</button>
        <button @click="modify(-100)">-100 ml</button>
        <button @click="resetAll()" style="color:#c00">清零</button>
      </div>
    </div>
    <div style="height:12px;background:#f0f0f0;border-radius:6px;margin-top:12px;overflow:hidden">
      <div :style="barStyle"></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import api from '../api'

const props = defineProps({ status: Object })
const emit = defineEmits(['change'])

const percent = computed(() => {
  const w = props.status.water_ml || 0
  const g = props.status.goal_ml_full || 1500
  return Math.min(100, Math.round((w / g) * 100))
})

const barStyle = computed(() => ({ width: percent.value + '%', height: '100%', background: '#2b6cff' }))

async function modify(delta) {
  try {
    await api.drink(delta);
    emit('change');
    if (delta > 0 && props.status.stand_enabled) {
      setTimeout(() => {
        if (Notification.permission === 'granted') {
          new Notification('站立提醒', `喝完水，站起来活动 ${props.status.stand_duration_minutes} 分钟吧！`);
        }
      }, 1000);
    }
  } catch (e) { console.error(e); }
}

async function resetAll() {
  if (!confirm('确认清零今日饮水吗？')) return
  try {
    await api.reset()
    emit('change')
  } catch (e) { console.error(e) }
}
</script>
