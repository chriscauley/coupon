<template>
  <div v-if="channel">
    <h1>{{ channel.name }}</h1>
    <table class="table">
      <thead>
        <tr>
          <th>Sponsor</th>
          <th>Promo URL</th>
          <th>Video</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="{ sponsor, short_url, url, video } in channel.latest_promos" :key="url">
          <td>
            <router-link class="flex items-center" :to="sponsor.internal_url">
              <img :src="sponsor.image_url" class="w-8 mr-2" />
              {{ sponsor.name }}
            </router-link>
          </td>
          <td>
            <a :href="url" class="flex items-center">
              <div>{{ short_url }}</div>
            </a>
          </td>
          <td>
            <a v-if="video" :href="video.url" class="flex items-center">
              <i class="fa fa-youtube-play text-youtube mr-2 fa-2x" />
              {{ video.title }}
            </a>
          </td>
          <td>{{ video.age }} ago</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { formatDistanceToNowStrict } from 'date-fns'
import { startCase, kebabCase } from 'lodash'

export default {
  __route: {
    meta: {
      title: (to) => startCase(to.params.channel_name),
    },
    path: '/channel/:channel_id/:channel_name/',
  },
  computed: {
    channel() {
      const { channel_id } = this.$route.params
      const channel = this.$store.channel.getOne(channel_id)

      // TODO copied from sponsor detail page
      const sponsors = this.$store.sponsor.getPage()?.items || []
      channel?.latest_promos.forEach((promo) => {
        promo.sponsor = sponsors.find((s) => s.id === promo.sponsor_id) || {}
        const { name, id } = promo.sponsor
        promo.sponsor.internal_url = `/sponsor/${id}/${kebabCase(name)}/`
        promo.paragraph = promo.paragraph.replace(/https?:\/\//g, '')
        promo.short_url = promo.url.replace(/^https?:\/\//, '').replace(/^www\./, '')
        promo.video.age = formatDistanceToNowStrict(new Date(promo.video.created))
      })
      return channel
    },
  },
}
</script>
