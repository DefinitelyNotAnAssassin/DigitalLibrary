
async function loadNames(selectval, inputval) {
var your_data = {
  "category": selectval,
  "search": `%${inputval}%`
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
}




/* $("#Title").on("keyup", async function(){
  var data = await loadNames($('select').val(), $('#Title').val())
  
  
  
  $( "#Title" ).autocomplete({
  source: data,
  minLength: 0,
  search: $('#Title').val()
})

})
*/
var debounce = null
$('#Title').on('keyup', async function(){
   clearTimeout(debounce);
   debounce = setTimeout(async function(){
     
     var data = await loadNames($("select").val(), $('#Title').val())
     
      $("#Title").autocomplete({
     source: data,
   })
    $("#Title").autocomplete("enable");
    $('#Title').autocomplete("search", $("#Title").val())
   }, 800)
  
});
