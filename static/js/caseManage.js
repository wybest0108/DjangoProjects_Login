function caseDebug() {
    var requestData = {
        "name": $("#req_name").val(),
        "url": $("#req_url").val(),
        "method": $("input[name='req_method']:checked").val(),
        "paramType": $("input[name='req_type']:checked").val(),
        "headers": $("#req_header").val() === ""? "{}" : $("#req_header").val(),
        "params": $("#req_parameter").val() === ""? "{}" : $("#req_parameter").val(),
    };

    if(!isRequestDataValid(requestData)) return false;

    $("#result").text("");
    $.ajax({
        type: "post",
        url: "/interface/api_debug/",
        data: requestData,
        async:false,        //IE浏览器必须设为false，否则会报错
        success: function(data) {
            //$("#result").html(data);
            $("#result").text(data);
        }
    });
}

function isRequestDataValid(requestData){
    var errorStr = "";
    errorStr += (requestData.url === "")? "请求的URL不能为空！\n" : "";
    //errorStr += (requestData.method === "")? "请求的方法不能为空！\n" : "";
    if(errorStr !== "") {
        //alert(errorStr);
        showErrorsInfo(errorStr);
        return false;
    }
    return true;
}

function showErrorsInfo(data){
    $("#dialog-error-tips").html(data);
    $("#dialog-error-tips").dialog({
        autoOpen: true,
        modal: true,
        resizable: false,
        width: 350,
        height: 200,
        title: "错误信息",
        position: {
            using: function (pos) {
                var topOffset = $(this).css(pos).offset().top;
                if (topOffset = 0||topOffset>0) {
                    $(this).css('top', ($(window).height() - 200) / 2);
                }
            }
        },
        buttons:{
            '确定':function(){
                 $(this).dialog("close");
            }
        }
    });
}

