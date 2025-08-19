<template>
  <div class="ai-config-container">
    <div class="config-header">
      <h2>AI配置管理</h2>
      <p>配置AI模型参数、API密钥和其他相关设置</p>
    </div>
    
    <div class="config-content">
      <el-card class="config-card">
        <template #header>
          <div class="card-header">
            <span>OpenAI配置</span>
          </div>
        </template>
        
        <el-form :model="openaiConfig" label-width="120px">
          <el-form-item label="API密钥">
            <el-input 
              v-model="openaiConfig.apiKey" 
              type="password" 
              placeholder="请输入OpenAI API密钥"
              show-password
            />
          </el-form-item>
          
          <el-form-item label="模型名称">
            <el-select v-model="openaiConfig.model" placeholder="请选择模型">
              <el-option label="GPT-4" value="gpt-4" />
              <el-option label="GPT-3.5 Turbo" value="gpt-3.5-turbo" />
              <el-option label="GPT-4 Turbo" value="gpt-4-turbo-preview" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="最大Token">
            <el-input-number 
              v-model="openaiConfig.maxTokens" 
              :min="100" 
              :max="4000" 
              :step="100"
            />
          </el-form-item>
          
          <el-form-item label="温度">
            <el-slider 
              v-model="openaiConfig.temperature" 
              :min="0" 
              :max="2" 
              :step="0.1"
              :format-tooltip="(val) => val.toFixed(1)"
            />
          </el-form-item>
        </el-form>
      </el-card>
      
      <el-card class="config-card">
        <template #header>
          <div class="card-header">
            <span>AutoGen配置</span>
          </div>
        </template>
        
        <el-form :model="autogenConfig" label-width="120px">
          <el-form-item label="工作目录">
            <el-input 
              v-model="autogenConfig.workDir" 
              placeholder="请输入工作目录路径"
            />
          </el-form-item>
          
          <el-form-item label="超时时间(秒)">
            <el-input-number 
              v-model="autogenConfig.timeout" 
              :min="30" 
              :max="3600" 
              :step="30"
            />
          </el-form-item>
          
          <el-form-item label="最大重试次数">
            <el-input-number 
              v-model="autogenConfig.maxRetries" 
              :min="1" 
              :max="10" 
              :step="1"
            />
          </el-form-item>
        </el-form>
      </el-card>
      
      <el-card class="config-card">
        <template #header>
          <div class="card-header">
            <span>系统配置</span>
          </div>
        </template>
        
        <el-form :model="systemConfig" label-width="120px">
          <el-form-item label="日志级别">
            <el-select v-model="systemConfig.logLevel" placeholder="请选择日志级别">
              <el-option label="DEBUG" value="debug" />
              <el-option label="INFO" value="info" />
              <el-option label="WARNING" value="warning" />
              <el-option label="ERROR" value="error" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="启用调试模式">
            <el-switch v-model="systemConfig.debugMode" />
          </el-form-item>
          
          <el-form-item label="自动保存">
            <el-switch v-model="systemConfig.autoSave" />
          </el-form-item>
        </el-form>
      </el-card>
    </div>
    
    <div class="config-actions">
      <el-button type="primary" @click="saveConfig">保存配置</el-button>
      <el-button @click="resetConfig">重置配置</el-button>
      <el-button @click="testConnection">测试连接</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { ElMessage } from 'element-plus';

// OpenAI配置
const openaiConfig = reactive({
  apiKey: '',
  model: 'gpt-4',
  maxTokens: 2000,
  temperature: 0.7
});

// AutoGen配置
const autogenConfig = reactive({
  workDir: './ai_test_cases',
  timeout: 300,
  maxRetries: 3
});

// 系统配置
const systemConfig = reactive({
  logLevel: 'info',
  debugMode: false,
  autoSave: true
});

// 保存配置
const saveConfig = () => {
  // TODO: 实现配置保存逻辑
  ElMessage.success('配置保存成功');
};

// 重置配置
const resetConfig = () => {
  // TODO: 实现配置重置逻辑
  ElMessage.info('配置已重置');
};

// 测试连接
const testConnection = () => {
  // TODO: 实现连接测试逻辑
  ElMessage.info('正在测试连接...');
};
</script>

<style scoped>
.ai-config-container {
  padding: 20px;
}

.config-header {
  margin-bottom: 30px;
  text-align: center;
}

.config-header h2 {
  font-size: 28px;
  color: #1f2937;
  margin-bottom: 10px;
  font-weight: 600;
}

.config-header p {
  font-size: 16px;
  color: #6b7280;
  margin: 0;
}

.config-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
  margin-bottom: 30px;
}

.config-card {
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
}

.card-header {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
}

.config-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  padding: 20px 0;
}

.config-actions .el-button {
  padding: 12px 24px;
  font-size: 16px;
  border-radius: 8px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .config-content {
    grid-template-columns: 1fr;
  }
  
  .config-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .config-actions .el-button {
    width: 200px;
  }
}
</style> 