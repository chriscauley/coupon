import { RestStorage } from '@unrest/vue-reactive-storage'
import { kebabCase } from 'lodash'
import { formatDistanceToNowStrict } from 'date-fns'

const fromServer = (sponsor) => {
  const { id, name } = sponsor
  sponsor.url = `/sponsor/${id}/${kebabCase(name)}/`
  sponsor.sponsor_channels?.forEach((sc) => {
    sc.short_url = sc.url.replace(/https?:\/\//, '')
    sc.video.age = formatDistanceToNowStrict(new Date(sc.video.created))
  })
  return sponsor
}

export default () => RestStorage('sponsor', { fromServer })
