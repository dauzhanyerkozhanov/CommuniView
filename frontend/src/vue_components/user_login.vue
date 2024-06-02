<template>
  <div>
    <!-- Login form -->
    <h1>Login</h1>
    <form @submit.prevent="login">
      <!-- User input fields for username and password -->
      <input v-model="username" placeholder="Username" required>
      <input v-model="password" type="password" placeholder="Password" required>
      <!-- Submit button triggers the login method -->
      <button type="submit">Login</button>
    </form>
    <!-- Logout button triggers the logout method -->
    <button @click="logout">Logout</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    // Data properties for user input
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    // Login method sends a POST request to the server with user credentials
    async login() {
      try {
        const response = await axios.post('/login', {
          username: this.username,
          password: this.password,
        });
        console.log(response.data);
      } catch (error) {
        // Log any errors that occur during the request
        console.error(error);
      }
    },
    // Logout method sends a GET request to the server to logout the user
    async logout() {
      try {
        const response = await axios.post('/logout'); // Changed from axios.get to axios.post
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>