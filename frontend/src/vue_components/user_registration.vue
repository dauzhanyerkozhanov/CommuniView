<template>
  <div>
    <!-- Display registration form -->
    <h1>Register</h1>
    <!-- Display error message if any -->
    <p class="error" v-if="errorMessage">{{ errorMessage }}</p>
    <!-- Form submission triggers the register method -->
    <form @submit.prevent="register">
      <!-- User input fields for username, email, and password -->
      <input v-model="username" placeholder="Username" required>
      <input v-model="email" placeholder="Email" required>
      <input v-model="password" type="password" placeholder="Password" required>
      <!-- Submit button for the form -->
      <button type="submit">Register</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    // Data properties for user input and error message
    return {
      username: '',
      email: '',
      password: '',
      errorMessage: '',
    };
  },
  methods: {
    // Register method sends a POST request to the server with user details
    async register() {
      try {
        const response = await axios.post('/register_form', {
          username: this.username,
          email: this.email,
          password: this.password,
        });
        // If the server response contains errors, update the errorMessage data property// Inserted code snippet for defect repair
      if (response.data.errors) {
        this.errorMessage = response.data.errors;
      } else {
        this.errorMessage = ''; // Added to clear the error message after successful registration
        console.log(response.data);
        }
      } catch (error) {
        // Log any errors that occur during the request
        console.error(error);
      }
    },
  },
};
</script>