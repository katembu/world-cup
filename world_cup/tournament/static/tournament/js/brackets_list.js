$(document).ready(function(){
/**
 * Created by idfl on 1/27/14.
 */
    $(".delete-bracket").on("click", function(e){
        e.stopPropagation();
        if (confirm("This will delete this bracket and remove it from any groups it is associated with.  Continue?")){
            $.ajax({
                type: "POST",
                url: "/tournament/delete/",
                data: {"bracket":$("#bracket-name").text()},
                error: function(){
                    alert("There was an error and your bracket was not deleted.");
                },
                success: function(){
                    window.location.href = '/tournament/brackets/';
                }
            })
        }
    })
})