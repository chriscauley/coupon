<template>
  <header :class="css.nav.outer()">
    <section :class="css.nav.section('left')">
      <router-link to="/" :class="css.nav.brand()">Coupon</router-link>
    </section>
    <section :class="css.nav.section('flex items-center')">
      <unrest-auth-menu />
    </section>
  </header>
</template>

<script>
import css from '@unrest/css'

export default {
  data() {
    return { css }
  },
}
</script>
