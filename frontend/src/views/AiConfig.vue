<template>
  <div class="ai-config-container">
    <el-tabs tab-position="left" style="height: calc(100vh - 80px)" class="demo-tabs">
      <el-tab-pane label="模型配置">
        <div class="tab-content">
          <div class="config-container">
        <el-form 
          :model="configForm" 
          :rules="configRules" 
          ref="configFormRef" 
          label-width="120px"
          class="config-form"
        >
              <div class="form-section">
                <h4>基础信息</h4>
          <el-form-item label="模型类型" prop="modelType">
            <el-select 
              v-model="configForm.modelType" 
              placeholder="请选择模型类型"
              class="config-input"
            >
              <el-option label="通义千问" value="qwen" />
              <el-option label="字节跳动（火山引擎）" value="volcengine" />
              <el-option label="DeepSeek" value="deepseek" />
              <el-option label="智谱AI" value="zhipu" />
              <el-option label="OpenAI" value="openai" />
              <el-option label="百度文心一言" value="wenxin" />
              <el-option label="讯飞星火" value="xunfei" />
              <el-option label="MiniMax" value="minimax" />
              <el-option label="月之暗面" value="moonshot" />
              <el-option label="360智脑" value="360" />
              <el-option label="Claude (Anthropic)" value="claude" />
              <el-option label="Gemini (Google)" value="gemini" />
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
              </div>
          
              <div class="form-section">
                <h4>价格配置</h4>
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
              </div>
          
              <el-form-item class="form-actions">
                <el-button type="primary" @click="saveConfig" :disabled="saving" class="save-btn">
              <template v-if="saving">
                <div class="saving-inline">
                  <div class="circular-loading"></div>
                  正在保存
                </div>
              </template>
              <template v-else>
              保存配置
              </template>
            </el-button>
                <el-button @click="resetConfig" :disabled="saving" class="reset-btn">重置</el-button>
          </el-form-item>
        </el-form>
          </div>
        </div>
      </el-tab-pane>
      
      <el-tab-pane label="帮助文档">
        <div class="tab-content">
          <div class="help-container">
            <el-collapse>
              <el-collapse-item title="模型推荐" name="1" class="custom-collapse-item">
                <p><strong>通义千问系列：</strong></p>
                <ul>
                  <li><strong>qwen-turbo</strong>：强烈推荐！快速响应，生成的用例完整覆盖度高</li>
                  <li><strong>qwen-plus</strong>：平衡性能，适合复杂对话和中等难度任务</li>
                  <li><strong>qwen-max</strong>：最强性能，适合高难度任务和专业应用</li>
                </ul>
              </el-collapse-item>
              <el-collapse-item title="如何获取API密钥？" name="2" class="custom-collapse-item">
                <p>1. 登录您的AI服务提供商账户</p>
                <p>2. 进入API管理页面</p>
                <p>3. 创建新的API密钥</p>
                <p>4. 复制密钥并粘贴到配置中</p>
              </el-collapse-item>
              <el-collapse-item title="模型URL接口地址说明" name="3" class="custom-collapse-item">
                <p>通义千问：https://dashscope.aliyuncs.com/compatible-mode/v1</p>
                <p>火山引擎：https://ark.cn-beijing.volces.com/api/v3</p>
                <p>DeepSeek：https://api.deepseek.com</p>
                <p>智谱AI：https://open.bigmodel.cn/api/paas/v4</p>
                <p>OpenAI：https://api.openai.com/v1</p>
                <p>百度文心一言：https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat</p>
                <p>讯飞星火：https://spark-api.xf-yun.com/v3.1/chat</p>
                <p>MiniMax：https://api.minimax.chat/v1</p>
                <p>月之暗面：https://api.moonshot.cn/v1</p>
                <p>360智脑：https://api.360.cn/v1</p>
                <p>Claude (Anthropic)：https://api.anthropic.com/v1</p>
                <p>Gemini (Google)：https://generativelanguage.googleapis.com/v1beta</p>
              </el-collapse-item>
              <el-collapse-item title="更新日志" name="4" class="custom-collapse-item update-log-item">
                <p><strong>V1.0.7 (2025-09-02)</strong></p>
                <ul>
                  <li>新增支持Claude (Anthropic)、Gemini (Google)等全球顶级AI模型</li>
                  <li>优化AI模型配置界面，支持12种主流AI模型</li>
                  <li>完善模型URL接口地址说明文档</li>
                </ul>
                <p><strong>V1.0.6 (2025-09-02)</strong></p>
                <ul>
                  <li>新增支持OpenAI、百度文心一言、讯飞星火、MiniMax、月之暗面、360智脑等AI模型</li>
                  <li>优化AI模型配置界面，支持10种主流AI模型</li>
                  <li>完善模型URL接口地址说明文档</li>
                </ul>
                <p><strong>V1.0.5 (2025-09-02)</strong></p>
                <ul>
                  <li>完成AI配置服务层</li>
                  <li>增加多模型适配</li>
                  <li>修复一些报错</li>
                  <li>脱离env文件，改为配置化</li>
                </ul>
                <p><strong>V1.0.4 (2025-08-29)</strong></p>
                <ul>
                  <li>增加AI生成用例策略组json识别</li>
                  <li>增加用例需求分析功能点规则匹配度</li>
                  <li>补充用例上传的部分识别逻辑</li>
                  <li>增加系统设置，后续所有的模型配置将不在代码中写死，改为配置</li>
                  <li>解决AutoAgent框架识别部分模型时，无法计算价格导致的warning</li>
                </ul>
                <p><strong>V1.0.3 (2025-08-22)</strong></p>
                <ul>
                  <li>手动增加测试用例功能</li>
                  <li>运行日志</li>
                </ul>
                <p><strong>V1.0.2 (2025-08-12)</strong></p>
                <ul>
                  <li>优化AI生成用例的用户体验</li>
                  <li>修复文件选择后清除生成总结的问题</li>
                  <li>修复用例类型显示问题</li>
                  <li>优化下载中心弹窗标题样式</li>
                  <li>改进错误处理和用户提示</li>
                </ul>
                <p><strong>V1.0.1 (2025-08-10)</strong></p>
                <ul>
                  <li>AI生成能力（已开发完成）接入用例平台</li>
                  <li>生成用例总结数据实时显示</li>
                  <li>支持多种测试类型（功能测试、接口测试、UI自动化测试）</li>
                  <li>智能文档解析和用例生成</li>
                  <li>生成历史记录和统计</li>
                </ul>
                <p><strong>v1.0.0 (2025-08-01)</strong></p>
                <ul>
                  <li>基础项目管理功能</li>
                  <li>Excel文件上传和解析</li>
                  <li>测试用例批量导入</li>
                  <li>重复数据检测和处理</li>
                  <li>响应式Web界面</li>
                </ul>
              </el-collapse-item>
            </el-collapse>
          </div>
    </div>
      </el-tab-pane>
    </el-tabs>
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
  overflow: hidden;
}

.demo-tabs {
  height: 100%;
  border-radius: 16px;
  overflow: hidden;
}

.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 16px;
  font-weight: 400;
}

.el-tabs--right .el-tabs__content,
.el-tabs--left .el-tabs__content {
  height: 100%;
}

.el-tabs--left .el-tabs__header {
  border-right: 1px solid #e4e7ed;
  border-bottom: none;
  border-top: none;
  border-left: none;
}

.el-tabs--left .el-tabs__nav-wrap {
  border-bottom: none;
}

.el-tabs--left .el-tabs__nav {
  border: none;
}

.el-tabs--left .el-tabs__item {
  border: none;
  border-right: 2px solid transparent;
  transition: all 0.3s;
}

.el-tabs--left .el-tabs__item.is-active {
  border-right: 2px solid #409eff;
  background-color: #f0f9ff;
}

.tab-content {
  height: 100%;
  overflow-y: auto;
}

.config-container {
  padding: 20px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.form-section {
  margin-bottom: 25px;
}

.form-section h4 {
  margin-bottom: 15px;
  color: #409eff;
  font-size: 18px;
  font-weight: 600;
  display: flex;
  align-items: center;
}

.form-section h4::before {
  content: '';
  width: 4px;
  height: 18px;
  background: #409eff;
  margin-right: 8px;
  border-radius: 2px;
}

.config-form {
  max-width: 600px;
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

.form-actions {
  text-align: center;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.save-btn, .reset-btn {
  margin: 0 10px;
  padding: 12px 24px;
  font-weight: 600;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.save-btn {
  background: #38bdf8;
  border-color: #38bdf8;
  box-shadow: 0 2px 8px rgba(56,189,248,0.25);
}

.save-btn:hover {
  background: #0ea5e9;
  border-color: #0ea5e9;
  box-shadow: 0 4px 12px rgba(56,189,248,0.35);
}

.reset-btn {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  color: #64748b;
}

.reset-btn:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
  color: #475569;
}

.saving-inline {
  display: inline-flex;
  align-items: center;
}

.circular-loading {
  width: 16px;
  height: 16px;
  border: 2px solid #e4e7ed;
  border-top: 2px solid #409eff;
  border-radius: 50%;
  margin-right: 8px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.stat-card {
  margin-top: 20px;
  max-width: 400px;
}

.stat-container {
  padding-left: 40px;
  padding-top: 20px;
}

.help-container {
  /* 隐藏右侧滚动条 */
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
  padding-left: 40px;
  padding-top: 20px;
  max-height: calc(100vh - 200px);
  overflow-y: auto;
  padding-bottom: 40px;
}

.custom-collapse-item {
  margin-bottom: 16px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.custom-collapse-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.custom-collapse-item :deep(.el-collapse-item__header) {
  background: #94a3b8;
  color: white;
  font-weight: 600;
  font-size: 16px;
  padding: 16px 20px;
  border: none;
  border-radius: 8px 8px 0 0;
  transition: all 0.3s ease;
}

.custom-collapse-item :deep(.el-collapse-item__header:hover) {
  background: #64748b;
}

.custom-collapse-item :deep(.el-collapse-item__content) {
  background: #f8fafc;
  padding: 20px;
  border-radius: 0 0 8px 8px;
  border: 1px solid #e2e8f0;
  border-top: none;
  overflow-y: visible;
}

/* 更新日志特殊样式 */
.update-log-item :deep(.el-collapse-item__content) {
  max-height: 220px;
  overflow-y: auto;
}

/* 隐藏更新日志内容区域的滚动条 */
.update-log-item :deep(.el-collapse-item__content)::-webkit-scrollbar {
  display: none;
}

.update-log-item :deep(.el-collapse-item__content) {
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
}

.custom-collapse-item :deep(.el-collapse-item__wrap) {
  border: none;
}

.custom-collapse-item :deep(.el-collapse-item__arrow) {
  color: white;
  font-weight: bold;
}

/* 自定义滚动条样式 */
.custom-collapse-item :deep(.el-collapse-item__content)::-webkit-scrollbar {
  width: 6px;
}

.custom-collapse-item :deep(.el-collapse-item__content)::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.custom-collapse-item :deep(.el-collapse-item__content)::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.custom-collapse-item :deep(.el-collapse-item__content)::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.stat-item:last-child {
  border-bottom: none;
}

.stat-label {
  font-weight: 500;
  color: #666;
}

.stat-value {
  font-weight: 600;
  color: #409eff;
  font-size: 18px;
}

h3 {
  margin-bottom: 16px;
  color: #333;
  font-size: 20px;
  font-weight: 600;
}

p {
  margin-bottom: 16px;
  line-height: 1.6;
  color: #666;
}

ul {
  padding-left: 20px;
  margin-bottom: 16px;
}

li {
  margin-bottom: 8px;
  color: #666;
}
</style> 