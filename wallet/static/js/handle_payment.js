function requestPayment(amount, to_user_id) {

  $.ajax({
    url: "/payment/request/",
    method: "POST",
    data: {
      to_user_id: to_user_id,
      amount: amount
    },
    success: function (resp) {
      if (resp.status === 200) {
        alert("payment request done")
      } else {
        alert("user not found.. ")
      }
    },
    error: function(err) {
      alert("something went wrong")
    }
  })
}


function sendPayment(amount, to_user_id) {
  $.ajax({
    url: "/payment/pay/",
    method: "POST",
    data: {
      to_user_id: to_user_id,
      amount: amount
    },
    success: function (resp) {
      if (resp.status === 200) {
        alert("successfully paid")
        return
      } else if (resp.status === 400) {
       alert("not enough balance to pay ")
       return 
      } else{
        alert("something went wrong in  db.. ")
        return 
      }
    },
    error: function(err) {
      alert("something went wrong")
    }
  })
}