<template>
  <div>
    <el-card shadow="never" style="margin-bottom: 24px;">
      <div style="font-size: 20px; font-weight: bold; margin-bottom: 12px;">用例上传</div>
      <el-form :inline="true">
        <el-form-item label="选择项目">
          <el-select v-model="selectedProject" placeholder="请选择项目" @change="onProjectChange" :loading="loadingProjects" style="width: 200px;">
            <el-option
              v-for="project in projects"
              :key="project.id"
              :label="project.name"
              :value="project.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button 
            type="warning" 
            :disabled="!hasDuplicate" 
            @click="removeDuplicateCases"
            :title="hasDuplicate ? '点击移除所有重复用例' : '当前没有重复用例'"
            class="remove-duplicate-btn"
          >
            <el-icon v-if="hasDuplicate" class="delete-icon">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 6H5H21M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 3.46957 16 4V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </el-icon>
            <span class="btn-text">
              去除重复用例
              <span v-if="hasDuplicate" class="duplicate-count">
                ({{ duplicateCount }}条)
              </span>
            </span>
          </el-button>
        </el-form-item>
        <el-form-item>
          <el-button 
            type="success" 
            :disabled="!selectedCases.length" 
            @click="onImport"
            class="import-btn"
          >
            <el-icon class="import-icon">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15M17 8L12 3M12 3L7 8M12 3V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </el-icon>
            <span class="btn-text">导入选中用例</span>
          </el-button>
        </el-form-item>
        <el-form-item>
          <el-upload
            :show-file-list="false"
            :before-upload="beforeUpload"
            accept=".xlsx"
            action="#"
            :http-request="customUpload"
            :disabled="!selectedProject"
          >
            <el-button type="primary" :disabled="!selectedProject">选择文件</el-button>
            <span v-if="fileName" style="margin-left: 16px; color: #666;">{{ fileName }}</span>
          </el-upload>
        </el-form-item>
      </el-form>
    </el-card>
    <!-- 用例列表区域 -->
    <div class="case-list-container">
      <!-- 有用例时显示表格 -->
      <el-table
        v-if="cases.length"
        :data="cases"
        border
        style="width: 100%;"
        height="600"
        :row-class-name="rowClassName"
        @selection-change="onSelectionChange"
        ref="caseTable"
        class="case-table"
      >
        <el-table-column type="selection" width="50" />
        <el-table-column v-for="h in headers.filter(h => !['Created At', 'Updated At', 'Created By', 'Last Updated By'].includes(h))" :key="h" :prop="h" :label="headerMap[h] || h" :min-width="getColWidth(h)" :show-overflow-tooltip="false">
          <template #default="scope">
            <!-- 优先级列使用标签样式 -->
            <template v-if="h === 'Priority' || h === '优先级'">
              <el-tag 
                :type="getPriorityType(scope.row[h])" 
                class="priority-tag"
                size="small"
              >
                {{ scope.row[h] || '未设置' }}
              </el-tag>
            </template>
            <!-- 状态列使用标签样式 -->
            <template v-else-if="h === 'Status' || h === '状态'">
              <el-tag 
                :type="getStatusType(scope.row[h])" 
                class="status-tag"
                size="small"
              >
                {{ getStatusDisplay(scope.row[h]) }}
              </el-tag>
            </template>
            <!-- 其他列使用普通文本 -->
            <template v-else>
              <div style="white-space: pre-line; word-break: break-all;">{{ scope.row[h] }}</div>
            </template>
          </template>
        </el-table-column>
        <el-table-column label="是否重复" width="140">
          <template #default="scope">
            <transition name="duplicate-status" mode="out-in">
              <el-tag 
                v-if="scope.row.duplicate" 
                :key="'duplicate-' + scope.row.ID + '-' + scope.row.duplicate_reason"
                type="danger" 
                class="deep-danger-tag duplicate-status-tag" 
                style="white-space: normal;"
              >
                是({{ scope.row.duplicate_reason }})
              </el-tag>
              <el-tag 
                v-else 
                :key="'not-duplicate-' + scope.row.ID"
                type="success" 
                class="deep-success-tag duplicate-status-tag"
              >
                否
              </el-tag>
            </transition>
          </template>
        </el-table-column>
        <el-table-column v-if="hasDuplicate" label="新ID" width="120">
          <template #default="scope">
            <el-input 
              v-if="scope.row.duplicate || scope.row.new_ID" 
              v-model="scope.row.new_ID" 
              placeholder="输入新ID" 
              size="small" 
              @input="onNewIdInput(scope.row)"
              @blur="onNewIdBlur(scope.row)"
            />
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 没有用例时显示空状态 -->
      <div v-else class="empty-state-container">
        <div class="empty-state-content">
          <div class="empty-state-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 11H5M19 11C20.1046 11 21 11.8954 21 13V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V13C3 11.8954 3.89543 11 5 11M19 11V9C19 7.89543 18.1046 7 17 7M5 11V9C5 7.89543 5.89543 7 7 7M7 7V5C7 3.89543 7.89543 3 9 3H15C16.1046 3 17 3.89543 17 5V7M7 7H17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h3 class="empty-state-title">暂无用例数据</h3>
          <p class="empty-state-description">
            请先选择项目并上传Excel文件来查看用例列表
          </p>
        </div>
      </div>
    </div>
    <!-- 删除<CompareDialog v-model:visible="showCompareDialog" /> -->
    <CaseCompareDialog
      v-if="showCaseCompareDialog"
      v-model:visible="showCaseCompareDialog"
      :caseA="compareCurrentA"
      :caseB="compareCurrentB"
      :currentIndex="currentGroupIndex"
      :totalCount="duplicateGroups.length"
      :canGoPrevious="currentGroupIndex > 0"
      :canGoNext="currentGroupIndex < duplicateGroups.length - 1"
      :currentGroupId="duplicateGroups[currentGroupIndex]?.id || ''"
      :groupCompleted="completedGroups.includes(duplicateGroups[currentGroupIndex]?.id)"
      @keep="handleCompareKeep"
      @previous="handlePreviousGroup"
      @next="handleNextGroup"
    />
  </div>
</template>

<script>
import { uploadCase, importCase, getProjects, checkCaseIdDuplicate } from '@/api/case.js';
import { inject, watch } from 'vue';
import CaseCompareDialog from './CaseCompareDialog.vue';

export default {
  name: 'UploadCase',
  components: { CaseCompareDialog },
  data() {
    return {
      headers: [],
      cases: [],
      fileName: '',
      selectedCases: [],
      projects: [],
      selectedProject: '',
      loadingProjects: false,
      // 对比弹窗及流程相关
      showCaseCompareDialog: false,
      compareQueue: [], // 当前组的重复用例队列
      compareIndex: 0,  // 当前对比到第几个
      compareCurrentA: null,
      compareCurrentB: null,
      duplicateGroups: [], // 所有重复组
      currentGroupIndex: 0, // 当前处理的重复组索引
      completedGroups: [], // 已完成的组id
      // 字段中英文对照表
      headerMap: {
        'ID': '用例ID',
        'Title': '用例标题',
        'Description': '用例描述',
        'Preconditions': '前置条件',
        'Steps': '操作步骤',
        'Expected Results': '预期结果',
        'Priority': '优先级',
        'Category': '分类',
        'Status': '状态',
        // 其它字段如有需要可继续补充
      }
    };
  },
  computed: {
    hasDuplicate() {
      return this.cases.some(c => c.duplicate);
    },
    duplicateCount() {
      return this.cases.filter(c => c.duplicate).length;
    }
  },
  async mounted() {
    // 页面加载时获取项目列表
    await this.loadProjects();
    
    // 检查是否有通过路由传递的项目ID
    const projectId = this.$route.query.projectId;
    if (projectId) {
      this.selectedProject = parseInt(projectId);
    }
    
    // 验证当前选择的项目是否仍然存在
    this.validateSelectedProject();
  },
  setup() {
    // 注入项目删除事件
    const projectDeletedEvent = inject('projectDeletedEvent');
    
    return {
      projectDeletedEvent
    };
  },
  created() {
    // 监听项目删除事件
    watch(
      () => this.projectDeletedEvent,
      (newVal, oldVal) => {
        if (newVal && newVal !== oldVal) {
          this.handleProjectDeleted(newVal);
        }
      }
    );
  },
  methods: {
    async loadProjects() {
      this.loadingProjects = true;
      try {
        const data = await getProjects();
        this.projects = data.projects || [];
        
        // 加载项目列表后验证当前选择的项目是否仍然存在
        this.validateSelectedProject();
      } catch (err) {
        this.$message.error('加载项目列表失败：' + (err.response?.data?.error || err.message));
      } finally {
        this.loadingProjects = false;
      }
    },
    
    validateSelectedProject() {
      // 如果当前有选择的项目，但该项目不在最新的项目列表中，则清空选择
      if (this.selectedProject && this.projects.length > 0) {
        const projectExists = this.projects.some(project => project.id === this.selectedProject);
        if (!projectExists) {
          this.selectedProject = '';
          // 同时清空相关数据
          this.cases = [];
          this.headers = [];
          this.fileName = '';
          this.selectedCases = [];
        }
      }
    },
    
    handleProjectDeleted(projectId) {
      // 如果删除的项目正是当前选择的项目，则清空选择
      if (this.selectedProject === projectId) {
        this.selectedProject = '';
        // 同时清空相关数据
        this.cases = [];
        this.headers = [];
        this.fileName = '';
        this.selectedCases = [];
      }
      
      // 重新加载项目列表
      this.loadProjects();
    },
    
    onProjectChange() {
      // 项目选择变化时清空之前的数据
      this.cases = [];
      this.headers = [];
      this.fileName = '';
      this.selectedCases = [];
    },
    beforeUpload(file) {
      this.fileName = file.name;
      return true;
    },
    async customUpload(option) {
      try {
        // 重置对比相关状态，确保新文件上传时状态干净
        this.resetComparisonState();
        
        // 上传文件时传递项目ID
        const res = await uploadCase(option.file, this.selectedProject);
        if (res && res.data) {
          this.headers = res.data.headers || [];
          this.cases = (res.data.cases || []).map(c => ({ ...c, new_ID: '' }));
          // 按用例ID升序排序
          this.cases.sort((a, b) => {
            const idA = isNaN(Number(a.ID)) ? a.ID : Number(a.ID);
            const idB = isNaN(Number(b.ID)) ? b.ID : Number(b.ID);
            if (idA < idB) return -1;
            if (idA > idB) return 1;
            return 0;
          });
        }

        this.$nextTick(() => {
          if (this.$refs.caseTable) {
            this.$refs.caseTable.clearSelection();
            this.cases.forEach((row, idx) => {
              if (!row.duplicate) this.$refs.caseTable.toggleRowSelection(row, true);
            });
          }
        });
      } catch (err) {
        this.$message.error('上传失败：' + (err.response?.data?.error || err.message));
      }
    },
    onSelectionChange(val) {
      this.selectedCases = val;
    },
    onNewIdInput(row) {
      // 输入新ID后自动选中
      if (row.new_ID && this.$refs.caseTable) {
        this.$refs.caseTable.toggleRowSelection(row, true);
      }
    },
    
    onNewIdBlur(row) {
      // 输入框失焦时检查新ID是否重复
      if (row.new_ID && this.selectedProject) {
        // 1. 先检查是否与其他正在编辑的新ID重复
        const duplicateNewId = this.cases.some(caseItem => {
          // 排除自己这一行，检查其他行是否有相同的新ID
          return caseItem !== row && caseItem.new_ID === row.new_ID;
        });
        
        if (duplicateNewId) {
          // 与其他正在编辑的新ID重复
          row.duplicate = true;
          row.duplicate_reason = '新ID重复';
          return;
        }
        
        // 2. 检查新ID是否与当前文件中的原始ID重复
        const duplicateWithOriginalId = this.cases.some(caseItem => {
          // 检查新ID是否与任何原始ID相同
          return caseItem.ID === row.new_ID;
        });
        
        if (duplicateWithOriginalId) {
          // 新ID与当前文件中的原始ID重复
          row.duplicate = true;
          row.duplicate_reason = '新ID重复';
          return;
        }
        
        // 3. 检查数据库中是否重复
        this.checkNewIdDuplicate(row);
      }
    },
    
    /**
     * 检查新ID是否重复
     */
    async checkNewIdDuplicate(row) {
      try {
        const result = await checkCaseIdDuplicate(this.selectedProject, row.new_ID);
        
        if (!result.is_duplicate) {
          // 新ID不重复，更新用例状态
          row.duplicate = false;
          row.duplicate_reason = '';
        } else {
          // 新ID仍然重复
          row.duplicate = true;
          row.duplicate_reason = '数据库中存在';
        }
      } catch (error) {
        console.error('检查新ID重复状态失败:', error);
        // 检查失败时保持原有状态
      }
    },
    getColWidth(h) {
      // 根据字段名自适应列宽，调整状态列宽度以显示标签，缩小分类列宽度
      if (h === 'Priority' || h === '优先级') return 80;
      if (h === 'Category' || h === '分类') return 90; // 分类列宽度调整为90px
      if (h === 'Status' || h === '状态') return 80; // 状态列宽度调整为80px
      if (h === 'ID' || h === '用例ID') return 120;
      return 180;
    },
    async onImport() {
      // 过滤出有效的选中用例
      const selected = this.selectedCases.filter(c => 
        !c.duplicate || (c.duplicate && c.new_ID)
      );

      // 检查是否至少选择了一条用例
      if (!selected.length) {
        // 检查是否所有用例都是重复的
        const allDuplicates = this.cases.every(c => c.duplicate);
        if (allDuplicates) {
          this.$message.warning('导入的数据已重复，请为重复用例设置新的ID或移除重复用例');
        } else {
          this.$message.warning('请至少选择一条用例');
        }
        return;
      }

      // 确保已选择项目
      if (!this.selectedProject) {
        this.$message.warning('请选择要导入用例的项目');
        return;
      }

      try {
        const res = await importCase(selected, this.selectedProject);
        this.$message.success('导入成功：' + res.data.count + ' 条');
        this.removeImportedCases(selected);
      } catch (err) {
        const errorData = err.response?.data;
        if (errorData?.error_type === 'duplicate_case_id') {
          // 处理重复ID错误
          this.$message.error(errorData.error);
          // 可以在这里添加额外的处理逻辑，比如高亮显示重复的用例
        } else {
          this.$message.error('导入失败：' + (errorData?.error || err.message));
        }
      }
    },

    /**
     * 清除所有选中状态
     */
    clearSelection() {
      this.cases = [];
      this.headers = [];
      this.selectedCases = [];
      this.fileName = '';
      if (this.$refs.caseTable) {
        this.$refs.caseTable.clearSelection();
      }
    },

    /**
     * 只清除表格选中状态，不清空用例列表
     */
    clearTableSelection() {
      this.selectedCases = [];
      if (this.$refs.caseTable) {
        this.$refs.caseTable.clearSelection();
      }
    },

    /**
     * 移除已导入的用例并清除选中状态
     */
    removeImportedCases(importedCases) {
      // 从cases中移除已导入的用例
      this.cases = this.cases.filter(caseItem => {
        // 检查当前用例是否在已导入列表中
        return !importedCases.some(imported => {
          const caseId = caseItem.ID || caseItem.case_id;
          const importedId = imported.ID || imported.case_id;
          const newImportedId = imported.new_ID;
          
          // 匹配条件：原始ID相同 或 新ID相同
          return (caseId === importedId) || (caseId === newImportedId);
        });
      });
      
      // 清除选中状态
      this.selectedCases = [];
      if (this.$refs.caseTable) {
        this.$refs.caseTable.clearSelection();
      }
    },
    rowClassName({ row }) {
      return row.duplicate ? 'row-duplicate' : '';
    },
    
    // 获取优先级标签类型
    getPriorityType(priority) {
      const priorityMap = {
        '高': 'danger',
        '中': 'warning',
        '低': 'info',
        'P0': 'danger',
        'P1': 'warning',
        'P2': 'info',
        'P3': 'success'
      };
      return priorityMap[priority] || 'info';
    },
    
    // 获取状态标签类型
    getStatusType(status) {
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
    },
    
    // 获取状态显示文本
    getStatusDisplay(status) {
      if (!status) return '未设置';
      if (status === 'Draft') return '未完成';
      if (status === 'success') return '已完成';
      return status;
    },
    
    /**
     * 去除重复用例
     */
    removeDuplicateCases() {
      // 收集所有重复用例，按ID分组
      const duplicates = this.cases.filter(c => c.duplicate);
      if (duplicates.length < 2) {
        this.$message.warning('没有足够的重复用例进行对比');
        return;
      }
      
      // 按ID分组，找到所有有2个及以上的ID组
      const idMap = {};
      for (const c of duplicates) {
        const id = c.ID || c.case_id;
        if (!idMap[id]) idMap[id] = [];
        idMap[id].push(c);
      }
      
      // 收集所有需要处理的重复组（每组至少2个用例）
      this.duplicateGroups = [];
      for (const [id, group] of Object.entries(idMap)) {
        if (group.length > 1) {
          this.duplicateGroups.push({
            id: id,
            cases: group.map(this.normalizeCaseFields)
          });
        }
      }
      
      if (this.duplicateGroups.length === 0) {
        this.$message.warning('没有足够的重复用例进行对比');
        return;
      }
      
      // 开始处理第一个重复组
      this.currentGroupIndex = 0;
      this.startCurrentGroupComparison();
    },
    
    /**
     * 开始当前组的对比
     */
    startCurrentGroupComparison() {
      const currentGroup = this.duplicateGroups[this.currentGroupIndex];
      if (!currentGroup) {
        this.finishAllComparisons();
        return;
      }
      
      this.compareQueue = currentGroup.cases;
      this.compareIndex = 1;
      this.compareCurrentA = this.compareQueue[0];
      this.compareCurrentB = this.compareQueue[1];
      this.showCaseCompareDialog = true;
    },
    
    /**
     * 字段映射，保证compareCurrentA/B字段为小写
     */
    normalizeCaseFields(c) {
      return {
        case_id: c.ID || c.case_id,
        title: c.Title || c.title,
        description: c.Description || c.description,
        preconditions: c.Preconditions || c.preconditions,
        steps: c.Steps || c.steps,
        expected_results: c['Expected Results'] || c.expected_results,
        priority: c.Priority || c.priority,
        category: c.Category || c.category,
        status: c.Status || c.status,
      };
    },
    handleCompareKeep(which) {
      // which: 'A' or 'B'
      let keep, remove;
      if (which === 'A') {
        keep = this.compareCurrentA;
        remove = this.compareCurrentB;
      } else {
        keep = this.compareCurrentB;
        remove = this.compareCurrentA;
      }
      // 1. 从compareQueue中移除被淘汰的用例
      this.compareQueue = this.compareQueue.filter(item => item !== remove);
      // 2. 从cases中移除被淘汰的用例（只删除被淘汰的那一个特定用例）
      let removedCount = 0;
      this.cases = this.cases.filter(c => {
        // 检查是否是要删除的用例
        const id = c.ID || c.case_id;
        const isTargetCase = (
          (id === remove.case_id) &&
          (c.Title === remove.title || c.title === remove.title) &&
          (c.Description === remove.description || c.description === remove.description)
        );
        
        // 如果是目标用例且还没删除过，则删除它
        if (isTargetCase && removedCount === 0) {
          removedCount++;
          return false; // 删除这个用例
        }
        
        return true; // 保留其他用例
      });
      // 3. 如果compareQueue只剩一条，说明本组对比完成
      if (this.compareQueue.length === 1) {
        // 标记当前组已完成
        const groupId = this.duplicateGroups[this.currentGroupIndex]?.id;
        if (groupId && !this.completedGroups.includes(groupId)) {
          this.completedGroups.push(groupId);
        }
        // 设置最终保留的用例为compareCurrentA，用于完成模式显示
        this.compareCurrentA = this.compareQueue[0];
        this.compareCurrentB = null; // 清空B，因为对比已完成
        // 更新cases中该用例的重复状态 - 先查询数据库确认
        const last = this.compareQueue[0];
        this.updateCaseDuplicateStatus(last);
        this.$message.success(`已完成 ${this.duplicateGroups[this.currentGroupIndex].id} 组的对比`);
        // 检查是否还有其他组
        if (this.currentGroupIndex < this.duplicateGroups.length - 1) {
          this.$message.info('请点击"下一组"按钮继续处理其他重复组');
        } else {
          this.finishAllComparisons();
        }
        // 不要关闭弹窗，等待用户点击下一组
        // this.showCaseCompareDialog = false;
      } else {
        // 继续下一轮对比，保留上一轮胜出的用例
        this.compareIndex = 1;
        this.compareCurrentA = keep;
        this.compareCurrentB = this.compareQueue[1];
      }
    },
    
    /**
     * 完成所有对比
     */
    async finishAllComparisons() {
      this.showCaseCompareDialog = false;
      this.$message.success(`已完成所有重复用例对比，共处理 ${this.duplicateGroups.length} 个重复组`);
      
      // 重新查询所有剩余用例的重复状态
      await this.updateAllRemainingCasesStatus();
      
      // 重置状态
      this.duplicateGroups = [];
      this.currentGroupIndex = 0;
      this.compareQueue = [];
      this.compareIndex = 0;
      this.compareCurrentA = null;
      this.compareCurrentB = null;
    },
    
    /**
     * 处理上一组
     */
    handlePreviousGroup() {
      if (this.currentGroupIndex > 0) {
        this.currentGroupIndex--;
        this.startCurrentGroupComparison();
      }
    },
    
    /**
     * 处理下一组
     */
    handleNextGroup() {
      if (this.currentGroupIndex < this.duplicateGroups.length - 1) {
        this.currentGroupIndex++;
        this.startCurrentGroupComparison();
        this.showCaseCompareDialog = true;
      }
    },

    /**
     * 更新用例的重复状态
     */
    async updateCaseDuplicateStatus(caseItem) {
      try {
        // 使用原始的case_id查询数据库
        const result = await checkCaseIdDuplicate(this.selectedProject, caseItem.case_id);
        
        // 找到对应的用例并更新状态
        this.cases.forEach(c => {
          const id = c.ID || c.case_id;
          if (
            id === caseItem.case_id &&
            (c.Title === caseItem.title || c.title === caseItem.title) &&
            (c.Description === caseItem.description || c.description === caseItem.description)
          ) {
            if (!result.is_duplicate) {
              c.duplicate = false;
              c.duplicate_reason = '';
            } else {
              c.duplicate = true;
              c.duplicate_reason = '数据库中存在';
            }
          }
        });
      } catch (error) {
        console.error('更新用例重复状态失败:', error);
        // 更新失败时保持原有状态
      }
    },

    /**
     * 更新所有剩余用例的重复状态
     */
    async updateAllRemainingCasesStatus() {
      try {
        // 获取所有剩余用例的ID
        const remainingCases = this.cases.filter(c => !c.duplicate);
        
        if (remainingCases.length === 0) {
          return;
        }

        // 批量查询所有剩余用例的重复状态
        for (const caseItem of remainingCases) {
          const caseId = caseItem.ID || caseItem.case_id;
          const newId = caseItem.new_ID;
          
          // 使用新ID（如果设置了）或原始ID查询
          const queryId = newId || caseId;
          
          if (queryId) {
            try {
              const result = await checkCaseIdDuplicate(this.selectedProject, queryId);
              
              // 更新用例状态
              if (result.is_duplicate) {
                caseItem.duplicate = true;
                caseItem.duplicate_reason = '数据库中存在';
              } else {
                caseItem.duplicate = false;
                caseItem.duplicate_reason = '';
              }
            } catch (error) {
              console.error(`查询用例 ${queryId} 重复状态失败:`, error);
              // 查询失败时保持原有状态
            }
          }
        }
        
        this.$message.info(`已重新查询 ${remainingCases.length} 个用例的重复状态`);
      } catch (error) {
        console.error('批量更新用例重复状态失败:', error);
        this.$message.error('更新用例重复状态失败，请手动检查');
      }
    },

    /**
     * 重置对比相关状态
     */
    resetComparisonState() {
      // 重置对比弹窗状态
      this.showCaseCompareDialog = false;
      
      // 重置对比队列和索引
      this.compareQueue = [];
      this.compareIndex = 0;
      this.compareCurrentA = null;
      this.compareCurrentB = null;
      
      // 重置重复组状态
      this.duplicateGroups = [];
      this.currentGroupIndex = 0;
      this.completedGroups = [];
      
      // 清除选中状态
      this.selectedCases = [];
      
      // 清除表格选中状态
      if (this.$refs.caseTable) {
        this.$refs.caseTable.clearSelection();
      }
    },


  }
};
</script>

<style scoped>
.el-card {
  margin-bottom: 24px;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  border: 1px solid #e2e8f0;
}

/* 表格倒角样式 */
.el-table {
  border-radius: 16px !important;
  overflow: hidden !important;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
  border: 1px solid #e2e8f0 !important;
}

.el-table__header-wrapper {
  border-radius: 16px 16px 0 0 !important;
}

.el-table__body-wrapper {
  border-radius: 0 0 16px 16px !important;
}

/* 表格标题样式 */
.el-table th.el-table__cell,
.el-table th.el-table__cell .cell,
.el-table .el-table__header th.el-table__cell,
.el-table .el-table__header th.el-table__cell .cell {
  background-color: #f5f7fa !important;
  color: #000000 !important;
  font-weight: bold !important;
  font-size: 14px !important;
  border-bottom: 1px solid #e2e8f0 !important;
}

/* 确保所有表头文字都是黑色加粗 */
.el-table .el-table__header-wrapper th,
.el-table .el-table__header-wrapper th .cell,
.el-table .el-table__header th,
.el-table .el-table__header th .cell {
  color: #000000 !important;
  font-weight: bold !important;
}

/* 使用深度选择器强制覆盖Element Plus样式 */
:deep(.case-table .el-table__header th) {
  color: #000000 !important;
  font-weight: bold !important;
  background-color: #f5f7fa !important;
}

:deep(.case-table .el-table__header th .cell) {
  color: #000000 !important;
  font-weight: bold !important;
}

:deep(.case-table .el-table__header-wrapper th) {
  color: #000000 !important;
  font-weight: bold !important;
}

:deep(.case-table .el-table__header-wrapper th .cell) {
  color: #000000 !important;
  font-weight: bold !important;
}

/* 全局表格标题样式 */
:deep(.el-table th.el-table__cell) {
  color: #000000 !important;
  font-weight: bold !important;
  background-color: #f5f7fa !important;
}

:deep(.el-table th.el-table__cell .cell) {
  color: #000000 !important;
  font-weight: bold !important;
}
.el-table .row-duplicate {
  background: #fff0f0;
}

.deep-danger-tag.el-tag--danger {
  background-color: #b91c1c !important;
  border-color: #b91c1c !important;
  color: #fff !important;
}

.deep-success-tag.el-tag--success {
  background-color: #15803d !important;
  border-color: #15803d !important;
  color: #fff !important;
}

/* 去除重复用例按钮样式 */
.remove-duplicate-btn {
  display: flex !important;
  align-items: center !important;
  gap: 6px !important;
  padding: 8px 16px !important;
  min-width: 120px !important;
  background-color: #d97706 !important;
  border-color: #d97706 !important;
  color: #ffffff !important;
}

.remove-duplicate-btn .delete-icon {
  width: 16px !important;
  height: 16px !important;
  flex-shrink: 0 !important;
}

.remove-duplicate-btn .btn-text {
  display: flex !important;
  align-items: center !important;
  gap: 4px !important;
  white-space: nowrap !important;
}

.remove-duplicate-btn .duplicate-count {
  font-size: 12px !important;
  opacity: 0.9 !important;
  font-weight: normal !important;
}

.remove-duplicate-btn:disabled {
  background-color: #f5f5f5 !important;
  border-color: #d9d9d9 !important;
  color: #bfbfbf !important;
  cursor: not-allowed !important;
}

.remove-duplicate-btn:not(:disabled):hover {
  background-color: #b45309 !important;
  border-color: #b45309 !important;
}

/* 导入选中用例按钮样式 */
.import-btn {
  display: flex !important;
  align-items: center !important;
  gap: 6px !important;
  padding: 8px 16px !important;
  min-width: 120px !important;
  background-color: #16a34a !important;
  border-color: #16a34a !important;
  color: #ffffff !important;
}

.import-btn .import-icon {
  width: 16px !important;
  height: 16px !important;
  flex-shrink: 0 !important;
}

.import-btn .btn-text {
  display: flex !important;
  align-items: center !important;
  gap: 4px !important;
  white-space: nowrap !important;
}

.import-btn:disabled {
  background-color: #f5f5f5 !important;
  border-color: #d9d9d9 !important;
  color: #bfbfbf !important;
  cursor: not-allowed !important;
}

.import-btn:not(:disabled):hover {
  background-color: #15803d !important;
  border-color: #15803d !important;
}

/* 选择文件按钮样式 */
.el-upload .el-button[type="primary"] {
  background-color: #2563eb !important;
  border-color: #2563eb !important;
  color: #ffffff !important;
}

.el-upload .el-button[type="primary"]:hover {
  background-color: #1d4ed8 !important;
  border-color: #1d4ed8 !important;
}

.el-upload .el-button[type="primary"]:disabled {
  background-color: #f5f5f5 !important;
  border-color: #d9d9d9 !important;
  color: #bfbfbf !important;
  cursor: not-allowed !important;
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

.status-tag.el-tag--info {
  background-color: #0369a1 !important;
  border-color: #0369a1 !important;
  color: white !important;
}

/* 重复状态标签动画样式 */
.duplicate-status-tag {
  transition: all 0.3s ease;
}

/* 重复状态切换动画 */
.duplicate-status-enter-active,
.duplicate-status-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.duplicate-status-leave-to {
  opacity: 0;
  transform: translateX(-20px) scale(0.8);
}

.duplicate-status-enter-from {
  opacity: 0;
  transform: translateX(30px) scale(0.8);
}

.duplicate-status-enter-to,
.duplicate-status-leave-from {
  opacity: 1;
  transform: translateX(0) scale(1);
}

/* 用例列表容器 */
.case-list-container {
  min-height: 600px;
  display: flex;
  flex-direction: column;
}

/* 空状态样式 */
.empty-state-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 600px;
  background: #fafafa;
  border: 2px dashed #d1d5db;
  border-radius: 12px;
  margin: 16px 0;
}

.empty-state-content {
  text-align: center;
  padding: 40px 20px;
  max-width: 400px;
}

.empty-state-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f3f4f6;
  border-radius: 50%;
  color: #9ca3af;
}

.empty-state-icon svg {
  width: 40px;
  height: 40px;
}

.empty-state-title {
  font-size: 20px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 12px 0;
}

.empty-state-description {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.6;
  margin: 0;
}
</style>