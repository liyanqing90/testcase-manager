<template>
  <div class="logs-view-container">
    <div class="logs-content">
      <div class="placeholder-content">
        <div class="placeholder-icon">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M14 2V8H20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M16 13H8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M16 17H8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M10 9H9H8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h3>运行日志模块</h3>
        <p>此模块正在开发中，将提供以下功能：</p>
        <ul class="feature-list">
          <li>系统运行日志查看</li>
          <li>AI测试用例生成记录</li>
          <li>错误日志分析</li>
          <li>性能监控数据</li>
        </ul>
        <p class="coming-soon">敬请期待...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
// 运行日志视图组件
// 目前作为占位符，后续将实现完整的日志功能
</script>

<style scoped>
.logs-view-container {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.logs-content {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  padding: 40px;
  margin-top: 20px;
}

.placeholder-content {
  text-align: center;
}

.placeholder-icon {
  margin-bottom: 24px;
}

.placeholder-icon svg {
  width: 64px;
  height: 64px;
  color: #94a3b8;
}

.placeholder-content h3 {
  font-size: 24px;
  font-weight: 600;
  color: #334155;
  margin: 0 0 16px 0;
}

.placeholder-content p {
  font-size: 16px;
  color: #64748b;
  margin: 0 0 20px 0;
}

.feature-list {
  text-align: left;
  max-width: 400px;
  margin: 0 auto 24px auto;
  padding: 0;
  list-style: none;
}

.feature-list li {
  padding: 8px 0;
  color: #475569;
  position: relative;
  padding-left: 24px;
}

.feature-list li::before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #10b981;
  font-weight: bold;
}

.coming-soon {
  font-size: 18px;
  font-weight: 500;
  color: #f59e0b;
  font-style: italic;
}
</style> 