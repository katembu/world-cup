$(document).ready(function(){
    $("#messageForm").on("submit", function(e){
        e.preventDefault();
        $.ajax({
            url: '/tournament/message/' + $("#groupName").text() + '/',
            type: 'POST',
            data: $(this).serialize(),
            error: function(data) {
                alert("An error has occurred. Your message was not sent.");
            },
            success: function(data) {
                if (data == 'Success') {
                    alert("Message sent.");
                    $("#messageModal").modal("toggle");
                    $("#messageForm").find("input[type=text], textarea").val("");
                }
                else {
                    alert("An error has occurred. Your message was not sent.");
                }
            },
        });
    });
    
});