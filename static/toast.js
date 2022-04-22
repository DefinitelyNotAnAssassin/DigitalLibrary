
  
  
  



var toastLiveExample = document.getElementById('liveToast')

bootstrap.Toast.Default.delay = 50000
window.onload = function(){

var toast = new bootstrap.Toast(toastLiveExample)
    toast.show()
}