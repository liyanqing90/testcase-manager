<script setup>
import { ref, provide, computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import UploadCase from './views/UploadCase.vue';
import ManageCase from './views/ManageCase.vue';
import AiGenerateCase from './views/AiGenerateCase.vue';

const router = useRouter();
const route = useRoute();

const sidebarCollapsed = ref(false);
const sidebarDisabled = ref(false);

// 创建响应式的项目删除事件
const projectDeletedEvent = ref(null);

// 提供事件给子组件
provide('projectDeletedEvent', projectDeletedEvent);

// 根据当前路由计算当前tab
const tab = computed(() => {
  const path = route.path;
  if (path === '/upload') {
    return 'upload';
  }
  if (path === '/ai-generate') {
    return 'ai-generate';
  }
  return 'manage'; // 默认为manage，包括 /manage 和 /
});

// 处理项目删除事件
const handleProjectDeleted = (projectId) => {
  projectDeletedEvent.value = projectId;
};

// 切换侧边栏状态
const toggleSidebar = () => {
  if (!sidebarDisabled.value) {
    sidebarCollapsed.value = !sidebarCollapsed.value;
  }
};

// 处理侧边栏禁用状态
const handleSidebarDisabled = (disabled) => {
  sidebarDisabled.value = disabled;
};

// 处理tab选择
const handleTabSelect = (selectedTab) => {
  if (!sidebarDisabled.value) {
    if (selectedTab === 'upload') {
      router.push('/upload');
    } else if (selectedTab === 'ai-generate') {
      router.push('/ai-generate');
    } else {
      router.push('/manage');
    }
  }
};

// 监听路由变化，自动恢复侧边栏状态
watch(() => route.path, (newPath) => {
  // 当路由变化时，自动恢复侧边栏状态
  sidebarDisabled.value = false;
});
</script>

<template>
  <el-container style="height: 100vh; width: 100vw; margin: 0; padding: 0;">
    <!-- 美化后的侧边栏 -->
    <el-aside :width="sidebarCollapsed ? '80px' : '240px'" class="sidebar" :class="{ 'collapsed': sidebarCollapsed, 'disabled': sidebarDisabled }">
      <!-- Logo区域 -->
      <div class="sidebar-header">
        <div class="logo-container" :class="{ 'collapsed': sidebarCollapsed }">
          <div class="logo-icon">
            <img src="/src/icon/边牧.png" alt="Logo" />
          </div>
          <div class="logo-text" v-show="!sidebarCollapsed">
            <h1>AIsystem</h1>
            <p>Case Manager</p>
          </div>
        </div>
      </div>

      <!-- 导航菜单 -->
      <div class="sidebar-menu">
        <el-menu 
          :default-active="tab" 
          class="custom-menu" 
          background-color="transparent" 
          text-color="#E2E8F0" 
          active-text-color="#60A5FA"
          @select="handleTabSelect"
          :disabled="sidebarDisabled"
        >
          <el-menu-item index="manage" class="menu-item">
            <div class="menu-item-content">
              <div class="menu-icon">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M19 11H5M19 11C20.1046 11 21 11.8954 21 13V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V13C3 11.8954 3.89543 11 5 11M19 11V9C19 7.89543 18.1046 7 17 7M5 11V9C5 7.89543 5.89543 7 7 7M7 7V5C7 3.89543 7.89543 3 9 3H15C16.1046 3 17 3.89543 17 5V7M7 7H17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <span v-show="!sidebarCollapsed">项目用例管理</span>
            </div>
          </el-menu-item>
          
          <el-menu-item index="upload" class="menu-item">
            <div class="menu-item-content">
              <div class="menu-icon">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15M17 8L12 3M12 3L7 8M12 3V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <span v-show="!sidebarCollapsed">用例上传</span>
            </div>
          </el-menu-item>

          <el-menu-item index="ai-generate" class="menu-item">
            <div class="menu-item-content">
              <div class="menu-icon">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <rect x="4" y="8" width="16" height="10" rx="4" stroke="currentColor" stroke-width="2"/>
                  <rect x="9" y="2" width="6" height="4" rx="2" stroke="currentColor" stroke-width="2"/>
                  <circle cx="8.5" cy="13.5" r="1.5" fill="currentColor"/>
                  <circle cx="15.5" cy="13.5" r="1.5" fill="currentColor"/>
                  <path d="M12 18v2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </div>
              <span v-show="!sidebarCollapsed">AI生成用例</span>
            </div>
          </el-menu-item>
      </el-menu>
      </div>

      <!-- 底部信息 -->
      <div class="sidebar-footer">
        <div class="footer-info">
          <!-- 可以在这里添加其他信息 -->
        </div>
      </div>
      
      <!-- 收缩按钮 -->
      <div class="sidebar-toggle" @click="toggleSidebar">
        <div class="toggle-button">
          <svg v-if="!sidebarCollapsed" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
      </div>
    </el-aside>

          <!-- 主内容区域 -->
    <el-container>
        <el-header height="80px" class="main-header">
          <div class="header-content">
            <div class="breadcrumb-container">
              <div class="breadcrumb">
                <span class="breadcrumb-item">首页</span>
                <span class="breadcrumb-separator">/</span>
                <transition name="fade" mode="out-in">
                  <span class="breadcrumb-item active" :key="tab">
                    {{ tab==='upload' ? '用例上传' : tab==='ai-generate' ? 'AI生成用例' : '项目用例管理' }}
                  </span>
                </transition>
              </div>
            </div>
          </div>
      </el-header>
      
      <el-main class="main-content">
        <UploadCase v-if="tab==='upload'" />
        <AiGenerateCase v-else-if="tab==='ai-generate'" />
        <ManageCase v-else @project-deleted="handleProjectDeleted" @sidebar-disabled="handleSidebarDisabled" />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
/* 侧边栏样式 */
.sidebar {
  background: linear-gradient(180deg, #0ea5e9 0%, #38bdf8 50%, #7dd3fc 100%);
  box-shadow: 4px 0 20px rgba(14, 165, 233, 0.2);
  position: relative;
  overflow: visible;
  z-index: 10;
  border-top-right-radius: 12px;
  border-bottom-right-radius: 12px;
}

.sidebar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.03) 100%);
  pointer-events: none;
}

/* Logo区域 */
.sidebar-header {
  padding: 32px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 16px;
  width: 100%;
}

.logo-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.logo-icon svg {
  width: 24px;
  height: 24px;
}

.logo-icon img {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  object-fit: cover;
}

.logo-text h1 {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: white;
  line-height: 1.2;
  transition: opacity 0.3s ease;
  font-family: 'PingFang SC', 'Helvetica Neue', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif !important;
}

.logo-text p {
  margin: 4px 0 0 0;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 400;
  transition: opacity 0.3s ease;
  font-family: 'PingFang SC', 'Helvetica Neue', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif !important;
}

/* 菜单区域 */
.sidebar-menu {
  padding: 24px 0;
  flex: 1;
}

.custom-menu {
  border: none;
  background: transparent;
}

.menu-item {
  margin: 8px 16px;
  border-radius: 12px;
  height: 56px;
  transition: all 0.3s ease;
}

.menu-item:hover {
  background: rgba(255, 255, 255, 0.8) !important;
  transform: translateX(4px);
}

.menu-item.is-active {
  background: rgba(255, 255, 255, 0.95) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.menu-item-content {
  display: flex;
  align-items: center;
  gap: 16px;
  height: 100%;
  width: 100%;
}

.menu-item-content span {
  transition: opacity 0.3s ease;
  font-weight: 600 !important;
  font-size: 15px !important;
  font-family: 'PingFang SC', 'Helvetica Neue', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif !important;
}

.menu-icon {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.menu-icon svg {
  width: 18px;
  height: 18px;
}

/* 底部信息 */
.sidebar-footer {
  padding: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* 收缩按钮 */
.sidebar-toggle {
  position: absolute;
  top: 50%;
  right: -16px;
  transform: translateY(-50%);
  z-index: 9999;
}

.toggle-button {
  width: 32px;
  height: 32px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6B7280;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
  border: 2px solid #E5E7EB;
}

.toggle-button:hover {
  background: #F3F4F6;
  color: #374151;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transform: scale(1.05);
}

.toggle-button svg {
  width: 16px;
  height: 16px;
  transition: transform 0.3s ease;
}

/* 侧边栏动画 */
.sidebar {
  transition: width 0.3s ease;
}

/* 收缩状态样式 */
.sidebar.collapsed .logo-container {
  justify-content: center;
  align-items: center;
  padding: 0;
  width: 100%;
}

.sidebar.collapsed .logo-icon {
  margin: 0;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sidebar.collapsed .logo-icon svg {
  width: 18px;
  height: 18px;
}

.sidebar.collapsed .logo-icon img {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  object-fit: cover;
}

.sidebar.collapsed .menu-item-content {
  justify-content: center;
  align-items: center;
  padding: 0;
  width: 100%;
}

.sidebar.collapsed .menu-icon {
  margin: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sidebar.collapsed .menu-icon svg {
  width: 16px;
  height: 16px;
}

.sidebar.collapsed .sidebar-header {
  padding: 24px 0;
}

.sidebar.collapsed .sidebar-menu {
  padding: 16px 0;
}

.sidebar.collapsed .sidebar-footer {
  padding: 16px 0;
}

/* 主内容区域 */
.main-header {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  padding: 0 40px;
  position: relative;
  z-index: 1;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  height: 100%;
  padding-left: 0;
}

/* 面包屑导航区域 */
.breadcrumb-container {
  display: flex;
  align-items: center;
  margin-left: -40px;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  position: relative;
  min-height: 24px;
}

/* 面包屑导航 */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  position: relative;
  min-height: 24px;
}

.breadcrumb-item {
  font-size: 16px;
  color: #6B7280;
  font-weight: 500;
  transition: color 0.3s ease;
  font-family: 'PingFang SC', 'Helvetica Neue', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  display: flex;
  align-items: center;
  height: 1.2em;
  line-height: 1.2;
}

.breadcrumb-item.active {
  color: #1F2937;
  font-weight: 600;
  position: relative;
  min-width: 80px;
  display: flex;
  align-items: center;
  height: 1.2em;
  line-height: 1.2;
}

.breadcrumb-separator {
  color: #9CA3AF;
  font-size: 14px;
  font-weight: 400;
  display: flex;
  align-items: center;
  height: 1.2em;
  line-height: 1.2;
}

/* 淡入淡出动画 */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  height: 1.2em;
  line-height: 1.2;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(-15px) scale(0.95);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(15px) scale(0.95);
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
  transform: translateY(0) scale(1);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.main-content {
  background: #e2e8f0;
  padding: 32px 40px;
  height: calc(100vh - 70px);
  overflow: auto;
  position: relative;
  z-index: 1;
}

/* 全局样式 */
:deep(.el-menu-item) {
  color: #e0f2fe !important;
  font-weight: 700 !important;
  font-family: 'PingFang SC', 'Helvetica Neue', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif !important;
}

:deep(.el-menu-item.is-active) {
  color: #1f2937 !important;
  font-weight: 800 !important;
  font-family: 'PingFang SC', 'Helvetica Neue', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif !important;
}

:deep(.el-menu-item:hover) {
  color: #1f2937 !important;
  font-weight: 700 !important;
  font-family: 'PingFang SC', 'Helvetica Neue', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif !important;
}

/* 禁用状态样式 */
.sidebar.disabled {
  position: relative;
}

.sidebar.disabled::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  z-index: 100;
  pointer-events: none;
}

:deep(.el-menu.is-disabled) {
  opacity: 0.6;
  pointer-events: none;
}

:deep(.el-menu.is-disabled .el-menu-item) {
  color: #9CA3AF !important;
  background: transparent !important;
}

:deep(.el-menu.is-disabled .el-menu-item:hover) {
  color: #9CA3AF !important;
  background: transparent !important;
}

:deep(.el-menu.is-disabled .el-menu-item.is-active) {
  color: #9CA3AF !important;
  background: transparent !important;
}

/* 禁用状态下的收缩按钮 */
.sidebar.disabled .sidebar-toggle {
  opacity: 0.6;
  pointer-events: none;
}

.sidebar.disabled .toggle-button {
  opacity: 0.3;
  pointer-events: none;
  background: rgba(0, 0, 0, 0.3);
  color: rgba(255, 255, 255, 0.5);
  border-color: rgba(255, 255, 255, 0.2);
}

.sidebar.disabled .toggle-button:hover {
  background: rgba(0, 0, 0, 0.3);
  color: rgba(255, 255, 255, 0.5);
  transform: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 禁用状态下的菜单项 */
.sidebar.disabled .menu-item {
  pointer-events: none;
}

.sidebar.disabled .menu-item:hover {
  background: transparent !important;
  transform: none !important;
}

.sidebar.disabled .menu-item.is-active {
  background: transparent !important;
}
</style>

<style>
html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #F1F5F9;
}

::-webkit-scrollbar-thumb {
  background: #CBD5E1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94A3B8;
}
</style>