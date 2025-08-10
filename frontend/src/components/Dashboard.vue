<script>
import axios from "axios";

export default {
  data() {
    return {
      token: "",
      role: "",
      userdata: "",
      machines: [],
      error: "",
      filters: {
        os_update_status: "",
        encryption: ""
      }
    };
  },
  mounted() {
    this.loadToken();
    this.loadDashboard();
  },
  methods: {
    loadToken() {
      const token = localStorage.getItem("token");
      if (token) {
        console.log(token)
        this.token = token;
      }
    },

    loadDashboard() {
        const response=axios.get("http://127.0.0.1:5000/api/dashboard", {
          headers: {
            "Authorization": `Bearer ${this.token}`,
            // "Access-Control-Allow-Origin":"**",
            
          },
        })
        response
        .then((res) => {
            console.log(res)
          this.role = res.data.role;
          this.userdata = res.data;
          this.machines = res.data.machines;
        })
        .catch((err) => {
          this.error = err.response?.data?.message || "Unknown error";
        });
    },

    filteredMachines() {
    return this.machines.filter((machine) => {
      const osMatch =
        !this.filters.os_update_status ||
        machine.os_update_status === this.filters.os_update_status;

      const encryptionMatch =
        !this.filters.encryption ||
        (this.filters.encryption === "encrypted" &&
          machine.disk_encryption_status === true) || // lowercase true
        (this.filters.encryption === "not_encrypted" &&
          machine.disk_encryption_status === false); // lowercase false

      return osMatch && encryptionMatch;
    });
  },
  logout() {
    localStorage.removeItem("token"); // if you store auth in localStorage
    this.$router.push("/login"); // redirect to login
  },
  },
};
</script>
<template>
  <div v-if="token">

    <!-- USER DASHBOARD -->
    <div v-if="role === 'user'" class="main--content">
      <!-- Header -->
      <div class="header--wrapper">
        <div class="header--title">
          <span>Welcome {{ userdata.username }}</span>
          <h2>Dashboard</h2>
        </div>
        <div class="user--info">
          <div class="search--box">
            <div class="search--box">
               <button class="btn btn-danger ms-2" @click="logout">Logout</button>
            </div>
          </div>
        </div>
      </div>

      <!-- User Machine Cards -->
      <div class="tabular-wrapper">
        <h3 class="main-title">My Machines</h3>
        <div class="d-flex flex-wrap">
          <div v-for="m in machines" :key="m.id" class="machine-card m-3 p-3 border rounded shadow-sm" style="width: 300px;">
            <h4>{{ m.name }}</h4>
            <p><strong>Model:</strong> {{ m.model }}</p>
            <p><strong>Serial Number:</strong> {{ m.serial_number }}</p>
            <p><strong>Last Service:</strong> {{ m.last_service_date }}</p>
            <p><strong>Last Check-in:</strong> {{ m.last_checkin }}</p>
            <p><strong>Disk Encrypted:</strong> {{ m.disk_encryption_status ? "Yes" : "No" }}</p>
            <p><strong>OS:</strong> {{ m.os_update_status }}</p>
            <p><strong>CPU Usage:</strong> {{ m.cpu_usage }}%</p>
            <p><strong>Memory Usage:</strong> {{ m.memory_usage }}%</p>
            <p><strong>Disk Usage:</strong> {{ m.disk_usage }}%</p>
            <p>
              <strong>Issue:</strong>
              <span v-if="m.issue_detected" class="text-danger">⚠️ {{ m.issue_description }}</span>
              <span v-else>✅ All good</span>
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- ADMIN DASHBOARD -->
    <div v-else-if="role === 'admin'" class="main--content">
      <!-- Header -->
      <div class="header--wrapper">
        <div class="header--title">
          <span>Welcome {{ userdata.username }}</span>
          <h2>Dashboard</h2>
        </div>
        <div class="user--info">
           <div class="search--box">
  <!-- OS Filter -->
  <select v-model="filters.os_update_status" class="form-select w-auto">
    <option value="">Filter by OS</option>
    <option value="Up-to-date">Up-to-date</option>
    <option value="Outdated">Outdated</option>
  </select>

  <!-- Encryption Filter -->
  <select v-model="filters.encryption" class="form-select w-auto">
    <option value="">Disk Encryption</option>
    <option value="encrypted">Encrypted</option>
    <option value="not_encrypted">Not Encrypted</option>
  </select>
            </div>
            <div class="search--box">
               <button class="btn btn-danger ms-2" @click="logout">Logout</button>
            </div>


        </div>
      </div>

      

      <!-- Machine Table -->
      <div class="tabular-wrapper">
        <h3 class="main-title">Machines</h3>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Owner</th>
                <th>Model</th>
                <th>Serial</th>
                <th>OS</th>
                <th>Encrypted</th>
                <th>Last Check-in</th>
                <th>Issue?</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="m in filteredMachines()" :key="m.id">
                <td>{{ m.name }}</td>
                <td>{{ m.owner }}</td>
                <td>{{ m.model }}</td>
                <td>{{ m.serial_number }}</td>
                <td>{{ m.os_update_status }}</td>
                <td>{{ m.disk_encryption_status ? "Yes" : "No" }}</td>
                <td>{{ m.last_checkin }}</td>
                <td>
                  <span v-if="m.issue_detected" class="text-danger">⚠️</span>
                  <span v-else>✅</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-else class="text-center">
      Loading...
    </div>
  </div>

  <!-- Not Logged In -->
  <div v-else class="text-center">
    Please login
  </div>
</template>


<style scoped>
.dashboard-admin, .dashboard-user {
  padding: 20px;
}

.machine-card {
  border: 1px solid #ddd;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 6px;
  box-shadow: 1px 1px 8px rgba(0, 0, 0, 0.1);
}

.machine-table {
  width: 100%;
  border-collapse: collapse;
}

.machine-table th,
.machine-table td {
  padding: 10px;
  border: 1px solid #ccc;
  text-align: center;
}

.filters {
  margin-bottom: 15px;
}
</style>
