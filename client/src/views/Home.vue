<template>
  <div class="sponsor-cards">
    <div v-for="sponsor in sponsors" :key="sponsor.id" class="sponsor-card card">
      <router-link class="card-body" :to="sponsor.internal_url">
        <img :src="sponsor.image_url" v-if="sponsor.image_url" class="w-8" />
        {{ sponsor.name }}
        <div class="flex-grow" />
        <div class="pill pill-primary">{{ sponsor.sponsor_count }}</div>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  __route: {
    meta: { title: 'Sponsors' },
    path: '/',
  },
  computed: {
    sponsors() {
      return this.$store.sponsor.getPage()?.items || []
    },
  },
}
</script>
