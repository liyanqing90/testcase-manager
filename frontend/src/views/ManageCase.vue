<template>
  <div class="manage-case-container" v-loading="pageLoading" element-loading-text="加载项目中..." element-loading-background="rgba(255, 255, 255, 0.8)">
    <!-- 页面操作栏 -->
    <div class="page-header">
      <div class="header-content">
        <div class="filter-section">
          <el-input
            v-model="filterText"
            placeholder="搜索项目ID、名称或维护人员"
            class="filter-input"
            clearable
            @input="handleFilter"
          >
            <template #prefix>
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 21L16.514 16.506L21 21ZM19 10.5C19 15.194 15.194 19 10.5 19C5.806 19 2 15.194 2 10.5C2 5.806 5.806 2 10.5 2C15.194 2 19 5.806 19 10.5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </template>
          </el-input>
        </div>
        <div class="header-actions">
          <el-button type="primary" class="create-btn" @click="openCreateDialog">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            创建项目
          </el-button>
        </div>
      </div>
    </div>

    <!-- 项目列表 -->
    <div class="projects-container">
      <div class="projects-grid">
        <div
          v-for="project in filteredProjects"
          :key="project.id"
          class="project-card"
          @click="viewTestCases(project)"
        >
          <div class="project-header">
            <div class="project-icon">
              <img src="/src/icon/MBE风格常用图标-文件夹.png" alt="项目图标" />
            </div>
            <div class="project-info">
              <h3 class="project-name">{{ project.name }}</h3>
              <p class="project-description">{{ project.description || '暂无描述' }}</p>
            </div>
            <div class="project-actions">
              <el-button
                size="small"
                link
                @click.stop="openEditDialog(project)"
                class="action-btn edit-btn"
              >
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M11 4H4C3.46957 4 2.96086 4.21071 2.58579 4.58579C2.21071 4.96086 2 5.46957 2 6V20C2 20.5304 2.21071 21.0391 2.58579 21.4142C2.96086 21.7893 3.46957 22 4 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V13M18.5 2.5C18.8978 2.10217 19.4374 1.87868 20 1.87868C20.5626 1.87868 21.1022 2.10217 21.5 2.5C21.8978 2.89782 22.1213 3.43739 22.1213 4C22.1213 4.56261 21.8978 5.10217 21.5 5.5L12 15L8 16L9 12L18.5 2.5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </el-button>
              <el-button
                size="small"
                link
                @click.stop="deleteProject(project.id)"
                class="action-btn delete-btn"
              >
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M3 6H5H21M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 3.46957 16 4V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </el-button>
            </div>
          </div>
          <div class="project-footer">
            <div class="project-meta">
              <span class="meta-item">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M12 14C8.13401 14 5 17.134 5 21H19C19 17.134 15.866 14 12 14Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                {{ project.maintainers || '未设置维护人员' }}
              </span>
              <span class="meta-item">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 8V12L15 15M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                项目ID: {{ project.id }}
              </span>
            </div>

          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="filteredProjects.length === 0" class="empty-state">
        <div class="empty-icon">
          <svg v-if="filterText" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 21L16.514 16.506L21 21ZM19 10.5C19 15.194 15.194 19 10.5 19C5.806 19 2 15.194 2 10.5C2 5.806 5.806 2 10.5 2C15.194 2 19 5.806 19 10.5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M19 11H5M19 11C20.1046 11 21 11.8954 21 13V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V13C3 11.8954 3.89543 11 5 11M19 11V9C19 7.89543 18.1046 7 17 7M5 11V9C5 7.89543 5.89543 7 7 7M7 7V5C7 3.89543 7.89543 3 9 3H15C16.1046 3 17 3.89543 17 5V7M7 7H17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h3 class="empty-title">{{ filterText ? '未找到匹配的项目' : '暂无项目' }}</h3>
        <p class="empty-description">{{ filterText ? '请尝试调整搜索条件' : '创建您的第一个项目来开始管理测试用例' }}</p>
        <el-button v-if="!filterText" type="primary" @click="openCreateDialog">创建项目</el-button>
        <el-button v-else type="default" @click="clearFilter">清除筛选</el-button>
      </div>
    </div>

    <!-- 创建/编辑项目弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      width="500px"
      @close="resetForm"
      :show-close="true"
      :close-on-click-modal="false"
    >
      <template #header>
        <div class="dialog-header-center">
          <h3 class="dialog-title">{{ isEditing ? '编辑项目' : '创建项目' }}</h3>
        </div>
      </template>

      <el-form :model="projectForm" :rules="projectRules" ref="projectFormRef" label-width="100px">
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="projectForm.name" placeholder="请输入项目名称"></el-input>
        </el-form-item>
        <el-form-item label="项目描述" prop="description">
          <el-input
            v-model="projectForm.description"
            type="textarea"
            placeholder="请输入项目描述"
            :rows="3">
          </el-input>
        </el-form-item>
        <el-form-item label="用例维护人员" prop="maintainers">
          <el-input
            v-model="projectForm.maintainers"
            placeholder="请输入用例维护人员（多个用逗号分隔）">
          </el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitProject">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 项目用例侧边栏 -->
    <el-drawer
      v-model="drawerVisible"
      direction="rtl"
      size="60%"
      :modal="true"
      :with-header="false"
      :before-close="handleDrawerClose"
      :close-on-click-modal="false"
    >
      <!-- 收缩按钮 -->
      <div v-if="drawerVisible && !detailDialogVisible" class="drawer-toggle-button" @click="closeDrawer">
        <div class="toggle-button-inner">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
      </div>

      <div v-if="currentProject" class="testcase-container">
        <!-- 页面头部 -->
        <div class="testcase-header">
          <div class="header-content">
            <div class="header-left">
              <h2 class="page-title">测试用例列表</h2>
              <p class="project-info">项目：{{ currentProject.name }}</p>
            </div>
            <div class="header-right">
              <el-button type="primary" class="upload-btn" @click="uploadTestCases">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15M17 8L12 3M12 3L7 8M12 3V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                上传用例
              </el-button>
            </div>
          </div>

          <!-- 搜索区域 -->
          <div class="search-section">
            <el-input
              v-model="testCaseSearchText"
              placeholder="搜索用例ID、优先级、状态"
              class="testcase-search-input"
              clearable
              @input="handleTestCaseSearch"
            >
              <template #prefix>
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M21 21L16.514 16.506L21 21ZM19 10.5C19 15.194 15.194 19 10.5 19C5.806 19 2 15.194 2 10.5C2 5.806 5.806 2 10.5 2C15.194 2 19 5.806 19 10.5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </template>
            </el-input>
          </div>
        </div>

        <!-- 用例列表卡片 -->
        <div class="testcase-content">
          <el-card shadow="never" class="testcase-card">
            <div class="table-container" v-loading="loading">
              <el-table
                :data="filteredTestCases.length > 0 ? filteredTestCases : testCases"
                class="testcase-table"
                :row-class-name="tableRowClassName"
                @row-click="handleRowClick"
                empty-text=""
              >
                <el-table-column prop="case_id" label="用例ID" width="140" class-name="case-id-column">
                  <template #default="scope">
                    <div class="case-id">
                      <span class="case-id-text">{{ scope.row.case_id }}</span>
            </div>
          </template>
                </el-table-column>

                <el-table-column prop="title" label="用例标题" min-width="200">
              <template #default="scope">
                    <div class="case-title">
                      <h4 class="title-text">{{ scope.row.title || '无标题' }}</h4>
                      <p class="title-desc">{{ scope.row.description || '暂无描述' }}</p>
                    </div>
                  </template>
                </el-table-column>

                <el-table-column prop="priority" label="优先级" width="120" align="center">
                  <template #default="scope">
                    <el-tag
                      :type="getPriorityType(scope.row.priority)"
                      class="priority-tag"
                      size="small"
                    >
                      {{ scope.row.priority || '未设置' }}
                    </el-tag>
                  </template>
                </el-table-column>

                <el-table-column prop="status" label="状态" width="120" align="center">
                  <template #default="scope">
                    <el-tag
                      :type="getStatusType(scope.row.status)"
                      class="status-tag"
                      size="small"
                    >
                      {{ getStatusDisplay(scope.row.status) }}
                    </el-tag>
                  </template>
                </el-table-column>

                <el-table-column label="操作" width="180" align="center">
                  <template #default="scope">
                    <div class="action-buttons">
                      <el-button
                        type="primary"
                        size="small"
                        class="view-btn"
                        @click.stop="viewTestCase(scope.row)"
                      >
                        查看用例
                      </el-button>
                      <el-button
                        type="danger"
                        size="small"
                        class="testcase-delete-btn"
                        @click.stop="deleteTestCase(scope.row)"
                      >
                        删除用例
                      </el-button>
                    </div>
                  </template>
                </el-table-column>
          </el-table>

              <!-- 空状态 -->
              <div v-if="!loading && testCases.length === 0" class="empty-state">
                <div class="empty-icon">
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <h3 class="empty-title">暂无测试用例</h3>
                <p class="empty-desc">点击上方"上传用例"按钮开始添加测试用例</p>
              </div>
            </div>
        </el-card>
        </div>

        <!-- 用例详情弹窗 -->
        <el-dialog
          v-model="detailDialogVisible"
          width="1000px"
          :show-close="true"
          :close-on-click-modal="false"
          class="testcase-detail-dialog"
        >

          <template #header>
            <div class="detail-dialog-header">
              <h3 class="detail-dialog-title">用例详情</h3>
            </div>
          </template>
          <div class="dialog-content-wrapper">
          <el-form label-width="120px" v-if="currentTestCase">
            <el-form-item label="基本信息:">
              <div class="form-item-content">
                <div class="basic-info-row">
                  <div class="info-item">
                    <span class="info-label">用例ID:</span>
                    <span class="info-value">{{ currentTestCase.case_id }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">优先级:</span>
                    <el-tag
                      :type="getPriorityType(currentTestCase.priority)"
                      class="priority-tag"
                      size="small"
                    >
                      {{ currentTestCase.priority || '未设置' }}
                    </el-tag>
                  </div>
                  <div class="info-item">
                    <span class="info-label">分类:</span>
                    <span class="info-value">{{ currentTestCase.category || '无' }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">状态:</span>
                    <el-tag
                      :type="getStatusType(currentTestCase.status)"
                      class="status-tag"
                      size="small"
                    >
                      {{ getStatusDisplay(currentTestCase.status) }}
                    </el-tag>
                  </div>
                </div>
              </div>
            </el-form-item>
            <el-form-item label="用例标题:">
              <div class="form-item-content">{{ currentTestCase.title }}</div>
            </el-form-item>
            <el-form-item label="用例描述:">
              <div class="form-item-content">{{ currentTestCase.description || '无' }}</div>
            </el-form-item>
            <el-form-item label="前置条件:">
              <div class="form-item-content">{{ currentTestCase.preconditions || '无' }}</div>
            </el-form-item>
            <el-form-item label="操作步骤:">
              <div class="form-item-content">{{ currentTestCase.steps || '无' }}</div>
            </el-form-item>
            <el-form-item label="预期结果:">
              <div class="form-item-content">{{ currentTestCase.expected_results || '无' }}</div>
            </el-form-item>
          </el-form>
          </div>
          <template #footer>
            <!-- 标记按钮 -->
            <div class="mark-complete-section">
              <div class="mark-complete-btn"
                   @click="markAsComplete"
                   :class="{ 'marking': isMarkingComplete }"
                   :style="{ pointerEvents: isMarkingComplete ? 'none' : 'auto' }"
              >
                <div class="mark-icon" :class="{ 'completed': currentTestCase && (currentTestCase.status === '已完成' || currentTestCase.status === 'success') && !isMarkingComplete }">
                  <svg v-if="isMarkingComplete" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2V6M12 18V22M4.93 4.93L7.76 7.76M16.24 16.24L19.07 19.07M2 12H6M18 12H22M4.93 19.07L7.76 16.24M16.24 7.76L19.07 4.93" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <svg v-else-if="currentTestCase && (currentTestCase.status === '已完成' || currentTestCase.status === 'success')" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <span class="mark-text">
                  {{ isMarkingComplete ? '处理中...' : (currentTestCase && (currentTestCase.status === '已完成' || currentTestCase.status === 'success') ? '已完成' : '标记完成') }}
                </span>
              </div>
            </div>

            <div class="dialog-footer">
              <div
                v-if="currentTestCaseIndex > 0"
                class="nav-area nav-left-bottom"
                :class="{ 'disabled': isNavigating }"
                @click="showPreviousTestCase"
              >
                <div class="nav-arrow">
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
              </div>

              <div class="case-counter">
                {{ currentTestCaseIndex + 1 }} / {{ testCases.length }}
              </div>

              <div
                v-if="currentTestCaseIndex < testCases.length - 1"
                class="nav-area nav-right-bottom"
                :class="{ 'disabled': isNavigating }"
                @click="showNextTestCase"
              >
                <div class="nav-arrow">
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
              </div>
            </div>
          </template>
        </el-dialog>
      </div>
    </el-drawer>
  </div>
</template>

<script>
import {
  getProjects,
  createProject,
  updateProject,
  deleteProject,
  getProjectTestcases,
  updateTestCaseStatus,
  deleteTestCase
} from '@/api/case.js';

export default {
  name: 'ManageCase',
  data() {
    return {
      projects: [],
      filterText: '',
      dialogVisible: false,
      drawerVisible: false,
      projectForm: {
        name: '',
        description: '',
        maintainers: ''  // 添加维护人员字段
      },
      isEditing: false,
      editingProjectId: null,
      projectRules: {
        name: [
          { required: true, message: '请输入项目名称', trigger: 'blur' }
        ]
      },
      currentProject: null,
      testCases: [],
      loading: false,
      pageLoading: false, // 页面级loading状态
      detailDialogVisible: false,
      currentTestCase: null,
      currentTestCaseIndex: -1,
      isMarkingComplete: false,  // 添加标记状态控制
      isNavigating: false,       // 添加导航状态控制
      testCaseSearchText: '',    // 用例搜索文本
      filteredTestCases: []      // 过滤后的用例列表
    };
  },
  mounted() {
    this.loadProjects();
  },
  computed: {
    // 筛选项目
    filteredProjects() {
      let projects = this.projects;
      
      // 按ID升序排序
      projects = projects.sort((a, b) => a.id - b.id);
      
      if (!this.filterText) {
        return projects;
      }

      const searchText = this.filterText.toLowerCase();
      return projects.filter(project => {
        return (
          project.id.toString().includes(searchText) ||
          project.name.toLowerCase().includes(searchText) ||
          (project.maintainers && project.maintainers.toLowerCase().includes(searchText))
        );
      });
    }
  },
  methods: {
    async loadProjects() {
      this.pageLoading = true;
      try {
        const data = await getProjects();
        this.projects = data.projects || [];
      } catch (err) {
        this.$message.error('加载项目列表失败: ' + (err.response?.data?.error || err.message));
      } finally {
        this.pageLoading = false;
      }
    },

      // 处理筛选
      handleFilter() {
        // 筛选逻辑已在computed中处理
      },

      // 处理用例搜索
      handleTestCaseSearch() {
        if (!this.testCaseSearchText.trim()) {
          this.filteredTestCases = [];
          return;
        }

        const searchText = this.testCaseSearchText.toLowerCase().trim();

        this.filteredTestCases = this.testCases.filter(testCase => {
          // 搜索用例ID
          if (testCase.case_id && testCase.case_id.toLowerCase().includes(searchText)) {
            return true;
          }

          // 搜索优先级
          if (testCase.priority && testCase.priority.toLowerCase().includes(searchText)) {
            return true;
          }

          // 搜索状态（包括显示文本和数据库值）
          const statusDisplay = this.getStatusDisplay(testCase.status);
          if (statusDisplay && statusDisplay.toLowerCase().includes(searchText)) {
            return true;
          }
          if (testCase.status && testCase.status.toLowerCase().includes(searchText)) {
            return true;
          }

          return false;
        });
      },

      // 清除筛选
      clearFilter() {
        this.filterText = '';
      },

      // 处理抽屉关闭
      handleDrawerClose(done) {
        this.closeDrawer();
        done();
      },

    async viewTestCases(project) {
      this.currentProject = project;
      this.drawerVisible = true;
      // 禁用侧边栏
      this.$emit('sidebar-disabled', true);
      await this.loadTestCases(project.id);
    },

    async loadTestCases(projectId) {
      this.loading = true;
      try {
        const data = await getProjectTestcases(projectId);
        this.testCases = data.testcases || [];
        this.filteredTestCases = []; // 重置过滤列表
        this.testCaseSearchText = ''; // 清空搜索文本
      } catch (err) {
        this.$message.error('加载测试用例失败: ' + (err.response?.data?.error || err.message));
      } finally {
        this.loading = false;
      }
    },

    closeDrawer() {
      this.drawerVisible = false;
      this.currentProject = null;
      this.testCases = [];
      // 启用侧边栏
      this.$emit('sidebar-disabled', false);
    },

    viewTestCase(testCase) {
      this.currentTestCase = testCase;
      // 找到当前用例在数组中的索引
      this.currentTestCaseIndex = this.testCases.findIndex(tc => tc.id === testCase.id);
      this.detailDialogVisible = true;
    },

    // 显示上一条用例
    showPreviousTestCase() {
      // 防止快速连续点击
      if (this.isNavigating) return;
      
      if (this.currentTestCaseIndex > 0) {
        this.isNavigating = true;
        
        // 添加滑动动画
        this.addSlideAnimation('left');

        setTimeout(() => {
          this.currentTestCaseIndex--;
          this.currentTestCase = this.testCases[this.currentTestCaseIndex];
          this.removeSlideAnimation();
          
          // 动画完成后重置导航状态
          setTimeout(() => {
            this.isNavigating = false;
          }, 400);
        }, 200);
      }
    },

    // 显示下一条用例
    showNextTestCase() {
      // 防止快速连续点击
      if (this.isNavigating) return;
      
      if (this.currentTestCaseIndex < this.testCases.length - 1) {
        this.isNavigating = true;
        
        // 添加滑动动画
        this.addSlideAnimation('right');

        setTimeout(() => {
          this.currentTestCaseIndex++;
          this.currentTestCase = this.testCases[this.currentTestCaseIndex];
          this.removeSlideAnimation();
          
          // 动画完成后重置导航状态
          setTimeout(() => {
            this.isNavigating = false;
          }, 400);
        }, 200);
      }
    },

    // 添加滑动动画
    addSlideAnimation(direction) {
      const dialogBody = document.querySelector('.testcase-detail-dialog .el-dialog__body');
      if (dialogBody) {
        dialogBody.style.transition = 'transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.4s ease';
        if (direction === 'left') {
          dialogBody.style.transform = 'translateX(-30px)';
          dialogBody.style.opacity = '0.7';
        } else {
          dialogBody.style.transform = 'translateX(30px)';
          dialogBody.style.opacity = '0.7';
        }
      }
    },

    // 移除滑动动画
    removeSlideAnimation() {
      const dialogBody = document.querySelector('.testcase-detail-dialog .el-dialog__body');
      if (dialogBody) {
        setTimeout(() => {
          dialogBody.style.transition = 'transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94), opacity 0.4s ease';
          dialogBody.style.transform = 'translateX(0)';
          dialogBody.style.opacity = '1';
        }, 100);
      }
    },

    // 标记用例为已完成
    async markAsComplete() {
      if (!this.currentTestCase) return;

      // 防止重复点击
      if (this.isMarkingComplete) {
        return;
      }

      // 如果已经是已完成状态，直接返回
      if (this.currentTestCase.status === 'success' || this.currentTestCase.status === '已完成') {
        this.$message.info('用例已经是已完成状态');
        return;
      }

      this.isMarkingComplete = true;

      try {
        // 调用后端API更新状态
        await updateTestCaseStatus(this.currentTestCase.id, 'success');

        // 延迟更新状态，确保处理中动画完整显示
        setTimeout(() => {
          // 更新当前用例的状态为数据库中的值
          this.currentTestCase.status = 'success';

          // 同时更新testCases数组中对应用例的状态
          const index = this.testCases.findIndex(tc => tc.id === this.currentTestCase.id);
          if (index !== -1) {
            this.testCases[index].status = 'success';
          }

          // 强制更新视图 - 使用Vue的响应式更新
          this.$nextTick(() => {
            // 触发响应式更新
            this.testCases = [...this.testCases];
            this.currentTestCase = { ...this.currentTestCase };
          });

          this.$message.success('用例已标记为已完成');
        }, 500); // 延迟500ms，让用户看到处理中动画

      } catch (error) {
        this.$message.error('标记失败: ' + (error.response?.data?.error || error.message));
        // 如果失败，恢复原状态
        const index = this.testCases.findIndex(tc => tc.id === this.currentTestCase.id);
        if (index !== -1) {
          this.currentTestCase.status = this.testCases[index].status || 'draft';
        }
      } finally {
        // 延迟重置状态，防止快速连续点击
        setTimeout(() => {
          this.isMarkingComplete = false;
        }, 1000);
      }
    },

    // 删除测试用例
    async deleteTestCase(testCase) {
      try {
        await this.$confirm(`确认删除测试用例 "${testCase.case_id}" 吗？此操作不可恢复`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        });

        this.loading = true;
        
        // 调用后端删除API
        const response = await deleteTestCase(testCase.id);
        
        if (response && response.message) {
          // 删除成功后从本地数组中移除该用例
          this.testCases = this.testCases.filter(tc => tc.id !== testCase.id);
          
          // 如果当前查看的用例被删除，关闭详情弹窗
          if (this.currentTestCase && this.currentTestCase.id === testCase.id) {
            this.detailDialogVisible = false;
            this.currentTestCase = null;
            this.currentTestCaseIndex = -1;
          }
          
          this.$message.success(response.message);
        } else {
          this.$message.success('用例删除成功');
        }
        
      } catch (err) {
        if (err !== 'cancel') {
          const errorMsg = err.response?.data?.error || err.message || '删除用例失败';
          this.$message.error(errorMsg);
        }
      } finally {
        this.loading = false;
      }
    },

    // 表格行样式
    tableRowClassName({ row, rowIndex }) {
      return 'table-row-hover';
    },

    // 行点击事件
    handleRowClick(row, column, event) {
      // 可以在这里添加行点击逻辑
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

    uploadTestCases() {
      // 恢复侧边栏状态
      this.$emit('sidebar-disabled', false);
      // 跳转到上传页面，并传递项目ID
      this.$router.push({
        name: 'UploadCase',
        query: { projectId: this.currentProject.id }
      });
    },

    openCreateDialog() {
      this.isEditing = false;
      this.dialogVisible = true;
    },

    openEditDialog(project) {
      this.isEditing = true;
      this.editingProjectId = project.id;
      this.projectForm.name = project.name;
      this.projectForm.description = project.description;
      this.projectForm.maintainers = project.maintainers || '';
      this.dialogVisible = true;
    },

    submitProject() {
      this.$refs.projectFormRef.validate(async (valid) => {
        if (valid) {
          this.pageLoading = true;
          try {
            if (this.isEditing) {
              // 更新项目
              const data = await updateProject(this.editingProjectId, this.projectForm);
              this.$message.success('项目更新成功');
            } else {
              // 创建项目
              const data = await createProject(this.projectForm);
              this.$message.success('项目创建成功');
            }

            this.dialogVisible = false;
            this.resetForm();
            await this.loadProjects();
          } catch (err) {
            this.$message.error((this.isEditing ? '更新' : '创建') + '项目失败: ' + (err.response?.data?.error || err.message));
          } finally {
            this.pageLoading = false;
          }
        }
      });
    },

    async deleteProject(projectId) {
      try {
        await this.$confirm('确认删除该项目吗？此操作不可恢复', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        });

        this.pageLoading = true;
        const data = await deleteProject(projectId);
        this.$message.success('项目删除成功');
        await this.loadProjects();

        // 如果删除的是当前查看用例的项目，则关闭侧边栏
        if (this.currentProject && this.currentProject.id === projectId) {
          this.drawerVisible = false;
        }

        // 通知其他组件项目已删除
        this.$emit('project-deleted', projectId);
      } catch (err) {
        if (err !== 'cancel') {
          this.$message.error('删除项目失败: ' + (err.response?.data?.error || err.message));
        }
      } finally {
        this.pageLoading = false;
      }
    },

    resetForm() {
      this.$refs.projectFormRef.resetFields();
      this.isEditing = false;
      this.editingProjectId = null;
      this.projectForm = {
        name: '',
        description: '',
        maintainers: ''
      };
    }
  }
};
</script>

<style scoped>
/* 容器样式 */
.manage-case-container {
  padding: 0;
}

/* 页面操作栏 */
.page-header {
  margin-bottom: 24px;
  padding: 0;
}

.header-content {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 16px;
}

.filter-section {
  flex: 0 0 auto;
  width: 400px;
}

.filter-input {
  width: 100%;
}

.filter-input :deep(.el-input__wrapper) {
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.filter-input :deep(.el-input__prefix) {
  color: #64748b;
}

.create-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  font-weight: 600;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
}

.create-btn svg {
  width: 18px;
  height: 18px;
}

.header-actions {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

/* 项目网格 */
.projects-container {
  margin-top: 24px;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

/* 项目卡片 */
.project-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 28px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.project-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-color: #cbd5e1;
}

/* 项目头部 */
.project-header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 20px;
}

.project-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.project-icon img {
  width: 56px;
  height: 56px;
  object-fit: contain;
}

.project-info {
  flex: 1;
  min-width: 0;
}

.project-name {
  margin: 0 0 10px 0;
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.3;
  font-family: 'PingFang SC', 'Helvetica Neue', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

.project-description {
  margin: 0;
  font-size: 15px;
  color: #64748b;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  font-family: 'PingFang SC', 'Helvetica Neue', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

/* 项目操作 */
.project-actions {
  display: flex;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.project-card:hover .project-actions {
  opacity: 1;
}

.action-btn {
  width: 32px;
  height: 32px;
  padding: 0;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.edit-btn {
  color: #3b82f6;
}

.edit-btn:hover {
  background: #eff6ff;
}

.delete-btn {
  color: #ef4444 !important;
}

.delete-btn:hover {
  background: #fef2f2 !important;
}

/* 使用深度选择器确保样式生效 */
:deep(.action-btn.delete-btn) {
  color: #ef4444 !important;
}

:deep(.action-btn.delete-btn:hover) {
  background: #fef2f2 !important;
}

/* 项目底部 */
.project-footer {
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  padding-top: 20px;
  border-top: 1px solid #f1f5f9;
  margin-top: 20px;
}

.project-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #64748b;
  font-family: 'PingFang SC', 'Helvetica Neue', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

.meta-item svg {
  width: 14px;
  height: 14px;
  flex-shrink: 0;
}

.project-status {
  display: flex;
  align-items: center;
}

.status-badge {
  padding: 6px 14px;
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  color: #166534;
  font-size: 13px;
  font-weight: 600;
  border-radius: 16px;
  font-family: 'PingFang SC', 'Helvetica Neue', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  box-shadow: 0 2px 4px rgba(22, 101, 52, 0.1);
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border: 2px dashed #e2e8f0;
  border-radius: 12px;
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  background: #f8fafc;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
}

.empty-icon svg {
  width: 40px;
  height: 40px;
}

.empty-title {
  margin: 0 0 12px 0;
  font-size: 20px;
  font-weight: 600;
  color: #374151;
}

.empty-description {
  margin: 0 0 24px 0;
  font-size: 16px;
  color: #6b7280;
  line-height: 1.5;
}

/* 弹窗样式 */
:deep(.el-dialog) {
  margin: 0 auto !important;
  position: absolute !important;
  top: 50% !important;
  left: 50% !important;
  transform: translate(-50%, -50%) !important;
}

:deep(.el-dialog__wrapper) {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 16px;
}

.dialog-footer {
  text-align: right;
}

/* 弹窗标题居中样式 */
.dialog-header-center {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding: 0;
  margin: 0;
}

.dialog-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  text-align: center;
  font-family: 'PingFang SC', 'Helvetica Neue', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  line-height: 1.2;
  padding: 0;
}

/* 弹窗头部样式优化 */
:deep(.el-dialog__header) {
  padding: 16px 20px 8px 20px;
  border-bottom: none;
  margin: 0;
}

:deep(.el-dialog__headerbtn) {
  top: 16px;
  right: 20px;
}

:deep(.el-dialog__body) {
  padding: 8px 20px 16px 20px;
}

:deep(.el-dialog__footer) {
  padding: 0 20px 16px 20px;
  border-top: none;
}

/* 弹窗表单样式优化 */
:deep(.el-dialog .el-form-item) {
  margin-bottom: 16px;
}

:deep(.el-dialog .el-form-item__label) {
  line-height: 1.4;
  padding-bottom: 6px;
}

:deep(.el-dialog .el-input__wrapper) {
  padding: 8px 12px;
}

:deep(.el-dialog .el-textarea__inner) {
  padding: 8px 12px;
}

/* 页面loading样式优化 */
:deep(.el-loading-mask) {
  background-color: rgba(255, 255, 255, 0.9) !important;
  backdrop-filter: blur(4px);
  border-radius: 16px; /* 新增圆角样式 */
}

:deep(.el-loading-spinner) {
  margin-top: -20px;
}

:deep(.el-loading-text) {
  color: #3b82f6 !important;
  font-weight: 600;
  font-size: 16px;
  margin-top: 12px;
}

:deep(.el-loading-spinner .path) {
  stroke: #3b82f6 !important;
}

/* 抽屉收缩按钮样式 */
.drawer-toggle-button {
  position: fixed;
  top: 50%;
  left: calc(40% - 16px); /* 60%的抽屉宽度，按钮在抽屉左侧边缘 */
  transform: translateY(-50%);
  z-index: 9999;
  cursor: pointer;
}

.toggle-button-inner {
  width: 32px;
  height: 32px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6B7280;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
  border: 2px solid #E5E7EB;
}

.toggle-button-inner:hover {
  background: #F3F4F6;
  color: #374151;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transform: scale(1.05);
}

.toggle-button-inner svg {
  width: 16px;
  height: 16px;
  transition: transform 0.3s ease;
}

/* 抽屉样式优化 */
:deep(.el-drawer) {
  /* 让Element Plus自己处理定位 */
}

:deep(.el-drawer__body) {
  padding: 0;
  height: 100%;
  overflow-y: auto;
}

/* 用例列表页面样式 */
.testcase-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #f8fafc;
}

.testcase-header {
  background: white;
  padding: 24px 32px;
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.page-title {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  font-family: 'PingFang SC', 'Helvetica Neue', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

.project-info {
  margin: 0;
  font-size: 14px;
  color: #64748b;
  font-family: 'PingFang SC', 'Helvetica Neue', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

.header-right {
  display: flex;
  align-items: center;
}

/* 搜索区域样式 */
.search-section {
  margin-top: 16px;
  margin-bottom: 0;
}

.testcase-search-input {
  width: 100%;
}

.testcase-search-input :deep(.el-input__wrapper) {
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

.testcase-search-input :deep(.el-input__wrapper:hover) {
  border-color: #cbd5e1;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

.testcase-search-input :deep(.el-input__wrapper.is-focus) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.testcase-search-input :deep(.el-input__prefix) {
  color: #64748b;
}

.upload-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  font-weight: 600;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
}

.upload-btn svg {
  width: 16px;
  height: 16px;
}

.testcase-content {
  flex: 1;
  padding: 24px 32px;
  overflow-y: auto;
}

.testcase-card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.table-container {
  position: relative;
  min-height: 400px;
}

/* 表格样式优化 */
.testcase-table {
  border: none;
}

.testcase-table :deep(.el-table__header) {
  background: #f8fafc;
}

.testcase-table :deep(.el-table__header th) {
  background: #f8fafc;
  color: #374151;
  font-weight: 600;
  font-size: 14px;
  border-bottom: 1px solid #e2e8f0;
}

.testcase-table :deep(.el-table__body tr) {
  transition: all 0.2s ease;
}

.testcase-table :deep(.el-table__body tr:hover) {
  background: #f1f5f9;
}

.testcase-table :deep(.el-table__body td) {
  border-bottom: 1px solid #f1f5f9;
  padding: 16px 0;
}

/* 用例ID列样式 */
.case-id {
  display: flex;
  align-items: center;
}

.case-id-text {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
  color: #1f2937;
  background: #e5e7eb;
  padding: 6px 10px;
  border-radius: 6px;
  font-weight: 700;
}

/* 用例标题列样式 */
.case-title {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.title-text {
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  color: #1f2937;
  line-height: 1.4;
}

.title-desc {
  margin: 0;
  font-size: 13px;
  color: #6b7280;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
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

/* 查看按钮样式 */
.view-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  margin: 0 auto;
}

/* 操作按钮容器样式 */
.action-buttons {
  display: flex;
  gap: 8px;
  justify-content: center;
  align-items: center;
}

/* 删除按钮样式 */
.testcase-delete-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  background-color: #dc2626 !important;
  border-color: #dc2626 !important;
  color: white !important;
}

.testcase-delete-btn:hover {
  background-color: #b91c1c !important;
  border-color: #b91c1c !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
}

.testcase-delete-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(220, 38, 38, 0.2);
}

/* 空状态样式 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin-bottom: 24px;
  background: #f8fafc;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
}

.empty-icon svg {
  width: 40px;
  height: 40px;
}

.empty-title {
  margin: 0 0 12px 0;
  font-size: 18px;
  font-weight: 600;
  color: #374151;
}

.empty-desc {
  margin: 0;
  font-size: 14px;
  color: #6b7280;
  line-height: 1.5;
}

/* 表格行悬停效果 */
.table-row-hover {
  transition: all 0.2s ease;
}

.table-row-hover:hover {
  background: #f1f5f9 !important;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* 用例详情弹窗样式 */
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

/* 用例详情弹窗头部样式优化 */
:deep(.el-dialog__header) {
  padding: 20px 20px 0 20px;
  border-bottom: none;
  margin: 0;
}

:deep(.el-dialog__headerbtn) {
  top: 20px;
  right: 20px;
}

:deep(.el-dialog__body) {
  padding: 20px 20px 0 20px;
}

:deep(.el-dialog__footer) {
  padding: 0 20px 20px 20px;
  border-top: none;
}

/* 用例详情弹窗表单项内容样式 */
.form-item-content {
  min-height: 20px;
  line-height: 1.5;
  white-space: pre-line;
  word-break: break-word;
  padding: 4px 0;
  color: #374151;
  font-size: 14px;
}

/* 基本信息行样式 */
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

.info-value {
  color: #374151;
  font-size: 14px;
  font-weight: 500;
}

/* 确保所有表单项内容对齐 */
:deep(.el-form-item__content) {
  display: flex;
  align-items: flex-start;
  min-height: 20px;
}

:deep(.el-form-item__label) {
  line-height: 1.5;
  padding-top: 4px;
  color: #6b7280;
  font-weight: 500;
}

/* 用例详情弹窗样式 */
.testcase-detail-dialog {
  position: relative;
}

/* 弹窗内容包装器 - 固定高度和滚动 */
.dialog-content-wrapper {
  height: 400px;
  overflow-y: auto;
  padding-right: 8px;
}

/* 隐藏滚动条 */
.dialog-content-wrapper::-webkit-scrollbar {
  display: none;
}

.dialog-content-wrapper {
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
}

/* 弹窗固定高度 */
:deep(.testcase-detail-dialog .el-dialog) {
  height: 620px;
  display: flex;
  flex-direction: column;
}

:deep(.testcase-detail-dialog .el-dialog__body) {
  height: 460px;
  overflow: hidden;
  padding: 20px 20px 0 20px;
}

/* 底部导航区域 */
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

.nav-left-bottom {
  margin-right: 16px;
}

.nav-right-bottom {
  margin-left: 16px;
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

/* 导航按钮禁用状态 */
.nav-area.disabled {
  pointer-events: none;
  opacity: 0.5;
  cursor: not-allowed;
}

.nav-area.disabled .nav-arrow {
  background: #9ca3af;
  box-shadow: none;
}

/* 底部导航样式 */
.dialog-footer {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  gap: 8px;
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
}

/* 滑动动画样式 */
:deep(.testcase-detail-dialog .el-dialog__body) {
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.4s ease;
  will-change: transform, opacity;
}

/* 标记完成按钮样式 */
.mark-complete-section {
  display: flex;
  justify-content: center;
  margin-bottom: 16px;
  padding: 0 20px;
}

.mark-complete-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: #f8fafc;
  border: 2px solid #e2e8f0;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.mark-complete-btn:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.mark-complete-btn.marking {
  background: #f3f4f6;
  border-color: #d1d5db;
  cursor: not-allowed;
  opacity: 0.7;
}

.mark-complete-btn.marking .mark-icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.mark-icon {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  transition: all 0.3s ease;
}

.mark-icon.completed {
  color: #10b981;
}

.mark-icon svg {
  width: 20px;
  height: 20px;
}

.mark-text {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  white-space: nowrap;
}

/* 弹窗相对定位，确保标记按钮定位正确 */
:deep(.testcase-detail-dialog) {
  position: relative;
}
</style>