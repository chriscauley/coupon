import { RestStorage } from '@unrest/vue-reactive-storage'
import { kebabCase } from 'lodash'

const fromServer = (sponsor) => {
  const { id, name } = sponsor
  sponsor.url = `/sponsor/${id}/${kebabCase(name)}/`
  sponsor.sponsor_channels?.forEach(sc => {
    sc.short_url = sc.url.replace(/https?:\/\//, '')
  })
  console.log(sponsor)
  return sponsor
}

export default () => RestStorage('sponsor', { fromServer })
