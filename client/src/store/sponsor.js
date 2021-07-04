import { RestStorage } from '@unrest/vue-storage'
import { kebabCase } from 'lodash'
import { formatDistanceToNowStrict } from 'date-fns'

const fromServer = (sponsor) => {
  const { id, name } = sponsor
  sponsor.internal_url = `/sponsor/${id}/${kebabCase(name)}/`
  sponsor.sponsor_channels?.forEach((sc) => {
    sc.short_url = sc.url
      .replace(/^https?:\/\//i, '')
      .replace(/^www\./i, '')
      .toLowerCase()
    sc.video.age = formatDistanceToNowStrict(new Date(sc.video.created))
  })
  return sponsor
}

export default () => RestStorage('sponsor', { fromServer })
