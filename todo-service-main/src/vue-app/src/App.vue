<template>
  <div id="app">
    <Navbar />
    <RouterView />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

import Navbar from "./components/Navbar.vue";

export default defineComponent({
  name: "App",
  components: {

    Navbar,
  },
  setup() {
    const reload = ref(false);

    const refreshTable = () => {
      reload.value = !reload.value;
    };

    return {
      reload,
      refreshTable,
    };
  },
});
</script>

<style src="src/assets/styles.scss"></style>
