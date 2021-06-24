<template>
  <div class="container mx-auto">
    <Nav />
    <router-view class="router-view" />
    <unrest-ui />
    <button class="add-channel-button" @click="$ui.alert({ tagName: 'add-channel' })">
      <i class="fa fa-plus" />
      <span class="text">Add a Channel</span>
    </button>
  </div>
</template>

<script>
import Nav from './components/Nav.vue'

export default {
  components: { Nav },
}
</script>
