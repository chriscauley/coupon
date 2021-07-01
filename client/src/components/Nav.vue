<template>
  <header :class="css.nav.outer()">
    <section :class="css.nav.section('left')">
      <router-link to="/" :class="css.nav.brand()">Promotheus</router-link>
    </section>
    <section :class="css.nav.section('flex items-center')">
      <div :class="tabClass(tab)" v-for="tab in tabs" :key="tab[0]">
        <router-link :to="tab[0]">{{ tab[1] }}</router-link>
      </div>
      <unrest-auth-menu />
    </section>
  </header>
</template>

<script>
import css from '@unrest/css'

const tabs = [
  ['/', 'Sponsors'],
  ['/channels/', 'Channels'],
]

export default {
  data() {
    return { css, tabs }
  },
  methods: {
    tabClass([path]) {
      return ['btn', path === this.$route.path ? '-primary' : '-light']
    },
  },
}
</script>
