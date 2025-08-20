<template>
  <div class="data-factory-container">
    <!-- 主内容区域 -->
    <div class="factory-content">
      <!-- 数据生成器页面 -->
      <div v-if="currentTab === 'generator'" class="tab-content">
        <div class="content-header">
          <h2>数据生成器</h2>
          <p>配置数据结构和生成规则，快速生成测试数据</p>
        </div>

        <div class="generator-workspace">
          <!-- 数据结构配置区 -->
          <div class="workspace-left">
            <div class="config-panel">
              <div class="panel-header">
                <h4>数据结构配置</h4>
                <el-button size="small" @click="addField">
                  <el-icon><Plus /></el-icon>
                  添加字段
                </el-button>
              </div>
              
              <div class="field-list">
                <div v-for="(field, index) in dataStructure" :key="index" class="field-item">
                  <div class="field-header">
                    <el-input 
                      v-model="field.name" 
                      placeholder="字段名称"
                      size="small"
                      class="field-name"
                    />
                    <el-select 
                      v-model="field.type" 
                      placeholder="数据类型"
                      size="small"
                      class="field-type"
                    >
                      <el-option label="字符串" value="string" />
                      <el-option label="数字" value="number" />
                      <el-option label="日期" value="date" />
                      <el-option label="布尔值" value="boolean" />
                      <el-option label="枚举" value="enum" />
                      <el-option label="自定义" value="custom" />
                    </el-select>
                    <el-button 
                      size="small" 
                      type="danger" 
                      @click="removeField(index)"
                      class="field-remove"
                    >
                      <el-icon><Delete /></el-icon>
                    </el-button>
                  </div>
                  
                  <!-- 字段配置选项 -->
                  <div v-if="field.type === 'string'" class="field-config">
                    <el-input 
                      v-model="field.minLength" 
                      placeholder="最小长度"
                      size="small"
                      type="number"
                      class="config-input"
                    />
                    <el-input 
                      v-model="field.maxLength" 
                      placeholder="最大长度"
                      size="small"
                      type="number"
                      class="config-input"
                    />
                    <el-input 
                      v-model="field.pattern" 
                      placeholder="正则表达式"
                      size="small"
                      class="config-input"
                    />
                  </div>
                  
                  <div v-if="field.type === 'number'" class="field-config">
                    <el-input 
                      v-model="field.min" 
                      placeholder="最小值"
                      size="small"
                      type="number"
                      class="config-input"
                    />
                    <el-input 
                      v-model="field.max" 
                      placeholder="最大值"
                      size="small"
                      type="number"
                      class="config-input"
                    />
                    <el-input 
                      v-model="field.decimals" 
                      placeholder="小数位数"
                      size="small"
                      type="number"
                      class="config-input"
                    />
                  </div>
                  
                  <div v-if="field.type === 'enum'" class="field-config">
                    <el-tag 
                      v-for="(value, idx) in field.enumValues" 
                      :key="idx"
                      closable
                      @close="removeEnumValue(field, idx)"
                      class="enum-tag"
                    >
                      {{ value }}
                    </el-tag>
                    <el-input 
                      v-model="newEnumValue" 
                      placeholder="添加枚举值"
                      size="small"
                      @keyup.enter="addEnumValue(field)"
                      class="enum-input"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 生成配置区 -->
          <div class="workspace-right">
            <div class="config-panel">
              <div class="panel-header">
                <h4>生成配置</h4>
              </div>
              
              <el-form :model="generationConfig" label-width="100px">
            <el-form-item label="生成数量">
              <el-input-number 
                    v-model="generationConfig.count" 
                :min="1" 
                    :max="100000"
                :step="100"
                    size="large"
                    style="width: 100%"
              />
            </el-form-item>
            
                <el-form-item label="输出格式">
                  <el-select v-model="generationConfig.format" size="large" style="width: 100%">
                <el-option label="JSON" value="json" />
                <el-option label="CSV" value="csv" />
                <el-option label="Excel" value="excel" />
                <el-option label="SQL" value="sql" />
              </el-select>
            </el-form-item>
            
                <el-form-item label="文件名">
                  <el-input 
                    v-model="generationConfig.filename" 
                    placeholder="generated_data"
                    size="large"
                  />
            </el-form-item>
            
            <el-form-item>
                  <el-button 
                    type="primary" 
                    size="large" 
                    @click="generateData"
                    :loading="generating"
                    style="width: 100%"
                  >
                    <el-icon><VideoPlay /></el-icon>
                    {{ generating ? '生成中...' : '开始生成' }}
                  </el-button>
            </el-form-item>
          </el-form>
        </div>
          </div>
        </div>
      </div>

      <!-- 数据模板页面 -->
      <div v-else-if="currentTab === 'template'" class="tab-content">
        <div class="content-header">
          <h2>数据模板</h2>
          <p>管理和复用常用的数据结构模板</p>
          </div>
        
        <div class="template-grid">
          <div class="template-card" @click="useTemplate(template)" v-for="template in templates" :key="template.id">
            <div class="template-icon">
              <el-icon><Files /></el-icon>
            </div>
            <h4>{{ template.name }}</h4>
                <p>{{ template.description }}</p>
            <div class="template-tags">
              <el-tag size="small" v-for="tag in template.tags" :key="tag">{{ tag }}</el-tag>
            </div>
          </div>
          
          <div class="template-card add-template" @click="createTemplate">
            <div class="template-icon">
              <el-icon><Plus /></el-icon>
            </div>
            <h4>创建新模板</h4>
            <p>自定义数据结构模板</p>
          </div>
        </div>
      </div>

      <!-- 批量生成页面 -->
      <div v-else-if="currentTab === 'batch'" class="tab-content">
        <div class="content-header">
          <h2>批量生成</h2>
          <p>批量处理多个数据生成任务</p>
    </div>
    
        <div class="batch-workspace">
          <el-upload
            class="batch-upload"
            drag
            action="#"
            :auto-upload="false"
            :on-change="handleBatchFileChange"
            :file-list="batchFiles"
          >
            <el-icon class="el-icon--upload"><Upload /></el-icon>
            <div class="el-upload__text">
              拖拽配置文件到此处，或<em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持 JSON、YAML 格式的配置文件
              </div>
            </template>
          </el-upload>
          
          <div v-if="batchFiles.length > 0" class="batch-tasks">
            <h4>批量任务列表</h4>
            <el-table :data="batchTasks" style="width: 100%">
              <el-table-column prop="name" label="任务名称" />
              <el-table-column prop="status" label="状态">
                <template #default="scope">
                  <el-tag :type="getStatusType(scope.row.status)">
                    {{ scope.row.status }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="progress" label="进度">
                <template #default="scope">
                  <el-progress :percentage="scope.row.progress" />
                </template>
              </el-table-column>
              <el-table-column label="操作">
                <template #default="scope">
                  <el-button size="small" @click="startBatchTask(scope.row)">开始</el-button>
                  <el-button size="small" type="danger" @click="cancelBatchTask(scope.row)">取消</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
      </div>
      
      <!-- 其他页面占位 -->
      <div v-else class="tab-content">
        <div class="content-header">
          <h2>{{ getTabTitle() }}</h2>
          <p>功能开发中，敬请期待...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { ElMessage } from 'element-plus';
import { 
  Plus, 
  DataAnalysis, 
  Files, 
  Upload, 
  RefreshRight, 
  Brush, 
  Check, 
  Folder, 
  Clock, 
  Setting,
  Delete,
  VideoPlay,
  Document,
  Collection,
  Grid,
  Tools,
  Monitor
} from '@element-plus/icons-vue';

// 接收父组件传递的当前标签页
const props = defineProps({
  currentTab: {
    type: String,
    default: 'generator'
  }
});

// 数据结构配置
const dataStructure = ref([
  {
    name: 'id',
    type: 'number',
    min: 1,
    max: 1000,
    decimals: 0
  },
  {
    name: 'name',
    type: 'string',
    minLength: 2,
    maxLength: 20,
    pattern: ''
  },
  {
    name: 'email',
    type: 'string',
    minLength: 5,
    maxLength: 50,
    pattern: '^[\\w-\\.]+@([\\w-]+\\.)+[\\w-]{2,4}$'
  }
]);

// 生成配置
const generationConfig = reactive({
  count: 100,
  format: 'json',
  filename: 'generated_data'
});

// 数据模板
const templates = ref([
  {
    id: 1,
    name: '用户基础信息',
    description: '包含用户ID、姓名、邮箱等基础字段',
    tags: ['用户', '基础信息', '常用']
  },
  {
    id: 2,
    name: '产品信息',
    description: '产品名称、价格、分类、描述等字段',
    tags: ['产品', '电商', '商品']
  },
  {
    id: 3,
    name: '订单数据',
    description: '订单号、商品、数量、金额、状态等字段',
    tags: ['订单', '交易', '财务']
  }
]);

// 批量文件
const batchFiles = ref([]);
const batchTasks = ref([]);

// 生成状态
const generating = ref(false);
const newEnumValue = ref('');

// 获取标签页标题
const getTabTitle = () => {
  const titles = {
    'generator': '数据生成器',
    'template': '数据模板',
    'batch': '批量生成',
    'transform': '格式转换',
    'projects': '项目管理',
    'history': '生成历史',
    'settings': '系统设置'
  };
  return titles[props.currentTab] || '未知页面';
};

// 添加字段
const addField = () => {
  dataStructure.value.push({
    name: '',
    type: 'string',
    minLength: 1,
    maxLength: 50,
    pattern: ''
  });
};

// 删除字段
const removeField = (index) => {
  dataStructure.value.splice(index, 1);
};

// 添加枚举值
const addEnumValue = (field) => {
  if (newEnumValue.value.trim()) {
    if (!field.enumValues) {
      field.enumValues = [];
    }
    field.enumValues.push(newEnumValue.value.trim());
    newEnumValue.value = '';
  }
};

// 删除枚举值
const removeEnumValue = (field, index) => {
  field.enumValues.splice(index, 1);
};

// 生成数据
const generateData = async () => {
  if (dataStructure.value.length === 0) {
    ElMessage.warning('请至少添加一个字段');
    return;
  }
  
  generating.value = true;
  
  try {
    // 模拟生成过程
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    ElMessage.success(`成功生成 ${generationConfig.count} 条测试数据`);
    
    // 这里可以添加下载逻辑
    const dataStr = JSON.stringify({
      structure: dataStructure.value,
      config: generationConfig,
      generated_at: new Date().toISOString()
    }, null, 2);
    
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${generationConfig.filename}.json`;
    a.click();
    URL.revokeObjectURL(url);
    
  } catch (error) {
    ElMessage.error('生成失败：' + error.message);
  } finally {
    generating.value = false;
  }
};

// 使用模板
const useTemplate = (template) => {
  ElMessage.info(`使用模板：${template.name}`);
  // 这里可以加载模板到数据结构中
};

// 创建模板
const createTemplate = () => {
  ElMessage.info('创建新模板功能开发中...');
};

// 处理批量文件上传
const handleBatchFileChange = (file) => {
  ElMessage.success(`文件 ${file.name} 上传成功`);
  // 这里可以解析配置文件
};

// 开始批量任务
const startBatchTask = (task) => {
  ElMessage.info(`开始任务：${task.name}`);
};

// 取消批量任务
const cancelBatchTask = (task) => {
  ElMessage.info(`取消任务：${task.name}`);
};

// 获取状态类型
const getStatusType = (status) => {
  const types = {
    'pending': 'info',
    'running': 'warning',
    'completed': 'success',
    'failed': 'danger'
  };
  return types[status] || 'info';
};
</script>

<style scoped>
.data-factory-container {
  height: 100%;
  background: #f5f7fa;
}

.factory-content {
  padding: 24px;
  height: 100%;
  overflow-y: auto;
}

.tab-content {
  max-width: 1200px;
  margin: 0 auto;
}

.content-header {
  margin-bottom: 32px;
  text-align: center;
}

.content-header h2 {
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 600;
  color: #1f2937;
}

.content-header p {
  margin: 0;
  color: #6b7280;
  font-size: 16px;
}

.generator-workspace {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 24px;
}

.workspace-left {
  min-width: 0;
}

.workspace-right {
  min-width: 0;
}

.config-panel {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.panel-header h4 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
}

.field-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field-item {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  background: #f9fafb;
}

.field-header {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
}

.field-name {
  flex: 1;
}

.field-type {
  width: 120px;
}

.field-remove {
  flex-shrink: 0;
}

.field-config {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.config-input {
  width: 120px;
}

.enum-tag {
  margin-right: 8px;
  margin-bottom: 8px;
}

.enum-input {
  width: 150px;
}

.template-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.template-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid #e5e7eb;
}

.template-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.template-card.add-template {
  border: 2px dashed #d1d5db;
  color: #6b7280;
}

.template-card.add-template:hover {
  border-color: #1d4ed8;
  color: #1d4ed8;
}

.template-icon {
  font-size: 48px;
  color: #1d4ed8;
  margin-bottom: 16px;
}

.template-card.add-template .template-icon {
  color: #9ca3af;
}

.template-card.add-template:hover .template-icon {
  color: #1d4ed8;
}

.template-card h4 {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
}

.template-card p {
  margin: 0 0 16px 0;
  color: #6b7280;
  font-size: 14px;
}

.template-tags {
  display: flex;
  gap: 8px;
  justify-content: center;
  flex-wrap: wrap;
}

.batch-workspace {
  max-width: 800px;
  margin: 0 auto;
}

.batch-upload {
  margin-bottom: 32px;
}

.batch-tasks h4 {
  margin: 0 0 16px 0;
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .generator-workspace {
    grid-template-columns: 1fr;
  }
  
  .workspace-right {
    order: -1;
  }
}

@media (max-width: 768px) {
  .factory-content {
    padding: 16px;
  }
  
  .template-grid {
    grid-template-columns: 1fr;
  }
}
</style> 