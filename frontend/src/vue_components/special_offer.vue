<template>
    <div>
        <!-- Form for submitting an offer -->
        <form @submit.prevent="submitForm">
            <!-- Input fields for offer details -->
            <input v-model="offer.title" placeholder="Title" required />
            <textarea v-model="offer.description" placeholder="Description" required></textarea>
            <input v-model="offer.expiration_date" placeholder="Expiration Date" required />
            <input v-model="offer.associated_business" placeholder="Associated Business" required />
            <!-- Submit button for the form -->
            <button type="submit">Submit</button>
        </form>

        <!-- Button for deleting an offer -->
        <button @click="deleteOffer">Delete Offer</button>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        // Initialize offer object and offerId
        return {
            offer: {
                title: '',
                description: '',
                expiration_date: '',
                associated_business: ''
            },
            offerId: '' // Changed from null to an empty string for consistency in types and reactivity
        };
    },
    methods: {
        async submitForm() {
            // Check if offerId exists, if it does, update the offer, else create a new offer
            if (this.offerId) {
                try {
                    const response = await axios.put(`/offers/${this.offerId}`, this.offer);
                    console.log(response.data);
                } catch (error) {
                    console.error(error);
                }
            } else {
                try {
                    const response = await axios.post('/offers', this.offer);
                    console.log(response.data);
                } catch (error) {
                    console.error(error);
                }
            }
        },
        async deleteOffer() {
            // Delete the offer with the given offerId
            try {
                const response = await axios.delete(`/offers/${this.offerId}`);
                console.log(response.data);
            } catch (error) {
                console.error(error);
            }
        },
        async getOffer() {
            // Fetch the offer with the given offerId
            try {
                const response = await axios.get(`/offers/${this.offerId}`);
                this.offer = response.data;
            } catch (error) {
                console.error(error);
            }
        }
    },
    created() {
        // If offerId exists, fetch the offer when the component is created
        if (this.offerId) {
            this.getOffer();
        }
    }
};
</script>