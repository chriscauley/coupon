<template>
  <div v-if="sponsor">
    <h1>{{ sponsor.name }}</h1>
    <table class="table">
      <thead>
        <tr>
          <th>Promo URL</th>
          <th>Channel</th>
          <th>Video</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="{ channel, video, short_url, url, id } in sponsor.sponsor_channels" :key="id">
          <td>
            <a :href="url" class="flex items-center">
              <img :src="sponsor.image_url" class="w-8 mr-2" />
              <div class="truncate">{{ short_url }}</div>
            </a>
          </td>
          <td>
            <a :href="channel.url" class="flex items-center">
              <img :src="channel.image_url" class="w-8 mr-2" />
              {{ channel.name }}
            </a>
          </td>
          <td>
            <a :href="video.url" class="flex items-center">
              <i class="fa fa-youtube-play text-youtube mr-2 fa-2x" />
              <div class="truncate">{{ video.title }}</div>
            </a>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { startCase } from 'lodash'

export default {
  __route: {
    meta: {
      title: (to) => startCase(to.params.sponsor_name),
    },
    path: '/sponsor/:sponsor_id/:sponsor_name/',
  },
  computed: {
    sponsor() {
      const { sponsor_id } = this.$route.params
      return this.$store.sponsor.getOne(sponsor_id)
    },
  },
}
</script>
