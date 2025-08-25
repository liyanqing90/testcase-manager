<template>
  <div class="data-factory-container">
    <!-- 根据当前选中的tab显示不同的内容 -->
    <DataGenerator v-if="currentTab === 'generator'" />
    <DataTemplate v-else-if="currentTab === 'template'" />
    <BatchGenerator v-else-if="currentTab === 'batch'" />
    <FormatTransform v-else-if="currentTab === 'transform'" />
              </div>
</template>

<script setup>
import { defineProps } from 'vue';
import DataGenerator from './DataGenerator.vue';
import DataTemplate from './DataTemplate.vue';
import BatchGenerator from './BatchGenerator.vue';
import FormatTransform from './FormatTransform.vue';

// 接收父组件传递的当前tab
const props = defineProps({
  currentTab: {
    type: String,
    default: 'generator'
  }
});
</script>

<style scoped>
.data-factory-container {
  width: 100%;
  height: 100%;
}
</style> 