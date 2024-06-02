<template>
    <div>
      <h1>My Bookmarks</h1>
      <div v-if="isLoading">Loading...</div> <!-- Display loading indicator when fetching bookmarks -->
      <div v-for="bookmark in bookmarks" :key="bookmark.id" class="bookmark-item">
        <h3>{{ bookmark.associated_business }}</h3>
        <button @click="editBookmark(bookmark.id)">Edit</button>
        <button @click="deleteBookmark(bookmark.id)">Delete</button>
      </div>
      <button @click="createBookmark">Create Bookmark</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        bookmarks: [],
        errorMessage: '',
        isLoading: false // Added loading flag
      };
    },
    methods: {
      getBookmarks() {
        this.isLoading = true; // Flag toggled before the request
        axios.get('/bookmark')
          .then(response => {
            this.bookmarks = response.data;
          })
          .catch(error => {
            if (error.response && error.response.status === 401) {
              this.$router.push('/login');
            } else {
              this.errorMessage = 'Failed to load bookmarks.';
              console.error(error);
            }
          })
          .finally(() => {
            this.isLoading = false; // Ensures the loading flag is turned off 
          });
      },
      deleteBookmark(bookmarkId) {
        axios.delete(`/bookmark/${bookmarkId}`)
          .then(() => {
            this.getBookmarks(); // Refreshes the bookmarks after deletion
          })
          .catch(error => {
            this.errorMessage = 'Failed to delete bookmark.';
            console.error(error);
          });
      },
      editBookmark(bookmarkId) {
        const updatedBookmarkData = {
          new_associated_user: 'Updated User Name',
          new_associated_business: 'Updated Business Name'
        };
        axios.put(`/bookmark/${bookmarkId}/edit`, updatedBookmarkData)
          .then(() => {
            this.getBookmarks(); // Refreshes the bookmarks after editing
          })
          .catch(error => {
            this.errorMessage = 'Failed to edit bookmark.';
            console.error(error);
          });
      },
      createBookmark() {
        const newBookmarkData = {
          associated_user: 'User Name',
          associated_business: 'Business Name'
        };
        axios.post('/bookmark', newBookmarkData)
          .then(() => {
            this.getBookmarks(); // Refreshes the bookmarks after creating a new one
          })
          .catch(error => {
            this.errorMessage = 'Failed to create bookmark.';
            console.error(error);
          });
      },
    },
    created() {
      this.getBookmarks();
    }
  };
  </script>
  
  <style scoped>
  .bookmark-item {
    margin-bottom: 15px;
  }
  </style>
  