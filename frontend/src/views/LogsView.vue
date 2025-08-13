<template>
  <el-config-provider :locale="locale">
    <div class="logs-view">
    <!-- 日志条件过滤筛选区域 -->
    <div class="logs-filter-section">
      <el-card class="filter-card" shadow="hover">
        <template #header>
          <div class="filter-header">
            <el-icon><Filter /></el-icon>
            <span>日志筛选条件</span>
          </div>
        </template>
        
        <el-form :model="filterForm" :inline="true" class="filter-form">
          <!-- 日志级别筛选 -->
          <el-form-item label="日志级别：">
            <el-select 
              v-model="filterForm.level" 
              placeholder="请选择日志级别"
              clearable
              style="width: 120px"
            >
              <el-option label="INFO" value="INFO" />
              <el-option label="WARNING" value="WARNING" />
              <el-option label="ERROR" value="ERROR" />
              <el-option label="DEBUG" value="DEBUG" />
            </el-select>
          </el-form-item>
          
          <!-- 时间范围筛选 -->
          <el-form-item label="时间范围：">
            <el-date-picker
              v-model="filterForm.timeRange"
              type="datetimerange"
              range-separator="至"
              start-placeholder="开始时间"
              end-placeholder="结束时间"
              format="YYYY-MM-DD HH:mm:ss"
              value-format="YYYY-MM-DD HH:mm:ss"
              :locale="locale"
              style="width: 320px"
            />
          </el-form-item>
          
          <!-- 关键词筛选 -->
          <el-form-item label="关键词：">
            <el-input
              v-model="filterForm.keyword"
              placeholder="请输入搜索关键词"
              clearable
              style="width: 200px"
            />
          </el-form-item>
          
          <!-- 功能按钮 -->
          <el-form-item>
            <el-button type="primary" @click="handleSearch" :icon="Search">
              搜索
            </el-button>
            <el-button @click="handleReset" :icon="Refresh">
              重置
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
    
    <!-- 日志数据统计区域 -->
    <div class="logs-statistics-section">
      <el-card class="statistics-card" shadow="hover">
        <template #header>
          <div class="statistics-header">
            <el-icon><DataAnalysis /></el-icon>
            <span>日志数据统计</span>
          </div>
        </template>
        
        <div class="statistics-grid">
          <!-- 日志总数 -->
          <div class="stat-item total-item">
            <div class="stat-icon total-icon">
              <el-icon><Document /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ statistics.total }}</div>
              <div class="stat-label">日志总数</div>
            </div>
          </div>
          
          <!-- INFO总数 -->
          <div class="stat-item info-item">
            <div class="stat-icon info-icon">
              <el-icon><InfoFilled /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ statistics.info }}</div>
              <div class="stat-label">INFO总数</div>
            </div>
          </div>
          
          <!-- WARNING总数 -->
          <div class="stat-item warning-item">
            <div class="stat-icon warning-icon">
              <el-icon><WarningFilled /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ statistics.warning }}</div>
              <div class="stat-label">WARNING总数</div>
            </div>
          </div>
          
          <!-- ERROR总数 -->
          <div class="stat-item error-item">
            <div class="stat-icon error-icon">
              <el-icon><CircleCloseFilled /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ statistics.error }}</div>
              <div class="stat-label">ERROR总数</div>
            </div>
          </div>
          
          <!-- DEBUG总数 -->
          <div class="stat-item debug-item">
            <div class="stat-icon debug-icon">
              <el-icon><Tools /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">{{ statistics.debug }}</div>
              <div class="stat-label">DEBUG总数</div>
            </div>
          </div>
        </div>
      </el-card>
    </div>
    
    <!-- 实时日志监控区域 -->
    <div class="logs-monitor-section">
      <el-card class="monitor-card" shadow="hover">
        <template #header>
          <div class="monitor-header">
            <div class="monitor-title">
              <el-icon><Monitor /></el-icon>
              <span>实时日志监控</span>
              <!-- 连接状态指示器 -->
              <div class="connection-status">
                <el-tag 
                  :type="connectionStatus === 'connected' ? 'success' : 
                         connectionStatus === 'connecting' ? 'warning' : 
                         connectionStatus === 'error' ? 'danger' : 'info'"
                  size="small"
                >
                  <el-icon class="el-icon--left">
                    <Monitor v-if="connectionStatus === 'connected'" />
                    <div v-else-if="connectionStatus === 'connecting'" class="custom-loading">
                      <div class="loading-spinner"></div>
                    </div>
                    <WarningFilled v-else-if="connectionStatus === 'error'" />
                    <InfoFilled v-else />
                  </el-icon>
                  {{ connectionStatus === 'connected' ? '已连接' : 
                     connectionStatus === 'connecting' ? '连接中' : 
                     connectionStatus === 'error' ? '连接错误' : '未连接' }}
                </el-tag>
              </div>
            </div>
            <div class="monitor-controls">
              <div class="control-card">
                <el-switch
                  v-model="autoScroll"
                  active-text="自动滚动"
                  inactive-text="手动滚动"
                  size="small"
                />
              </div>
              <div class="clear-button-card">
                <el-button 
                  type="danger" 
                  size="small" 
                  @click="handleClearLogs"
                  :icon="Delete"
                  class="clear-button"
                >
                  清空日志
                </el-button>
              </div>
            </div>
          </div>
        </template>
        
        <div class="logs-content-container">
          <!-- 日志内容区域 -->
          <div 
            ref="logsContentRef"
            class="logs-content"
            :class="{ 'auto-scroll': autoScroll }"
            @scroll="handleScroll"
          >
            <div v-if="logs.length === 0" class="empty-logs">
              <el-icon><Document /></el-icon>
              <p>暂无日志内容</p>
              <p class="empty-tip">日志内容将在这里实时显示</p>
            </div>
            
            <div v-else class="logs-list">
              <div 
                v-for="(log, index) in logs" 
                :key="index"
                class="log-item"
                :class="getLogLevelClass(log.level)"
              >
                <div class="log-level">
                  <el-tag 
                    :type="getLogLevelTagType(log.level)" 
                    size="small"
                  >
                    {{ log.level }}
                  </el-tag>
                </div>
                <div class="log-timestamp">{{ log.timestamp }}</div>
                <div class="log-agent">{{ log.agent }}</div>
                <div class="log-message">{{ log.message }}</div>
              </div>
            </div>
          </div>
          
          <!-- 滚动控制按钮 -->
          <div v-if="!autoScroll" class="scroll-controls">
            <!-- 滚动到顶部按钮 -->
            <el-button 
              type="info" 
              circle
              size="default" 
              @click="scrollToTop"
              :icon="ArrowUp"
              class="scroll-to-top"
            />
            <!-- 滚动到底部按钮 -->
            <el-button 
              type="primary" 
              circle
              size="default" 
              @click="scrollToBottom"
              :icon="ArrowDown"
              class="scroll-to-bottom"
            />
          </div>
      </div>
      </el-card>
    </div>
  </div>
</el-config-provider>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox, ElConfigProvider } from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn.mjs'
import { 
  Filter, 
  Search, 
  Refresh, 
  DataAnalysis, 
  Document, 
  InfoFilled, 
  WarningFilled, 
  CircleCloseFilled, 
  Tools,
  Monitor,
  Delete,
  ArrowDown,
  ArrowUp,
  Loading
} from '@element-plus/icons-vue'

// 筛选表单数据
const filterForm = reactive({
  level: '',           // 日志级别
  timeRange: null,     // 时间范围
  keyword: ''          // 关键词
})

// 统计数据
const statistics = reactive({
  total: 0,            // 日志总数
  info: 0,             // INFO总数
  warning: 0,          // WARNING总数
  error: 0,            // ERROR总数
  debug: 0             // DEBUG总数
})

// 更新统计数据
const updateStatistics = () => {
  const stats = {
    total: logs.value.length,
    info: 0,
    warning: 0,
    error: 0,
    debug: 0
  }
  
  for (const log of logs.value) {
    const level = log.level?.toUpperCase()
    if (level === 'INFO') {
      stats.info++
    } else if (level === 'WARNING') {
      stats.warning++
    } else if (level === 'ERROR') {
      stats.error++
    } else if (level === 'DEBUG') {
      stats.debug++
    }
  }
  
  Object.assign(statistics, stats)
}

// 中文语言配置
const locale = zhCn

// 实时日志监控相关
const logsContentRef = ref(null)
const autoScroll = ref(false)
const showScrollToBottom = ref(false)
const logs = ref([])
const connectionStatus = ref('disconnected') // 连接状态：disconnected, connecting, connected, error



// 搜索处理
const handleSearch = async () => {
  // 构建搜索条件
  const searchConditions = {
    level: filterForm.level,
    timeRange: filterForm.timeRange,
    keyword: filterForm.keyword.trim()
  }
  
  // 验证搜索条件
  if (!searchConditions.keyword && !searchConditions.level && !searchConditions.timeRange) {
    ElMessage.warning('请至少选择一个筛选条件')
    return
  }
  
  try {
    // 调用后端API进行日志筛选
    const params = new URLSearchParams()
    if (searchConditions.level) params.append('level', searchConditions.level)
    if (searchConditions.keyword) params.append('keyword', searchConditions.keyword)
    if (searchConditions.timeRange) {
      params.append('start_time', searchConditions.timeRange[0])
      params.append('end_time', searchConditions.timeRange[1])
    }
    
    const response = await fetch(`/logs/get_logs?${params.toString()}`)
    const data = await response.json()
    
    if (data.success) {
      logs.value = data.logs
      // 搜索时不更新统计数据，保持显示所有日志的统计
      ElMessage.success(`找到 ${data.logs.length} 条符合条件的日志`)
    } else {
      ElMessage.error(data.error || '搜索失败')
    }
  } catch (error) {
    console.error('搜索日志失败:', error)
    ElMessage.error('搜索失败，请稍后重试')
  }
}

// 重置处理
const handleReset = () => {
  filterForm.level = ''
  filterForm.timeRange = null
  filterForm.keyword = ''
  // 重新加载所有日志，统计数据会显示所有日志的统计
  loadInitialLogs()
  ElMessage.info('筛选条件已重置，日志级别已重置为"全部"')
}



const handleScroll = () => {
  // 滚动事件处理，现在主要用于记录滚动状态
  // 不再需要控制按钮显示逻辑
}

const scrollToTop = () => {
  const element = logsContentRef.value
  if (element) {
    element.scrollTo({
      top: 0,
      behavior: 'smooth'
    })
  }
}

const scrollToBottom = () => {
  const element = logsContentRef.value
  if (element) {
    element.scrollTo({
      top: element.scrollHeight,
      behavior: 'smooth'
    })
  }
}

const getLogLevelClass = (level) => {
  return `log-level-${level.toLowerCase()}`
}

const getLogLevelTagType = (level) => {
  const typeMap = {
    'INFO': 'primary',
    'WARNING': 'warning',
    'ERROR': 'danger',
    'DEBUG': 'success'
  }
  return typeMap[level] || 'primary'
}

// 实时日志监控相关
let eventSource = null

// 启动实时日志监控
const startRealTimeLogs = () => {
  try {
    // 关闭之前的连接
    if (eventSource) {
      eventSource.close()
    }
    
    // 创建新的SSE连接
    connectionStatus.value = 'connecting'
    eventSource = new EventSource('/logs/stream_logs')
    
    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        
        if (data.error) {
          console.error('日志流错误:', data.error)
          return
        }
        
        // 处理心跳消息
        if (data.heartbeat) {
          return
        }
        
        // 添加新日志
        logs.value.push(data)
        
        // 更新统计数据（反映所有日志的统计）
        updateStatistics()
        
        // 保持最多5000条日志
        if (logs.value.length > 5000) {
          logs.value.splice(0, logs.value.length - 5000)
        }
        
        // 自动滚动到底部
        if (autoScroll.value) {
          nextTick(() => {
            scrollToBottom()
          })
        }
      } catch (e) {
        console.error('解析日志数据失败:', e)
      }
    }
    
    eventSource.onerror = (error) => {
      console.error('SSE连接错误:', error)
      connectionStatus.value = 'error'
      
      // 检查连接状态
      if (eventSource.readyState === EventSource.CLOSED) {
        // 立即重连
        setTimeout(() => {
          startRealTimeLogs()
        }, 1000)
      } else if (eventSource.readyState === EventSource.CONNECTING) {
        connectionStatus.value = 'connecting'
      } else {
        // 等待一段时间后重连
        setTimeout(() => {
          if (eventSource && eventSource.readyState !== EventSource.OPEN) {
            startRealTimeLogs()
          }
        }, 3000)
      }
    }
    
    eventSource.onopen = () => {
      connectionStatus.value = 'connected'
      ElMessage.success('实时日志监控已启动')
    }
    
    eventSource.onclose = () => {
      connectionStatus.value = 'disconnected'
    }
    
  } catch (error) {
    console.error('启动实时日志失败:', error)
  }
}

// 停止实时日志监控
const stopRealTimeLogs = () => {
  if (eventSource) {
    eventSource.close()
    eventSource = null
  }
}

// 加载初始日志数据
const loadInitialLogs = async () => {
  try {
    const response = await fetch('/logs/get_logs')
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
    
    const data = await response.json()
    
    if (data.success) {
      logs.value = data.logs
      // 加载初始日志后，更新统计数据（显示所有日志的统计）
      updateStatistics()
    } else {
      console.error('加载日志失败:', data.error)
      ElMessage.error(`加载日志失败: ${data.error}`)
    }
  } catch (error) {
    console.error('请求日志失败:', error)
    ElMessage.error(`请求日志失败: ${error.message}`)
    
    // 如果是网络错误，尝试重试
    if (error.name === 'TypeError' || error.message.includes('fetch')) {
      setTimeout(() => {
        loadInitialLogs()
      }, 3000)
    }
  }
}

// 清空日志（调用后端API）
const handleClearLogs = async () => {
  try {
    const confirmed = await ElMessageBox.confirm(
      '确定要清空所有日志内容吗？此操作不可恢复。',
      '确认清空',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    if (confirmed) {
      const response = await fetch('/logs/clear_logs', {
        method: 'POST'
      })
      const data = await response.json()
      
      if (data.success) {
        logs.value = []
        // 清空日志后，统计数据应该为0
        updateStatistics()
        ElMessage.success('日志内容已清空')
      } else {
        ElMessage.error(data.error || '清空失败')
      }
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('清空日志失败')
    }
  }
}

// 页面加载时启动真实日志监控
onMounted(async () => {
  await loadInitialLogs()
  startRealTimeLogs()
})

// 页面卸载时清理连接
onUnmounted(() => {
  stopRealTimeLogs()
})
</script>

<style scoped>
.logs-view {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
  border-radius: 12px;
}

.logs-filter-section {
  margin-bottom: 20px;
}

.logs-statistics-section {
  margin-bottom: 20px;
}

.logs-monitor-section {
  margin-bottom: 20px;
}

.filter-card {
  border-radius: 8px;
}

.filter-header {
  display: flex;
  align-items: center;
  font-weight: 600;
  color: #303133;
}

.filter-header .el-icon {
  margin-right: 8px;
  color: #409eff;
}

.filter-form {
  margin-top: 10px;
}

.filter-form .el-form-item {
  margin-bottom: 16px;
  margin-right: 20px;
}

.filter-form .el-form-item__label {
  font-weight: 500;
  color: #606266;
}

.statistics-card {
  border-radius: 8px;
}

.statistics-header {
  display: flex;
  align-items: center;
  font-weight: 600;
  color: #303133;
}

.statistics-header .el-icon {
  margin-right: 8px;
  color: #409eff;
}

.statistics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 10px;
}

.stat-item {
  display: flex;
  align-items: center;
  padding: 20px;
  border-radius: 8px;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  transition: all 0.3s ease;
}

.stat-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  font-size: 24px;
}

.total-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.info-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.warning-icon {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  color: white;
}

.error-icon {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  color: white;
}

.debug-icon {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  color: #333;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 28px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #7f8c8d;
  font-weight: 500;
}

.monitor-card {
  border-radius: 8px;
}

.monitor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.monitor-title {
  display: flex;
  align-items: center;
  font-weight: 600;
  color: #303133;
}

.monitor-title .el-icon {
  margin-right: 8px;
  color: #409eff;
}

.monitor-title .connection-status {
  margin-left: 16px;
}

.monitor-title .connection-status .el-tag {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 4px;
  height: 24px;
  line-height: 24px;
  color: white !important;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

/* 自定义连接状态标签的背景色 */
.monitor-title .connection-status .el-tag--success {
  background: linear-gradient(135deg, #67c23a 0%, #4caf50 100%) !important;
  border-color: #67c23a !important;
}

.monitor-title .connection-status .el-tag--warning {
  background: linear-gradient(135deg, #e6a23c 0%, #ff9800 100%) !important;
  border-color: #e6a23c !important;
}

.monitor-title .connection-status .el-tag--danger {
  background: linear-gradient(135deg, #f56c6c 0%, #e74c3c 100%) !important;
  border-color: #f56c6c !important;
}

.monitor-title .connection-status .el-tag--info {
  background: linear-gradient(135deg, #909399 0%, #607d8b 100%) !important;
  border-color: #909399 !important;
}

/* 确保图标也是白色 */
.monitor-title .connection-status .el-tag .el-icon {
  color: white !important;
}

/* 统一所有图标大小和间距，并确保垂直居中 */
.monitor-title .connection-status .el-tag .el-icon--left {
  margin-right: 4px !important;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 14px;
  height: 14px;
}

.monitor-title .connection-status .el-tag .el-icon--left .el-icon {
  width: 14px;
  height: 14px;
  font-size: 14px;
}

/* 自定义Loading动画 - 视觉平衡 */
.monitor-title .connection-status .el-tag .custom-loading {
  width: 12px;
  height: 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  position: relative;
  flex-shrink: 0;
  margin: 0;
  padding: 0;
}

.monitor-title .connection-status .el-tag .loading-spinner {
  width: 12px;
  height: 12px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  flex-shrink: 0;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.monitor-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.control-card {
  background: linear-gradient(135deg, #ffffff 0%, #f5f5f5 100%);
  border-radius: 8px;
  padding: 8px 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #e4e7ed;
}

.control-card .el-switch {
  --el-switch-on-color: #409eff;
  --el-switch-off-color: #c0c4cc;
}

.control-card .el-switch__label {
  color: #606266 !important;
  font-weight: 500;
  font-family: 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Helvetica Neue', Arial, sans-serif;
  font-size: 13px;
  letter-spacing: 0.5px;
}

.clear-button-card {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  border-radius: 6px;
  padding: 2px;
  box-shadow: 0 2px 8px rgba(255, 107, 107, 0.3);
  border: 1px solid #ff6b6b;
  transition: all 0.3s ease;
}

.clear-button-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 107, 107, 0.4);
}

.clear-button-card .clear-button {
  background: transparent;
  border: none;
  color: white;
  font-weight: 500;
  font-family: 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Helvetica Neue', Arial, sans-serif;
  font-size: 11px;
  letter-spacing: 0.3px;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.clear-button-card .clear-button:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: scale(1.02);
}

.clear-button-card .clear-button:active {
  transform: scale(0.98);
}

.logs-content-container {
  position: relative;
  height: 500px;
}

.logs-content {
  height: 100%;
  overflow-y: auto;
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  background: #fafafa;
  padding: 16px;
  font-family: 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Helvetica Neue', Arial, sans-serif;
  font-size: 13px;
  line-height: 1.6;
}

.logs-content.auto-scroll {
  scroll-behavior: smooth;
}

.empty-logs {
  text-align: center;
  color: #909399;
  padding: 40px 20px;
}

.empty-logs .el-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty-tip {
  font-size: 12px;
  margin-top: 8px;
}

.logs-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.log-item {
  display: grid;
  grid-template-columns: 80px 140px 150px 1fr;
  gap: 12px;
  align-items: center;
  padding: 8px 12px;
  border-radius: 4px;
  background: white;
  border-left: 4px solid #e4e7ed;
  transition: background-color 0.2s ease;
}

.log-item:hover {
  background: #f5f7fa;
}

.log-item.log-level-info {
  border-left-color: transparent;
}

.log-item.log-level-warning {
  border-left-color: transparent;
}

.log-item.log-level-error {
  border-left-color: transparent;
}

.log-item.log-level-debug {
  border-left-color: transparent;
}

.log-timestamp {
  color: #606266;
  font-size: 12px;
  white-space: nowrap;
  font-weight: 600;
}

.log-level {
  text-align: center;
}

.log-agent {
  color: #909399;
  font-size: 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.log-message {
  color: #303133;
  word-break: break-word;
}

/* 滚动控制按钮样式 */
.scroll-controls {
  position: absolute;
  bottom: 20px;
  right: 20px;
  z-index: 10;
  display: flex;
  flex-direction: row;
  gap: 12px;
}

.scroll-to-top {
  box-shadow: 0 4px 12px rgba(144, 147, 153, 0.3);
  transition: all 0.3s ease;
}

.scroll-to-top:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(144, 147, 153, 0.4);
}

.scroll-to-bottom {
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
  transition: all 0.3s ease;
}

.scroll-to-bottom:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(64, 158, 255, 0.4);
}

/* 自定义日志级别标签样式 */
.log-level .el-tag {
  border-radius: 6px;
  font-weight: 700;
  font-size: 10px;
  padding: 6px 12px;
  border: none;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.12), 0 1px 3px rgba(0, 0, 0, 0.08);
  text-transform: uppercase;
  letter-spacing: 1px;
  width: 70px;
  height: 28px;
  text-align: center;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
}

.log-level .el-tag::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.log-level .el-tag:hover::before {
  left: 100%;
}

.log-level .el-tag--primary {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.log-level .el-tag--warning {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.log-level .el-tag--danger {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.log-level .el-tag--success {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  color: #2c3e50;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);
}

.log-level .el-tag:hover {
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15), 0 4px 10px rgba(0, 0, 0, 0.1);
  filter: brightness(1.1);
}

.log-level .el-tag:active {
  transform: translateY(0) scale(1.02);
  transition: all 0.1s ease;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .filter-form .el-form-item {
    margin-right: 15px;
  }
  
  .filter-form .el-date-picker {
    width: 280px !important;
  }
  
  .statistics-grid {
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
  }
  
  .logs-content-container {
    height: 400px;
  }
  
  .log-item {
    grid-template-columns: 70px 120px 120px 1fr;
    gap: 8px;
  }
}

@media (max-width: 768px) {
  .logs-view {
    padding: 15px;
  }
  
  .filter-form .el-form-item {
    margin-right: 10px;
    margin-bottom: 12px;
  }
  
  .filter-form .el-date-picker {
    width: 240px !important;
}

  .statistics-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .stat-item {
    padding: 16px;
  }
  
  .stat-number {
    font-size: 24px;
  }
  
  .logs-content-container {
    height: 350px;
  }
  
  .log-item {
    grid-template-columns: 1fr;
    gap: 4px;
    padding: 6px 8px;
  }
  
  .log-timestamp,
  .log-level,
  .log-agent {
    font-size: 11px;
  }
  
  .monitor-controls {
    flex-direction: column;
    gap: 8px;
  }
}
</style> 