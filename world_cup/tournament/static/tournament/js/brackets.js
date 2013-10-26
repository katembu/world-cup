$(document).ready(function(){
    $(".country").on("click", function(){
        var row = $(this);
        var table = row.parents("table");
        if (row.hasClass("success")) {
            $.ajax({
                type: "POST",
                url: "save/",
                data: {'type': 'remove-group', 'country': row.data("country")},
                error: function(){
                    alert("There was an error and your choice was not saved.");
                },
                success: function(){
                    row.removeClass("success");
                    unlockTable(table);
                }
            });
        }
        else if (row.hasClass("warning")) {
            $.ajax({
                type: "POST",
                url: "save/",
                data: {'type': 'remove-group', 'country': row.data("country")},
                error: function(){
                    alert("There was an error and your choice was not saved.");
                },
                success: function(){
                    row.removeClass("warning");
                    unlockTable(table);
                }
            });
        }
        else{
            if (!tableLocked(table)) {
                if (table.find("tr").hasClass("success")) {
                    //Save Second Place
                    $.ajax({
                        type: "POST",
                        url: "save/",
                        data: {'type': 'add-group', 'country': row.data("country"), 'position':2},
                        error: function(){
                            alert("There was an error and your choice was not saved.");
                        },
                        success: function(){
                            row.addClass("warning");
                            lockTable(table);
                        }
                    });
                }
                else {
                    //Save First Place
                    $.ajax({
                        type: "POST",
                        url: "save/",
                        data: {'type': 'add-group', 'country': row.data("country"), 'position':1},
                        error: function(){
                            alert("There was an error and your choice was not saved.");
                        },
                        success: function(){
                            row.addClass("success");
                            lockTable(table);
                        }
                    });
                }
            }
        }
    });
});

function tableLocked(table){
    return (table.find("tr").hasClass("success") && table.find("tr").hasClass("warning"));
}

function lockTable(table) {
    if (table.find("tr").hasClass("success") && table.find("tr").hasClass("warning")) {
        table.find("tr").each(function(){
            if (!$(this).hasClass("success") || !$(this).hasClass("warning")) {
                $(this).toggleClass("active");
            }
        });
    }
}

function unlockTable(table) {
    table.find("tr").each(function(){
        $(this).removeClass("active");
    });
}