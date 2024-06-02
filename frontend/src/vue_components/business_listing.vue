<template>
  <div>
    <!-- Input field for search query -->
    <input v-model="query" placeholder="Search for businesses">
    <!-- Button to trigger search operation -->
    <button @click="search">Search</button>
    <!-- List of businesses returned from search -->
    <ul>
      <li v-for="business in businesses" :key="business.id">
        {{ business.name }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      // Search query entered by the user
      query: '',
      // Array to store the businesses returned from the search
      businesses: []
    };
  },
  methods: {
  search() {
    this.businesses = []; // Clear businesses array before performing a new search
    axios.get('/search', { params: { query: this.query } })
      .then(response => {
        this.businesses = response.data;
      })
      .catch(error => {
        console.error(error);
        alert('An error occurred while searching for businesses.');
        this.businesses = []; // Clear businesses array in case of an error
      });
  }
}
};
</script>