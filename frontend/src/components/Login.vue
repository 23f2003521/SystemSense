<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();

const FormData = ref({
  email: '',
  password: ''
});

const error = ref("");

async function login() {
  try {
    const response = await axios.post('http://127.0.0.1:5000/api/login', JSON.stringify(FormData.value), {
      headers: { "Content-Type": "application/json" }
    });
    localStorage.setItem('token', response.data.access_token);
    localStorage.setItem('role', response.data.role);
    error.value = '';
    await router.push('/dashboard');
  } catch (err) {
    error.value = err.response?.data?.message || "Login failed";
  }
}

// Registration removed — dummy function so UI doesn't break
function register() {
  error.value = "Registration is disabled. Please contact admin.";
}
</script>

<template>
  <div class="container" id="container">
    <!-- Registration form stays in view but won't work -->
    <div class="form-container sign-up">
      <form id="reg" @submit.prevent="register">
        <h1>Create Account</h1>
        <div class="social-icons">
          <a href="#" class="icon"><i class="fa-brands fa-google-plus-g"></i></a>
          <a href="#" class="icon"><i class="fa-brands fa-facebook-f"></i></a>
          <a href="#" class="icon"><i class="fa-brands fa-github"></i></a>
          <a href="#" class="icon"><i class="fa-brands fa-linkedin-in"></i></a>
        </div>
        <input type="text" placeholder="Enter your Name" disabled>
        <input type="email" placeholder="Enter your Email" disabled>
        <input type="password" placeholder="Enter Password" disabled>
        <input type="v-number" placeholder="Enter your vehicle-no" disabled>
        <button type="submit" disabled>Sign Up</button>
      </form>
    </div>

    <!-- Login form works as before -->
    <div class="form-container sign-in">
      <p v-if="error">{{ error }}</p>
      <form id="sign-in" @submit.prevent="login">
        <h1>Sign In</h1>
        <div class="social-icons">
          <a href="#" class="icon"><i class="fa-brands fa-google-plus-g"></i></a>
          <a href="#" class="icon"><i class="fa-brands fa-facebook-f"></i></a>
          <a href="#" class="icon"><i class="fa-brands fa-github"></i></a>
          <a href="#" class="icon"><i class="fa-brands fa-linkedin-in"></i></a>
        </div>
        <span>or use your email password</span>
        <input type="email" v-model="FormData.email" placeholder="Email">
        <input type="password" v-model="FormData.password" placeholder="Password">
        <a href="#">New user registration is disabled</a>
        <button type="submit">Sign In</button>
      </form>
    </div>

    <!-- Toggle stays for UI but disabled -->
    <div class="toggle-container">
      <div class="toggle">
        <div class="toggle-panel toggle-left">
          <h1>Welcome Back!</h1>
          <p>Enter your personal details to use all of site features</p>
          <button class="hidden" disabled>Sign In</button>
        </div>
        <div class="toggle-panel toggle-right">
          <h1>Hello, Friends !</h1>
                  <p>Please Login Here </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Keep your styles as is */
</style>
