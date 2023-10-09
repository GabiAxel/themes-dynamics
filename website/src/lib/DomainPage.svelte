<script>
  import SideMenu from './SideMenu.svelte'
  import DynamicDomainsAndThemes from './DynamicDomainsAndThemes.svelte'

  export let domainId

</script>

<div class="xl:container center mx-auto h-full max-w-screen-2xl flex flex-row">
  <SideMenu domainId={domainId}/>
  <DynamicDomainsAndThemes domainId={domainId}/>
</div>