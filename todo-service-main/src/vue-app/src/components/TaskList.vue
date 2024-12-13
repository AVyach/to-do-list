<template>
    <div class="task-list">
      <div class="task-list__filters">
        <input 
          v-model="searchQuery"
          type="text"
          class="search-input"
          placeholder="Поиск по названию..."
        />
        <select v-model="stateFilter" class="state-filter">
          <option value="">Все статусы</option>
          <option value="new">Новые</option>
          <option value="in_progress">В работе</option>
          <option value="completed">Завершенные</option>
        </select>
      </div>
  
      <div class="task-list__content">
        <TaskCard
          v-for="task in filteredTasks"
          :key="task.id"
          :task="task"
          @view="$emit('view', $event)"
        />
      </div>
  
      <div v-if="!filteredTasks.length" class="task-list__empty">
        Задачи не найдены
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, PropType, ref, computed } from 'vue';
  import { TaskResponse } from '../services/taskService';
  import TaskCard from './TaskCard.vue';
  
  export default defineComponent({
    name: 'TaskList',
    components: {
      TaskCard
    },
    props: {
      tasks: {
        type: Array as PropType<TaskResponse[]>,
        required: true
      }
    },
    emits: ['edit', 'delete', 'view'],
    setup(props) {
      const searchQuery = ref('');
      const stateFilter = ref('');
  
      const filteredTasks = computed(() => {
        return props.tasks.filter(task => {
          const matchesSearch = task.name.toLowerCase()
            .includes(searchQuery.value.toLowerCase());
          const matchesState = !stateFilter.value || task.state === stateFilter.value;
          return matchesSearch && matchesState;
        });
      });
  
      return {
        searchQuery,
        stateFilter,
        filteredTasks
      };
    }
  });
  </script>

<style src="src/assets/components/task-list.scss"></style>