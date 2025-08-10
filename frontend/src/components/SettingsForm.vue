<template>
  <div style="padding:16px;border:1px solid #eee;border-radius:8px;">
    <h3>提醒设置</h3>
    <div style="display:flex;gap:8px;align-items:center">
      <label>提醒间隔（分钟）</label>
      <input v-model.number="local.reminder_interval_minutes" type="number" min="0.1" step="0.1" style="width:80px" />
    </div>
    <div style="display:flex;gap:8px;align-items:center;margin-top:8px">
      <label>站立时长（分钟）</label>
      <input v-model.number="local.stand_duration_minutes" type="number" min="0" style="width:80px" />
    </div>
    <div style="margin-top:8px">
      <label><input type="checkbox" v-model="local.stand_enabled"/> 喝水后提醒站立活动</label>
    </div>
    <div style="margin-top:12px">
      <button @click="save">保存设置</button>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue'
import api from '../api'

const props = defineProps({ settings: Object })
const emit = defineEmits(['update'])

const local = reactive({
  reminder_interval_minutes: props.settings.reminder_interval_minutes || 30,
  stand_duration_minutes: props.settings.stand_duration_minutes || 3,
  stand_enabled: props.settings.stand_enabled ?? true
})

watch(() => props.settings, (v) => {
  if (!v) return
  local.reminder_interval_minutes = v.reminder_interval_minutes
  local.stand_duration_minutes = v.stand_duration_minutes
  local.stand_enabled = v.stand_enabled
})

async function save() {
  try {
    await api.updateSettings({
      reminder_interval_minutes: local.reminder_interval_minutes,
      stand_duration_minutes: local.stand_duration_minutes,
      stand_enabled: local.stand_enabled
    })
    alert('设置已保存')
    emit('update', {...local})
  } catch (e) { console.error(e); alert('保存失败') }
}
</script>
