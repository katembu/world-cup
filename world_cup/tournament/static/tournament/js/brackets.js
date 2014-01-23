$(document).ready(function(){
    $("#reset").on("click", function(){
        $.ajax({
            type: "POST",
            url: "/tournament/reset/",
            data: {"bracket":$("#bracket-name").text(), },
            error: function(){
                alert("There was an error and your choices were not reset.");
            },
            success: function(){
                location.reload();
            }
        })
    });
    
    // Check to see if knockout stage has enough info to be shown
    displayKnockout();
    
    $(".country").on("click", function(){
        var row = $(this);
        var table = row.parents("table");
        //Remove First Place
        if (row.hasClass("success")) {
            $.ajax({
                type: "POST",
                url: "/tournament/save/",
                data: {'bracket':$("#bracket-name").text(), 'type': 'remove-group', 'country': row.data("country")},
                error: function(){
                    alert("There was an error and your choice was not saved.");
                },
                success: function(data){
                    var ids = data[0];
                    for(var i = 0; i < ids.length; i++){
                        $("#" + ids[i]).removeClass("text-success");
                        $("#" + ids[i]).html('<div class="label label-default">' + $("#" + ids[i]).data("default") + '</div>');
                    }
                    row.removeClass("success").removeClass("bold");
                    row.find(".gold").addClass("hide");
                    unlockTable(table);
                    displayKnockout();
                }
            });
        }
        //Remove Second Place
        else if (row.hasClass("warning")) {
            $.ajax({
                type: "POST",
                url: "/tournament/save/",
                data: {'bracket':$("#bracket-name").text(), 'type': 'remove-group', 'country': row.data("country")},
                error: function(){
                    alert("There was an error and your choice was not saved.");
                },
                success: function(data){
                    var ids = data[0];
                    for(var i = 0; i < ids.length; i++){
                        $("#" + ids[i]).removeClass("text-success");
                        $("#" + ids[i]).html('<div class="label label-default">' + $("#" + ids[i]).data("default") + '</div>');
                    }
                    row.removeClass("warning").removeClass("bold");
                    row.find(".silver").addClass("hide");
                    unlockTable(table);
                    displayKnockout();
                }
            });
        }
        //Add First or Second Place
        else{
            if (!tableLocked(table)) {
                if (table.find("tr").hasClass("success")) {
                    //Save Second Place
                    $.ajax({
                        type: "POST",
                        url: "/tournament/save/",
                        data: {'bracket':$("#bracket-name").text(), 'type': 'add-group', 'country': row.data("country"), 'position':2},
                        error: function(){
                            alert("There was an error and your choice was not saved.");
                        },
                        success: function(data){
                            $("#" + data[0]).html('<div class="label label-default"> <img src="/static/img/blank.png" class="flag flag-' + data[2] + '"></img> ' + data[2] + '</div>');
                            $("#" + data[0]).data("country", data[1]);
                            row.addClass("warning").addClass("bold");
                            row.find(".silver").removeClass("hide");
                            lockTable(table);
                            displayKnockout();
                        }
                    });
                }
                else {
                    //Save First Place
                    $.ajax({
                        type: "POST",
                        url: "/tournament/save/",
                        data: {'bracket':$("#bracket-name").text(), 'type': 'add-group', 'country': row.data("country"), 'position':1},
                        error: function(){
                            alert("There was an error and your choice was not saved.");
                        },
                        success: function(data){
                            $("#" + data[0]).html('<div class="label label-default"> <img src="/static/img/blank.png" class="flag flag-' + data[2] + '"></img> ' + data[2] + '</div>');
                            $("#" + data[0]).data("country", data[1]);
                            row.addClass("success").addClass("bold");
                            row.find(".gold").removeClass("hide");
                            lockTable(table);
                            displayKnockout();
                        }
                    });
                }
            }
        }
    });
    
    $(".match").on("click", function(){
        if (!($(this).text().indexOf("Winner") > -1 || $(this).text().indexOf("Group") > -1)) {
            var match_number = $(this).attr("id").split("-")[0]
            var home_away = $(this).attr("id").split("-")[1]
            var row = $(this);
            $.ajax({
                type: "POST",
                url: "/tournament/save/",
                data:{'bracket':$("#bracket-name").text(), 'type': 'save-match', 'match_number': match_number, 'home_away': home_away},
                error: function(){
                    alert("There was an error and your choice was not saved.");
                },
                success: function(data){
                    var final_match = '';
                    if (match_number == "64") {
                        final_match = ' final-match';
                    }
                    if (!data[0]) {
                        data[0] = match_number + "-" + home_away;
                    }
                    $("#" + data[0]).html('<div class="label label-default' + final_match + '" data-name="' + data[2] + '"><img src="/static/img/blank.png" class="flag flag-' + data[2] + '"></img> ' + data[2] + '</div>');
                    $("#" + data[0]).data("country", data[1]);
                    if (data[0] == "65-home") {
                        $("#" + data[0]).addClass("label-success").addClass("winner");
                    }
                    row.children(".label").removeClass("label-default").addClass("label-success");
                    var match = row.attr("id").split("-")[0];
                    var homeAway = row.attr("id").split("-")[1];
                    if (homeAway == "home") {
                        homeAway = "away";
                    }
                    else if (homeAway == "away") {
                        homeAway = "home"
                    }
                    $("#" + match + "-" + homeAway).children(".label").removeClass("label-success").addClass("label-default");
                    // Displays the correct final winner
                    var country = "";
                    $(".final-match").each(function(){
                        if ($(this).hasClass('label-success')){
                            country = $(this).data("name");
                        }    
                    });
                    //if ($("#64-home").children(".label-success").length > 0) {
                    //    country = $("#64-home").data("name");
                    //} else if ($("#64-away").children(".label-success").length > 0) {
                    //    country = $("#64-away").data("name");
                    //}
                    if (!country) {
                        $(".winner").removeClass("label-success").addClass("label-default").html("Winner");
                    } else {
                        $(".winner").addClass("label-success").html('<img src="/static/img/blank.png" class="flag flag-' + country + '"></img> ' + country);    
                    }
                }
            });
        }
    });
});

function tableLocked(table){
    return (table.find("tr").hasClass("success") && table.find("tr").hasClass("warning"));
}

function lockTable(table) {
    if (table.find("tr").hasClass("success") && table.find("tr").hasClass("warning")) {
        table.find("tr").each(function(){
            if (!$(this).hasClass("success") && !$(this).hasClass("warning") && !$(this).hasClass("group-header")) {
                $(this).toggleClass("active").addClass("text-muted");
            }
        });
    }
}

function unlockTable(table) {
    table.find("tr").each(function(){
        $(this).removeClass("active").removeClass("text-muted");
    });
}

function displayKnockout() {
    if (($("#group-div .country.success").length == 16 && $("#group-div .country.warning").length == 16) || ($("#group-div .country.success").length == 8 && $("#group-div .country.warning").length == 8)) {
        $("#knockout-div").fadeIn(500);
        $(".knockout-hidden").fadeOut(500);
        $(".knockout-hidden").hide();
    }
    else if ($("#group-div .country.success").length == 0 && $("#group-div .country.warning").length == 0) {
        $("#knockout-div").fadeOut(500);
        $(".knockout-hidden").fadeIn(500);
    }
}