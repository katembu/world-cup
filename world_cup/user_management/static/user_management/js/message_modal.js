$(document).ready(function(){
    localStorage.clear();
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
    
    $('#id_to').typeahead({                              
        name: 'user-list',                                                        
        prefetch: '/userlist/',                                             
        template: [
            '<p><img src="{{image}}" width="25"/> {{value}}</p>',
        ].join(''),                                                                 
        engine: Hogan                                                               
    });
});