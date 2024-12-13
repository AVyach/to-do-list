<template>
    <div class="task-form-container">
      <h2 class="form-title">Редактирование задачи</h2>
      <form @submit.prevent="handleSubmit" class="task-form">
        <div class="form-group">
          <label for="name">Название задачи*</label>
          <input 
            id="name"
            v-model="taskData.name"
            type="text"
            required
            class="form-input"
            placeholder="Введите название задачи"
          />
        </div>
   
        <div class="form-group">
          <label for="tags">Теги</label>
          <input 
            id="tags"
            v-model="tagInput"
            type="text"
            class="form-input"
            placeholder="Введите теги через пробел"
          />
          <div class="tags-container" v-if="taskData.tags?.length">
            <span v-for="(tag, index) in taskData.tags" :key="index" class="tag">
              {{ tag }}
              <button type="button" class="remove-tag" @click="removeTag(index)">×</button>
            </span>
          </div>
        </div>
   
        <div class="form-group">
          <label for="state">Статус*</label>
          <select id="state" v-model="taskData.state" required class="form-select">
            <option value="new">Новая</option>
            <option value="in_progress">В работе</option>
            <option value="completed">Завершена</option>
          </select>
        </div>
   
        <div class="form-group">
          <label for="deadline">Дедлайн</label>
          <input 
            id="deadline"
            v-model="taskData.deadline"
            type="datetime-local"
            class="form-input"
          />
        </div>
   
        <div class="form-group">
          <label for="comments">Комментарии</label>
          <textarea 
            id="comments"
            v-model="taskData.comments"
            class="form-textarea"
            placeholder="Добавьте комментарии к задаче"
          ></textarea>
        </div>
   
        <div class="form-actions">
          <button type="button" class="btn-delete" @click="handleDelete">Удалить</button>
          <button type="button" class="btn-cancel" @click="$emit('cancel')">Отмена</button>
          <button type="submit" class="btn-submit">Сохранить</button>
        </div>
      </form>
    </div>
   </template>
   
   <script lang="ts">
   import { defineComponent, PropType, reactive, ref, watch } from 'vue';
   import { taskService, TaskDTO, TaskResponse } from '../services/taskService';
   
   export default defineComponent({
    name: 'TaskEditForm',
    props: {
      task: {
        type: Object as PropType<TaskResponse>,
        required: true
      }
    },
    emits: ['submit', 'cancel', 'delete'],
    setup(props, { emit }) {
      const tagInput = ref('');
      const error = ref('');
   
      const taskData = reactive<TaskDTO>({
        name: props.task.name,
        tags: props.task.tags ? [...props.task.tags] : [],
        state: props.task.state,
        comments: props.task.comments || '',
        deadline: props.task.deadline,
        user_id: props.task.user_id
      });
   
      watch(tagInput, (newValue) => {
        if (newValue.includes(' ')) {
          const newTags = [...new Set(
            newValue.split(' ')
              .map(tag => tag.trim())
              .filter(tag => tag && !taskData.tags?.includes(tag))
          )];
          
          if (newTags.length) {
            if (!taskData.tags) {
              taskData.tags = [];
            }
            taskData.tags.push(...newTags);
          }
          tagInput.value = '';
        }
      });
   
      const removeTag = (index: number) => {
        if (taskData.tags) {
          taskData.tags.splice(index, 1);
        }
      };
   
      const handleSubmit = async () => {
        try {
          await taskService.updateTask(props.task.id, taskData);
          emit('submit');
        } catch (err: any) {
          error.value = err.message;
        }
      };
   
      const handleDelete = async () => {
        if (confirm('Вы уверены, что хотите удалить задачу?')) {
            await taskService.deleteTask(props.task.id);
          emit('delete', props.task.id);
          
        }
      };
   
      return {
        taskData,
        tagInput,
        error,
        removeTag,
        handleSubmit,
        handleDelete
      };
    }
   });
   </script>
   
   <style lang="scss" src="src/assets/components/task-form.scss"></style>