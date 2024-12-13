<template>
  <div class="task-page">
    <div class="task-page__header">
      <h1 class="task-page__title">Мои задачи</h1>
      <button class="btn-create" @click="showCreateModal = true">
        Создать задачу
      </button>
    </div>

    <div class="view-toggle">
    <button 
      v-for="view in viewModes"
      :key="view.value"
      class="view-btn"
      :class="{ active: viewMode === view.value }"
      @click="viewMode = view.value"
    >
      {{ view.label }}
    </button>
  </div>
 
    <div class="task-navigation" v-if="viewMode === 'list'">
     <button 
       class="nav-btn"
       :class="{ active: currentView === 'all' }"
       @click="currentView = 'all'"
     >
       Все задачи
     </button>
     <button
       v-for="tab in tabs" 
       :key="tab.value"
       class="nav-btn"
       :class="{ active: currentView === tab.value }"
       @click="currentView = tab.value"
     >
       {{ tab.label }}
     </button>
   </div>



  <div v-if="loading" class="task-page__loading">Загрузка...</div>
  <div v-else-if="error" class="task-page__error">{{ error }}</div>
  <div v-else-if="viewMode === 'list' && !filteredTasks.length" class="task-page__empty">
    {{ getEmptyMessage() }}
  </div>

  <template v-else>
    <TaskList
      v-if="viewMode === 'list'"
      :tasks="filteredTasks"
      @edit="handleEdit"
      @delete="handleDelete"
      @view="handleViewTask"
    />
    <TaskCalendar
      v-else-if="viewMode === 'calendar'"
      :tasks="tasks"
      @view="handleViewTask"
    />
    <KanbanBoard
      v-else
      :tasks="tasks"
      @edit="handleEdit"
      @delete="handleDelete"
      @view="handleViewTask"
    />
  </template>
 
 
    <div v-if="showCreateModal" class="modal-overlay" @click="handleModalClose">
      <div class="modal-content" @click.stop>
        <TaskForm 
          @submit="handleTaskCreate" 
          @cancel="showCreateModal = false"
        />
      </div>
    </div>
    <div v-if="selectedTask" class="modal-overlay" @click="selectedTask = null">
   <div class="modal-content" @click.stop>
     <TaskEditForm
       :task="selectedTask"
       @submit="handleTaskEdit"
       @delete="handleDelete"
       @cancel="selectedTask = null"
     />
   </div>
 </div>
  </div>
 </template>
 
 <script lang="ts">
 import { defineComponent, onMounted, ref, computed } from 'vue';
 import { taskService, TaskResponse } from '../services/taskService';
 import TaskList from '../components/TaskList.vue';
 import TaskForm from '../components/TaskForm.vue';
import TaskEditForm from './TaskEditForm.vue';
import TaskCalendar from './TaskCalendar.vue';
import KanbanBoard from './KanbanBoard.vue';
 
 interface Tab {
  value: string;
  label: string;
 }
 
 export default defineComponent({
  name: 'TaskPage',
  components: { TaskList, TaskForm, TaskEditForm , TaskCalendar, KanbanBoard},
  setup() {
    const tasks = ref<TaskResponse[]>([]);
    const loading = ref(true);
    const error = ref('');
    const showCreateModal = ref(false);
    const currentView = ref<string>('all');
    const selectedTask = ref<TaskResponse | null>(null);
    const viewMode = ref<'list' | 'calendar' | 'kanban'>('list');
    const viewModes = [
      { value: 'list', label: 'Список' },
      { value: 'calendar', label: 'Календарь' },
      { value: 'kanban', label: 'Kanban' }
    ];
 
    const tabs: Tab[] = [
      { value: 'today', label: 'Задачи на сегодня' },
      { value: 'tomorrow', label: 'Задачи на завтра' },
      { value: 'past', label: 'Прошлые задачи' }
    ];
    const handleViewTask = (task: TaskResponse) => {
     selectedTask.value = task;
   };
    const getEmptyMessage = () => {
      const messages = {
        all: 'Задач нет',
        today: 'На сегодня задач нет',
        tomorrow: 'На завтра задач нет',
        past: 'Прошлых задач нет'
      };
      return messages[currentView.value] || 'Задач не найдено';
    };
 
    const filteredTasks = computed(() => {
      if (currentView.value === 'all') {
        return tasks.value;
      }
 
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      
      const tomorrow = new Date(today);
      tomorrow.setDate(tomorrow.getDate() + 1);
 
      return tasks.value.filter(task => {
        if (!task.deadline) return false;
        const taskDate = new Date(task.deadline);
        taskDate.setHours(0, 0, 0, 0);
 
        switch (currentView.value) {
          case 'today':
            return taskDate.getTime() === today.getTime();
          case 'tomorrow':
            return taskDate.getTime() === tomorrow.getTime();
          case 'past':
            return taskDate < today;
          default:
            return true;
        }
      });
    });
 
    const loadTasks = async () => {
      try {
        loading.value = true;
        tasks.value = await taskService.getTasks();
      } catch (err: any) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    };
 
    const handleEdit = (task: TaskResponse) => {
      // Логика редактирования
    };
 
    const handleDelete = async (taskId: number) => {
        try {
          await loadTasks();
          selectedTask.value = null;
        } catch (err: any) {
          error.value = err.message;
        }

    };
 
    const handleTaskCreate = async () => {
      try {
        showCreateModal.value = false;
        await loadTasks();
      } catch (err: any) {
        error.value = err.message;
      }
    };
    const handleTaskEdit = async () => {
     try {
       selectedTask.value = null;
       await loadTasks();
     } catch (err: any) {
       error.value = err.message;
     }
   };
 
    const handleModalClose = (e: MouseEvent) => {
      if (e.target === e.currentTarget) {
        showCreateModal.value = false;
      }
    };
 
    onMounted(loadTasks);
 
    return {
      tasks,
      loading,
      error,
      showCreateModal,
      currentView,
      tabs,
      filteredTasks,
      handleEdit,
      handleDelete,
      handleTaskCreate,
      handleModalClose,
      getEmptyMessage,
      selectedTask,
      handleViewTask,
      handleTaskEdit,
      viewMode,
      viewModes,
    };
  }
 });
 </script>
  <style src="src/assets/components/task-page.scss"></style>
