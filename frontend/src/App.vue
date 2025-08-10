<script setup>
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
import { ref, onMounted } from 'vue'

const isLoggedIn = ref(false)

// On mount, check if user is logged in
onMounted(() => {
  const token = localStorage.getItem('token') // You can check user_id or role too
  isLoggedIn.value = !!token
}) // Set false for logged-out users
</script>

<template>
  <div class="layout-wrapper">
    <Header/>

    <div class="main-body">
      

      <div class="main-content">
        <RouterView />
      </div>
    </div>

    <Footer/>
  </div>
</template>

<style>
.layout-wrapper {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.main-body {
  display: flex;
  flex-grow: 1;
  overflow: hidden;
}

.main-content {
  flex-grow: 1;
  overflow-y: auto;
  padding: 0; /* Optional: remove padding if you want full bleed */
  display: flex;
  flex-direction: column;
}

</style>
