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
  <h1 class="text-3xl my-10">Reused Protein Segments Linked to Functional Dynamics - Supplementary Website</h1>
  <div  class="text-left">
    <p>
      This website contains the aggregated analysis results of 150 ECOD domains<sup>1</sup>.
      Each ECOD domain's page lists the dynamic domains for the top normal modes<sup>2</sup>,
      themes<sup>3</sup>, and Pfam annotations<sup>4</sup> along the ECOD domain sequence and structure.
      The analysis results and PyMOL sessions can be downloaded for each ECOD domain.
    </p>
    <h2 class="text-xl mt-6 mb-2">References</h2>
    <ol class="list-decimal">
      <li class="mt-2">Cheng, Hua, et al. "ECOD: an evolutionary classification of protein domains." <i>PLoS computational biology</i> 10.12 (2014): e1003926.</li>
      <li class="mt-2">Yiğit Kutlu, Gabriel Axel, Rachel Kolodny, Nir Ben-Tal and Turkan Haliloglu. "Reused Protein Segments Linked to Functional Dynamics"</li>
      <li class="mt-2">Sergey Nepomnyachiy, Nir Ben-Tal, and Rachel Kolodny. "Complex evolutionary footprints revealed in an analysis of reused protein segments of diverse lengths." <i>Proceedings of the National Academy of Sciences</i> 114.44 (2017): 11703-11708.</li>
      <li class="mt-2">Mistry, Jaina, et al. "Pfam: The protein families database in 2021." <i>Nucleic acids research</i> 49.D1 (2021): D412-D419.</li>
    </ol>
  </div>
  <p class="text-2xl mt-20">Select an ECOD domain to view its dynamic domains, themes and Pfam annotations</p>
  {#each domainNavigation as group}
    <h3 class="text-xl mt-10">{group.groupName}</h3>
    <div>
      {#each group.domains as domain}
        <a href={`#/${domain.domainId}`} class="m-4 border-4 border-gray-300 hover:border-gray-500 rounded-3xl p-4 bg-gray-100 inline-block">
          <img src={`thumbnail/${domain.domainId}.png`} alt={domain.domainId} class="w-[200px] h-[200px]"/>
          <footer class="text-xl">{domain.domainName}</footer>
        </a>
      {/each}
    </div>
  {/each}
</div>