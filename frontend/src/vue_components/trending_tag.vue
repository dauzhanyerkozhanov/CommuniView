<template>
  <div>
    <!-- Display the title and loading state or the list of trending tags -->
    <h1>Trending Tags</h1>
    <p v-if="isLoading">Loading...</p>
    <ul v-else>
      <li v-for="tag in tags" :key="tag.id">{{ tag.name }}</li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
data() {
  return {
    isLoading: false, // This line was added
    tags: [],
    businesses: [],
    tagForm: {
      name: '',
      popularityScore: 0,
    },
  };
},
methods: {
  // Method to create a new trending tag
  async createTrendingTag() {
    try {
      const response = await axios.post('/tags', this.tagForm);
      this.tags.push(response.data);
    } catch (error) {
      console.error(error);
    }
  },
  // Method to edit an existing trending tag
  async editTrendingTag(tagId) {
    try {
      const response = await axios.put(`/tags/${tagId}`, this.tagForm);
      const index = this.tags.findIndex(tag => tag.id === tagId);
      this.tags[index] = response.data;
    } catch (error) {
      console.error(error);
    }
  },
  // Method to delete a trending tag
  async deleteTrendingTag(tagId) {
    try {
      await axios.delete(`/tags/${tagId}`);
      this.tags = this.tags.filter(tag => tag.id !== tagId);
    } catch (error) {
      console.error(error);
    }
  },
  // Method to fetch all trending tags
  async getTrendingTags() {
    this.isLoading = true; // Start loading
    try {
      const response = await axios.get('/tags');
      this.tags = response.data;
    } catch (error) {
      console.error(error);
    } finally {
      this.isLoading = false; // End loading
    }
  },
  // Method to fetch businesses associated with a specific tag
  async getBusinessesForTag(tagId) {
    try {
      const response = await axios.get(`/tags/${tagId}/businesses`);
      this.businesses = response.data;
    } catch (error) {
      console.error(error);
    }
  },
},
// Fetch the trending tags when the component is created
created() {
  this.getTrendingTags();
},
};
</script>

<style scoped>
/* No styles defined yet */
</style>