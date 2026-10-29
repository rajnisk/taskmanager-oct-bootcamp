<template>

<h1>Login</h1>
<br>
<form @submit.prevent="login()">
  <div class="mb-3">
    <label for="email" class="form-label">Email address</label>
    <input type="email" v-model="form_data.email" class="form-control" id="email" aria-describedby="emailHelp">
  </div>
  <div class="mb-3">
    <label for="Password" class="form-label">Password</label>
    <input type="password" v-model="form_data.password" class="form-control" id="Password" required>
  </div>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
<router-link to="/register">Don't have an account? Register</router-link>

</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginView',
  data() {
    return {
      form_data:{}
    }
  },
  methods: {
    async login(){
      const resp = await axios.post('http://127.0.0.1:5000/login',this.form_data)
      if (resp.status === 200){
        this.$toast.success('Login successful!')
        localStorage.setItem('token', resp.data.token)
        this.$router.push('/')
      } else {
        this.$toast.error(resp.data.error)
      }
    }
  }
}
</script>