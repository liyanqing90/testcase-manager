<template>
  <div class="format-transform-container">
    <div class="empty-page">
      <div class="empty-icon">
        <el-icon><Switch /></el-icon>
      </div>
      <h2>格式转换</h2>
      <p>格式转换功能开发中...</p>
    </div>
  </div>
</template>

<script setup>
import { Switch } from '@element-plus/icons-vue';
</script>

<style scoped>
.format-transform-container {
  padding: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.empty-page {
  text-align: center;
  padding: 60px 20px;
  color: #94a3b8;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 24px;
  color: #cbd5e1;
}

.empty-page h2 {
  margin: 0 0 16px 0;
  font-size: 24px;
  font-weight: 600;
  color: #64748b;
}

.empty-page p {
  margin: 0;
  font-size: 16px;
  color: #94a3b8;
}
</style> 