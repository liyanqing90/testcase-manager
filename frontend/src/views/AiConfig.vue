<template>
  <div class="ai-config-container">
    <div class="config-content">
      <el-card class="config-card" shadow="never">
        <template #header>
          <div class="card-header">
            <el-icon><Setting /></el-icon>
            <span>AI模型配置</span>
          </div>
        </template>
        
        <el-form 
          :model="configForm" 
          :rules="configRules" 
          ref="configFormRef" 
          label-width="120px"
          class="config-form"
        >
          <el-form-item label="模型类型" prop="modelType">
            <el-select 
              v-model="configForm.modelType" 
              placeholder="请选择模型类型"
              class="config-input"
            >
              <el-option label="通义千问" value="qwen" />
              <el-option label="OpenAI" value="openai" />
              <el-option label="Claude" value="claude" />
              <el-option label="Gemini" value="gemini" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="API密钥" prop="apiKey">
            <el-input 
              v-model="configForm.apiKey" 
              placeholder="请输入API密钥"
              type="password"
              show-password
              class="config-input"
            />
          </el-form-item>
          
          <el-form-item label="模型URL" prop="baseUrl">
            <el-input 
              v-model="configForm.baseUrl" 
              placeholder="请输入模型URL"
              class="config-input"
            />
          </el-form-item>
          
          <el-form-item label="模型版本" prop="modelVersion">
            <el-input 
              v-model="configForm.modelVersion" 
              placeholder="请输入模型版本"
              class="config-input"
            />
          </el-form-item>
          
          <el-form-item label="输入价格" prop="promptPrice">
            <el-input 
              v-model="configForm.promptPrice" 
              placeholder="每1000个输入token的价格"
              class="config-input"
            >
              <template #append>CNY</template>
            </el-input>
          </el-form-item>
          
          <el-form-item label="输出价格" prop="completionPrice">
            <el-input 
              v-model="configForm.completionPrice" 
              placeholder="每1000个输出token的价格"
              class="config-input"
            >
              <template #append>CNY</template>
            </el-input>
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="saveConfig" :loading="saving">
              保存配置
            </el-button>
            <el-button @click="resetConfig">重置</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Setting } from '@element-plus/icons-vue';

// 响应式数据
const configFormRef = ref();
const saving = ref(false);

const configForm = reactive({
  modelType: 'qwen',
  apiKey: '',
  baseUrl: '',
  modelVersion: '',
  promptPrice: '',
  completionPrice: ''
});

// 表单验证规则
const configRules = {
  modelType: [
    { required: true, message: '请选择模型类型', trigger: 'change' }
  ],
  apiKey: [
    { required: true, message: '请输入API密钥', trigger: 'blur' }
  ],
  baseUrl: [
    { required: true, message: '请输入基础URL', trigger: 'blur' }
  ],
  modelVersion: [
    { required: true, message: '请输入模型版本', trigger: 'blur' }
  ],
  promptPrice: [
    { required: true, message: '请输入每1000个输入token的价格', trigger: 'blur' }
  ],
  completionPrice: [
    { required: true, message: '请输入每1000个输出token的价格', trigger: 'blur' }
  ]
};

// 页面加载时初始化
onMounted(async () => {
  // 加载已有的配置
  await loadConfig();
});

// 加载配置
const loadConfig = async () => {
  try {
    const response = await fetch('/api/ai_config');
    const result = await response.json();
    
    if (result.success && result.data) {
      // 填充表单数据
      configForm.modelType = result.data.modelType || 'qwen';
      configForm.apiKey = result.data.apiKey || '';
      configForm.baseUrl = result.data.baseUrl || '';
      configForm.modelVersion = result.data.modelVersion || '';
      configForm.promptPrice = result.data.promptPrice || '0.001';
      configForm.completionPrice = result.data.completionPrice || '0.002';
    }
  } catch (error) {
    console.error('加载配置失败:', error);
    ElMessage.error('加载配置失败');
  }
};

// 保存配置
const saveConfig = async () => {
  try {
    await configFormRef.value.validate();
    saving.value = true;
    
    const response = await fetch('/api/ai_config', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        modelType: configForm.modelType,
        apiKey: configForm.apiKey,
        baseUrl: configForm.baseUrl,
        modelVersion: configForm.modelVersion,
        promptPrice: configForm.promptPrice,
        completionPrice: configForm.completionPrice
      })
    });
    
    const result = await response.json();
    
    if (result.success) {
      ElMessage.success('配置保存成功！');
    } else {
      ElMessage.error(result.message || '配置保存失败');
    }
  } catch (error) {
    console.error('配置保存失败:', error);
    ElMessage.error('配置保存失败，请检查输入');
  } finally {
    saving.value = false;
  }
};

// 重置配置
const resetConfig = () => {
  ElMessageBox.confirm(
    '确定要重置所有配置吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    configFormRef.value.resetFields();
    ElMessage.success('配置已重置');
  }).catch(() => {
    // 用户取消
  });
};
</script>

<style scoped>
.ai-config-container {
  padding: 24px;
  width: 100%;
  height: 100%;
  background: #f8fafc;
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  overflow-y: auto;
}

.config-content {
  max-width: 500px;
  margin: 0 0 0 40px;
  padding-top: 20px;
}

.config-card {
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
}

.card-header .el-icon {
  font-size: 20px;
  color: #3b82f6;
}

.config-form {
  padding: 20px 0;
}

.config-input {
  width: 100%;
}

.el-form-item {
  margin-bottom: 20px;
}

.el-form-item:last-child {
  margin-bottom: 0;
  text-align: center;
}

.el-form-item:last-child .el-button {
  margin: 0 8px;
}
</style> 