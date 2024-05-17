<script>
  import SideMenu from './SideMenu.svelte'
  import DynamicDomainsAndThemes from './DynamicDomainsAndThemes.svelte'

  export let domainId

</script>

<div class="h-full flex flex-row">
  <SideMenu domainId={domainId}/>
  <DynamicDomainsAndThemes domainId={domainId}/>
</div>