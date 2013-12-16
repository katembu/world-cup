$(document).ready(function(){
    $("#messageForm").on("submit", function(e){
        e.preventDefault();
        $.ajax({
               url: '/message/send/',
               type: 'POST',
               data: $(this).serialize(),
               error: function(data) {
                    alert("An error has occurred. Your message was not sent.");
               },
               success: function(data) {
                    if (data == 'Success') {
                        alert("Message sent.");
                        $("#messageModal").modal("toggle");
                        $("#messageModal").html("");
                    }
                    else {
                        alert("An error has occurred. Your message was not sent.");
                    }
               },
          });
     });
});