<script context="module">
  import { writable } from 'svelte/store'

  const scrollY = writable(0)
</script>

<script>
	import { domainNavigation } from './domainNavigation'
  import { onMount, onDestroy } from 'svelte'
  import { get } from 'svelte/store'

  onMount(() => {
    window.scrollTo({left: 0, top: get(scrollY)})
  })

  onDestroy(() => {
    scrollY.set(window.scrollY)
  })
</script>

<div class="container mx-auto text-center">
  <h1 class="text-4xl my-10">Reused Protein Segments Linked to Functional Dynamics</h1>
  <i class="text-3xl">Supplementary Data</i>
  {#each domainNavigation as group}
    <h3 class="text-3xl mt-20">{group.groupName}</h3>
    <div>
      {#each group.domains as domain}
        <a href={`#/${domain.domainId}`} class="m-4 border-4 border-gray-300 hover:border-gray-500 rounded-3xl p-4 bg-gray-100 inline-block">
          <img src={`thumbnail/${domain.domainId}.png`} alt={domain.domainId} class="w-[300px] h-[300px]"/>
          <footer class="text-xl">{domain.domainName}</footer>
        </a>
      {/each}
    </div>
  {/each}
</div>