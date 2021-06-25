<template>
  <div :class="css.root">
    <div v-if="results">
      <h3>Add a Channel</h3>
      <div
        class="list-group-item list-group-item-action"
        v-for="(channel, i) in results"
        :key="i"
        @click="addChannel(i)"
      >
        <img :src="channel.thumbnails.default.url" class="avatar" />
        {{ channel.title }}
        <div class="flex-grow" />
      </div>
    </div>
    <unrest-form v-else :schema="schema" @submit="search" :state="state" />
  </div>
</template>

<script>
import { getClient } from '@unrest/vue-reactive-storage'
import querystring from 'querystring'

const client = getClient()

const schema = {
  type: 'object',
  required: ['q'],
  properties: {
    q: {
      type: 'string',
      title: 'Search YouTube for channels',
    },
  },
}

export default {
  emits: ['close'],
  data() {
    return { schema, results: null, state: { q: 'hbomberguy' }, loading: false }
  },
  computed: {
    css() {
      return { root: ['add-channel-list', { '-loading': this.loading }] }
    },
  },
  methods: {
    search(data) {
      if (this.loading) {
        return
      }
      this.loading = true
      const url = 'search-channel/?' + querystring.stringify(data)
      client.get(url).then(({ results }) => {
        this.loading = false
        this.results = results
      })
    },
    addChannel(index) {
      if (this.loading) {
        return
      }
      const data = { index, q: this.state.q }
      this.loading = true
      client.post('add-channel/', data).then(({ name, id }) => {
        this.$ui.toast.success(`Added channel: ${name}`)
        this.$router.push(`/channel/${id}/${name}/`)
        this.$emit('close')
      })
    },
  },
}
</script>
