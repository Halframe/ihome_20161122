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
            $("#user-name").prop("placeholder", data.data.name);
            if (data.data.avatar) {
                $("#user-avatar").attr("src", data.data.avatar);
            };
        };
    });

    //上传头像 
    $("#form-avatar").submit(function (e) {
        e.preventDefault();
        var $uploading = $('.uploading');
        $uploading.fadeIn('fast');
        $(this).ajaxSubmit({
            url: "/api/profile/avatar",
            type: "POST",
            contentType: "application/json",
            headers: {
                "X-XSRFTOKEN": getCookie("_xsrf"),
            },
            dataType: "json",
            success: function (data) {
                if ("4101" == data.errno) {
                    location.href = "/login.html";
                } else if ("0" == data.errno) {
                    $uploading.fadeOut('fast');
                    $("#user-avatar").attr("src", data.avatar);
                };
            },
        });
    });

    // 修改用户名
    $("#form-name").submit(function (e) {
        e.preventDefault();
        var $user_name = $(this).children("#user-name");
        var $error_msg = $(this).next(".error-msg");
        $.ajax({
            url: "/api/profile/name",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({"user_name": $user_name.val()}),
            headers: {
                "X-XSRFTOKEN": getCookie("_xsrf"),
            },
            dataType: "json",
            success: function (data) {
                if ("0" == data.errno) {
                    $error_msg.hide();
                    showSuccessMsg();
                    $user_name.val("").attr("placeholder", data.new_username);
                } else if ("4001" == data.errno) {
                    $error_msg.show();
                } else if ("4101" == data.errno) {
                    location.href = "/login.html";
                };
            }
        });
    });
});