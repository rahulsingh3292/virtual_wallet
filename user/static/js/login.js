

let hideLoginAlert = (color,msg)=>{$("#login-alert").hide() }
let showLoginAlert = (color,msg)=>{$("#login-alert").show().addClass("alert-"+color).text(msg)}

$("#login").click(function(){ 
  $.ajax({
    url: "/accounts/login/" ,
    method: "POST",
    data: { 
      username: $("#username").val(),
      password: $("#password").val()
    }, 
    success: function(data){
       if(data.status === 200){
         showLoginAlert("success", "login success redirecting you to homepage" )
         setTimeout(function() {  window.location.href = "/";}, 2000);
       
       }
        else if (data.status === 404){
          showLoginAlert("danger","invalid credentials..")
        } else{
          showLoginAlert("primary", "something went wrong with server")
        }
 
    },
    
  })
  
})
