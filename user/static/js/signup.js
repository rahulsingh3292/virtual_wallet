

let hideAlert = (color,msg)=>{
   $("#alert").attr("class","")
  $("#alert").hide()
  }
let showAlert = (color,msg)=>{
  $("#alert").attr("class","")
  $("#alert").show().addClass("alert alert-"+color).text(msg)}



function getFields(){

  return {
        username: $("#username").val(),
        first_name: $("#first_name").val()
        ,
        is_premium_user: $("#is_premium_user").val(),
        last_name: $("#last_name").val(),
        password: $("#password").val(),
        confirm_password: $("#confirm_password").val(),
      } 
}

function validateFields(fieldObj){
  if (fieldObj.first_name.length < 5){
    showAlert("danger", "firstName length should be more than 5 characters"); 
    return
  } 
  
  
  if (fieldObj.username.length < 5){
    showAlert("danger", "username length should be more than 5 characters")
     return 
  }
  
  const password = fieldObj.password 
  const confirm_password = fieldObj.confirm_password 
  
  if (password.length < 5){
    showAlert("danger", "password length should be more than 5 characters") 
    return 
  }
  
  if (password!=confirm_password){
    showAlert("danger", "password didn't matched...")
    return
  }
  
  hideAlert() 
}

$("#signup").click(function(){ 
  
  const fields = getFields() 
  validateFields(fields)
  delete fields.confirm_password
  $.ajax({
    url: "/accounts/signup/" ,
    method: "POST",
    data: fields, 
    success: function(data){
       if(data.status === 201){
         showAlert("success", "signup success.. redirecting to login page.." )
         setTimeout(function() {   window.location.href = "/accounts/login/";}, 2000);
     
       }
        else if (data.status === 403){
          showAlert("danger", "this account already exist.\n try to signup with other username.. ")
          return 
        } else{
          showAlert("warning", "something went wrong with server.. please try again later..")
          return 
        }
 
    },
    
  })
  
})
