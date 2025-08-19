import axios from 'axios';

export function uploadCase(file, projectId = null) {
  const formData = new FormData();
  formData.append('file', file);
  if (projectId) {
    formData.append('project_id', projectId);
  }
  return axios.post('/upload_case', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
}

export function importCase(cases, projectId) {
  return axios.post('/import_case', { cases, project_id: projectId });
}

// 项目管理相关API
export function getProjects() {
  return axios.get('/project')
    .then(response => response.data);
}

export function createProject(project) {
  return axios.post('/project', project)
    .then(response => response.data);
}

export function updateProject(projectId, project) {
  return axios.put(`/project/${projectId}`, project)
    .then(response => response.data);
}

export function deleteProject(projectId) {
  return axios.delete(`/project/${projectId}`)
    .then(response => response.data);
}

export function getProjectTestcases(projectId) {
  return axios.get(`/project/${projectId}/testcases`)
    .then(response => response.data);
}

// 新增测试用例相关API
export function addTestCase(projectId, testcase) {
  return axios.post(`/project/${projectId}/testcase`, testcase)
    .then(response => response.data);
}

export function updateTestCase(testcaseId, testcase) {
  return axios.put(`/test_case/${testcaseId}`, testcase)
    .then(response => response.data);
}

export function deleteTestCase(testcaseId) {
  return axios.delete(`/test_case/${testcaseId}`)
    .then(response => response.data);
}

// 更新测试用例状态
export function updateTestCaseStatus(testCaseId, status) {
  return axios.put(`/test_case/${testCaseId}/status`, { status })
    .then(response => response.data);
}

// 检查case_id是否重复
export function checkCaseIdDuplicate(projectId, caseId) {
  return axios.post('/test_case/check_duplicate', { 
    project_id: projectId, 
    case_id: caseId 
  })
    .then(response => response.data);
}