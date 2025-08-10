<script>
export default {
  methods: {
    toLogin() {
      this.$router.push("/login");
    }
  }
}
</script>

<template>
  <div>
    <!-- Hero Section -->
    <section class="hero">
      <img
        class="hero-image"
        src="../assets/bg1.jpeg"
        alt="Cross-platform system utility and admin dashboard"
        onerror="this.style.display='none'"
      />

      <div class="hero-content">
        <h1>
          Welcome to <span style="color: #49b675;">System Health Monitor</span><br />
          Cross-Platform Utility & Admin Dashboard
        </h1>
        <p>
          Collect and monitor critical system health data effortlessly. Our utility
          works across macOS, Windows, and Linux to track disk encryption, OS updates,
          antivirus status, and inactivity settings.
        </p>
        <p>
          The admin dashboard offers centralized control to view machine statuses,
          detect issues, and ensure your systems are secure and up-to-date.
        </p>
        <button @click="toLogin" class="btn-orange big">Get Started</button>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features">
      <div class="feature">
        <h3>Cross-Platform Utility</h3>
        <p>
          Runs background checks on your system’s health, using minimal resources and
          reports only when changes are detected.
        </p>
      </div>
      <div class="feature">
        <h3>Secure Backend API</h3>
        <p>
          Receives and stores machine data securely, supports filtering and CSV exports
          for admin ease-of-use.
        </p>
      </div>
      <div class="feature">
        <h3>Admin Dashboard</h3>
        <p>
          Visualize real-time machine statuses, flag configuration issues, and get
          last check-in timestamps — all in a clean, responsive interface.
        </p>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* Reset & base */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  background: #fff;
  color: #111;
}

.btn-orange {
  background-color: #712898;
  border: none;
  color: white;
  padding: 0.65rem 1.5rem;
  font-weight: 700;
  font-size: 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-orange:hover {
  background-color: #c032b6;
}

/* Hero Section */
.hero {
  position: relative;
  text-align: center;
  color: white;
  overflow: hidden;
}

.hero-image {
  width: 100%;
  max-height: 400px;
  object-fit: cover;
  filter: brightness(0.6);
  user-select: none;
}

.hero-content {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  max-width: 900px;
  padding: 1rem 2rem;
  transform: translate(-50%, -50%);
  background-color: rgba(0, 0, 0, 0.4);
  border-radius: 12px;
}

.hero-content h1 {
  font-size: 2.2rem;
  font-weight: 900;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8);
}

.hero-content p {
  font-weight: 400;
  font-size: 1.25rem;
  margin-bottom: 1rem;
  text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.6);
}

/* Features Section */
.features {
  display: flex;
  max-width: 900px;
  margin: 4rem auto 6rem auto;
  gap: 3rem;
  padding: 0 1rem;
  justify-content: center;
  flex-wrap: wrap;
  color: #333;
  text-align: center;
}

.feature {
  flex: 1 1 280px;
  padding: 1.5rem 1.2rem;
  border-radius: 8px;
  background-color: #f5f5f5;
}

.feature h3 {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #49b675;
}

.feature p {
  font-weight: 400;
  font-size: 1rem;
  line-height: 1.4;
  color: #555;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 1.7rem;
  }

  .hero-content p {
    font-size: 1rem;
  }

  .features {
    flex-direction: column;
    max-width: 100%;
    margin: 3rem auto;
  }
}
</style>
