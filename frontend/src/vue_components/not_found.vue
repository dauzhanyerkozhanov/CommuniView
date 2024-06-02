<template>
  <div class="not-found-container">
    <h1>Oops!</h1>
    <h2>404 - Page Not Found</h2>
    <p>The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.</p>
    <router-link to="/" class="home-link">Go to Homepage</router-link>
  </div>
</template>

<script>
export default {
  name: 'NotFoundComponent'
}
</script>

<style scoped>
.not-found-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  text-align: center;
}

h1 {
  font-size: 3rem;
  color: #4A90E2;
}

h2 {
  font-size: 2rem;
  margin: 20px 0;
}

p {
  font-size: 1.25rem;
  color: #666;
  margin-bottom: 20px;
}

.home-link {
  display: inline-block;
  background-color: #4A90E2;
  color: #fff;
  padding: 10px 20px;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.home-link:hover {
  background-color: #357ABD;
}
</style>
