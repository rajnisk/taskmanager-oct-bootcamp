<template>
  <nav class="navbar navbar-expand-lg navbar-dark custom-navbar fixed-top">
    <div class="container">
      <!-- Brand -->
      <router-link class="navbar-brand fw-bold" to="/">
        <i class="bi bi-check2-square me-2"></i>
        Task Manager
      </router-link>

      <!-- Mobile toggle -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarContent"
        aria-controls="navbarContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Navigation links -->
      <div class="collapse navbar-collapse" id="navbarContent">
        <div class="navbar-nav ms-auto gap-lg-2">
          <router-link v-if="!isLoggedIn" class="nav-link custom-link" to="/login">
            Login
          </router-link>

          <router-link v-if="!isLoggedIn" class="nav-link register-btn" to="/register">
            Get Started
          </router-link>
          <button v-if="isLoggedIn" class="btn btn-outline-light" @click="$emit('logout')">
            Logout
        </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.custom-navbar {
  background: linear-gradient(135deg, #172554, #2563eb);
  box-shadow: 0 3px 15px rgba(0, 0, 0, 0.15);
  padding: 12px 0;
  z-index: 1030;
}

.navbar-brand {
  font-size: 1.35rem;
  letter-spacing: -0.5px;
}

.custom-link {
  color: rgba(255, 255, 255, 0.85);
  padding: 8px 16px !important;
  border-radius: 8px;
  transition: 0.2s ease;
}

.custom-link:hover,
.custom-link.router-link-active {
  color: #fff;
  background: rgba(255, 255, 255, 0.12);
}

.register-btn {
  color: #1d4ed8;
  background: #fff;
  padding: 8px 18px !important;
  border-radius: 8px;
  font-weight: 600;
  text-align: center;
  transition: 0.2s ease;
}

.register-btn:hover {
  color: #1e40af;
  background: #eff6ff;
  transform: translateY(-1px);
}
</style>

<script>
export default {
  name: "NavBar",
  data() {
    return {
      msg: "Hello from NavBar!",
    };
  },
  mounted() {
    console.log("NavBar mounted. isLoggedIn:", this.isLoggedIn);
  },
  methods: {
    
    alertMessage() {
      alert(this.isLoggedIn);
    },

  },
  emits: ['logout'],
  props: {
    isLoggedIn: {
      type: Boolean,
      required: true,
    },
  },

};


</script>