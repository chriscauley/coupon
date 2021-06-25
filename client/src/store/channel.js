import { RestStorage } from '@unrest/vue-reactive-storage'
import { kebabCase } from 'lodash'

const fromServer = (data) => {
  data.internal_url = `/channel/${data.id}/${kebabCase(data.name)}/`
  return data
}

export default () => RestStorage('channel', { fromServer })
