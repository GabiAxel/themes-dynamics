<script>
  export let domainId

  import { chain } from 'lodash'
  import * as NGL from 'ngl'
  import domains from '../assets/domains.json'
  import pfam from '../assets/pfam.json'

  let domain = domains.find(d => d.domain === domainId)

  let stage
  let modeRepresentation
  let themeRepresentations
  let modeLabel

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
            fragments: mode.map(([start, end], j) => ({
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
      }, {
        label: 'Pfam',
        data: domainId in pfam ? pfam[domainId].map(([pfam, start, end]) => ({
          label: pfam,
          type: '',
          locations: [{
            fragments: [{ start: start + domain.modes[0][0][0] - 1, end: end + domain.modes[0][0][0] - 1, color: 'orchid', tooltipContent: pfam }]
          }]
        })) : []
      }]
    }
    protvistaPdb.layoutHelper.showSubtracks(1)
    protvistaPdb.layoutHelper.showSubtracks(2)
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

  const loadStructure = (domainId) => {
    modeLabel = 'Mode 1'
    themeRepresentations = {}

    const colorScheme = NGL.ColormakerRegistry.addSelectionScheme([
      ['blue', chain(domain.modes[0]).filter((_, i) => i % 2 === 0).map(([start, end]) => `${start}-${end}`).join(' or ').value(), undefined],
      ['red', '*', undefined]
    ])

    stage.loadFile(`pdb/${domainId}.pdb`)
      .then(o => {
        modeRepresentation = o.addRepresentation('cartoon', { color: colorScheme })
        o.autoView()
      })
  }

  const viewStructure = (node, domainId) => {
    stage = new NGL.Stage(node, { backgroundColor: '#e2e8f0'})
    loadStructure(domainId)

    return {
      update(domainId) {
        stage.removeAllComponents()
        loadStructure(domainId)
      }
    }
  }

  const selectFragment = ({detail}) => {
    console.log(detail)
    if(detail.feature.label.startsWith('Mode ')) {
      modeLabel = detail.feature.label
      stage.compList[0].removeRepresentation(modeRepresentation)

      const colorScheme = NGL.ColormakerRegistry.addSelectionScheme([
        ['blue', chain(detail.feature.locations[0].fragments).filter({ color: 'blue' }).map(({start, end}) => `${start}-${end}`).join(' or ').value(), undefined],
        ['red', '*', undefined]
      ])

      modeRepresentation = stage.compList[0].addRepresentation('cartoon', { color: colorScheme })
    } else {
      const { label, start, end } = detail.feature

      let themeRepresentation = themeRepresentations[label]
      if(themeRepresentation) {
        stage.compList[0].removeRepresentation(themeRepresentation)
        delete themeRepresentations[label]
      } else {
        const { color } = detail.feature.locations[0].fragments[0]
        themeRepresentation = stage.compList[0].addRepresentation('rope', { radiusScale: 3, colorScheme: 'uniform', color, sele: `${start}-${end}` })
        themeRepresentations[label] = themeRepresentation
      }
    }

  }
</script>

<style>
  .pdbe-protvista-wrapper {
    width: 700px;
    height: 500px;
  }
  .ngl-wrapper {
      position: relative;
      width: 500px;
      height: 500px;
  }

</style>

<div class="pt-4 px-4 max-h-screen overflow-auto flex-auto">
  <div class="container">
    <div class="flex justify-between">
      <a href="#/" class="border border-gray-400 bg-gray-400/50 hover:bg-gray-300 px-4 py-2 rounded-md">« All Domains</a>
      <div class="flex space-x-2">
        <a href={`xlsx/${domain.domain}_results.xlsx`} target="_blank" class="download_button">↓ Download Analysis Results</a>
        <a href={`pymol/${domain.domain}.pse`} target="_blank" class="download_button">↓ Download PyMOL Session</a>
      </div>
    </div>
    <h1 class="text-2xl my-4">{domain.group} / {domain.domain}</h1>
    <p class="my-10">
      The panel on the left shows bars representing the <strong class="text-red-700">dynamic</strong> <strong class="text-blue-700">elements</strong> for each mode, <strong class="text-green-700">themes</strong> and <strong class="text-fuchsia-600">Pfam annotations</strong> along the ECOD domain sequence.<br/><br/>
      The 3D representation on the right initially shows the dynamic elements for Mode 1. Click on the <strong class="text-red-700">dynamic</strong> <strong class="text-blue-700">element</strong> bar of any other mode to update the 3D representation to that mode.<br/><br/>
      Click on any bar representing any <strong class="text-green-700">theme</strong> or <strong class="text-fuchsia-600">Pfam annotation</strong> to toggle it on or off in the 3D representation.<br/><br/>
      Use the left mouse button to rotate the 3D representation, the right mouse button to pan, to the mouse wheel to zoom in and out.
    </p>
    <div class="flex flex-row">
      <div>
        <div use:viewTracks={domainId} on:protvista-click={selectFragment} class="pdbe-protvista-wrapper"></div>
      </div>
      <div class="relative">
        <div class="absolute top-4 left-4 z-10 text-xl">{modeLabel}</div>
        <div use:viewStructure={domainId} class="ngl-wrapper"></div>
      </div>
    </div>
  </div>
</div>