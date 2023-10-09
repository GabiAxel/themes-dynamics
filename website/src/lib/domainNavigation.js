import domains from '../assets/domains.json'
import { chain } from 'lodash'

export const domainNavigation = chain(domains)
  .groupBy('group')
  .mapValues(domains => domains.map(d => d.domain))
  .toPairs()
  .sortBy(pair => pair[0].toLowerCase())
  .map(([groupName, domains]) => ({
    groupName,
    domains: domains.map(domain => ({ domainId: domain, domainName: domain }))
  }))
  .value()