$(document).ready(function(){
     $(".reply-all").on("click", function(e){
          e.stopPropagation();
          $.ajax({
               type: "GET",
               url: "/message/form/",
               data: {"group": $(this).data("group")},
               error: function(){
                    alert("There was an error and we could not load the message.");
               },
               success: function(data){
                    $("#messageModal").html(data);
                    $("#messageModal").modal("toggle");
               }
          })
     });
     
     $(".reply").on("click", function(e){
          e.stopPropagation();
          $.ajax({
               type: "GET",
               url: "/message/form/",
               data: {"message": $(this).data("message")},
               error: function(){
                    alert("There was an error and we could not load the message.");
               },
               success: function(data){
                    $("#messageModal").html(data);
                    $("#messageModal").modal("toggle");
               }
          })
     });
     
     $(".new-message").on("click", function(e){
          e.stopPropagation();
          $.ajax({
               type: "GET",
               url: "/message/form/",
               data: {},
               error: function(){
                    alert("There was an error and we could not load the message.");
               },
               success: function(data){
                    $("#messageModal").html(data);
                    $("#messageModal").modal("toggle");
               }
          })
     });
     
     $(".delete-message").on("click", function(e){
          e.stopPropagation();
          $.ajax({
               type: "POST",
               url: "/message/delete/",
               data: {"message": $(this).data("message")},
               error: function(){
                    alert("There was an error and we could not load the message.");
               },
               success: function(data){
                    location.reload();
               }
          })
     });
});

$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                 }
             }
         }
         return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});