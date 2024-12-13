<template>
    <div class="calendar">
      <div class="calendar-header">
        <button @click="previousMonth" class="calendar-nav-btn">&lt;</button>
        <h3>{{ currentMonthName }} {{ currentYear }}</h3>
        <button @click="nextMonth" class="calendar-nav-btn">&gt;</button>
      </div>
  
      <div class="calendar-grid">
        <div v-for="day in weekDays" :key="day" class="calendar-day-header">
          {{ day }}
        </div>
  
        <div
          v-for="(day, index) in calendarDays"
          :key="index"
          :class="[
            'calendar-day',
            { 'current-month': day.currentMonth },
            { 'today': isToday(day.date) }
          ]"
        >
          <div class="day-number">{{ day.dayNumber }}</div>
          <div class="day-tasks">
            <div
              v-for="task in getTasksForDay(day.date)"
              :key="task.id"
              class="calendar-task"
              :class="`task-state-${task.state}`"
              @click="$emit('view', task)"
            >
              {{ task.name }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, computed, PropType } from 'vue';
  import { TaskResponse } from '../services/taskService';
  
  export default defineComponent({
    name: 'TaskCalendar',
    props: {
      tasks: {
        type: Array as PropType<TaskResponse[]>,
        required: true
      }
    },
    emits: ['view'],
    setup(props) {
      const currentDate = ref(new Date());
      const weekDays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
  
      const currentMonthName = computed(() => {
        return currentDate.value.toLocaleString('ru', { month: 'long' });
      });
  
      const currentYear = computed(() => {
        return currentDate.value.getFullYear();
      });
  
      const calendarDays = computed(() => {
        const year = currentDate.value.getFullYear();
        const month = currentDate.value.getMonth();
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const days = [];
  
        // Получаем предыдущий месяц
        let start = firstDay.getDay() - 1;
        if (start === -1) start = 6;
        for (let i = start; i > 0; i--) {
          const date = new Date(year, month, 1 - i);
          days.push({
            date,
            dayNumber: date.getDate(),
            currentMonth: false
          });
        }
  
        // Текущий месяц
        for (let i = 1; i <= lastDay.getDate(); i++) {
          const date = new Date(year, month, i);
          days.push({
            date,
            dayNumber: i,
            currentMonth: true
          });
        }
  
        // Следующий месяц
        const remaining = 42 - days.length;
        for (let i = 1; i <= remaining; i++) {
          const date = new Date(year, month + 1, i);
          days.push({
            date,
            dayNumber: i,
            currentMonth: false
          });
        }
  
        return days;
      });
  
      const getTasksForDay = (date: Date) => {
        return props.tasks.filter(task => {
          if (!task.deadline) return false;
          const taskDate = new Date(task.deadline);
          return (
            taskDate.getDate() === date.getDate() &&
            taskDate.getMonth() === date.getMonth() &&
            taskDate.getFullYear() === date.getFullYear()
          );
        });
      };
  
      const isToday = (date: Date) => {
        const today = new Date();
        return (
          date.getDate() === today.getDate() &&
          date.getMonth() === today.getMonth() &&
          date.getFullYear() === today.getFullYear()
        );
      };
  
      const nextMonth = () => {
        currentDate.value = new Date(
          currentDate.value.setMonth(currentDate.value.getMonth() + 1)
        );
      };
  
      const previousMonth = () => {
        currentDate.value = new Date(
          currentDate.value.setMonth(currentDate.value.getMonth() - 1)
        );
      };
  
      return {
        weekDays,
        currentMonthName,
        currentYear,
        calendarDays,
        getTasksForDay,
        isToday,
        nextMonth,
        previousMonth
      };
    }
  });
  </script>

<style src="src/assets/components/calendar.scss"></style>