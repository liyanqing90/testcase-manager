<template>
    <div class="factory-content">
    <!-- 数据生成器 -->
    <div class="data-generator">


      <!-- 主要内容区域 -->
      <div class="main-content">
        <!-- 左侧：数据结构配置 -->
        <div class="config-section data-structure-section">
          <div class="section-header">
            <h3>数据结构配置</h3>
            <el-button type="primary" @click="addField" class="add-btn">
                  <el-icon><Plus /></el-icon>
                  添加字段
                </el-button>
              </div>
              
          <!-- 字段列表 -->
          <div v-if="dataStructure.length > 0" class="field-list">
                <div v-for="(field, index) in dataStructure" :key="index" class="field-item">
              <!-- 字段基本信息 -->
              <div class="field-basic">
                    <el-input 
                      v-model="field.name" 
                      placeholder="字段名称"
                      class="field-name"
                    />
                    <el-select 
                      v-model="field.type" 
                      placeholder="数据类型"
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
                      type="danger" 
                      @click="removeField(index)"
                  class="remove-btn"
                  circle
                    >
                      <el-icon><Delete /></el-icon>
                    </el-button>
                  </div>
                  
                  <!-- 字段配置选项 -->
              <div v-if="field.type === 'string'" class="field-options">
                <div class="option-item">
                  <label class="option-label">
                    字符串格式
                    <el-tooltip content="选择生成字符串的类型，比如选择'姓名'会生成真实的中文姓名，选择'邮箱'会生成有效的邮箱地址" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-select v-model="field.stringFormat" placeholder="选择字符串格式" class="option-input">
                    <el-option label="随机字符串" value="random" />
                    <el-option label="姓名" value="name" />
                    <el-option label="邮箱" value="email" />
                    <el-option label="手机号" value="phone" />
                    <el-option label="身份证号" value="idcard" />
                    <el-option label="地址" value="address" />
                    <el-option label="公司名" value="company" />
                    <el-option label="职位" value="job" />
                    <el-option label="URL" value="url" />
                    <el-option label="IP地址" value="ip" />
                    <el-option label="银行卡号" value="bankcard" />
                    <el-option label="车牌号" value="license" />
                  </el-select>
                </div>
                <div class="option-item">
                  <label class="option-label">
                    最小长度
                    <el-tooltip content="设置生成字符串的最短长度，比如设置为3，生成的字符串至少3个字符" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                    <el-input 
                      v-model="field.minLength" 
                    placeholder="请输入最小长度"
                      type="number"
                    class="option-input"
                  />
                </div>
                <div class="option-item">
                  <label class="option-label">
                    最大长度
                    <el-tooltip content="设置生成字符串的最长长度，比如设置为20，生成的字符串最多20个字符" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                    <el-input 
                      v-model="field.maxLength" 
                    placeholder="请输入最大长度"
                      type="number"
                    class="option-input"
                  />
                </div>
                <div class="option-item">
                  <label class="option-label">
                    正则表达式
                    <el-tooltip content="用正则表达式限制字符串格式，比如^[A-Za-z]+$表示只能包含英文字母" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                    <el-input 
                      v-model="field.pattern" 
                    placeholder="请输入正则表达式"
                    class="option-input"
                  />
                </div>
                <div class="option-item">
                  <label class="option-label">
                    前缀
                    <el-tooltip content="在生成的字符串前面添加固定内容，比如设置'USER_'，生成的字符串会是'USER_abc123'" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-input 
                    v-model="field.prefix" 
                    placeholder="请输入字符串前缀"
                    class="option-input"
                  />
                </div>
                <div class="option-item">
                  <label class="option-label">
                    后缀
                    <el-tooltip content="在生成的字符串后面添加固定内容，比如设置'_END'，生成的字符串会是'abc123_END'" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-input 
                    v-model="field.suffix" 
                    placeholder="请输入字符串后缀"
                    class="option-input"
                  />
                </div>
                <div class="option-item">
                  <label class="option-label">
                    字符集
                    <el-tooltip content="选择生成字符串使用的字符类型，比如选择'数字'只会生成0-9的字符串" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-select v-model="field.charSet" placeholder="选择字符集" class="option-input">
                    <el-option label="数字" value="numeric" />
                    <el-option label="字母" value="alpha" />
                    <el-option label="数字+字母" value="alphanumeric" />
                    <el-option label="数字+字母+符号" value="all" />
                    <el-option label="中文" value="chinese" />
                    <el-option label="自定义" value="custom" />
                  </el-select>
                </div>
                <div v-if="field.charSet === 'custom'" class="option-item">
                  <label class="option-label">
                    自定义字符集
                    <el-tooltip content="当选择'自定义'字符集时，在这里输入你想要的字符，比如'ABCD123'，生成的字符串只会包含这些字符" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-input 
                    v-model="field.customCharSet" 
                    placeholder="请输入自定义字符集"
                    class="option-input"
                    />
                  </div>
                  
                <!-- 通用配置 -->
                <div class="option-item">
                  <label class="option-label">
                    是否必填
                    <el-tooltip content="开启后，该字段不会生成空值；关闭后，可能会生成null或空字符串" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-switch v-model="field.required" />
                </div>
              </div>

              <div v-if="field.type === 'number'" class="field-options">
                <div class="option-item">
                  <label class="option-label">
                    数字格式
                    <el-tooltip content="选择生成数字的方式，比如'递增序列'会生成1,2,3,4...，'随机数'配合精度控制生成整数或小数" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-select v-model="field.numberFormat" placeholder="选择数字格式" class="option-input">
                    <el-option label="随机数" value="random" />
                    <el-option label="递增序列" value="increment" />
                    <el-option label="递减序列" value="decrement" />
                    <el-option label="价格" value="price" />
                    <el-option label="百分比" value="percentage" />
                    <el-option label="年龄" value="age" />
                    <el-option label="数量" value="quantity" />
                    <el-option label="ID" value="id" />
                    <el-option label="评分" value="rating" />
                    <el-option label="金额" value="amount" />
                    <el-option label="权重" value="weight" />
                  </el-select>
                </div>
                <div class="option-item">
                  <label class="option-label">
                    最小值
                    <el-tooltip content="设置生成数字的下限，比如设置为1，生成的数字不会小于1" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                    <el-input 
                      v-model="field.min" 
                    placeholder="请输入最小值"
                      type="number"
                    class="option-input"
                  />
                </div>
                <div class="option-item">
                  <label class="option-label">
                    最大值
                    <el-tooltip content="设置生成数字的上限，比如设置为100，生成的数字不会大于100" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                    <el-input 
                      v-model="field.max" 
                    placeholder="请输入最大值"
                      type="number"
                    class="option-input"
                  />
                </div>

                <div v-if="field.numberFormat === 'increment' || field.numberFormat === 'decrement'" class="option-item">
                  <label class="option-label">
                    起始值
                    <el-tooltip content="递增或递减序列的第一个数字，比如设置为10，递增序列会从10开始：10,11,12,13..." placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                    <el-input 
                    v-model="field.startValue" 
                    placeholder="请输入起始值"
                      type="number"
                    class="option-input"
                  />
                </div>
                <div v-if="field.numberFormat === 'increment' || field.numberFormat === 'decrement'" class="option-item">
                  <label class="option-label">
                    步长
                    <el-tooltip content="递增或递减序列中相邻数字的差值，比如设置为2，递增序列会是：1,3,5,7,9..." placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-input 
                    v-model="field.step" 
                    placeholder="请输入步长"
                    type="number"
                    class="option-input"
                  />
                </div>
                <div class="option-item">
                  <label class="option-label">
                    精度
                    <el-tooltip content="控制数字的小数位数，选择'整数'生成1,2,3，选择'2位小数'生成12.34，选择'3位小数'生成12.345" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-select v-model="field.precision" placeholder="选择精度" class="option-input">
                    <el-option label="整数" value="integer" />
                    <el-option label="1位小数" value="1" />
                    <el-option label="2位小数" value="2" />
                    <el-option label="3位小数" value="3" />
                    <el-option label="4位小数" value="4" />
                  </el-select>
                  </div>
                  
                <!-- 通用配置 -->
                <div class="option-item">
                  <label class="option-label">
                    是否必填
                    <el-tooltip content="开启后，该字段不会生成空值；关闭后，可能会生成null或0" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-switch v-model="field.required" />
                </div>
              </div>

              <div v-if="field.type === 'boolean'" class="field-options">
                <div class="option-item">
                  <label class="option-label">
                    布尔值分布
                    <el-tooltip content="控制生成的真值和假值的比例，比如选择'70% 真，30% 假'，生成100个值中大约70个是true，30个是false" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-select v-model="field.booleanDistribution" placeholder="选择布尔值分布" class="option-input">
                    <el-option label="50% 真/假" value="50_50" />
                    <el-option label="70% 真，30% 假" value="70_30" />
                    <el-option label="30% 真，70% 假" value="30_70" />
                    <el-option label="90% 真，10% 假" value="90_10" />
                    <el-option label="10% 真，90% 假" value="10_90" />
                    <el-option label="自定义比例" value="custom" />
                  </el-select>
                </div>
                <div v-if="field.booleanDistribution === 'custom'" class="option-item">
                  <label class="option-label">
                    真值概率 (%)
                    <el-tooltip content="当选择'自定义比例'时，设置true值出现的百分比，比如设置为75，表示75%的值是true，25%是false" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-input-number 
                    v-model="field.trueProbability" 
                    :min="0" 
                    :max="100"
                    placeholder="请输入真值概率"
                    class="option-input"
                  />
                </div>
                <div class="option-item">
                  <label class="option-label">
                    显示格式
                    <el-tooltip content="选择布尔值的显示方式，比如选择'是/否'，true会显示为'是'，false会显示为'否'" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-select v-model="field.booleanFormat" placeholder="选择显示格式" class="option-input">
                    <el-option label="true/false" value="true_false" />
                    <el-option label="1/0" value="1_0" />
                    <el-option label="是/否" value="yes_no" />
                    <el-option label="Y/N" value="Y_N" />
                    <el-option label="✓/✗" value="check_cross" />
                    <el-option label="对/错" value="right_wrong" />
                  </el-select>
                </div>
                <div class="option-item">
                  <label class="option-label">
                    是否允许空值
                    <el-tooltip content="开启后，除了true和false，还会生成null值，增加数据的多样性" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-switch v-model="field.allowNull" />
                </div>
                
                <!-- 通用配置 -->
                <div class="option-item">
                  <label class="option-label">
                    是否必填
                    <el-tooltip content="开启后，该字段不会生成空值；关闭后，可能会生成null值" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-switch v-model="field.required" />
                </div>
              </div>

              <div v-if="field.type === 'enum'" class="field-options">
                  <div class="enum-container">
                    <div class="enum-list-section">
                      <div class="enum-header">
                        <span class="enum-title">枚举值列表</span>
                        <span class="enum-count">{{ field.enumValues.length }} 个值</span>
                      </div>
                                            <div class="enum-values">
                        <div class="enum-container-border">
                          <div v-if="field.enumValues.length === 0" class="enum-empty">
                            <el-icon class="enum-empty-icon"><InfoFilled /></el-icon>
                            <span>暂无枚举值，点击右侧添加</span>
                          </div>
                          <div v-else class="enum-tags-container">
                    <el-tag 
                      v-for="(value, idx) in field.enumValues" 
                              :key="`${field.name}-${idx}-${value}`"
                      closable
                      @close="removeEnumValue(field, idx)"
                      class="enum-tag"
                              :class="{ 'removing': field.removingIndex === idx }"
                    >
                      {{ value }}
                    </el-tag>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div class="enum-divider"></div>
                    
                    <div class="enum-add-section">
                      <div class="enum-add-header">
                        <span>添加新值</span>
                        <el-tooltip content="枚举值用于限制字段的可选值范围，比如性别字段可以设置'男'、'女'两个枚举值，生成的数据只会包含这些预设值" placement="top">
                          <el-icon class="help-icon"><InfoFilled /></el-icon>
                        </el-tooltip>
                      </div>
                      <div class="enum-input-group">
                    <el-input 
                      v-model="newEnumValue" 
                          placeholder="输入枚举值"
                      @keyup.enter="addEnumValue(field)"
                      class="enum-input"
                    />
                        <el-button @click="addEnumValue(field)" type="success" size="small">
                          添加
                        </el-button>
                  </div>
                  
                  <!-- 通用配置 -->
                  <div class="option-item" style="margin-top: 16px;">
                    <label class="option-label">
                      是否必填
                      <el-tooltip content="开启后，该字段不会生成空值；关闭后，可能会生成null值" placement="top">
                        <el-icon class="help-icon"><InfoFilled /></el-icon>
                      </el-tooltip>
                    </label>
                    <el-switch v-model="field.required" />
                </div>
              </div>
            </div>
          </div>

            <div v-if="field.type === 'date'" class="field-options">
                <div class="option-item">
                  <label class="option-label">
                    日期格式
                    <el-tooltip content="选择日期的显示格式，比如'YYYY-MM-DD'会显示为'2024-01-15'，'YYYY年MM月DD日'会显示为'2024年01月15日'" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-select v-model="field.dateFormat" placeholder="选择日期格式" class="option-input">
                    <el-option label="YYYY-MM-DD" value="YYYY-MM-DD" />
                    <el-option label="MM/DD/YYYY" value="MM/DD/YYYY" />
                    <el-option label="DD/MM/YYYY" value="DD/MM/YYYY" />
                    <el-option label="YYYY年MM月DD日" value="YYYY年MM月DD日" />
                    <el-option label="时间戳" value="timestamp" />
                    <el-option label="ISO格式" value="iso" />
                    <el-option label="Unix时间戳" value="unix" />
                    <el-option label="相对时间" value="relative" />
                  </el-select>
                </div>
                <div class="option-item">
                  <label class="option-label">
                    开始日期
                    <el-tooltip content="设置生成日期的起始时间，生成的日期不会早于这个时间" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-date-picker
                    v-model="field.startDate"
                    type="date"
                    placeholder="请选择开始日期"
                    class="option-input"
                  />
                </div>
                <div class="option-item">
                  <label class="option-label">
                    结束日期
                    <el-tooltip content="设置生成日期的结束时间，生成的日期不会晚于这个时间" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-date-picker
                    v-model="field.endDate"
                    type="date"
                    placeholder="请选择结束日期"
                    class="option-input"
                  />
                </div>
                <div class="option-item">
                  <label class="option-label">
                    是否包含时间
                    <el-tooltip content="开启后生成的日期会包含具体时间，比如'2024-01-15 14:30:25'" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-switch v-model="field.includeTime" />
                </div>
                <div v-if="field.includeTime" class="option-item">
                  <label class="option-label">
                    时间精度
                    <el-tooltip content="选择时间的精确程度，比如选择'毫秒'会生成'14:30:25.123'这样的时间" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-select v-model="field.timePrecision" placeholder="选择时间精度" class="option-input">
                    <el-option label="秒" value="second" />
                    <el-option label="毫秒" value="millisecond" />
                    <el-option label="微秒" value="microsecond" />
                  </el-select>
                </div>
                <div class="option-item">
                  <label class="option-label">
                    日期分布
                    <el-tooltip content="控制生成日期的分布方式，比如'工作日优先'会生成更多的周一到周五的日期" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-select v-model="field.dateDistribution" placeholder="选择日期分布" class="option-input">
                    <el-option label="均匀分布" value="uniform" />
                    <el-option label="最近优先" value="recent" />
                    <el-option label="历史优先" value="historical" />
                    <el-option label="工作日优先" value="workday" />
                    <el-option label="周末优先" value="weekend" />
                  </el-select>
              </div>
              
                <!-- 通用配置 -->
                <div class="option-item">
                  <label class="option-label">
                    是否必填
                    <el-tooltip content="开启后，该字段不会生成空值；关闭后，可能会生成null或空日期" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-switch v-model="field.required" />
                </div>
              </div>

              <div v-if="field.type === 'custom'" class="field-options">
                <div class="option-item">
                  <label class="option-label">
                    自定义表达式
                    <el-tooltip content="使用JavaScript代码自定义数据生成逻辑，比如'return field1 + field2'表示返回两个字段的和" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-input 
                    v-model="field.customExpression" 
                    type="textarea"
                    :rows="3"
                    placeholder="请输入自定义表达式，支持JavaScript语法"
                    class="option-input"
                  />
                </div>
                <div class="option-item">
                  <label class="option-label">
                    依赖字段
                    <el-tooltip content="选择这个自定义字段需要依赖的其他字段，比如计算总价时需要依赖单价和数量字段" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-select 
                    v-model="field.dependentFields" 
                    multiple
                    placeholder="选择依赖的字段（可选）"
                    class="option-input"
                  >
                    <el-option 
                      v-for="depField in dataStructure.filter(f => f.name && f.name !== field.name)" 
                      :key="depField.name"
                      :label="depField.name" 
                      :value="depField.name" 
                    />
                  </el-select>
                </div>
                <div class="option-item">
                  <label class="option-label">
                    数据类型
                    <el-tooltip content="指定自定义表达式返回的数据类型，确保生成的数据格式正确" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-select v-model="field.customDataType" placeholder="选择返回数据类型" class="option-input">
                    <el-option label="字符串" value="string" />
                    <el-option label="数字" value="number" />
                    <el-option label="布尔值" value="boolean" />
                    <el-option label="数组" value="array" />
                    <el-option label="对象" value="object" />
                    <el-option label="日期" value="date" />
                  </el-select>
                </div>
                <div class="option-item">
                  <label class="option-label">
                    验证规则
                    <el-tooltip content="用正则表达式验证生成的数据是否符合要求，比如验证邮箱格式、手机号格式等" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-input 
                    v-model="field.validationRule" 
                    placeholder="请输入验证规则（正则表达式）"
                    class="option-input"
                  />
                </div>
                <div class="option-item">
                  <label class="option-label">
                    错误提示
                    <el-tooltip content="当数据验证失败时显示的错误信息，帮助用户理解问题所在" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-input 
                    v-model="field.errorMessage" 
                    placeholder="请输入验证失败时的错误提示"
                    class="option-input"
                  />
                </div>
                
                <!-- 通用配置 -->
                <div class="option-item">
                  <label class="option-label">
                    是否必填
                    <el-tooltip content="开启后，该字段不会生成空值；关闭后，可能会生成null或空值" placement="top">
                      <el-icon class="help-icon"><InfoFilled /></el-icon>
                    </el-tooltip>
                  </label>
                  <el-switch v-model="field.required" />
                </div>
              </div>
            </div>
              </div>
              
          <!-- 空状态提示 -->
          <div v-if="dataStructure.length === 0" class="empty-state">
            <el-icon class="empty-icon"><Document /></el-icon>
            <p>还没有配置任何字段，点击"添加字段"开始配置</p>
          </div>
        </div>

                <!-- 右侧：生成配置 -->
        <div class="config-section generation-section">
          <div class="section-header">
            <h3>生成配置</h3>
          </div>
          
          <div class="generation-config">
            <el-form label-position="top" class="config-form">
              <el-form-item>
                <template #label>
                  生成数量
                  <el-tooltip content="设置要生成的数据条数，比如设置为100会生成100条测试数据" placement="top">
                    <el-icon class="help-icon"><InfoFilled /></el-icon>
                  </el-tooltip>
                </template>
              <el-input-number 
                    v-model="generationConfig.count" 
                :min="1" 
                  :max="10000"
                  placeholder="请输入生成数量"
                  class="config-input"
              />
            </el-form-item>
            
              <el-form-item>
                <template #label>
                  输出格式
                  <el-tooltip content="选择生成数据的文件格式，JSON适合程序读取，CSV适合Excel打开，Excel直接生成Excel文件" placement="top">
                    <el-icon class="help-icon"><InfoFilled /></el-icon>
                  </el-tooltip>
                </template>
                <el-select v-model="generationConfig.format" placeholder="选择输出格式" class="config-input">
                <el-option label="JSON" value="json" />
                <el-option label="CSV" value="csv" />
                <el-option label="Excel" value="excel" />
                <el-option label="SQL" value="sql" />
              </el-select>
            </el-form-item>
            
            <el-form-item>
                <template #label>
                  数据种子
                  <el-tooltip content="设置随机种子，相同种子会生成相同的数据，便于测试结果重现" placement="top">
                    <el-icon class="help-icon"><InfoFilled /></el-icon>
                  </el-tooltip>
                </template>
                  <el-input 
                  v-model="generationConfig.seed" 
                  placeholder="留空使用随机种子"
                  class="config-input"
                  />
            </el-form-item>
            
            <el-form-item>
                <template #label>
                  生成模式
                  <el-tooltip content="选择数据生成的方式，批量模式适合大量数据，实时模式适合少量数据预览" placement="top">
                    <el-icon class="help-icon"><InfoFilled /></el-icon>
                  </el-tooltip>
                </template>
                <el-select v-model="generationConfig.mode" placeholder="选择生成模式" class="config-input">
                  <el-option label="批量生成" value="batch" />
                  <el-option label="实时预览" value="realtime" />
                </el-select>
            </el-form-item>
            
            <el-form-item>
                <template #label>
                  数据质量
                  <el-tooltip content="控制生成数据的真实性和多样性，高质量数据更接近真实场景" placement="top">
                    <el-icon class="help-icon"><InfoFilled /></el-icon>
                  </el-tooltip>
                </template>
                <el-select v-model="generationConfig.quality" placeholder="选择数据质量" class="config-input">
                  <el-option label="标准质量" value="standard" />
                  <el-option label="高质量" value="high" />
                  <el-option label="真实场景" value="realistic" />
                </el-select>
            </el-form-item>
            
            <el-form-item>
                <template #label>
                  高级选项
                  <el-tooltip content="启用高级功能，如数据验证、重复检查、性能优化等" placement="top">
                    <el-icon class="help-icon"><InfoFilled /></el-icon>
                  </el-tooltip>
                </template>
                <div class="advanced-options">
                  <el-checkbox v-model="generationConfig.enableValidation">启用数据验证</el-checkbox>
                  <el-checkbox v-model="generationConfig.enableDeduplication">启用去重检查</el-checkbox>
                  <el-checkbox v-model="generationConfig.enablePerformance">启用性能优化</el-checkbox>
          </div>
            </el-form-item>
            
            <el-form-item>
                <el-button type="primary" @click="generateData" class="generate-btn" :loading="generating">
                  生成数据
                  </el-button>
            </el-form-item>
          </el-form>
          </div>
        </div>
      </div>

      <!-- 生成预览区域 -->
      <div class="preview-section">
        <div class="section-header">
          <h3>生成预览</h3>
          <div class="preview-info">
            <span v-if="hasPreviewData" class="preview-count">
              预览前 {{ previewData.table.length }} 条数据
              <span v-if="previewData.table.length < generationConfig.count" class="preview-note">
                (共生成 {{ generationConfig.count }} 条，导出后可查看全部)
              </span>
            </span>
          </div>
          <div class="preview-actions">
            <el-button type="success" size="small" @click="refreshPreview" :disabled="!hasPreviewData" class="refresh-btn">
              <el-icon><RefreshRight /></el-icon>
              刷新预览
            </el-button>
            <el-button type="primary" size="small" @click="exportPreview" :disabled="!hasPreviewData" class="export-btn">
              <el-icon><Download /></el-icon>
              导出数据
            </el-button>
            </div>
          </div>
          
                        <!-- 标签页导航 -->
        <div v-if="hasPreviewData" class="preview-tabs-nav">
          <div class="custom-tabs">
            <div 
              class="tab-item" 
              :class="{ 'active': previewActiveTab === 'json' }"
              @click="previewActiveTab = 'json'"
            >
              JSON
            </div>
            <div 
              class="tab-item" 
              :class="{ 'active': previewActiveTab === 'table' }"
              @click="previewActiveTab = 'table'"
            >
              表格
            </div>
            <div 
              class="tab-item" 
              :class="{ 'active': previewActiveTab === 'csv' }"
              @click="previewActiveTab = 'csv'"
            >
              CSV
            </div>
          </div>
        </div>

        <!-- 预览内容区域 -->
        <div class="preview-content">
          <div v-if="!hasPreviewData" class="preview-empty">
            <el-icon class="preview-empty-icon"><Document /></el-icon>
            <span>点击"生成数据"按钮开始生成预览</span>
    </div>
    
          <div v-else class="preview-data">
            <!-- JSON预览 -->
            <div v-if="previewActiveTab === 'json'" class="preview-code-container">
              <div class="preview-code">
                <pre>{{ previewData.json }}</pre>
            </div>
              </div>
            
                        <!-- 表格预览 -->
            <div v-else-if="previewActiveTab === 'table'" class="preview-table-container">
              <div class="preview-table">
                <el-table :data="previewData.table" border stripe height="100%">
                  <el-table-column 
                    v-for="column in previewData.columns" 
                    :key="column.prop"
                    :prop="column.prop" 
                    :label="column.label"
                    :width="column.width"
                  />
                </el-table>
              </div>
            </div>
            
            <!-- CSV预览 -->
            <div v-else-if="previewActiveTab === 'csv'" class="preview-csv-container">
              <div class="preview-csv">
                <div class="csv-header">
                  <span class="csv-info">CSV格式预览 (可直接复制到Excel)</span>
                  <el-button 
                    type="primary" 
                    size="small" 
                    @click="copyCSVToClipboard"
                    class="copy-csv-btn"
                  >
                    <el-icon><DocumentCopy /></el-icon>
                    复制CSV
                  </el-button>
                </div>
                <div class="csv-content">
                  <div class="csv-table">
                    <table>
                      <thead>
                        <tr>
                          <th v-for="column in previewData.columns" :key="column.prop">
                            {{ column.label }}
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(row, index) in previewData.table" :key="index">
                          <td v-for="column in previewData.columns" :key="column.prop">
                            {{ row[column.prop] !== null && row[column.prop] !== undefined ? row[column.prop] : '-' }}
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, nextTick } from 'vue';
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
  Monitor,
  InfoFilled,
  Download,
  DocumentCopy
} from '@element-plus/icons-vue';

// 数据结构配置
const dataStructure = ref([
  {
    name: '',
    type: 'number',
    numberFormat: 'random',
    min: 1,
    max: 999999,
    startValue: 1,
    step: 1,
    precision: 'integer',
    required: true,
    dateFormat: 'YYYY-MM-DD',
    includeTime: false,
    timePrecision: 'second',
    dateDistribution: 'uniform',
    booleanDistribution: '50_50',
    trueProbability: 50,
    booleanFormat: 'true_false',
    allowNull: false,
    customExpression: '',
    dependentFields: [],
    customDataType: 'string',
    validationRule: '',
    errorMessage: '',
    enumValues: [],
    startDate: null,
    endDate: null,
    removingIndex: undefined
  },
  {
    name: '',
    type: 'string',
    stringFormat: 'random',
    minLength: 3,
    maxLength: 20,
    pattern: '',
    prefix: '',
    suffix: '',
    charSet: 'alphanumeric',
    customCharSet: '',
    required: true,
    min: 0,
    max: 100,
    startValue: 1,
    step: 1,
    precision: 'integer',
    numberFormat: 'random',
    dateFormat: 'YYYY-MM-DD',
    includeTime: false,
    timePrecision: 'second',
    dateDistribution: 'uniform',
    booleanDistribution: '50_50',
    trueProbability: 50,
    booleanFormat: 'true_false',
    allowNull: false,
    customExpression: '',
    dependentFields: [],
    customDataType: 'string',
    validationRule: '',
    errorMessage: '',
    enumValues: [],
    startDate: null,
    endDate: null,
    removingIndex: undefined
  }
]);
const newEnumValue = ref('');

// 生成配置
const generationConfig = reactive({
  count: 100,
  format: 'json',
  seed: '',
  mode: 'batch',
  quality: 'standard',
  enableValidation: true,
  enableDeduplication: false,
  enablePerformance: true
});

const generating = ref(false);

// 预览相关状态
const hasPreviewData = ref(false);
const previewActiveTab = ref('json');
const previewData = ref({
  json: '',
  table: [],
  columns: [],
  csv: ''
});

// 添加字段
const addField = () => {
  dataStructure.value.push({
    name: '',
    type: 'string',
    stringFormat: 'random',
    minLength: 1,
    maxLength: 50,
    pattern: '',
    prefix: '',
    suffix: '',
    charSet: 'alphanumeric',
    customCharSet: '',
    required: true,
    min: 0,
    max: 100,
    startValue: 1,
    step: 1,
    precision: 'integer',
    numberFormat: 'random',
    dateFormat: 'YYYY-MM-DD',
    includeTime: false,
    timePrecision: 'second',
    dateDistribution: 'uniform',
    booleanDistribution: '50_50',
    trueProbability: 50,
    booleanFormat: 'true_false',
    allowNull: false,
    customExpression: '',
    dependentFields: [],
    customDataType: 'string',
    validationRule: '',
    errorMessage: '',
    enumValues: [],
    startDate: null,
    endDate: null,
    removingIndex: undefined
  });
  
  // 滚动到最新添加的字段
  nextTick(() => {
    const fieldList = document.querySelector('.field-list');
    if (fieldList) {
      fieldList.scrollTo({
        top: fieldList.scrollHeight,
        behavior: 'smooth'
      });
    }
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
  // 设置删除动画状态
  field.removingIndex = index;
  
  // 延迟删除，让动画有时间播放
  setTimeout(() => {
  field.enumValues.splice(index, 1);
    field.removingIndex = undefined;
  }, 200);
};

// 生成数据
const generateData = async () => {
  if (dataStructure.value.length === 0) {
    ElMessage.warning('请先配置数据结构');
    return;
  }
  
  generating.value = true;
  try {
    // 这里后续会对接后端API
    await new Promise(resolve => setTimeout(resolve, 2000)); // 模拟生成过程
    
    // 生成预览数据
    generatePreviewData();
    
    ElMessage.success('数据生成完成！');
  } catch (error) {
    ElMessage.error('数据生成失败');
  } finally {
    generating.value = false;
  }
};

// 生成预览数据
const generatePreviewData = () => {
  // 模拟生成预览数据
  const mockData = [];
  const columns = [];
  
  // 根据数据结构生成列定义
  dataStructure.value.forEach(field => {
    if (field.name) {
      columns.push({
        prop: field.name,
        label: field.name,
        width: 120
      });
    }
  });
  
  // 生成模拟数据行 - 固定预览前20条，避免性能问题
  const previewCount = Math.min(generationConfig.count, 20);
  
  for (let i = 0; i < previewCount; i++) {
    const row = {};
    dataStructure.value.forEach(field => {
      if (field.name) {
        row[field.name] = generateMockValue(field, i);
      }
    });
    mockData.push(row);
  }
  
  // 生成CSV数据
  const csvData = generateCSVData(mockData, columns);
  
  previewData.value = {
    json: JSON.stringify(mockData, null, 2),
    table: mockData,
    columns: columns,
    csv: csvData
  };
  
  hasPreviewData.value = true;
  previewActiveTab.value = 'json';
};

// 生成模拟值
const generateMockValue = (field, index) => {
  // 检查是否必填
  if (!field.required && Math.random() < 0.1) { // 10%的概率生成空值
    return null;
  }
  
  switch (field.type) {
    case 'string':
      return `示例字符串${index + 1}`;
    case 'number':
      return generateNumberValue(field, index);
    case 'date':
      return new Date(Date.now() + index * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
    case 'boolean':
      return index % 2 === 0;
    case 'enum':
      return field.enumValues && field.enumValues.length > 0 
        ? field.enumValues[index % field.enumValues.length] 
        : '枚举值';
    default:
      return `值${index + 1}`;
  }
};

// 生成数字值
const generateNumberValue = (field, index) => {
  let value = 0;
  
  switch (field.numberFormat) {
    case 'increment':
      value = (field.startValue || 1) + (index * (field.step || 1));
      break;
    case 'decrement':
      value = (field.startValue || 1000) - (index * (field.step || 1));
      break;
    case 'price':
      value = Math.round((Math.random() * 1000 + 10) * 100) / 100;
      break;
    case 'percentage':
      value = Math.round((Math.random() * 100) * 100) / 100;
      break;
    case 'age':
      value = Math.floor(Math.random() * 60) + 18;
      break;
    case 'quantity':
      value = Math.floor(Math.random() * 1000) + 1;
      break;
    case 'id':
      value = index + 1;
      break;
    case 'rating':
      value = Math.floor(Math.random() * 5) + 1;
      break;
    case 'amount':
      value = Math.round((Math.random() * 10000 + 100) * 100) / 100;
      break;
    case 'weight':
      value = Math.round((Math.random() * 200 + 50) * 10) / 10;
      break;
    default: // random
      value = Math.floor(Math.random() * (field.max - field.min + 1)) + field.min;
  }
  
  // 根据精度设置处理小数位数
  if (field.precision === 'integer') {
    return Math.floor(value);
  } else {
    const decimalPlaces = parseInt(field.precision);
    return Math.round(value * Math.pow(10, decimalPlaces)) / Math.pow(10, decimalPlaces);
  }
};

// 刷新预览
const refreshPreview = () => {
  generatePreviewData();
  ElMessage.success('预览已刷新');
};

// 生成CSV数据
const generateCSVData = (data, columns) => {
  if (!data || data.length === 0 || !columns || columns.length === 0) {
    return '';
  }
  
  // 生成CSV头部
  const headers = columns.map(col => col.label).join(',');
  
  // 生成CSV数据行
  const rows = data.map(row => {
    return columns.map(col => {
      const value = row[col.prop];
      // 如果值包含逗号、引号或换行符，需要用引号包围并转义
      if (value === null || value === undefined) {
        return '';
      }
      const stringValue = String(value);
      if (stringValue.includes(',') || stringValue.includes('"') || stringValue.includes('\n')) {
        return `"${stringValue.replace(/"/g, '""')}"`;
      }
      return stringValue;
    }).join(',');
  });
  
  return [headers, ...rows].join('\n');
};

// 复制CSV到剪贴板
const copyCSVToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(previewData.value.csv);
    ElMessage.success('CSV数据已复制到剪贴板');
  } catch (error) {
    // 降级方案：使用传统方法
    const textArea = document.createElement('textarea');
    textArea.value = previewData.value.csv;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand('copy');
    document.body.removeChild(textArea);
    ElMessage.success('CSV数据已复制到剪贴板');
  }
};

// 导出预览数据
const exportPreview = () => {
  // 这里后续会实现导出功能
  ElMessage.success('导出功能开发中...');
};
</script>

<style scoped>
/* 基础容器样式 */
.factory-content {
  padding: 24px 24px 0 24px;
  height: 100%;
  overflow-y: auto;
  background: #f8fafc;
  border-radius: 20px;
  margin: 16px;
}

/* 隐藏 factory-content 的滚动条 */
.factory-content::-webkit-scrollbar {
  display: none;
}

.factory-content {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

/* 数据生成器样式 */
.data-generator {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0;
}



/* 主要内容区域 */
.main-content {
  display: flex;
  gap: 24px;
  justify-content: flex-start;
}

/* 配置区域样式 */
.config-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  height: 600px;
  display: flex;
  flex-direction: column;
  /* 防止外部滚动影响 */
  overflow: hidden;
}

.data-structure-section {
  flex: 6;
}

.generation-section {
  flex: 4;
}

/* 生成配置样式 */
.generation-config {
  padding: 16px 0;
  flex: 1;
  overflow-y: auto;
  padding-right: 8px;
  /* 确保滚动事件正确工作 */
  overscroll-behavior: contain;
}

.config-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.config-input {
  width: 100%;
}

.generate-btn {
  width: 100%;
  height: 44px;
  border-radius: 8px;
  font-weight: 500;
}

.advanced-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.advanced-options .el-checkbox {
  margin-right: 0;
}

.advanced-options .el-checkbox__label {
  font-size: 14px;
  color: #374151;
}

/* 预览操作按钮样式 */
.refresh-btn {
  border-radius: 8px;
  font-weight: 500;
  height: 36px;
  padding: 0 16px;
  background: #10b981;
  border: none;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.2);
  transition: all 0.2s ease;
}

.refresh-btn:hover {
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
  background: #059669;
}

.refresh-btn .el-icon {
  margin-right: 6px;
  font-size: 14px;
}

.export-btn {
  border-radius: 8px;
  font-weight: 500;
  height: 36px;
  padding: 0 16px;
  background: #0ea5e9;
  border: none;
  box-shadow: 0 2px 8px rgba(14, 165, 233, 0.2);
  transition: all 0.2s ease;
}

.export-btn:hover {
  box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
  background: #0284c7;
}

.export-btn .el-icon {
  margin-right: 6px;
  font-size: 14px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e2e8f0;
  gap: 24px;
}

.section-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #1e293b;
}

.add-btn {
  border-radius: 8px;
  font-weight: 500;
  height: 40px;
  padding: 0 20px;
  background: #0ea5e9;
  border: none;
  box-shadow: 0 2px 8px rgba(14, 165, 233, 0.2);
  transition: all 0.2s ease;
}

.add-btn:hover {
  box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
  background: #0284c7;
}

.add-btn:active {
  transform: translateY(0);
}

.add-btn .el-icon {
  margin-right: 6px;
  font-size: 16px;
}

/* 字段列表样式 */
.field-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  flex: 1;
  overflow-y: auto;
  padding-right: 8px;
  /* 确保滚动事件正确工作 */
  overscroll-behavior: contain;
}

/* 当没有字段时，隐藏字段列表 */
.field-list:empty {
  display: none;
}

.field-item {
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 20px;
  background: #fafbfc;
  transition: all 0.2s ease;
}

.field-item:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

/* 字段基本信息样式 */
.field-basic {
  display: flex;
  gap: 16px;
  align-items: center;
  margin-bottom: 16px;
}

.field-name {
  flex: 1;
}

.field-type {
  width: 140px;
}

.remove-btn {
  flex-shrink: 0;
}

/* 字段配置选项样式 */
.field-options {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  padding: 20px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.option-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 160px;
}

.option-label {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin: 0;
}

.option-input {
  width: 160px;
}

/* 枚举值样式 */
.enum-values {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 0;
}

.enum-tag {
  border-radius: 8px;
  background: #eff6ff;
  color: #1d4ed8;
  border: 1px solid #3b82f6;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
  position: relative;
  cursor: pointer;
  min-height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.enum-tag:hover {
  background: #dbeafe;
  border-color: #2563eb;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
}

.enum-tag .el-icon {
  margin-left: 8px;
  font-size: 14px;
  opacity: 0.7;
  transition: opacity 0.2s ease;
}

.enum-tag:hover .el-icon {
  opacity: 1;
}

/* 枚举值标签动画 */
.enum-tags-container {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  width: 100%;
  height: 100%;
  padding: 16px;
  align-items: flex-start;
  justify-content: flex-start;
  overflow-y: auto;
}

.enum-tag {
  transition: all 0.2s ease;
  transform: translate3d(0, 0, 0);
}

.enum-tag.removing {
  opacity: 0;
  transform: scale(0.95) translate3d(0, 0, 0);
  pointer-events: none;
}

.enum-container {
  display: flex;
  gap: 0;
  width: 100%;
  background: #fafbfc;
  border-radius: 12px;
  overflow: hidden;
}

.enum-list-section {
  flex: 1;
  padding: 20px;
  background: white;
}

.enum-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e2e8f0;
}

.enum-title {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.enum-count {
  font-size: 12px;
  color: #6b7280;
  background: #f3f4f6;
  padding: 2px 8px;
  border-radius: 12px;
}

.enum-values {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  min-height: 32px;
  align-items: center;
}

.enum-container-border {
  background: #f9fafb;
  border: 1px dashed #d1d5db;
  border-radius: 8px;
  margin-top: 8px;
  width: 100%;
  height: 110px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0;
  padding-bottom: 0;
}

.enum-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 24px;
  color: #9ca3af;
  font-size: 13px;
}

.enum-empty-icon {
  font-size: 16px;
  color: #9ca3af;
}

.enum-divider {
  width: 2px;
  background: linear-gradient(to bottom, #3b82f6, #8b5cf6, #3b82f6);
  margin: 20px 0;
  border-radius: 1px;
  box-shadow: 0 0 8px rgba(59, 130, 246, 0.3);
}

.enum-add-section {
  flex: 0 0 220px;
  padding: 20px;
  background: white;
}

.enum-add-header {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.enum-input-group {
  display: flex;
  gap: 8px;
  align-items: center;
}

.enum-input {
  width: 200px;
}

/* 空状态样式 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #94a3b8;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  color: #cbd5e1;
}

.empty-state p {
  margin: 0;
  font-size: 16px;
}

/* 生成预览区域样式 */
.preview-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  margin-top: 24px;
  margin-bottom: 0;
  height: 450px;
  display: flex;
  flex-direction: column;
}

.preview-info {
  display: flex;
  align-items: center;
  margin-right: auto;
  margin-left: 16px;
}

/* 自定义标签页样式 */
.preview-tabs-nav {
  margin-bottom: 0;
  padding: 0;
}

.custom-tabs {
  display: flex;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-bottom: none;
  border-radius: 8px 8px 0 0;
  overflow: hidden;
}

.tab-item {
  flex: 1;
  height: 44px;
  line-height: 44px;
  text-align: center;
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  background: transparent;
  cursor: pointer;
  transition: all 0.2s ease;
  border-right: 1px solid #e2e8f0;
  user-select: none;
}

.tab-item:last-child {
  border-right: none;
}

.tab-item.active {
  color: #0ea5e9;
  background: white;
  font-weight: 600;
}

.tab-item:hover:not(.active) {
  color: #0ea5e9;
  background: rgba(14, 165, 233, 0.05);
}

/* 预览内容容器样式 */
.preview-code-container,
.preview-table-container,
.preview-csv-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: white;
  border: 1px solid #e2e8f0;
  border-top: none;
  border-radius: 0 0 8px 8px;
  margin-top: 0;
}

.preview-code {
  flex: 1;
  overflow: auto;
  padding: 20px;
  background: #1e293b;
  color: #e2e8f0;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
  line-height: 1.5;
  border-radius: 0 0 8px 8px;
}

/* 隐藏JSON代码区域的滚动条 */
.preview-code::-webkit-scrollbar {
  display: none;
}

.preview-code {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

.preview-code pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.preview-table {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.preview-table .el-table {
  flex: 1;
  border: none;
}

.preview-table .el-table__header-wrapper {
  position: sticky;
  top: 0;
  z-index: 10;
  background: white;
}

.preview-table .el-table__body-wrapper {
  flex: 1;
  overflow-y: auto;
}

/* 隐藏表格区域的滚动条 */
.preview-table .el-table__body-wrapper::-webkit-scrollbar {
  display: none;
}

.preview-table .el-table__body-wrapper {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

/* CSV预览样式 */
.preview-csv {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.csv-header {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
  position: relative;
}

.csv-info {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

.copy-csv-btn {
  height: 32px;
  padding: 0 14px;
  background: #0ea5e9;
  border: none;
  box-shadow: 0 2px 8px rgba(14, 165, 233, 0.2);
  transition: all 0.2s ease;
  border-radius: 8px;
  font-weight: 500;
  font-size: 12px;
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
}

.copy-csv-btn:hover {
  box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
  background: #0284c7;
}

.copy-csv-btn .el-icon {
  margin-right: 6px;
  font-size: 16px;
}

.csv-content {
  flex: 1;
  overflow: auto;
  padding: 0;
  background: white;
  border-radius: 0 0 8px 8px;
}

.csv-table {
  width: 100%;
  overflow: auto;
}

.csv-table table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.csv-table thead {
  background: #f8fafc;
  border-bottom: 2px solid #e2e8f0;
}

.csv-table th {
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  font-size: 14px;
  color: #374151;
  border-right: 1px solid #e2e8f0;
  white-space: nowrap;
  position: sticky;
  top: 0;
  background: #f8fafc;
  z-index: 10;
}

.csv-table th:last-child {
  border-right: none;
}

.csv-table tbody tr {
  border-bottom: 1px solid #f1f5f9;
  transition: background-color 0.2s ease;
}

.csv-table tbody tr:hover {
  background-color: #f8fafc;
}

.csv-table tbody tr:nth-child(even) {
  background-color: #fafbfc;
}

.csv-table tbody tr:nth-child(even):hover {
  background-color: #f1f5f9;
}

.csv-table td {
  padding: 12px 16px;
  text-align: left;
  font-size: 14px;
  color: #374151;
  border-right: 1px solid #f1f5f9;
  vertical-align: middle;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.csv-table td:last-child {
  border-right: none;
}

/* 空值样式 */
.csv-table td:empty::before,
.csv-table td:contains('-') {
  color: #9ca3af;
  font-style: italic;
}

/* 隐藏CSV内容区域的滚动条 */
.csv-content::-webkit-scrollbar,
.csv-table::-webkit-scrollbar {
  display: none;
}

.csv-content,
.csv-table {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

.preview-count {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

.preview-note {
  color: #9ca3af;
  font-size: 13px;
  font-weight: 400;
}

.preview-actions {
  display: flex;
  gap: 12px;
}

.preview-content {
  margin-top: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: auto;
}

/* 隐藏预览内容区域的滚动条 */
.preview-content::-webkit-scrollbar {
  display: none;
}

.preview-content {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

.preview-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #94a3b8;
  background: #f8fafc;
  border: 2px dashed #e2e8f0;
  border-radius: 12px;
  flex: 1;
  height: 100%;
  min-height: 300px;
}

.preview-empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  color: #cbd5e1;
}

.preview-data {
  background: transparent;
  border-radius: 0;
  padding: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.preview-tabs {
  background: white;
  border-radius: 8px;
  overflow: auto;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.preview-code {
  background: #1e293b;
  color: #e2e8f0;
  padding: 20px;
  border-radius: 8px;
  overflow: auto;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
  line-height: 1.5;
  max-height: 100%;
}

.preview-code pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.preview-table {
  padding: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Element Plus 标签页样式调整 */
.preview-tabs .el-tabs__content {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.preview-tabs .el-tab-pane {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
}

/* 帮助图标样式 */
.help-icon {
  margin-left: 6px;
  color: #909399;
  font-size: 14px;
  cursor: help;
  transition: color 0.2s ease;
}

.help-icon:hover {
  color: #409eff;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .factory-content {
    padding: 16px;
  }
  

  
  .main-content {
    flex-direction: column;
    gap: 20px;
  }
  
  .config-section {
    padding: 20px;
  }
  
  .field-basic {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }
  
  .field-type {
    width: 100%;
  }
  
  .field-options {
    flex-direction: column;
    gap: 12px;
  }
  
  .option-item {
    min-width: auto;
  }
  
  .option-input {
    width: 100%;
  }
  
  .enum-container {
    flex-direction: column;
  }
  
  .enum-divider {
    width: 100%;
    height: 2px;
    margin: 0 20px;
    background: linear-gradient(to right, #3b82f6, #8b5cf6, #3b82f6);
    border-radius: 1px;
    box-shadow: 0 0 8px rgba(59, 130, 246, 0.3);
  }
  
  .enum-add-section {
    flex: none;
    border-top: 2px solid #3b82f6;
  }
  
  .enum-input {
    width: 100%;
  }
  
  .enum-tags-container {
    gap: 6px;
  }
  
  .preview-section {
    margin-top: 16px;
    padding: 16px;
  }
  
  .preview-actions {
    flex-direction: column;
    gap: 8px;
  }
}

/* 隐藏滚动条 */
.field-list::-webkit-scrollbar,
.generation-config::-webkit-scrollbar {
  display: none;
}

.field-list,
.generation-config {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}
</style> 