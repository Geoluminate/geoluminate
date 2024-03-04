import JustGage from 'justgage'
import 'raphael'




// initialise justgage
Array.from(document.querySelectorAll('.gauge')).forEach(gaugeNode => {
  const gauge = new JustGage({
    id: gaugeNode.id,
    relativeGaugeSize: true,
    hideValue: true,
    hideMinMax: true,
  })
})
