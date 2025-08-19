<template>
  <div class="data-factory-container">
    <div class="factory-header">
      <h2>数据工厂</h2>
      <p>批量生成、转换和管理测试数据</p>
    </div>
    
    <div class="factory-content">
      <!-- 数据生成工具 -->
      <el-card class="factory-card">
        <template #header>
          <div class="card-header">
            <span>数据生成工具</span>
          </div>
        </template>
        
        <div class="tool-section">
          <h4>测试数据生成</h4>
          <el-form :model="dataGenForm" label-width="120px">
            <el-form-item label="数据类型">
              <el-select v-model="dataGenForm.dataType" placeholder="请选择数据类型">
                <el-option label="用户信息" value="user" />
                <el-option label="产品信息" value="product" />
                <el-option label="订单数据" value="order" />
                <el-option label="地址信息" value="address" />
                <el-option label="自定义数据" value="custom" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="生成数量">
              <el-input-number 
                v-model="dataGenForm.count" 
                :min="1" 
                :max="10000" 
                :step="100"
              />
            </el-form-item>
            
            <el-form-item label="数据格式">
              <el-select v-model="dataGenForm.format" placeholder="请选择输出格式">
                <el-option label="JSON" value="json" />
                <el-option label="CSV" value="csv" />
                <el-option label="Excel" value="excel" />
                <el-option label="SQL" value="sql" />
              </el-select>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="generateData">生成数据</el-button>
              <el-button @click="showPreviewData">预览数据</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-card>
      
      <!-- 数据转换工具 -->
      <el-card class="factory-card">
        <template #header>
          <div class="card-header">
            <span>数据转换工具</span>
          </div>
        </template>
        
        <div class="tool-section">
          <h4>格式转换</h4>
          <el-form :model="convertForm" label-width="120px">
            <el-form-item label="源格式">
              <el-select v-model="convertForm.sourceFormat" placeholder="请选择源格式">
                <el-option label="JSON" value="json" />
                <el-option label="CSV" value="csv" />
                <el-option label="Excel" value="excel" />
                <el-option label="XML" value="xml" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="目标格式">
              <el-select v-model="convertForm.targetFormat" placeholder="请选择目标格式">
                <el-option label="JSON" value="json" />
                <el-option label="CSV" value="csv" />
                <el-option label="Excel" value="excel" />
                <el-option label="SQL" value="sql" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="上传文件">
              <el-upload
                class="upload-demo"
                drag
                action="#"
                :auto-upload="false"
                :on-change="handleFileChange"
                :file-list="fileList"
              >
                <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                <div class="el-upload__text">
                  将文件拖到此处，或<em>点击上传</em>
                </div>
              </el-upload>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="convertData" :disabled="!convertForm.sourceFile">转换数据</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-card>
      
      <!-- 数据管理工具 -->
      <el-card class="factory-card">
        <template #header>
          <div class="card-header">
            <span>数据管理工具</span>
          </div>
        </template>
        
        <div class="tool-section">
          <h4>数据模板管理</h4>
          <div class="template-list">
            <div class="template-item" v-for="template in dataTemplates" :key="template.id">
              <div class="template-info">
                <h5>{{ template.name }}</h5>
                <p>{{ template.description }}</p>
                <span class="template-type">{{ template.type }}</span>
              </div>
              <div class="template-actions">
                <el-button size="small" @click="editTemplate(template)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteTemplate(template.id)">删除</el-button>
              </div>
            </div>
          </div>
          
          <el-button type="primary" @click="createTemplate" style="margin-top: 16px;">
            创建新模板
          </el-button>
        </div>
      </el-card>
    </div>
    
    <!-- 数据预览弹窗 -->
    <el-dialog
      v-model="previewDialogVisible"
      title="数据预览"
      width="80%"
      class="preview-dialog"
    >
      <div class="preview-content">
        <pre v-if="previewData" class="data-preview">{{ JSON.stringify(previewData, null, 2) }}</pre>
        <div v-else class="no-data">暂无预览数据</div>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="previewDialogVisible = false">关闭</el-button>
          <el-button type="primary" @click="downloadPreviewData">下载数据</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { UploadFilled } from '@element-plus/icons-vue';

// 数据生成表单
const dataGenForm = reactive({
  dataType: 'user',
  count: 100,
  format: 'json'
});

// 数据转换表单
const convertForm = reactive({
  sourceFormat: 'json',
  targetFormat: 'csv',
  sourceFile: null
});

// 文件列表
const fileList = ref([]);

// 数据模板
const dataTemplates = ref([
  {
    id: 1,
    name: '用户基础信息',
    description: '包含用户名、邮箱、手机号等基础字段',
    type: '用户数据'
  },
  {
    id: 2,
    name: '产品信息模板',
    description: '产品名称、价格、分类、描述等字段',
    type: '产品数据'
  },
  {
    id: 3,
    name: '订单数据模板',
    description: '订单号、商品、数量、金额、状态等字段',
    type: '订单数据'
  }
]);

// 预览弹窗
const previewDialogVisible = ref(false);
const previewData = ref(null);

// 生成数据
const generateData = () => {
  // TODO: 实现真实的数据生成逻辑
  const mockData = Array.from({ length: dataGenForm.count }, (_, index) => ({
    id: index + 1,
    name: `测试数据${index + 1}`,
    type: dataGenForm.dataType,
    timestamp: new Date().toISOString()
  }));
  
  previewData.value = mockData;
  previewDialogVisible.value = true;
  ElMessage.success(`成功生成 ${dataGenForm.count} 条测试数据`);
};

// 预览数据
const showPreviewData = () => {
  if (!previewData.value) {
    ElMessage.warning('请先生成数据');
    return;
  }
  previewDialogVisible.value = true;
};

// 处理文件上传
const handleFileChange = (file) => {
  convertForm.sourceFile = file;
  ElMessage.success(`文件 ${file.name} 上传成功`);
};

// 转换数据
const convertData = () => {
  if (!convertForm.sourceFile) {
    ElMessage.warning('请先上传文件');
    return;
  }
  // TODO: 实现真实的数据转换逻辑
  ElMessage.success(`数据从 ${convertForm.sourceFormat} 转换为 ${convertForm.targetFormat} 成功`);
};

// 编辑模板
const editTemplate = (template) => {
  ElMessage.info(`编辑模板: ${template.name}`);
};

// 删除模板
const deleteTemplate = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这个模板吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });
    
    dataTemplates.value = dataTemplates.value.filter(t => t.id !== id);
    ElMessage.success('模板删除成功');
  } catch {
    // 用户取消删除
  }
};

// 创建新模板
const createTemplate = () => {
  ElMessage.info('创建新模板功能开发中...');
};

// 下载预览数据
const downloadPreviewData = () => {
  if (!previewData.value) {
    ElMessage.warning('暂无数据可下载');
    return;
  }
  
  const dataStr = JSON.stringify(previewData.value, null, 2);
  const blob = new Blob([dataStr], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `test_data_${new Date().getTime()}.json`;
  a.click();
  URL.revokeObjectURL(url);
  
  ElMessage.success('数据下载成功');
};
</script>

<style scoped>
.data-factory-container {
  padding: 20px;
}

.factory-header {
  margin-bottom: 30px;
  text-align: center;
}

.factory-header h2 {
  font-size: 28px;
  color: #1f2937;
  margin-bottom: 10px;
  font-weight: 600;
}

.factory-header p {
  font-size: 16px;
  color: #6b7280;
  margin: 0;
}

.factory-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
  margin-bottom: 30px;
}

.factory-card {
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
}

.card-header {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
}

.tool-section {
  margin-bottom: 20px;
}

.tool-section h4 {
  margin: 0 0 16px 0;
  color: #374151;
  font-size: 16px;
  font-weight: 600;
}

.template-list {
  max-height: 300px;
  overflow-y: auto;
}

.template-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 12px;
  background: #f9fafb;
}

.template-info h5 {
  margin: 0 0 4px 0;
  color: #1f2937;
  font-size: 14px;
  font-weight: 600;
}

.template-info p {
  margin: 0 0 8px 0;
  color: #6b7280;
  font-size: 12px;
}

.template-type {
  display: inline-block;
  padding: 2px 8px;
  background: #dbeafe;
  color: #1e40af;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
}

.template-actions {
  display: flex;
  gap: 8px;
}

.preview-dialog {
  border-radius: 12px;
}

.preview-content {
  max-height: 400px;
  overflow-y: auto;
}

.data-preview {
  background: #f8fafc;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 12px;
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-all;
}

.no-data {
  text-align: center;
  color: #9ca3af;
  padding: 40px;
  font-size: 16px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .factory-content {
    grid-template-columns: 1fr;
  }
  
  .template-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .template-actions {
    width: 100%;
    justify-content: flex-end;
  }
}
</style> 