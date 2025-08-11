<template>
  <div class="ai-generate-case-root">
    <div class="ai-generate-cards-row">
      <!-- 需求文档上传卡片 -->
      <el-card class="ai-generate-card ai-generate-upload-card" shadow="always">
        <div class="ai-generate-card-title">上传需求</div>
        <div class="ai-generate-upload-vertical">
          <el-upload
            :show-file-list="false"
            :before-upload="beforeUpload"
            accept=".pdf,.doc,.docx,.md,.txt"
            action="#"
            class="ai-generate-upload"
          >
            <el-button type="primary" class="ai-generate-upload-btn">
              <el-icon style="margin-right:6px;"><upload-filled /></el-icon>
              选择文件
            </el-button>
            <span v-if="fileName" class="ai-generate-filename-bubble">
              <el-icon style="margin-right:4px;"><document /></el-icon>{{ shortFileName }}
            </span>
          </el-upload>
          <div class="ai-generate-upload-tip">
            <el-icon style="color:#409EFF;margin-right:4px;"><info-filled /></el-icon>
            支持上传 <b>PDF、Word、Markdown、TXT</b> 格式的文件
          </div>
        </div>
      </el-card>
      <!-- 参数选择卡片 -->
      <el-card class="ai-generate-card ai-generate-param-card" shadow="hover">
        <div class="ai-generate-card-title">参数配置</div>
        <el-form :inline="false" class="ai-generate-form">
          <el-form-item label="输出文件名：">
            <el-input v-model="outputFile" placeholder="test_cases.xlsx" />
          </el-form-item>
          <el-form-item label="并发数：">
            <el-input-number v-model="concurrency" :min="1" :max="10" />
          </el-form-item>
          <el-form-item label="测试类型：">
            <el-select v-model="caseType" placeholder="请选择测试类型">
              <el-option label="功能测试" value="functional" />
              <el-option label="接口测试" value="api" />
              <el-option label="UI自动化测试" value="ui_auto" disabled />
            </el-select>
          </el-form-item>
        </el-form>
        <div class="ai-generate-form-btn-outer">
          <el-button type="success" class="ai-generate-upload-btn" :loading="loading" :disabled="!fileObj || loading" @click="handleGenerate">
            <el-icon style="margin-right:6px;" v-if="!loading"><document /></el-icon>
            生成用例
          </el-button>
        </div>
      </el-card>
      <!-- 下载区卡片 -->
      <el-card class="ai-generate-card ai-generate-download-card" shadow="hover">
        <div class="ai-generate-card-title">用例下载</div>
        <div class="ai-generate-download-tip">生成成功后可在下载中心下载测试用例文件</div>
        <div class="ai-generate-download-center-btn">
          <el-button class="ai-generate-upload-btn" @click="openDownloadCenter">打开下载中心</el-button>
        </div>
      </el-card>
    </div>
    <!-- 生成用例总结部分 -->
    <div class="ai-generate-summary">
      <div class="ai-generate-summary-title">生成用例总结</div>
      <div class="ai-generate-summary-grid">
        <div class="summary-card">
          <div class="summary-card-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 11H5M19 11C20.1046 11 21 11.8954 21 13V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V13C3 11.8954 3.89543 11 5 11M19 11V9C19 7.89543 18.1046 7 17 7M5 11V9C5 7.89543 5.89543 7 7 7M7 7V5C7 3.89543 7.89543 3 9 3H15C16.1046 3 17 3.89543 17 5V7M7 7H17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="summary-card-content">
            <div class="summary-card-label">用例类型</div>
            <div class="summary-card-value">
              <span class="custom-tag functional">功能测试</span>
              <span class="custom-tag api">接口测试</span>
              <span class="custom-tag ui_auto">UI自动化测试</span>
            </div>
          </div>
        </div>
        <div class="summary-card">
          <div class="summary-card-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M10.29 3.86L1.82 18A2 2 0 0 0 3.54 21H20.46A2 2 0 0 0 22.18 18L13.71 3.86A2 2 0 0 0 10.29 3.86ZM12 9V13M12 17H12.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="summary-card-content">
            <div class="summary-card-label">优先级分布</div>
            <div class="summary-card-value">
              <el-tag :type="getPriorityType('P0')" class="priority-tag" size="small">P0: 10</el-tag>
              <el-tag :type="getPriorityType('P1')" class="priority-tag" size="small">P1: 56</el-tag>
              <el-tag :type="getPriorityType('P2')" class="priority-tag" size="small">P2: 57</el-tag>
            </div>
          </div>
        </div>
        <div class="summary-card">
          <div class="summary-card-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9 5H7C5.89543 5 5 5.89543 5 7V19C5 20.1046 5.89543 21 7 21H17C18.1046 21 19 20.1046 19 19V7C19 5.89543 18.1046 5 17 5H15M9 5C9 6.10457 9.89543 7 11 7H13C14.1046 7 15 6.10457 15 5M9 5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 5M12 12H15M12 16H15M9 12H9.01M9 16H9.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="summary-card-content">
            <div class="summary-card-label">用例总数</div>
            <div class="summary-card-value">123</div>
          </div>
        </div>
        <div class="summary-card">
          <div class="summary-card-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="summary-card-content">
            <div class="summary-card-label">功能测试用例数</div>
            <div class="summary-card-value">60</div>
          </div>
        </div>
        <div class="summary-card">
          <div class="summary-card-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M10 20L14 4M18 8L22 12L18 16M6 16L2 12L6 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="summary-card-content">
            <div class="summary-card-label">接口测试用例数</div>
            <div class="summary-card-value">40</div>
          </div>
        </div>
        <div class="summary-card">
          <div class="summary-card-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9.75 17L9 20L8 21H16L15 20L14.25 17M3 13H21M5 17H19C20.1046 17 21 16.1046 21 15V7C21 5.89543 20.1046 5 19 5H5C3.89543 5 3 5.89543 3 7V15C3 16.1046 3.89543 17 5 17Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="summary-card-content">
            <div class="summary-card-label">UI自动化测试用例数</div>
            <div class="summary-card-value">23</div>
          </div>
        </div>
        <div class="summary-card">
          <div class="summary-card-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15M17 8L12 3M12 3L7 8M12 3V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="summary-card-content">
            <div class="summary-card-label">预估文件大小</div>
            <div class="summary-card-value">1.2MB</div>
          </div>
        </div>
        <div class="summary-card">
          <div class="summary-card-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 8V12L15 15M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="summary-card-content">
            <div class="summary-card-label">最新生成时间</div>
            <div class="summary-card-value">2024-05-01 12:34:56</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 成功弹窗已移除 -->

  <!-- 下载中心弹窗 -->
  <el-dialog
    v-model="downloadCenterVisible"
    title="下载中心"
    width="720px"
    class="download-center-dialog"
    :close-on-click-modal="false"
  >
    <div class="download-center-body">
      <el-table :data="fileList" height="420" v-loading="downloadCenterLoading">
        <el-table-column prop="filename" label="文件名" min-width="280" />
        <el-table-column prop="size" label="大小" width="120">
          <template #default="scope">{{ formatSize(scope.row.size) }}</template>
        </el-table-column>
        <el-table-column prop="modified_at" label="更新时间" min-width="180">
          <template #default="scope">{{ formatTime(scope.row.modified_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button type="primary" link @click="downloadFile(scope.row.filename)">下载</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <template #footer>
      <el-button @click="downloadCenterVisible = false">关闭</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox, ElNotification } from 'element-plus'
import { UploadFilled, InfoFilled, Document } from '@element-plus/icons-vue'

const fileName = ref('')
const fileObj = ref(null)
const outputFile = ref('test_cases.xlsx')
const concurrency = ref(1)
const caseType = ref('functional')
const loading = ref(false)
const downloadCenterVisible = ref(false)
const downloadCenterLoading = ref(false)
const fileList = ref([])

const shortFileName = computed(() => {
  if (!fileName.value) return ''
  if (fileName.value.length <= 24) return fileName.value
  // 省略中间部分
  return fileName.value.slice(0, 12) + '...' + fileName.value.slice(-8)
})

function beforeUpload(file) {
  // 如果上传新文件，重置表单状态
  resetForm()
  
  fileName.value = file.name
  fileObj.value = file
  // 阻止自动上传，后续逻辑后面实现
  return false
}

function resetForm() {
  fileName.value = ''
  fileObj.value = null
  outputFile.value = 'test_cases.xlsx'
  concurrency.value = 1
  caseType.value = 'functional'
}

async function handleGenerate() {
  if (!fileObj.value) {
    ElMessage.warning('请先选择需求文档文件！')
    return
  }
  if (!outputFile.value || !outputFile.value.trim()) {
    ElMessage.warning('请填写输出文件名！')
    return
  }
  
  // 显示生成开始提示
  ElMessageBox.alert(
    'AI正在分析需求文档并生成测试用例，此过程可能需要5-15分钟，请耐心等待，期间请勿进行其他操作',
    '生成开始',
    {
      confirmButtonText: '我知道了',
      type: 'info',
      center: true,
      customClass: 'generate-start-dialog'
    }
  )
  
  loading.value = true
  try {
    // 1. 上传文件
    const formData = new FormData()
    formData.append('file', fileObj.value)
    
    const uploadResponse = await fetch('/ai_generate/upload', {
      method: 'POST',
      body: formData
    })
    
    if (!uploadResponse.ok) {
      const errorData = await uploadResponse.json()
      throw new Error(errorData.error || '文件上传失败')
    }
    
    const uploadResult = await uploadResponse.json()
    
    // 2. 生成测试用例
    const generateResponse = await fetch('/ai_generate/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        filename: uploadResult.filename,
        output_filename: outputFile.value,
        test_type: caseType.value,
        concurrency: concurrency.value
      })
    })
    
    if (!generateResponse.ok) {
      const errorData = await generateResponse.json()
      throw new Error(errorData.error || '测试用例生成失败')
    }
    
    const generateResult = await generateResponse.json()
    
    if (generateResult.success) {
      ElMessage.success('测试用例生成成功！')
      notifyGenerated(outputFile.value) // 生成成功后的全局通知
    } else {
      throw new Error(generateResult.error || '生成失败')
    }
    
  } catch (e) {
    ElMessage.error('生成失败：' + e.message)
  } finally {
    loading.value = false
  }
}

function formatSize(size) {
  if (!size && size !== 0) return '-'
  const units = ['B','KB','MB','GB']
  let i = 0
  let s = size
  while (s >= 1024 && i < units.length - 1) { s /= 1024; i++ }
  return `${s.toFixed(1)} ${units[i]}`
}

function formatTime(ts) {
  if (!ts) return '-'
  try {
    const d = new Date(ts)
    const pad = n => n.toString().padStart(2,'0')
    return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
  } catch { return ts }
}

function downloadFile(name) {
  const url = `/ai_generate/download/${name}`
  const a = document.createElement('a')
  a.href = url
  a.download = name
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}

// 生成成功后的全局通知
function notifyGenerated(name) {
  ElNotification({
    title: '生成完成',
    message: `文件 ${name} 已生成，可在下载中心查看并下载`,
    type: 'success',
    position: 'top-right',
    duration: 6000,
    showClose: true
  })
}

// 修复：优先级标签类型映射
function getPriorityType(priority) {
  const priorityMap = {
    '高': 'danger',
    '中': 'warning',
    '低': 'info',
    'P0': 'danger',
    'P1': 'warning',
    'P2': 'info',
    'P3': 'success'
  }
  return priorityMap[priority] || 'info';
}

function openDownloadCenter() {
  downloadCenterVisible.value = true
  fetchFileList()
}

async function fetchFileList() {
  try {
    downloadCenterLoading.value = true
    const res = await fetch('/ai_generate/files')
    const data = await res.json()
    if (data.success) {
      fileList.value = data.files || []
    } else {
      ElMessage.error(data.error || '获取文件列表失败')
    }
  } catch (e) {
    ElMessage.error('获取文件列表失败：' + e.message)
  } finally {
    downloadCenterLoading.value = false
  }
}
</script>

<style scoped>
.ai-generate-case-root {
  height: calc(100vh - 80px - 40px);
  background: #f7f8fa;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 6px;
  padding-bottom: 6px;
  box-sizing: border-box;
  border: 2.5px solid #e0e7ff;
  border-radius: 32px;
  max-width: 1700px;
  margin: 2px auto 0 auto;
  overflow: auto;
}
.ai-generate-title {
  font-size: 32px;
  font-weight: 800;
  color: #222;
  margin-bottom: 32px;
  letter-spacing: 1.5px;
  text-shadow: 0 2px 8px rgba(160,180,255,0.08);
}
.ai-generate-cards-row {
  display: flex;
  flex-direction: row;
  gap: 32px;
  width: 100%;
  justify-content: center;
  align-items: flex-start;
  box-sizing: border-box;
  padding: 32px 32px 0 32px;
}
.ai-generate-card {
  width: 480px;
  min-width: 480px;
  max-width: 480px;
  height: 320px;
  min-height: 320px;
  max-height: 320px;
  margin-bottom: 0;
  border-radius: 22px;
  box-shadow: 0 6px 32px 0 rgba(80,120,255,0.10), 0 1.5px 6px 0 rgba(0,0,0,0.04);
  padding: 56px 32px 24px 32px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #fff;
  border: none;
  position: relative;
}
.ai-generate-card-title {
  position: absolute;
  top: 18px;
  left: 0;
  right: 0;
  width: 100%;
  text-align: center;
  font-size: 20px;
  font-weight: 800;
  color: #333;
  letter-spacing: 0.5px;
  margin: 0;
  padding: 0;
  z-index: 2;
}
.ai-generate-upload-card {
  background: linear-gradient(135deg, #FFFFFF 60%, #38bdf8 100%);
  box-shadow: 0 8px 32px 0 rgba(56,189,248,0.10), 0 2px 8px 0 rgba(0,0,0,0.04);
  padding-top: 0 !important;
}
.ai-generate-param-card {
  background: linear-gradient(135deg, #FFFFFF 60%, #c145feb3 100%);
  box-shadow: 0 8px 32px 0 rgba(193,69,254,0.08), 0 2px 8px 0 rgba(0,0,0,0.04);
}
.ai-generate-download-card {
  background: linear-gradient(135deg, #FFFFFF 60%, #45fe88a8 100%);
  box-shadow: 0 8px 32px 0 rgba(69,254,136,0.08), 0 2px 8px 0 rgba(0,0,0,0.04);
}
.ai-generate-upload-card .ai-generate-card-title {
  margin-top: 8px !important;
  margin-bottom: 22px;
  text-align: center;
  font-weight: 800;
}
.ai-generate-upload-vertical {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 18px;
  margin-top: 80px;
}
.ai-generate-upload {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  margin-bottom: 0;
}
/* 上传和生成用例按钮统一样式 */
.ai-generate-upload-btn {
  height: 44px;
  font-size: 17px;
  border-radius: 24px;
  padding: 0 28px;
  font-weight: 600;
  background: #38bdf8;
  border-color: #38bdf8;
  color: #fff;
  box-shadow: 0 2px 8px rgba(56,189,248,0.25);
  transition: background 0.2s, box-shadow 0.2s;
}
.ai-generate-upload-btn:hover,
.ai-generate-upload-btn:focus {
  background: #0ea5e9;
  border-color: #0ea5e9;
  color: #fff;
  box-shadow: 0 4px 12px rgba(56,189,248,0.35);
}
/* 禁用和loading状态统一 */
.ai-generate-upload-btn.is-disabled,
.ai-generate-upload-btn.is-disabled:hover,
.ai-generate-upload-btn[disabled],
.ai-generate-upload-btn[disabled]:hover,
.ai-generate-upload-btn.is-loading,
.ai-generate-upload-btn.is-loading:hover {
  background: #b6e6fa !important;
  border-color: #b6e6fa !important;
  color: #fff !important;
  box-shadow: none !important;
  cursor: not-allowed !important;
  opacity: 1 !important;
}
/* 覆盖Element Plus默认禁用按钮样式 */
:deep(.el-button.is-disabled),
:deep(.el-button.is-disabled:hover),
:deep(.el-button.is-loading),
:deep(.el-button.is-loading:hover) {
  background: #b6e6fa !important;
  border-color: #b6e6fa !important;
  color: #fff !important;
  box-shadow: none !important;
  cursor: not-allowed !important;
  opacity: 1 !important;
}
.ai-generate-filename-bubble {
  display: inline-flex;
  align-items: center;
  background: #f3f6ff;
  color: #3b4a6b;
  border-radius: 16px;
  padding: 4px 14px 4px 8px;
  margin-left: 18px;
  font-size: 15px;
  font-weight: 500;
  box-shadow: 0 1px 4px rgba(80,120,255,0.08);
  transition: box-shadow 0.2s;
}
.ai-generate-filename-bubble:hover {
  box-shadow: 0 2px 8px rgba(80,120,255,0.16);
}
.ai-generate-upload-tip {
  color: #409EFF;
  font-size: 15px;
  margin-top: 14px;
  margin-left: 2px;
  font-weight: 500;
  display: flex;
  align-items: center;
}
.ai-generate-form {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
:deep(.ai-generate-form .el-form-item) {
  display: flex;
  align-items: center;
  width: 100%;
  margin-bottom: 22px;
}
:deep(.ai-generate-form .el-form-item__label) {
  min-width: 100px;
  width: 100px;
  text-align: left;
  padding-right: 8px;
  flex-shrink: 0;
}
:deep(.ai-generate-form .el-form-item__content) {
  flex: 1 1 auto;
  min-width: 0;
}
:deep(.ai-generate-form .el-input),
:deep(.ai-generate-form .el-input-number),
:deep(.ai-generate-form .el-select) {
  width: 100%;
}
.ai-generate-form .el-button {
  /* 统一按钮样式由ai-generate-upload-btn控制，无需额外样式 */
}
.ai-generate-form-btn-outer {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 18px;
}
:deep(.ai-generate-form-btn-row .el-form-item__content) {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: 0 !important;
  padding-left: 0 !important;
}
.ai-generate-download-tip {
  color: #888;
  font-size: 15px;
  margin-top: 8px;
  text-align: center;
}
.ai-generate-summary {
  width: calc(100% - 85px);
  max-width: 1700px;
  margin: 32px auto 0 auto;
  padding: 32px;
  background: #ffffff;
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.8);
  margin-left: 32px;
  margin-right: 32px;
}
.ai-generate-summary-title {
  font-size: 24px;
  font-weight: 800;
  color: #1e293b;
  margin-bottom: 24px;
  text-align: center;
  position: relative;
}
.ai-generate-summary-title::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  border-radius: 2px;
}
.ai-generate-summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  width: 100%;
}
.summary-card {
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border: 1px solid #e2e8f0;
  position: relative;
  overflow: hidden;
}
.summary-card:nth-child(1) {
  --card-color: #3b82f6;
}
.summary-card:nth-child(2) {
  --card-color: #8b5cf6;
}
.summary-card:nth-child(3) {
  --card-color: #10b981;
}
.summary-card:nth-child(4) {
  --card-color: #f59e0b;
}
.summary-card:nth-child(5) {
  --card-color: #ef4444;
}
.summary-card:nth-child(6) {
  --card-color: #06b6d4;
}
.summary-card:nth-child(7) {
  --card-color: #84cc16;
}
.summary-card:nth-child(8) {
  --card-color: #f97316;
}
.summary-card::before {
  /* 去除顶部彩色装饰条 */
  display: none;
}
.summary-card:hover {
  /* 去除悬停动画效果 */
}
.summary-card-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
  color: var(--card-color, #3b82f6);
  background: linear-gradient(135deg, color-mix(in srgb, var(--card-color, #3b82f6) 20%, white) 0%, color-mix(in srgb, var(--card-color, #3b82f6) 10%, white) 100%);
  border-radius: 14px;
  flex-shrink: 0;
}
.summary-card-icon svg {
  width: 28px;
  height: 28px;
}
.summary-card-content {
  flex: 1;
  min-width: 0;
}
.summary-card-label {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 6px;
  font-weight: 500;
}
.summary-card-value {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.2;
}
.case-type-tag {
  margin-right: 8px;
  margin-bottom: 4px;
  display: inline-block;
}
.summary-card-value .case-type-tag:last-child {
  margin-right: 0;
}
.custom-tag {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  color: #fff;
  margin-right: 8px;
  margin-bottom: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}
.custom-tag.functional {
  background: #3b82f6;
}
.custom-tag.api {
  background: #10b981;
}
.custom-tag.ui_auto {
  background: #f59e0b;
}
.priority-tag {
  margin-right: 8px;
  margin-bottom: 4px;
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

/* 下载中心样式 */
.download-center-dialog :deep(.el-dialog__body) { padding: 0 20px 20px 20px; }
.download-center-body { margin-top: 6px; }
.ai-generate-download-center-btn { margin-top: 12px; text-align: center; }

@media (max-width: 1700px) {
  .ai-generate-case-root {
    max-width: 100vw;
    border-radius: 0;
    margin: 0;
  }
  .ai-generate-cards-row {
    padding: 0 8px 0 8px;
  }
}
@media (max-width: 1100px) {
  .ai-generate-cards-row {
    flex-direction: column;
    gap: 28px;
    align-items: center;
    padding: 0 0 0 0;
  }
  .ai-generate-card {
    width: 98vw;
    max-width: 540px;
    min-width: 0;
    height: auto;
    min-height: 0;
    max-height: none;
    margin-bottom: 0;
    padding: 16px 6vw 12px 6vw;
  }
}
</style> 