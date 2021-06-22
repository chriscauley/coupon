<template>
  <div class="container mx-auto">
    <Nav />
    <router-view class="router-view" />
    <unrest-ui />
  </div>
</template>

<script>
import Nav from './components/Nav.vue'

export default {
  components: { Nav },
}
</script>
