<template>

<h1>Register</h1>
<br>
<form @submit.prevent="register()">
  <div class="mb-3">
    <label for="full_name" class="form-label">Full name</label>
    <input type="text"  v-model="form_data.full_name" class="form-control" id="full_name" required>
  </div>
  <div class="mb-3">
    <label for="email" class="form-label">Email address</label>
    <input type="email"  v-model="form_data.email" class="form-control" id="email" aria-describedby="emailHelp">
  </div>
  <div class="mb-3">
    <label for="Password"  class="form-label">Password</label>
    <input type="password" v-model="form_data.password" class="form-control" id="Password" required>
  </div>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
<router-link to="/login">Already have an account? Login</router-link>
</template>


<script>
import router from '@/router';
import axios from 'axios';

export default {
  name: 'RegisterView',
    data() {
      return {
        form_data:{}
      }
    },
    methods: {
        async register(){
            const resp = await axios.post('http://127.0.0.1:5000/register',this.form_data)
            console.log(resp)
            if(resp.status === 200){
                this.$toast.success('Register successful!')
            } else {
                this.$toast.error(resp.data.error)
            }
        }
    }



}

</script>