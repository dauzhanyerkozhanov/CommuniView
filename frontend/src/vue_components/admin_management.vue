<template>
  <!-- Display buttons for admin actions -->
  <div>
    <button @click="monitor">Monitor</button>
    <button @click="accessDashboard">Access Dashboard</button>
    <button @click="executeTasks">Execute Tasks</button>
    <button @click="logout">Logout</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  methods: {
    // Fetch and log monitoring data
    monitor() {
      axios.get('/admin/monitor')
        .then(response => {
          console.log(response.data);
        })
        .catch(error => {
          console.error(error);
        });
    },
    // Fetch and log dashboard data
    accessDashboard() {
      axios.get('/admin/dashboard')
        .then(response => {
          console.log(response.data);
        })
        .catch(error => {
          console.error(error);
        });
    },
    // Execute admin tasks and log the response
    executeTasks() {
      axios.post('/admin/execute')
        .then(response => {
          console.log(response.data);
        })
        .catch(error => {
          console.error(error);
        });
    },
    // Logout the admin user
    logout() {
      axios.post('/admin/logout')
        .then(response => {
          console.log(response.data);
        })
        .catch(error => {
          console.error(error);
        });
    }
  }
}
</script>

<!-- Scoped styles for this component -->
<style scoped>
</style>