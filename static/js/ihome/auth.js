function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000);
    });
}


function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(function () {

    var $real_name = $("#real-name"), $id_card = $("#id-card");

    $.get("/api/profile/auth", function (data) {
        if ("0" == data.errno) {
            $real_name.attr("placeholder", data.real_name);
            $id_card.attr("placeholder", data.id_card);
        } else if ("4101" == data.errno) {
            location.href = "/login.html";
        };
    });

    $("#form-auth").submit(function (e) {
        e.preventDefault();
        var req_data = {"real_name": $real_name.val(), "id_card": $id_card.val()};
        $.ajax({
            url: "/api/profile/auth",
            type: "POST",
            data: JSON.stringify(req_data),
            contentType: "application/json",
            headers: {
                "X-XSRFTOKEN": getCookie("_xsrf"),
            },
            dataType: "json",
            success: function (data) {
                if ("0" == data.errno) {
                    showSuccessMsg();
                    $real_name.val("").attr("placeholder", data.real_name);
                    $id_card.val("").attr("placeholder", data.id_card);
                } else if ("4101" == data.errno) {
                    location.href = "/login.html"
                };
            }
        });
    });
});

