<script>
  import domains from './assets/domains.json'
  import DomainListPage from './lib/DomainListPage.svelte'
  import DomainPage from './lib/DomainPage.svelte'

  const validTokens = ['/', ...domains.map(({domain}) => `/${domain}`)]

  let token = '/'

  const handleLocationChange = () => {
    const tempToken = window.location.hash.replace('#', '')
    if(validTokens.includes(tempToken)) {
      token = tempToken
    } else {
      window.location.hash = '#/'
    }
  }

  handleLocationChange()

  window.addEventListener('hashchange', handleLocationChange)
</script>

{#if token === '/'}
  <DomainListPage/>
{:else}
  <DomainPage domainId={token.substring(1)}/>
{/if}