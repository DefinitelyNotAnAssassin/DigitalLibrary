



async function loadNames(selectval) {
  var your_data = {
    "category": selectval
  }
  const response = await fetch(`/get_title`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(your_data),
    cache: "no-cache",
    headers: new Headers({
      "content-type": "application/json"
    })
  })
  const names = await response.json();
  return names
  
  
  // logs [{ name: 'Joker'}, { name: 'Batman' }]
}

$('select').on('change', async function() {
  var selectval = $('select').val()
  var dataset = await loadNames(selectval)
 
  
  Object.filter = (obj, predicate) => 
                  Object.fromEntries(Object.entries(obj).filter(predicate));
let filtered = Object.filter(dataset, ([name, category]) => category === `${this.value}`)
let availableTags = Object.keys(filtered)
    $( "#Title" ).autocomplete({
      source: availableTags
    });

})
  

