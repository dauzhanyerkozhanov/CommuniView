<template>
  <div>
    <!-- Display the title and list of reviews -->
    <h1>Reviews</h1>
    <ul>
      <!-- Loop through each review and display its content -->
      <li v-for="review in reviews" :key="review.id">{{ review.content }}</li>
    </ul>
    <!-- Form for submitting a new review -->
    <form @submit.prevent="submitReview">
      <textarea v-model="reviewContent" placeholder="Write a review"></textarea>
      <button type="submit">Submit Review</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    // Initialize data properties for storing reviews and review details
    return {
      reviews: [],
      reviewContent: '',
      reviewRating: '',
      reviewBusiness: '',
      reviewId: ''
    };
  },
  created() {
    // Fetch the reviews when the component is created
    this.getReview();
  },
  methods: {
    getReview() {
      // Send a GET request to the server to fetch a review by its ID
      axios.get('/get', { params: { review_id: this.reviewId } })
        .then(response => {
          // Update the reviews data property with the fetched data
          this.reviews = response.data;
        })
        .catch(error => {
          // Handle any errors that occur during the request
          alert('An error occurred while fetching the review: ' + error.message);
        });
    },
    submitReview() {
      if (!this.reviewContent.trim()) {
        alert('Review content cannot be empty.');
        return;
      }
      axios.post('/review', { content: this.reviewContent, rating_value: this.reviewRating, associated_business: this.reviewBusiness })
        .then(response => {
          this.getReview();
          alert('Review submitted successfully.');
        })
        .catch(error => {
          alert('An error occurred while submitting the review: ' + error.message);
        });
    },
    editReview() {
      if (!this.reviewContent.trim()) {
        alert('Review content cannot be empty when editing.');
        return;
      }
      axios.put('/edit', { review_id: this.reviewId, content: this.reviewContent, rating_value: this.reviewRating })
        .then(response => {
          this.getReview();
          alert('Review updated successfully.');
        })
        .catch(error => {
          alert('An error occurred while editing the review: ' + error.message);
        });
    },
    deleteReview() {
      if (this.reviewId == null) {
        alert('Invalid review ID. Cannot delete review.');
        return;
      }
      axios.delete('/delete', { data: { review_id: this.reviewId } })
        .then(response => {
          this.getReview();
          alert('Review deleted successfully.');
        })
        .catch(error => {
          alert('An error occurred while deleting the review: ' + error.message);
        });
    },
  }
};
</script>