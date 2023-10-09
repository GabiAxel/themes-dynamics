<script>
  export let domainId

  import domains from '../assets/domains.json'
  let domain = domains.find(d => d.domain === domainId)

  const createProtvistaPdbComponent = (node, domainId) => {
    domain = domains.find(d => d.domain === domainId)
    if (!domain) {
      return
    }
    const protvistaPdb = document.createElement('protvista-pdb')
    protvistaPdb.setAttribute('custom-data', 'true')
    protvistaPdb.setAttribute('subscribe-events', 'false')
    node.appendChild(protvistaPdb)
    protvistaPdb.viewerdata = {
      displayNavigation: true,
      displaySequence: true,
      length: domain.length,
      tracks: [{
        label: 'Modes',
        data: domain.modes.map((mode, i) => ({
          label: `Mode ${i + 1}`,
          type: '',
          locations: [{
            fragments: mode.filter(mode => mode[1] > 0).map(([start, end], j) => ({
              start,
              end,
              color: j % 2 == 0 ? 'red' : 'blue',
              tooltipContent: `Mode ${i + 1}`
            }))
          }]
        })),
      }, {
        label: 'Themes',
        data: domain.themes.map(([theme, start, end]) => ({
          label: theme,
          type: '',
          locations: [{
            fragments: [{ start, end, color: 'yellowgreen', tooltipContent: theme }]
          }]
        }))
      }]
    }
  }

  const viewTracks = (node, domainId) => {
    createProtvistaPdbComponent(node, domainId)
    return {
      update(domainId) {
        node.innerHTML = ''
        createProtvistaPdbComponent(node, domainId)
      }
    }

  }

  let pdbeMolstar

  const viewStructure = (node, domainId) => {
    pdbeMolstar = new PDBeMolstarPlugin()
    pdbeMolstar.render(node, {
      customData: {
        url: `pdb/${domainId}.pdb`,
        format: 'pdb'
      },
      hideControls: true,
      hideCanvasControls: ['expand', 'selection', 'animation', 'controlToggle', 'controlInfo'],
      bgColor: {r: 229, g: 231, b: 235}
    })
    return {
      update(domainId) {
        pdbeMolstar.load({
          url: `pdb/${domainId}.pdb`,
          format: 'pdb'
        }, true)
      }
    }
  }

  const selectFragment = ({detail}) => {
    pdbeMolstar.visual.select({
      data: [{
        start_residue_number: Math.max(1, detail.start),
        end_residue_number: detail.end
      }]})
  }

  const highlightFragment = ({detail}) => {
    pdbeMolstar.visual.highlight({
      data: [{
        start_residue_number: Math.max(1, detail.start),
        end_residue_number: detail.end
      }]})
  }

</script>

<style>
  .pdbe-protvista-wrapper {
    width: 700px;
    height: 500px;
  }
  .pdbe-molstar-wrapper {
      position: relative;
      width: 500px;
      height: 500px;
  }
</style>

<div class="pt-4 pl-4 max-h-screen overflow-auto">
  <div class="flex justify-between">
    <a href="#/" class="border border-gray-400 bg-gray-400/50 hover:bg-gray-300 px-4 py-2 rounded-md">« All Domains</a>
    <a href={`pymol/${domain.domain}.pse`} target="_blank" class="text-gray-100 border border-green-700 bg-green-700 hover:bg-green-600 px-4 py-2 rounded-md">↓ Download PyMOL Session</a>
  </div>
  <h1 class="text-2xl my-4">{domain.group} / {domain.domain}</h1>
  <div class="flex flex-row">
    <div>
      <div use:viewTracks={domainId}
           on:protvista-click={selectFragment}
           on:protvista-mouseover={highlightFragment}
           on:protvista-mouseout={pdbeMolstar.visual.clearHighlight}
           class="pdbe-protvista-wrapper"
      ></div>
    </div>
    <div>
      <div use:viewStructure={domainId}
           class="pdbe-molstar-wrapper"
      ></div>
    </div>
  </div>
</div>