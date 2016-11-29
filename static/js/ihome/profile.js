function showSuccessMsg() {
    var $save_success = $('.save_success');
    $save_success.fadeIn('fast', function() {
        setTimeout(function(){
            $save_success.fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(function () {
    $.get("/api/profile", function (data) {
        if ("4101" == data.errno) {
            location.href = "/login.html";
        } else if ("0" == data.errno) {
            $("#user-name").val(data.data.name);
            if (data.data.avatar) {
                $("#user-avatar").attr("src", data.data.avatar);
            };
        };
    });

    //表单提交 
    $("#form-avatar").submit(function (e) {
        e.preventDefault();
        $(this).ajaxSubmit({
            url: "/api/profile/avatar",
            type: "POST",
            contentType: "application/json",
            headers: {
                "X-XSRFTOKEN": getCookie("_xsrf"),
            }

        });

    });


});