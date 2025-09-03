<template>
  <div class="ai-config-container">
    <el-tabs tab-position="left" style="height: calc(100vh - 80px)" class="demo-tabs">
      <el-tab-pane label="模型配置">
        <div class="tab-content">
          <div class="config-container">
            <div class="config-layout">
              <div class="config-left">
        <el-form 
          :model="configForm" 
          :rules="configRules" 
          ref="configFormRef" 
          label-width="120px"
          class="config-form"
        >
              <div class="form-section">
                <h4>基础信息</h4>
                    <el-form-item label="配置名称" prop="configName">
                      <el-input 
                        v-model="configForm.configName" 
                        placeholder="请输入配置名称"
                        class="config-input"
                      />
                    </el-form-item>
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
                    <span>保存配置</span>
              </template>
            </el-button>
                <el-button @click="resetConfig" :disabled="saving" class="reset-btn">重置</el-button>
          </el-form-item>
        </el-form>
          </div>
              <div class="config-right">
                <div class="form-section">
                  <h4>配置列表</h4>
                  <div class="config-list">
                    <div v-if="configList.length === 0" class="empty-list">
                      <p>暂无配置</p>
                    </div>
                    <div v-else class="config-items">
                      <div class="config-header">
                        <div class="config-name">配置名称</div>
                        <div class="config-info">
                          <div class="model-type-container">
                            <span>模型类型</span>
                          </div>
                          <div class="model-version">模型版本</div>
                          <div class="config-time">更新时间</div>
                          <div class="header-enabled">启用状态</div>
                          <div class="config-actions">操作</div>
                        </div>
                      </div>
                      <div 
                        v-for="config in configList" 
                        :key="config.id" 
                        class="config-item"
                      >
                        <div class="config-name">{{ config.config_name }}</div>
                        <div class="config-info">
                          <div class="model-type-container">
                            <span class="model-type" :style="{ 
                              backgroundColor: getModelTypeInfo(config.model_type).bgColor, 
                              color: getModelTypeInfo(config.model_type).color 
                            }">
                              {{ getModelTypeInfo(config.model_type).name }}
                            </span>
                          </div>
                          <div class="model-version">{{ config.model_version }}</div>
                          <div class="config-time">{{ formatTime(config.updated_at) }}</div>
                          <div class="config-enabled">
                            <el-switch 
                              :model-value="Boolean(config.is_enabled)" 
                              @update:model-value="(value) => toggleConfigEnabled(config, value)"
                              size="small"
                              class="animated-switch"
                            />
                          </div>
                          <div class="config-actions">
                            <el-button size="small" type="success" @click="viewConfig(config)" class="action-btn view-btn">查看</el-button>
                            <el-button size="small" type="primary" @click="editConfig(config)" class="action-btn edit-btn">编辑</el-button>
                            <el-popconfirm
                              title="确定要删除这个配置吗？"
                              confirm-button-text="确定"
                              cancel-button-text="取消"
                              placement="left-end"
                              @confirm="deleteConfig(config)"
                            >
                              <template #reference>
                                <el-button size="small" type="danger" class="action-btn delete-btn">删除</el-button>
                              </template>
                            </el-popconfirm>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
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
                <p><strong>V1.0.9 (2025-09-03)</strong></p>
                <ul>
                  <li>更新AI模型多配置</li>
                </ul>
                <p><strong>V1.0.8 (2025-09-02)</strong></p>
                <ul>
                  <li>优化AI生成用例系统，支持Windows、macOS、Linux跨平台运行</li>
                  <li>改进subprocess命令执行机制，提升跨平台兼容性</li>
                  <li>增强错误处理和调试信息，便于问题诊断</li>
                </ul>
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
    
    <!-- 查看配置详情对话框 -->
    <el-dialog
      v-model="viewDialogVisible"
      width="600px"
      :close-on-click-modal="false"
      :close-on-press-escape="true"
    >
      <div class="config-detail">
        <div class="detail-section">
          <h4>基础信息</h4>
          <div class="detail-item">
            <label>配置名称：</label>
            <span>{{ viewConfigData.configName }}</span>
          </div>
          <div class="detail-item">
            <label>模型类型：</label>
            <span class="model-type-tag" :style="{ 
              backgroundColor: getModelTypeInfo(viewConfigData.modelType).bgColor, 
              color: getModelTypeInfo(viewConfigData.modelType).color 
            }">
              {{ getModelTypeInfo(viewConfigData.modelType).name }}
            </span>
          </div>
          <div class="detail-item">
            <label>模型版本：</label>
            <span>{{ viewConfigData.modelVersion }}</span>
          </div>
          <div class="detail-item">
            <label>API密钥：</label>
            <span class="api-key">{{ viewConfigData.apiKey }}</span>
          </div>
          <div class="detail-item">
            <label>模型URL：</label>
            <span class="url-text">{{ viewConfigData.baseUrl }}</span>
          </div>
        </div>
        
        <div class="detail-section">
          <h4>价格配置</h4>
          <div class="detail-item">
            <label>输入价格：</label>
            <span>{{ viewConfigData.promptPrice }} CNY / 1000 tokens</span>
          </div>
          <div class="detail-item">
            <label>输出价格：</label>
            <span>{{ viewConfigData.completionPrice }} CNY / 1000 tokens</span>
          </div>
        </div>
        
        <div class="detail-section">
          <h4>状态信息</h4>
          <div class="detail-item">
            <label>启用状态：</label>
            <el-tag :type="viewConfigData.isEnabled ? 'success' : 'info'">
              {{ viewConfigData.isEnabled ? '启用' : '禁用' }}
            </el-tag>
          </div>
          <div class="detail-item">
            <label>创建时间：</label>
            <span>{{ formatTime(viewConfigData.createdAt) }}</span>
          </div>
          <div class="detail-item">
            <label>更新时间：</label>
            <span>{{ formatTime(viewConfigData.updatedAt) }}</span>
          </div>
        </div>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="viewDialogVisible = false">关闭</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Setting } from '@element-plus/icons-vue';

// 响应式数据
const configFormRef = ref();
const saving = ref(false);
const configList = ref([]);
const viewDialogVisible = ref(false);
const viewConfigData = ref({});

const configForm = reactive({
  configId: null,
  configName: '',
  modelType: 'qwen',
  apiKey: '',
  baseUrl: '',
  modelVersion: '',
  promptPrice: '',
  completionPrice: ''
});

// 表单验证规则
const configRules = {
  configName: [
    { required: true, message: '请输入配置名称', trigger: 'blur' }
  ],
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
  // 初始化表单为空，只有模型类型默认为通义千问
  resetFormToDefault();
  // 加载配置列表
  await loadConfigList();
});

// 加载配置列表
const loadConfigList = async () => {
  try {
    const response = await fetch('/api/ai_configs?include_sensitive=true');
    const result = await response.json();
    
    if (result.success) {
      configList.value = result.data || [];
    } else {
      console.error('加载配置列表失败:', result.message);
    }
  } catch (error) {
    console.error('加载配置列表失败:', error);
  }
};

// 获取模型类型中文名称和颜色
const getModelTypeInfo = (modelType) => {
  const modelInfo = {
    'qwen': { name: '通义千问', color: '#ff6b35', bgColor: '#fff2ed' },
    'volcengine': { name: '字节跳动（火山引擎）', color: '#000000', bgColor: '#f5f5f5' },
    'deepseek': { name: 'DeepSeek', color: '#6366f1', bgColor: '#eef2ff' },
    'zhipu': { name: '智谱AI', color: '#059669', bgColor: '#ecfdf5' },
    'openai': { name: 'OpenAI', color: '#10b981', bgColor: '#ecfdf5' },
    'wenxin': { name: '百度文心一言', color: '#3b82f6', bgColor: '#eff6ff' },
    'xunfei': { name: '讯飞星火', color: '#f59e0b', bgColor: '#fffbeb' },
    'minimax': { name: 'MiniMax', color: '#8b5cf6', bgColor: '#f3f4f6' },
    'moonshot': { name: '月之暗面', color: '#6366f1', bgColor: '#eef2ff' },
    '360': { name: '360智脑', color: '#059669', bgColor: '#ecfdf5' },
    'claude': { name: 'Claude (Anthropic)', color: '#dc2626', bgColor: '#fef2f2' },
    'gemini': { name: 'Gemini (Google)', color: '#ea4335', bgColor: '#fef2f2' }
  };
  return modelInfo[modelType] || { name: modelType, color: '#6b7280', bgColor: '#f9fafb' };
};

// 格式化时间
const formatTime = (timeStr) => {
  if (!timeStr) return '';
  const date = new Date(timeStr);
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
};

// 查看配置
const viewConfig = async (config) => {
  try {
    console.log('查看配置:', config);
    
    const response = await fetch(`/api/ai_config/${config.id}`);
    const result = await response.json();
    
    if (result.success) {
      viewConfigData.value = result.data;
      viewDialogVisible.value = true;
    } else {
      ElMessage.error(result.message || '获取配置详情失败');
    }
  } catch (error) {
    console.error('获取配置详情失败:', error);
    ElMessage.error('获取配置详情失败');
  }
};

// 编辑配置
const editConfig = (config) => {
  console.log('编辑配置:', config);
  // 将选中的配置填充到表单中
  configForm.configId = config.id; // 添加配置ID
  configForm.configName = config.config_name;
  configForm.modelType = config.model_type;
  configForm.apiKey = config.api_key;
  configForm.baseUrl = config.model_url;
  configForm.modelVersion = config.model_version;
  configForm.promptPrice = config.prompt_price_per_1k;
  configForm.completionPrice = config.completion_price_per_1k;
  
  ElMessage.success('配置已加载到表单中，请修改后保存');
};

// 删除配置
const deleteConfig = async (config) => {
  try {
    console.log('删除配置:', config);
    
    const response = await fetch(`/api/ai_config/${config.id}/delete`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      }
    });
    
    const result = await response.json();
    
    if (result.success) {
      ElMessage.success(result.message);
      // 刷新配置列表
      await loadConfigList();
    } else {
      ElMessage.error(result.message);
    }
  } catch (error) {
    console.error('删除配置失败:', error);
    ElMessage.error('删除配置失败');
  }
};

// 切换配置启用状态
const toggleConfigEnabled = async (config, newValue) => {
  try {
    console.log('切换配置启用状态:', config, '新值:', newValue);
    
    // 如果要启用，先禁用所有其他配置
    if (newValue) {
      // 找到所有已启用的配置（除了当前配置）
      const otherEnabledConfigs = configList.value.filter(c => c.is_enabled && c.id !== config.id);
      
      if (otherEnabledConfigs.length > 0) {
        // 显示提示信息
        ElMessage.info('正在切换配置，请稍候...');
        
        // 先禁用其他已启用的配置
        for (const otherConfig of otherEnabledConfigs) {
          try {
            const disableResponse = await fetch(`/api/ai_config/${otherConfig.id}/toggle_enabled`, {
              method: 'PUT',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                enabled: false
              })
            });
            
            const disableResult = await disableResponse.json();
            if (!disableResult.success) {
              console.error('禁用其他配置失败:', disableResult.message);
            }
          } catch (error) {
            console.error('禁用其他配置失败:', error);
          }
        }
      }
    }
    
    // 然后切换当前配置的状态
    const response = await fetch(`/api/ai_config/${config.id}/toggle_enabled`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        enabled: newValue
      })
    });
    
    const result = await response.json();
    
    if (result.success) {
      ElMessage.success(result.message);
      // 刷新配置列表以获取最新状态
      await loadConfigList();
    } else {
      ElMessage.error(result.message);
    }
  } catch (error) {
    console.error('切换启用状态失败:', error);
    ElMessage.error('切换启用状态失败');
  }
};

// 重置表单为默认状态
const resetFormToDefault = () => {
  configForm.configId = null;
  configForm.configName = '';
  configForm.modelType = 'qwen';
  configForm.apiKey = '';
  configForm.baseUrl = '';
  configForm.modelVersion = '';
  configForm.promptPrice = '';
  configForm.completionPrice = '';
};

// 加载配置（暂时注释掉，后续从配置列表中选择时调用）
// const loadConfig = async () => {
//   try {
//     const response = await fetch('/api/ai_config');
//     const result = await response.json();
//     
//     if (result.success && result.data) {
//       // 填充表单数据
//       configForm.modelType = result.data.modelType || 'qwen';
//       configForm.apiKey = result.data.apiKey || '';
//       configForm.baseUrl = result.data.baseUrl || '';
//       configForm.modelVersion = result.data.modelVersion || '';
//       configForm.promptPrice = result.data.promptPrice || '0.001';
//       configForm.completionPrice = result.data.completionPrice || '0.002';
//     }
//   } catch (error) {
//     console.error('加载配置失败:', error);
//     ElMessage.error('加载配置失败');
//   }
// };

// 保存配置
const saveConfig = async () => {
  try {
    await configFormRef.value.validate();
    saving.value = true;
    
    const isEdit = configForm.configId !== null;
    const url = isEdit ? `/api/ai_config/${configForm.configId}` : '/api/ai_config';
    const method = isEdit ? 'PUT' : 'POST';
    
    const response = await fetch(url, {
      method: method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        configId: configForm.configId,
        configName: configForm.configName,
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
      ElMessage.success(isEdit ? '配置更新成功！' : '配置保存成功！');
      // 保存成功后清空表单
      resetFormToDefault();
      // 刷新配置列表
      await loadConfigList();
    } else {
      // 显示具体的验证错误信息
      if (result.errors) {
        // 显示所有验证错误
        const errorMessages = Object.values(result.errors);
        if (errorMessages.length === 1) {
          ElMessage.error(errorMessages[0]);
        } else {
          // 如果有多个错误，显示所有错误
          const errorText = errorMessages.join('；');
          ElMessage.error(`验证失败：${errorText}`);
          console.error('所有验证错误:', result.errors);
        }
    } else {
      ElMessage.error(result.message || '配置保存失败');
      }
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
    resetFormToDefault();
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
  height: 100%;
  display: flex;
  flex-direction: column;
}

.config-layout {
  display: flex;
  gap: 30px;
  height: 100%;
}

.config-left {
  flex: 1;
  max-width: 620px;
  display: flex;
  flex-direction: column;
}

.config-right {
  flex: 1;
  max-width: 800px;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.config-right {
  flex: 1;
  max-width: 800px;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.config-list {
  margin-top: 15px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.config-list {
  margin-top: 15px;
}

.empty-list {
  text-align: center;
  padding: 40px 20px;
  color: #999;
  font-size: 14px;
}

.config-items {
  height: calc(100vh - 300px);
  overflow-y: auto;
  /* 隐藏滚动条 */
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}

/* 隐藏 Webkit 浏览器的滚动条 */
.config-items::-webkit-scrollbar {
  display: none;
}

.config-header {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  background-color: #f1f5f9;
  border-bottom: 2px solid #e2e8f0;
  font-weight: 600;
  color: #475569;
  font-size: 13px;
}

.header-name {
  flex: 0 0 150px;
}

.header-info {
  display: flex;
  align-items: center;
  font-size: 12px;
  flex: 1;
}

.config-header .config-name {
  font-weight: 600;
  color: #475569;
  font-size: 13px;
  flex: 0 0 120px;
  padding-right: 8px;
}

.header-model-type {
  width: 140px;
  text-align: left;
  display: flex;
  align-items: center;
  padding-right: 8px;
}

.header-model-version {
  width: 90px;
  text-align: left;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding-right: 8px;
}

.header-update-time {
  width: 120px;
  text-align: left;
}

.header-enabled {
  width: 80px;
  text-align: center;
}

.header-actions {
  width: 140px;
  text-align: left;
}

.config-item {
  display: flex;
  align-items: center;
  padding: 12px 15px;
  border-bottom: 1px solid #e2e8f0;
  transition: background-color 0.3s ease;
}

.config-item:hover {
  background-color: #f8fafc;
}

.config-item:last-child {
  border-bottom: none;
}

.config-name {
  font-weight: 600;
  color: #1e293b;
  font-size: 14px;
  flex: 0 0 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding-right: 8px;
}

.config-info {
  display: flex;
  align-items: center;
  font-size: 12px;
  flex: 1;
}

.model-type-container {
  width: 140px;
  display: flex;
  align-items: center;
  padding-right: 8px;
}

.model-type {
  padding: 2px 6px;
  border-radius: 3px;
  white-space: nowrap;
  text-align: left;
  display: inline-block;
  font-size: 12px;
  font-weight: 500;
}

.model-version {
  color: #64748b;
  white-space: nowrap;
  width: 90px;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-right: 8px;
}

.config-time {
  color: #94a3b8;
  white-space: nowrap;
  width: 120px;
}

.config-enabled {
  width: 80px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.config-actions {
  width: 140px;
  display: flex;
  gap: 6px;
}

/* 自定义按钮样式 */
.action-btn {
  font-weight: 500;
}

.view-btn {
  background-color: #10b981 !important;
  border-color: #10b981 !important;
  color: white !important;
}

.view-btn:hover {
  background-color: #059669 !important;
  border-color: #059669 !important;
}

.edit-btn {
  background-color: #409eff !important;
  border-color: #409eff !important;
  color: white !important;
}

.edit-btn:hover {
  background-color: #337ecc !important;
  border-color: #337ecc !important;
}

.delete-btn {
  background-color: #dc2626 !important;
  border-color: #dc2626 !important;
  color: white !important;
}

.delete-btn:hover {
  background-color: #b91c1c !important;
  border-color: #b91c1c !important;
}

/* 气泡确认框样式优化 */
:deep(.el-popconfirm) {
  .el-popconfirm__main {
    padding: 12px 16px;
  }
  
  .el-popconfirm__title {
    font-size: 14px;
    color: #374151;
    margin-bottom: 8px;
  }
  
  .el-popconfirm__action {
    margin-top: 12px;
  }
  
  .el-button {
    padding: 6px 12px;
    font-size: 12px;
  }
}

/* 配置详情对话框样式 */
.config-detail {
  padding: 0;
}

.detail-section {
  margin-bottom: 24px;
}

.detail-section:last-child {
  margin-bottom: 0;
}

.detail-section h4 {
  margin-bottom: 16px;
  color: #409eff;
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 8px;
}

.detail-section h4::before {
  content: '';
  width: 3px;
  height: 16px;
  background: #409eff;
  margin-right: 8px;
  border-radius: 2px;
}

.detail-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 12px;
  line-height: 1.6;
}

.detail-item:last-child {
  margin-bottom: 0;
}

.detail-item label {
  width: 100px;
  font-weight: 600;
  color: #374151;
  flex-shrink: 0;
}

.detail-item span {
  color: #64748b;
  word-break: break-all;
}

.detail-item .api-key {
  font-family: 'Courier New', monospace;
  background: #f1f5f9;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
}

.detail-item .url-text {
  font-family: 'Courier New', monospace;
  background: #f1f5f9;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  word-break: break-all;
}

.detail-item .model-type-tag {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  display: inline-block;
}

.dialog-footer {
  text-align: center;
}

/* 开关动画效果 */
.animated-switch {
  transition: all 0.3s ease;
}

:deep(.animated-switch .el-switch__core) {
  transition: all 0.3s ease;
}

:deep(.animated-switch .el-switch__action) {
  transition: all 0.3s ease;
}

:deep(.animated-switch.is-checked .el-switch__core) {
  background-color: #10b981;
  border-color: #10b981;
}

:deep(.animated-switch:not(.is-checked) .el-switch__core) {
  background-color: #d1d5db;
  border-color: #d1d5db;
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