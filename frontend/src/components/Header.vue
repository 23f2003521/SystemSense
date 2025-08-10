<template>
  <header class="app-header d-flex justify-content-between align-items-center px-4 py-2 shadow-sm">
    <div class="brand d-flex align-items-center gap-2">
      <i class="fas fa-layer-group fs-4"></i>
      <h5 class="mb-0">SystemSense</h5>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header'
}
</script>

<style scoped>
.app-header {
  height: 60px;
  background-color: #fff;
  border-bottom: 1px solid #ddd;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.brand h5 {
  font-weight: 600;
  color: #333;
}

.username {
  font-weight: 500;
  color: #666;
}
</style>
