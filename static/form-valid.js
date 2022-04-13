const name = document.getElementById('username')
const password = document.getElementById('password')
const form = document.getElementById('mainform')
const second_password = document.getElementById("secure_pass")


const password_error = document.getElementById("password-error")
const second_error = document.getElementById("second-error")
const name_error = document.getElementById("name-error")

form.addEventListener('submit', (e) => {
  let messages = []
  if (name.value === '' || name.value == null) {
    messages.push('Filler')
    name_error.innerText = "Name is required."
  }
  else{
    name_error.innerText = ""
  }

  
  
  
  
  if (password.value != second_password.value || second_password.value != password.value){
    
    messages.push("Filler")
    second_error.innerText = "Password doesn't match"
  }
  else{
    second_error.innerText = ""
  }
  

  if (password.value.length >= 20) {
    messages.push('Filler')
    password_error.innerText = "Password should be less than 20 characters"
  }
  else if (password.value.length <= 8){
    messages.push('Filler')
    password_error.innerText = "Password should be atleast 8 characters"
  }
  else{
    password_error.innerText = ""
  }

  if (password.value === 'password') {
    messages.push('Password cannot be password \n')
  }

  if (messages.length > 0) {
    e.preventDefault()
    let data = JSON.stringify(messages)
    
  }
 
})

