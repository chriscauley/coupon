<template>
  <Nav />
  <router-view class="router-view" />
  <unrest-ui />
</template>

<script>
import Nav from './components/Nav.vue'

export default {
  components: { Nav },
}
</script>
