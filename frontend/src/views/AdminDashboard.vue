<template>
  <NavBar @logout="logout" :is-logged-in="isLoggedIn" />

  <main class="container py-5 mt-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h1>Admin Dashboard</h1>
        <p class="text-muted mb-0">Create, update, and delete tasks.</p>
      </div>
      <button class="btn btn-primary" @click="getTasks">Refresh</button>
    </div>

    <form class="card card-body shadow-sm mb-4" @submit.prevent="createTask">
      <h5 class="mb-3">Create task</h5>
      <div class="row g-3">
        <div class="col-md-4">
          <label for="title" class="form-label">Title</label>
          <input id="title" v-model="newTask.title" class="form-control" required>
        </div>
        <div class="col-md-4">
          <label for="assigned_to" class="form-label">Employee</label>
          <select
            id="assigned_to"
            v-model.number="newTask.assigned_to"
            class="form-control"
          >
            <option :value="null">Select an employee</option>
            <option v-for="employee in employees" :key="employee.id" :value="employee.id">
              {{ employee.full_name }} ({{ employee.email }})
            </option>
          </select>
        </div>
        <div class="col-md-4">
          <label for="description" class="form-label">Description</label>
          <input id="description" v-model="newTask.description" class="form-control">
        </div>
      </div>
      <button type="submit" class="btn btn-success mt-3 align-self-start">
        Create task
      </button>
    </form>

    <div v-if="loading" class="text-center">Loading tasks...</div>
    <div v-else-if="tasks.length === 0" class="alert alert-info">
      No tasks found.
    </div>

    <div v-else class="table-responsive">
      <table class="table table-bordered align-middle">
        <thead>
          <tr>
            <th>Title</th>
            <th>Description</th>
            <th>Employee ID</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="task in tasks" :key="task.id">
            <td>
              <input v-if="editingTask && editingTask.id === task.id"
                v-model="editingTask.title" class="form-control">
              <span v-else>{{ task.title }}</span>
            </td>
            <td>
              <input v-if="editingTask && editingTask.id === task.id"
                v-model="editingTask.description" class="form-control">
              <span v-else>{{ task.description || "No description" }}</span>
            </td>
            <td>
              <select v-if="editingTask && editingTask.id === task.id"
                v-model.number="editingTask.assigned_to" class="form-select">
                <option :value="null">Unassigned</option>
                <option v-for="employee in employees" :key="employee.id" :value="employee.id">
                  {{ employee.full_name }}
                </option>
              </select>
              <span v-else>{{ task.assigned_to || "Unassigned" }}</span>
            </td>
            <td>
              <select v-if="editingTask && editingTask.id === task.id"
                v-model="editingTask.status" class="form-select">
                <option value="pending">Pending</option>
                <option value="in-progress">In progress</option>
                <option value="completed">Completed</option>
              </select>
              <span v-else>{{ task.status }}</span>
            </td>
            <td class="text-nowrap">
              <button v-if="editingTask && editingTask.id === task.id"
                class="btn btn-sm btn-success me-2" @click="saveTask">
                Save
              </button>
              <button v-if="editingTask && editingTask.id === task.id"
                class="btn btn-sm btn-secondary" @click="editingTask = null">
                Cancel
              </button>
              <button v-else class="btn btn-sm btn-outline-primary me-2"
                @click="startEditing(task)">
                Edit
              </button>
              <button class="btn btn-sm btn-outline-danger" @click="deleteTask(task)">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </main>
</template>

<script>
import axios from "axios";
import NavBar from "@/components/NavBar.vue";

export default {
  name: "AdminDashboard",
  components: {
    NavBar,
  },
  data() {
    return {
      isLoggedIn: false,
      loading: false,
      tasks: [],
      employees: [],
      editingTask: null,
      newTask: {
        title: "",
        description: "",
        assigned_to: null,
      },
    };
  },
  methods: {
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
    getHeaders() {
      return {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      };
    },
    async getTasks() {
      this.loading = true;
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/tasks",
          { headers: this.getHeaders() },
        );
        // alert(JSON.stringify(response.data.tasks));
        this.tasks = response.data.tasks;
      } catch (error) {
        this.$toast.error(error.response?.data?.message || "Could not load tasks.");
      } finally {
        this.loading = false;
      }
    },
    async getEmployees() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/employees",
          { headers: this.getHeaders() },
        );
        this.employees = response.data.employees;
      } catch (error) {
        this.$toast.error(error.response?.data?.message || "Could not load employees.");
      }
    },
    async createTask() {
      try {
        await axios.post(
          "http://127.0.0.1:5000/tasks",
          this.newTask,
          { headers: this.getHeaders() },
        );
        this.$toast.success("Task created.");
        this.newTask = { title: "", description: "", assigned_to: null };
        await this.getTasks();
      } catch (error) {
        this.$toast.error(error.response?.data?.message || "Could not create task.");
      }
    },
    startEditing(task) {
      this.editingTask = { ...task };
    },
    async saveTask() {
      try {
        await axios.put(
          `http://127.0.0.1:5000/tasks/${this.editingTask.id}`,
          this.editingTask,
          { headers: this.getHeaders() },
        );
        this.$toast.success("Task updated.");
        this.editingTask = null;
        await this.getTasks();
      } catch (error) {
        this.$toast.error(error.response?.data?.message || "Could not update task.");
      }
    },
    async deleteTask(task) {
      if (!window.confirm(`Delete "${task.title}"?`)) return;
      try {
        await axios.delete(
          `http://127.0.0.1:5000/tasks/${task.id}`,
          { headers: this.getHeaders() },
        );
        this.$toast.success("Task deleted.");
        await this.getTasks();
      } catch (error) {
        this.$toast.error(error.response?.data?.message || "Could not delete task.");
      }
    },
  },
  mounted() {
    this.isLoggedIn = !!localStorage.getItem("token");
    if (!this.isLoggedIn) {
      this.$router.push("/login");
      return;
    }
    this.getTasks();
    this.getEmployees();
  },
};
</script>
