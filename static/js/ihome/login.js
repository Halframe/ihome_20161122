function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });
    $(".form-login").submit(function(e){
        e.preventDefault();
        mobile = $("#mobile").val();
        password = $("#password").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写手机号！");
            $("#mobile-err").show();
            return;
        };
        if (!password) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        };

        var req_data = {
            mobile: mobile,
            password: passwd,
        };
        $.ajax({
            url: "api/Login", 
            type: "post", 
            data: JSON.stringify(req_data),
            contentType: 'application/json',
            dataType: 'json',
            success: function (data) {
                
            }


        });
    });
})