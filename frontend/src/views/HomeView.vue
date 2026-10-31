<template>
  <NavBar @logout="logout" :is-logged-in="isLoggedIn" />

  <main class="container py-5 mt-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h1>My Tasks</h1>
        <p class="text-muted mb-0">View and update your assigned tasks.</p>
      </div>
      <button class="btn btn-primary" @click="getTasks">Refresh</button>
    </div>

    <div v-if="loading" class="text-center">
      Loading tasks...
    </div>

    <div v-else-if="tasks.length === 0" class="alert alert-info">
      You do not have any assigned tasks.
    </div>

    <div v-else class="row g-3">
      <div v-for="task in tasks" :key="task.id" class="col-md-6 col-lg-4">
        <div class="card h-100 shadow-sm">
          <div class="card-body">
            <h5 class="card-title">{{ task.title }}</h5>
            <p class="card-text text-muted">
              {{ task.description || "No description" }}
            </p>
            <span class="badge mb-3" :class="statusClass(task.status)">
              {{ task.status }}
            </span>

            <select
              v-model="task.status"
              class="form-select"
              @change="updateTask(task)"
            >
              <option value="pending">Pending</option>
              <option value="in-progress">In progress</option>
              <option value="completed">Completed</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import axios from "axios";
import NavBar from "@/components/NavBar.vue";

export default {
  name: "HomeView",
  components: {
    NavBar,
  },
  data() {
    return {
      isLoggedIn: false,
      loading: false,
      tasks: [],
    };
  },
  methods: {
    getHeaders() {
      return {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      };
    },
    
    async logout() {
      const token = localStorage.getItem("token");
      localStorage.removeItem("token");
      localStorage.removeItem("role");
      localStorage.removeItem("full_name");
      this.$router.push("/login");
      const resp = await axios.post("http://127.0.0.1:5000/logout", {}, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      this.$toast.success(resp.data.message || "Logged out successfully.");
    },
    async getTasks() {
      this.loading = true;
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/tasks",
          { headers: this.getHeaders() },
        );
        this.tasks = response.data.tasks;
      } catch (error) {
        this.$toast.error(error.response?.data?.message || "Could not load tasks.");
      } finally {
        this.loading = false;
      }
    },
    async updateTask(task) {
      try {
        await axios.put(
          `http://127.0.0.1:5000/tasks/${task.id}`,
          { status: task.status },
          { headers: this.getHeaders() },
        );
        this.$toast.success("Task status updated.");
      } catch (error) {
        this.$toast.error(error.response?.data?.message || "Could not update task.");
        await this.getTasks();
      }
    },
    statusClass(status) {
      if (status === "completed") return "text-bg-success";
      if (status === "in-progress") return "text-bg-warning";
      return "text-bg-secondary";
    },
  },
  mounted() {
    this.isLoggedIn = !!localStorage.getItem("token");
    if (!this.isLoggedIn) {
      this.$router.push("/login");
      return;
    }
    this.getTasks();
  },
};
</script>
