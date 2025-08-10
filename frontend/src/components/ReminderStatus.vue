<template>
  <div>
    <p>提醒功能运行中…</p>
    <button @click="testNotification">测试通知功能</button>
  </div>
</template>

<script setup>
function testNotification() {
  if (!("Notification" in window)) {
    alert("浏览器不支持通知");
    return;
  }
  Notification.requestPermission().then(permission => {
    console.log("通知权限状态:", permission);
    if (permission === "granted") {
      new Notification("测试通知", { body: "这是测试消息" });
    } else {
      alert("请允许通知权限！");
    }
  });
}
</script>
