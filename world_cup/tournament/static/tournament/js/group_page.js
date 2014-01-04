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
    
    $("#leave").on("click", function(){
        if (confirm("You are about to leave this group.  If you are the last to leave the group will be deleted.")) {
            $.ajax({
                type: "POST",
                url: "/tournament/leavegroup/",
                data: {"group":$(this).data("group"), },
                error: function(){
                    alert("There was an error and you did not leave the group.");
                },
                success: function(){
                    window.location = "/tournament/groups/";
                }
            })
        }
    });
    
    $('#inviteInput').keydown(function (e){
        if ($("#emailFormGroup").hasClass("has-error")) {
            $("#emailFormGroup").removeClass("has-error");
        }
        if(e.keyCode == 13){
            e.preventDefault();
            var email_check = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,6}$/i;
            if (email_check.test($("#inviteInput").val())){
                $("#inviteList").append("<li><input type='hidden' name='invites[]' value='" + $("#inviteInput").val() + "'>" + $("#inviteInput").val() + "</li>");
                $("#inviteInput").val("");
            }
            else{
                $("#emailFormGroup").addClass("has-error");
            }
        }
    });
    
    $("#add").on("click", function(){
        var email_check = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,6}$/i;
        if (email_check.test($("#inviteInput").val())){
            $("#inviteList").append("<li><input type='hidden' name='invites[]' value='" + $("#inviteInput").val() + "'>" + $("#inviteInput").val() + "</li>");
            $("#inviteInput").val("");
        }
        else{
            $("#emailFormGroup").addClass("has-error");
        }
    });
    
    $("#inviteForm").on("submit", function(e){
        e.preventDefault();
        $.ajax({
            url: '/tournament/invite/' + $("#groupName").text() + '/',
            type: 'POST',
            data: $(this).serialize(),
            error: function(data) {
                alert("An error has occurred. Your message was not sent.");
            },
            success: function(data) {
                if (data == 'Success') {
                    alert("Message sent.");
                    $("#inviteModal").modal("toggle");
                    $("#inviteForm").find("ul").html("");
                }
                else {
                    alert("An error has occurred. Your message was not sent.");
                }
            },
        });
    });
});