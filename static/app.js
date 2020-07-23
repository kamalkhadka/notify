$("#signup-form").on('submit', async function(evt) {
    evt.preventDefault();

    const firstName = $("#first-name");
    const lastName =  $("#last-name");
    const email = $("#email");
    const password = $("#password");

    const user = { "first-name": firstName.val(), "last-name" : lastName.val(), 
                    "email": email.val(), "password": password.val() }

    const resp = await axios.post("/users", user)
    
})