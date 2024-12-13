<template>
  <div class="task-form-container">
    <h2 class="form-title">Новая задача</h2>
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
        <div class="tags-input-container">
          <input 
            id="tags"
            v-model="tagInput"
            type="text"
            class="form-input"
            placeholder="Добавьте теги"
            @keydown.enter.prevent="addTag"
          />
        </div>
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
        <button type="button" class="btn-cancel" @click="$emit('cancel')">Отмена</button>
        <button type="submit" class="btn-submit">Создать задачу</button>
      </div>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref, watch } from 'vue';
import { useUserStore } from '../store/userStore';
import { taskService, type TaskDTO } from '../services/taskService';

export default defineComponent({
 name: 'TaskForm',
 emits: ["submit", "cancel"],
 setup(_, {emit}) {
   const userStore = useUserStore();
   const tagInput = ref('');
   const error = ref('');

   const taskData = reactive<TaskDTO>({
     name: '',
     tags: [],
     state: 'new',
     comments: '',
     deadline: null,
     user_id: userStore.user?.id || ''
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

   const addTag = () => {
     if (tagInput.value.trim() && !taskData.tags?.includes(tagInput.value.trim())) {
       if (!taskData.tags) {
         taskData.tags = [];
       }
       taskData.tags.push(tagInput.value.trim());
       tagInput.value = '';
     }
   };

   const removeTag = (index: number) => {
     if (taskData.tags) {
       taskData.tags.splice(index, 1);
     }
   };

   const handleSubmit = async () => {
     try {
       await taskService.createTask(taskData);
        emit("submit")
     } catch (err: any) {
       error.value = err.message;
     }
   };

   return {
     taskData,
     tagInput,
     error,
     addTag,
     removeTag,
     handleSubmit
   };
 }
});
</script>
<style lang="scss" src="src/assets/components/task-form.scss"></style>