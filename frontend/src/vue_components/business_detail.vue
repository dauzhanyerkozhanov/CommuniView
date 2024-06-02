<template>
  <!-- Display business name and description -->
  <div>
    <h1>{{ business.name }}</h1>
    <p>{{ business.description }}</p>
    <!-- Form for updating business details -->
    <form @submit.prevent="updateBusiness">
      <input v-model="business.name" placeholder="Business Name">
      <input v-model="business.description" placeholder="Business Description">
      <button type="submit">Update Business</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    // Initialize business object
    return {
      business: {}
    };
  },
  created: async function() { // Made the function async
  const businessId = this.$route.params.id;
  try {
    const response = await axios.get(`/api/businesses/${businessId}`);
    this.business = response.data;
  } catch (error) {
    console.error(error);
    alert('An error occurred while fetching the business details.');
  }
},
methods: {
  updateBusiness: async function() { // Made the function async
    try {
      const response = await axios.post('/update_form', this.business);
      if (response.data.message) {
        alert(response.data.message);
      }
    } catch (error) {
      console.error(error);
      alert('An error occurred while updating the business.');
    }
  }
}
};
</script>