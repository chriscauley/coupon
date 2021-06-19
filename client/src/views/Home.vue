<template>
  <div class="channel-list">
    <div v-for="channel in channels" :key="channel.id" class="channel-card card">
      <div class="card-body">
        {{ channel.name }}
        <div class="sponsor-list">
          <div v-for="promo in channel.latest_promos" :key="promo.sponsor.id">
            <unrest-dropdown class="sponsor-dropdown">
              <div class="sponsor-dropdown__trigger">
                <img :src="promo.sponsor.image_url" v-if="promo.sponsor" />
                <i v-else class="fa fa-question" />
              </div>
              <template #content>
                <div class="dropdown-items" placement="left">
                  <a :href="promo.url" class="dropdown-item">
                    <img :src="promo.sponsor.image_url" v-if="promo.sponsor" />
                    &nbsp;
                    <div class="flex-grow">{{ promo.sponsor.name }}</div>
                  </a>
                  <markdown
                    :source="promo.paragraph"
                    :linkify="true"
                    class="dropdown-item markdown"
                  />
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
    path: '/',
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
