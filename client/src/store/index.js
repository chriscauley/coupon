import channel from './channel'
import sponsor from './sponsor'

const modules = { channel, sponsor }
const store = {
  install: (app) => {
    app.config.globalProperties.$store = store
  },
}

Object.entries(modules).forEach(([name, f]) => {
  store[name] = f({ store })
})

export default store
