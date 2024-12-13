<template>
    <div class="task-card" @click="$emit('view', task)">
      <div class="task-card__header">
        <h3 class="task-card__title">{{ task.name }}</h3>
        <span :class="['task-card__state', `task-card__state--${task.state}`]">
          {{ getStateLabel(task.state) }}
        </span>
      </div>
      
      <div class="task-card__tags" v-if="task.tags && task.tags.length">
        <span v-for="tag in task.tags" :key="tag" class="tag">{{ tag }}</span>
      </div>
      
      <div class="task-card__info">
        <div class="task-card__dates">
          <p class="task-card__created">
            Создано: {{ formatDate(task.created_at) }}
          </p>
          <p v-if="task.deadline" class="task-card__deadline">
            Дедлайн: {{ formatDate(task.deadline) }}
          </p>
        </div>
        
        <p v-if="task.comments" class="task-card__comments">
          {{ task.comments }}
        </p>
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

<style src="src/assets/components/task-card.scss"></style>