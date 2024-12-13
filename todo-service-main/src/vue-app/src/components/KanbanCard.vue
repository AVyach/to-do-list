<template>
    <div class="kanban-card" @click="$emit('view', task)">
      <div class="kanban-card-header">
        <h4 class="kanban-card-title">{{ task.name }}</h4>
        <span :class="['kanban-card-state', `kanban-card-state--${task.state}`]">
          {{ getStateLabel(task.state) }}
        </span>
      </div>
  
      <div v-if="task.tags?.length" class="kanban-card-tags">
        <span v-for="tag in task.tags" :key="tag" class="kanban-card-tag">
          {{ tag }}
        </span>
      </div>
  
      <div v-if="task.deadline" class="kanban-card-deadline">
        {{ formatDate(task.deadline) }}
      </div>
  
    </div>
  </template>
  <script lang="ts">
  import { defineComponent, PropType } from 'vue';
  import { TaskResponse } from '../services/taskService';
  
  export default defineComponent({
    name: 'TaskCard',
    props: {
      task: {
        type: Object as PropType<TaskResponse>,
        required: true
      }
    },
    emits: ['edit', 'delete', 'view'],
    setup() {
      const getStateLabel = (state: string): string => {
        const states: Record<string, string> = {
          new: 'Новая',
          in_progress: 'В работе',
          completed: 'Завершена'
        };
        return states[state] || state;
      };
  
      const formatDate = (date: string | null): string => {
        if (!date) return '';
        return new Date(date).toLocaleString('ru-RU', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        });
      };
  
      return {
        getStateLabel,
        formatDate
      };
    }
  });
  </script>

<style src="src/assets/components/kanban-card.scss"></style>