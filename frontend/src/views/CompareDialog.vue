<template>
  <el-dialog
    :model-value="visible"
    width="900px"
    class="compare-dialog"
    :close-on-click-modal="false"
    :show-close="true"
    @close="$emit('update:visible', false)"
  >
    <template #title>
      <span>重复用例对比</span>
    </template>
    <div class="compare-table-wrapper">
      <table class="compare-table">
        <thead>
          <tr>
            <th class="side">用例A</th>
            <th class="field">字段</th>
            <th class="side">用例B</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="field in fields" :key="field">
            <td class="side-value">
              <span>{{ caseA?.[field] ?? '—' }}</span>
            </td>
            <td class="field-label">{{ fieldLabels[field] || field }}</td>
            <td class="side-value">
              <span>{{ caseB?.[field] ?? '—' }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="compare-actions">
      <el-button type="primary" @click="$emit('keep', 'A')">保留用例A</el-button>
      <el-button type="primary" @click="$emit('keep', 'B')">保留用例B</el-button>
      <el-button @click="$emit('update:visible', false)">关闭</el-button>
    </div>
  </el-dialog>
</template>

<script setup>
const props = defineProps({
  visible: Boolean,
  caseA: Object,
  caseB: Object,
  fields: {
    type: Array,
    default: () => []
  },
  fieldLabels: {
    type: Object,
    default: () => ({})
  }
});
const emit = defineEmits(['update:visible', 'keep']);
</script>

<style scoped>
.compare-dialog >>> .el-dialog__body {
  padding: 24px 20px 12px 20px;
}
.compare-table-wrapper {
  max-height: 400px;
  overflow-y: auto;
}
.compare-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: #fff;
}
.compare-table th,
.compare-table td {
  padding: 10px 12px;
  text-align: center;
  border-bottom: 1px solid #e2e8f0;
}
.compare-table th.field,
.compare-table td.field-label {
  background: #f5f7fa;
  font-weight: bold;
  color: #222;
  width: 120px;
}
.compare-table th.side {
  background: #f0f9ff;
  font-weight: bold;
  color: #2563eb;
}
.compare-table td.side-value {
  background: #f9fafb;
  color: #333;
  word-break: break-all;
}
.compare-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 18px;
}
</style> 