var email = document.getElementById("email")
var valid_email = document.getElementById("valid-email")
var password = document.getElementById("password")
var valid_password = document.getElementById("valid-password")

document.getElementById("form-login").addEventListener("submit", function(e) {
    if(email.value === ""){
        e.preventDefault()
        valid_email.innerHTML = "Champs vide !"
        valid_email.style.display = "block"
    }
    else{
        valid_email.style.display = "none"
    }

    if(password.value === ""){
        e.preventDefault()
        valid_password.innerHTML = "Champs vide !"
        valid_password.style.display = "block"
    }
    else{
        valid_password.style.display = "none"
    }
})