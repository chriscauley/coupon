import { RestStorage } from '@unrest/vue-reactive-storage'
import { kebabCase } from 'lodash'

const fromServer = (sponsor) => {
  const { id, name } = sponsor
  sponsor.url = `/sponsor/${id}/${kebabCase(name)}/`
  return sponsor
}

export default () => RestStorage('sponsor', { fromServer })
