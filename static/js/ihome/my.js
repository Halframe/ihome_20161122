function logout() {
    $.get("/api/logout", function(data){
        if (0 == data.errno) {
            location.href = "/";
        }
    })
}

$(document).ready(function(){
    $.get("/api/profile", function (data) {
        if ("0" == data.errno) {
            $("#user-avatar").attr("src", data.data.avatar);
            $("#user-name").html(data.data.name);
            $("#user-mobile").html(data.data.mobile);
        } else if ("4101" == data.errno) {
            location.href = "/login.html";
        };
    }, "json");
})