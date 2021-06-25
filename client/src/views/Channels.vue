<template>
  <div class="channel-cards">
    <div v-for="channel in channels" :key="channel.id" class="channel-card card">
      <div class="card-body">
        <router-link class="card-title" :to="channel.internal_url">
          <h4 class="w-full border-b flex pb-1 items-center">
            <div>
              <img :src="channel.image_url" class="w-6 mr-2 rounded-full" />
            </div>
            {{ channel.name }}
          </h4>
        </router-link>
        <div class="channel-card__sponsors">
          <div v-for="promo in channel.latest_promos" :key="promo.sponsor.id">
            <unrest-dropdown class="sponsor-dropdown">
              <div class="sponsor-dropdown__trigger">
                <img :src="promo.sponsor.image_url" v-if="promo.sponsor" class="w-8" />
                <i v-else class="fa fa-question" />
              </div>
              <template #content>
                <div class="dropdown-items" placement="left">
                  <a :href="promo.url" class="dropdown-item">
                    <img :src="promo.sponsor.image_url" v-if="promo.sponsor" class="w-8 mr-2" />
                    <div class="flex-grow">{{ promo.sponsor.name }}</div>
                  </a>
                  <markdown :source="promo.paragraph" :linkify="true" class="p-4 pb-0 markdown" />
                </div>
              </template>
            </unrest-dropdown>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  __route: {
    meta: { title: 'Coupo' },
    path: '/channels/',
  },
  computed: {
    channels() {
      const channels = (this.$store.channel.getPage()?.items || []).filter(
        (c) => c.latest_promos.length,
      )
      const sponsors = this.$store.sponsor.getPage()?.items || []
      channels.forEach((channel) => {
        channel.latest_promos.forEach((promo) => {
          promo.sponsor = sponsors.find((s) => s.id === promo.sponsor_id)
          promo.paragraph = promo.paragraph.replace(/https?:\/\//g, '')
        })
      })
      return channels
    },
  },
}
</script>
