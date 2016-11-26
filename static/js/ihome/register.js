function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

var imageCodeId = "";

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}

function generateImageCode() {
    var preImageCodeId = imageCodeId;
    imageCodeId = generateUUID();
    $(".image-code img").attr("src", "/api/imagecode?pcodeid="+preImageCodeId+"&codeid="+imageCodeId);
}

function sendSMSCode() {
    $(".smscode-a").removeAttr("onclick");
    var mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".smscode-a").attr("onclick", "sendSMSCode();");
        return;
    } 
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".smscode-a").attr("onclick", "sendSMSCode();");
        return;
    }
    // 错误，传送的数据不是json格式
    // $.post("/api/smscode", {mobile:mobile, code:imageCode, codeId:imageCodeId}, 
    //     function(data){
    //         if (0 != data.errno) {
    //             $("#image-code-err span").html(data.errmsg); 
    //             $("#image-code-err").show();
    //             if (2 == data.errno || 3 == data.errno) {
    //                 generateImageCode();
    //             }
    //             $(".smscode-a").attr("onclick", "sendSMSCode();");
    //         }   
    //         else {
    //             var $time = $(".smscode-a");
    //             var duration = 60;
    //             var intervalid = setInterval(function(){
    //                 $time.html(duration + "秒"); 
    //                 if(duration === 1){
    //                     clearInterval(intervalid);
    //                     $time.html('获取验证码'); 
    //                     $(".smscode-a").attr("onclick", "sendSMSCode();");
    //                 }
    //                 duration = duration - 1;
    //             }, 1000, 60); 
    //         }
    // }, 'json'); 
    var req_data = {
        mobile:mobile, 
        image_code_text:imageCode, 
        image_code_id:imageCodeId,
    };
    $.ajax({
        url:"/api/smscode",
        type:"post",
        data: JSON.stringify(req_data),
        contentType:"application/json",
        dataType:"json",
        headers:{
            "X-XSRFTOKEN":getCookie("_xsrf"),
        },
        success:function (data) {
            if ("0" != data.errno) {
                $("#image-code-err span").html(data.errmsg); 
                $("#image-code-err").show();
                if ("4001" == data.errno || "4002" == data.errno || "4004" == data.errno) {
                    generateImageCode();
                }
                $(".smscode-a").attr("onclick", "sendSMSCode();");
            }   
            else {
                var $time = $(".smscode-a");
                var duration = 60;
                var intervalid = setInterval(function(){
                    $time.html(duration + "秒"); 
                    if(duration === 1){
                        clearInterval(intervalid);
                        $time.html('获取验证码'); 
                        $(".smscode-a").attr("onclick", "sendSMSCode();");
                    }
                    duration = duration - 1;
                }, 1000, 60); 
            }
        }
    });
}

$(document).ready(function() {
    generateImageCode();
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function(){
        $("#image-code-err").hide();
    });
    $("#smscode").focus(function(){
        $("#sms-code-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });
    $(".form-register").submit(function(e){
        e.preventDefault();
        mobile = $("#mobile").val();
        SMSCode = $("#smscode").val();
        password = $("#password").val();
        password2 = $("#password2").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        } 
        if (!SMSCode) {
            $("#sms-code-err span").html("请填写短信验证码！");
            $("#sms-code-err").show();
            return;
        }
        if (!password) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
        if (password != password2) {
            $("#password2-err span").html("两次密码不一致!");
            $("#password2-err").show();
            return;
        }

        // var req_data = {
        //     mobile: mobile,
        //     SMSCode: SMSCode,
        //     password: password,
        // }
        var req_data = {};
        $(this).serializeArray().map(function(x){req_data[x.name] = x.value;});
        var json_data = JSON.stringify(req_data)
        $.ajax({
            url: "/api/register",
            type: "post", 
            data: json_data,
            contentType: "application/json", 
            dataType: "json", 
            headers: {
                "X-XSRFTOKEN":getCookie("_xsrf"),
            },
            success: function (data) {
                if ("4103" == data.errno || "4003" == data.errno) {
                    $("#mobile-err").show().children("span").html(data.errmsg);
                    return;
                } else if ("4001" == data.errno || "4002" == data.errno || "4004" == data.errno) {
                    $("#sms-code-err").show().children("span").html(data.errmsg);
                    return;
                } else if ("0" == data.errno) {
                    location.href = "/";
                };
            }
        });
    });
})