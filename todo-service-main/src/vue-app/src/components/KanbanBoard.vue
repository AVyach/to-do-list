<template>
    <div class="kanban-container">
      <div 
        v-for="status in statuses" 
        :key="status.value" 
        class="kanban-column"
      >
        <div class="kanban-column-header">
          <h3>{{ status.label }}</h3>
          <span class="task-count">{{ getTasksByStatus(status.value).length }}</span>
        </div>
  
        <div class="kanban-column-content">
          <KanbanCard
            v-for="task in getTasksByStatus(status.value)"
            :key="task.id"
            :task="task"
            @edit="$emit('edit', $event)"
            @delete="$emit('delete', $event)"
            @view="$emit('view', $event)"
          />
  
          <div v-if="!getTasksByStatus(status.value).length" class="empty-column">
            Нет задач
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, PropType } from 'vue';
  import { TaskResponse } from '../services/taskService';
import KanbanCard from './KanbanCard.vue';
  
  export default defineComponent({
    name: 'KanbanBoard',
    components: { KanbanCard },
  
    props: {
      tasks: {
        type: Array as PropType<TaskResponse[]>,
        required: true
      }
    },
  
    emits: ['edit', 'delete', 'view'],
  
    setup(props) {
      const statuses = [
        { value: 'new', label: 'Новые' },
        { value: 'in_progress', label: 'В работе' },
        { value: 'completed', label: 'Завершённые' }
      ];
  
      const getTasksByStatus = (status: string) => {
        return props.tasks.filter(task => task.state === status);
      };
  
      return {
        statuses,
        getTasksByStatus
      };
    }
  });
  </script>
<style src="src/assets/components/kanban-board.scss"></style>