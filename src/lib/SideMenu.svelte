<script>
  export let domainId

  import { domainNavigation } from './domainNavigation'
</script>

<nav class="w-96 pb-8 px-6 max-h-screen overflow-y-auto hidden 2xl:block text-gray-600">
  {#each domainNavigation as group}
    <div class="text-xl mt-8 mb-2">{group.groupName}</div>
    <div>
      {#each group.domains as domain}
        <a href={`#/${domain.domainId}`} class={`inline-block m-1 text-lg hover:bg-blue-200 border border-blue-500 rounded-2xl px-3 ${domain.domainId === domainId ? '!bg-blue-500 !text-gray-200' : 'text-sky-700'}`}>{domain.domainName}</a>
      {/each}
    </div>
  {/each}
</nav>