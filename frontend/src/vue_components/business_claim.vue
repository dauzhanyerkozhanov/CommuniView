<template>
  <!-- Form for submitting a business claim -->
  <div>
    <h1>Claim a Business</h1>
    <form @submit.prevent="submitClaim">
      <!-- Input fields for claim details -->
      <input v-model="businessClaim.businessID" placeholder="Business ID">
      <input v-model="businessClaim.ownerID" placeholder="Owner ID">
      <input v-model="businessClaim.claimStatus" placeholder="Claim Status">
      <input v-model="businessClaim.proofDocuments" placeholder="Proof Documents">
      <!-- Submit button is disabled while the claim is being submitted -->
      <button type="submit" :disabled="isSubmitting">Submit Claim</button>
    </form>
    <!-- Buttons for editing and deleting a claim -->
    <!-- Modification in the template to disable buttons without a valid claimId -->
    <button @click="editClaim(businessClaim.claimId, businessClaim.claimStatus)" :disabled="!businessClaim.claimId">Edit Claim</button>
    <button @click="deleteClaim(businessClaim.claimId)" :disabled="!businessClaim.claimId">Delete Claim</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      // Object to hold the claim details
      businessClaim: {
        businessID: '',
        ownerID: '',
        claimStatus: '',
        proofDocuments: '',
        claimId: null
      },
      // Flag to indicate if a claim is being submitted
      isSubmitting: false,
    };
  },
  methods: {
    // Method to submit a claim
    submitClaim() {
      this.isSubmitting = true;
      axios.post('/submit_claim', {
        businessID: this.businessClaim.businessID,
        ownerID: this.businessClaim.ownerID,
        claimStatus: this.businessClaim.claimStatus,
        proofDocuments: this.businessClaim.proofDocuments
      })
      .then(response => {
        alert('Claim submitted successfully');
        // Assuming the response includes a unique claimId for the submitted claim
        this.businessClaim.claimId = response.data.claimId; 
      })
      .catch(error => {
        console.error(error);
        alert('An error occurred while submitting the claim.');
      })
      .finally(() => {
        // Reset the flag after the claim submission is complete
        this.isSubmitting = false;
      });
    },
    
    // Method to edit a claim
    editClaim(claimId, newStatus) {
      axios.put(`edit_claim/${claimId}`, { new_status: newStatus })
        .then(response => {
          if (response.data.message) {
            alert(response.data.message);
          }
        })
        .catch(error => {
          console.error(error);
          alert('An error occurred while editing the claim.');
        });
    },

    // Method to delete a claim
    deleteClaim(claimId) {
      axios.delete(`delete_claim/${claimId}`)
        .then(response => {
          if (response.data.message) {
            alert(response.data.message);
          }
        })
        .catch(error => {
          console.error(error);
          alert('An error occurred while deleting the claim.');
        });
    }
  }
};
</script>

<style scoped>
</style>