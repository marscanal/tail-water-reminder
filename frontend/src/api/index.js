import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 5000
})

export default {
  getStatus() { return api.get('/status') },
  drink(amount) { return api.post('/drink', { amount }) },
  reset() { return api.post('/reset') },
  updateSettings(payload) { return api.post('/settings', payload) }
}
