<template>
  <el-dialog
    :model-value="visible"
    width="900px"
    class="case-compare-dialog"
    :close-on-click-modal="false"
    :show-close="true"
    @close="$emit('update:visible', false)"
  >
    <template #header>
      <div class="detail-dialog-header">
        <h3 class="detail-dialog-title">重复用例对比</h3>
      </div>
    </template>
    <div class="compare-body" :class="{ 'completed-mode': groupCompleted }">
      <!-- 对比模式：显示两个用例 -->
      <template v-if="!groupCompleted">
        <el-card class="case-side case-card">
          <div class="case-form-container">
            <el-form label-width="110px" v-if="caseA">
            <el-form-item label="基本信息:">
              <div class="form-item-content">
                <div class="basic-info-row">
                  <div class="info-item">
                    <span class="info-label">用例ID:</span>
                    <span class="info-value case-id-value">{{ caseA.case_id }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">优先级:</span>
                    <el-tag :type="getPriorityType(caseA.priority)" class="priority-tag" size="small">
                      {{ caseA.priority || '未设置' }}
                    </el-tag>
                  </div>
                  <div class="info-item">
                    <span class="info-label">分类:</span>
                    <span class="info-value">{{ caseA.category || '无' }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">状态:</span>
                    <el-tag :type="getStatusType(caseA.status)" class="status-tag" size="small">
                      {{ getStatusDisplay(caseA.status) }}
                    </el-tag>
                  </div>
                </div>
              </div>
            </el-form-item>
            <el-form-item label="用例标题:"><div class="form-item-content">{{ caseA.title }}</div></el-form-item>
            <el-form-item label="用例描述:"><div class="form-item-content">{{ caseA.description || '无' }}</div></el-form-item>
            <el-form-item label="前置条件:"><div class="form-item-content">{{ caseA.preconditions || '无' }}</div></el-form-item>
            <el-form-item label="操作步骤:"><div class="form-item-content">{{ caseA.steps || '无' }}</div></el-form-item>
                        <el-form-item label="预期结果:"><div class="form-item-content">{{ caseA.expected_results || '无' }}</div></el-form-item>
            </el-form>
          </div>
          </el-card>
        <!-- 分割线已移除 -->
        <el-card class="case-side case-card">
          <div class="case-form-container">
            <el-form label-width="110px" v-if="caseB">
            <el-form-item label="基本信息:">
              <div class="form-item-content">
                <div class="basic-info-row">
                  <div class="info-item">
                    <span class="info-label">用例ID:</span>
                    <span class="info-value case-id-value">{{ caseB.case_id }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">优先级:</span>
                    <el-tag :type="getPriorityType(caseB.priority)" class="priority-tag" size="small">
                      {{ caseB.priority || '未设置' }}
                    </el-tag>
                  </div>
                  <div class="info-item">
                    <span class="info-label">分类:</span>
                    <span class="info-value">{{ caseB.category || '无' }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">状态:</span>
                    <el-tag :type="getStatusType(caseB.status)" class="status-tag" size="small">
                      {{ getStatusDisplay(caseB.status) }}
                    </el-tag>
                  </div>
                </div>
              </div>
            </el-form-item>
            <el-form-item label="用例标题:"><div class="form-item-content">{{ caseB.title }}</div></el-form-item>
            <el-form-item label="用例描述:"><div class="form-item-content">{{ caseB.description || '无' }}</div></el-form-item>
            <el-form-item label="前置条件:"><div class="form-item-content">{{ caseB.preconditions || '无' }}</div></el-form-item>
            <el-form-item label="操作步骤:"><div class="form-item-content">{{ caseB.steps || '无' }}</div></el-form-item>
                        <el-form-item label="预期结果:"><div class="form-item-content">{{ caseB.expected_results || '无' }}</div></el-form-item>
            </el-form>
          </div>
          </el-card>
      </template>
      
      <!-- 完成模式：只显示保留的用例 -->
      <template v-else>
        <el-card class="case-side case-card completed-case-card">
          <div class="case-form-container">
            <el-form label-width="110px" v-if="finalCase">
            <el-form-item label="基本信息:">
              <div class="form-item-content">
                <div class="basic-info-row">
                  <div class="info-item">
                    <span class="info-label">用例ID:</span>
                    <span class="info-value case-id-value">{{ finalCase.case_id }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">优先级:</span>
                    <el-tag :type="getPriorityType(finalCase.priority)" class="priority-tag" size="small">
                      {{ finalCase.priority || '未设置' }}
                    </el-tag>
                  </div>
                  <div class="info-item">
                    <span class="info-label">分类:</span>
                    <span class="info-value">{{ finalCase.category || '无' }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">状态:</span>
                    <el-tag :type="getStatusType(finalCase.status)" class="status-tag" size="small">
                      {{ getStatusDisplay(finalCase.status) }}
                    </el-tag>
                  </div>
                </div>
              </div>
            </el-form-item>
            <el-form-item label="用例标题:"><div class="form-item-content">{{ finalCase.title }}</div></el-form-item>
            <el-form-item label="用例描述:"><div class="form-item-content">{{ finalCase.description || '无' }}</div></el-form-item>
            <el-form-item label="前置条件:"><div class="form-item-content">{{ finalCase.preconditions || '无' }}</div></el-form-item>
            <el-form-item label="操作步骤:"><div class="form-item-content">{{ finalCase.steps || '无' }}</div></el-form-item>
                        <el-form-item label="预期结果:"><div class="form-item-content">{{ finalCase.expected_results || '无' }}</div></el-form-item>
            </el-form>
          </div>
          </el-card>
      </template>
    </div>
    <div class="compare-actions">
      <div class="compare-main-actions">
        <el-button type="primary" @click="$emit('keep', 'A')" :disabled="groupCompleted">保留左侧用例</el-button>
        <el-button type="primary" @click="$emit('keep', 'B')" :disabled="groupCompleted">保留右侧用例</el-button>
      </div>
      
      <!-- 导航按钮区域 -->
      <div class="compare-navigation">
        <div 
          v-if="canGoPrevious"
          class="nav-area nav-left"
          @click="$emit('previous')"
        >
          <div class="nav-arrow">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </div>
        
        <div class="case-counter">
          第 {{ currentIndex + 1 }} / {{ totalCount }} 组
        </div>
        
        <div 
          v-if="canGoNext"
          class="nav-area nav-right"
          @click="$emit('next')"
        >
          <div class="nav-arrow">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  visible: Boolean,
  caseA: Object,
  caseB: Object,
  currentIndex: Number,
  totalCount: Number,
  canGoPrevious: Boolean,
  canGoNext: Boolean,
  currentGroupId: String,
  groupCompleted: Boolean
});
const emit = defineEmits(['update:visible', 'keep', 'previous', 'next']);

// 计算最终保留的用例
const finalCase = computed(() => {
  // 当对比完成时，返回当前显示的用例（通常是保留的用例）
  // 这里假设caseA是当前保留的用例，如果需要更复杂的逻辑可以进一步调整
  return props.caseA || props.caseB;
});

function getPriorityType(priority) {
  const priorityMap = {
    'P0': 'danger',
    'P1': 'warning',
    'P2': 'info',
    'P3': 'success'
  };
  return priorityMap[priority] || 'info';
}
function getStatusType(status) {
  const statusMap = {
    '通过': 'success',
    '失败': 'danger',
    '阻塞': 'warning',
    '跳过': 'info',
    '待执行': 'info',
    '执行中': 'warning',
    'Draft': 'info',
    '未完成': 'info',
    'success': 'success',
    'failed': 'danger',
    'blocked': 'warning',
    'skipped': 'info',
    'pending': 'info',
    'running': 'warning'
  };
  return statusMap[status] || 'info';
}
function getStatusDisplay(status) {
  if (!status) return '未设置';
  
  const statusDisplayMap = {
    'Draft': '未完成',
    'draft': '未完成',
    'success': '已完成',
    'failed': '失败',
    'blocked': '阻塞',
    'skipped': '跳过',
    'pending': '待执行',
    'running': '执行中'
  };
  
  return statusDisplayMap[status] || status;
}
</script>

<style scoped>
:deep(.case-compare-dialog .el-dialog__body) {
  padding: 24px 20px 12px 20px;
  background: #d1d5db !important;
}
:deep(.case-compare-dialog .el-dialog) {
  background: #d1d5db !important;
}
.detail-dialog-header {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding: 0;
  margin: 0;
}
.detail-dialog-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  text-align: center;
  font-family: 'PingFang SC', 'Helvetica Neue', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  line-height: 1.2;
  padding: 0;
}

.dialog-subtitle {
  margin: 4px 0 0 0;
  font-size: 14px;
  font-weight: 400;
  color: #6b7280;
  text-align: center;
  font-family: 'PingFang SC', 'Helvetica Neue', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  line-height: 1.2;
  padding: 0;
}
.compare-body {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
  height: 500px; /* 固定高度 */
}
.case-side {
  flex: 1;
  min-width: 0;
  background: none;
  box-shadow: none;
  padding: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
}
.case-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  background: #fff;
  padding: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.case-form-container {
  flex: 1;
  overflow-y: auto !important;
  padding: 20px;
  max-height: 100%;
  min-height: 0; /* 确保flex子元素可以收缩 */
  /* 隐藏滚动条 */
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}

.case-form-container::-webkit-scrollbar {
  display: none; /* Chrome, Safari and Opera */
}

/* 确保Element Plus的表单样式不会影响滚动 */
:deep(.case-form-container .el-form) {
  height: auto;
  overflow: visible;
}

:deep(.case-form-container .el-form-item) {
  margin-bottom: 16px;
}

/* 确保el-card不会影响滚动 */
:deep(.case-card .el-card__body) {
  height: 100%;
  padding: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
/* .compare-divider 已移除 */
.compare-actions {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 18px;
}

.compare-main-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.compare-navigation {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 8px;
}

.nav-area {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 8px;
}

.nav-area:hover {
  /* 移除背景色，只保留箭头按钮的悬停效果 */
}

.nav-arrow {
  width: 40px;
  height: 40px;
  background: #3b82f6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
  transition: all 0.3s ease;
}

.nav-arrow svg {
  width: 20px;
  height: 20px;
  color: white;
  transition: all 0.3s ease;
}

.nav-area:hover .nav-arrow,
.nav-area:active .nav-arrow {
  background: #dc2626;
  box-shadow: 0 6px 16px rgba(220, 38, 38, 0.3);
  transform: scale(1.1);
}

.nav-area:hover .nav-arrow svg,
.nav-area:active .nav-arrow svg {
  color: white;
}

.case-counter {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
  padding: 8px 16px;
  background: #f9fafb;
  border-radius: 20px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  min-width: 80px;
  text-align: center;
}
.form-item-content {
  min-height: 20px;
  line-height: 1.5;
  white-space: pre-line;
  word-break: break-word;
  padding: 4px 0;
  color: #374151;
  font-size: 14px;
}
.basic-info-row {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  align-items: center;
}
.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 120px;
}
.info-label {
  font-weight: 500;
  color: #6b7280;
  font-size: 14px;
  white-space: nowrap;
}

/* 完成模式样式 */
.compare-body.completed-mode {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  width: 100%;
}

.completed-case-card {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

/* 确保完成模式下的滚动逻辑与对比模式一致 */
.completed-mode .case-form-container {
  flex: 1;
  overflow-y: auto !important;
  padding: 20px;
  max-height: 100%;
  min-height: 0;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.completed-mode .case-form-container::-webkit-scrollbar {
  display: none;
}
.info-value {
  color: #374151;
  font-size: 14px;
  font-weight: 500;
}

/* 用例ID特殊样式 - 使用圆润字体 */
.case-id-value {
  font-family: 'PingFang SC', 'Helvetica Neue', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', 'Segoe UI', 'Roboto', sans-serif;
  font-weight: 600;
  letter-spacing: 0.5px;
  color: #1f2937;
}

/* 标签样式 */
.priority-tag, .status-tag {
  font-weight: 500;
  border-radius: 6px;
}

/* 优先级标签自定义颜色 */
.priority-tag.el-tag--danger {
  background-color: #dc2626 !important;
  border-color: #dc2626 !important;
  color: white !important;
}

.priority-tag.el-tag--warning {
  background-color: #d97706 !important;
  border-color: #d97706 !important;
  color: white !important;
}

.priority-tag.el-tag--info {
  background-color: #0891b2 !important;
  border-color: #0891b2 !important;
  color: white !important;
}

.priority-tag.el-tag--success {
  background-color: #059669 !important;
  border-color: #059669 !important;
  color: white !important;
}

/* 状态标签自定义颜色 - 加深背景 */
.status-tag.el-tag--success {
  background-color: #047857 !important;
  border-color: #047857 !important;
  color: white !important;
}

.status-tag.el-tag--danger {
  background-color: #dc2626 !important;
  border-color: #dc2626 !important;
  color: white !important;
}

.status-tag.el-tag--warning {
  background-color: #d97706 !important;
  border-color: #d97706 !important;
  color: white !important;
}

.status-tag.el-tag--info {
  background-color: #0369a1 !important;
  border-color: #0369a1 !important;
  color: white !important;
}
</style> 