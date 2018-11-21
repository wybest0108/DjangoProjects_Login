function initDropDownMenu(defaultProjectName, defaultModuleName) {
    $.ajax({
        type: "get",
        url: "/interface/get_projects_and_modules/",
        dataType: "json",
        success: function(data) {
            if(data.success == "true") {
                createProjectDropDownMenu(data.data.projects, defaultProjectName);
                updateModuleDropDownMenu(defaultModuleName);
            }
            else {
                showTips(data.message);
            }
        }
    });

    $("#project_dropDownMenu").change(function () {
        updateModuleDropDownMenu();
    });
}

function createProjectDropDownMenu(projects, defaultProjectName) {
    var projectDropDownMenu = $("#project_dropDownMenu")[0];

    projectDropDownMenu.options.length = 0;
    projectDropDownMenu.options.add(new Option("--请选择--", "请选择"));
    for(var i = 0, len = projects.length; i < len; ++i) {
        var option = new Option(projects[i].projectName, projects[i].projectName);
        projectDropDownMenu.options.add(option);
        option.moduleNames = typeof(projects[i].moduleNames) == "undefined"? [] : projects[i].moduleNames;
    }
    if(typeof(defaultProjectName) != "undefined") {
        setDropDownMenuDefault(projectDropDownMenu, defaultProjectName);
    }
}

function updateModuleDropDownMenu(defaultModuleName) {
    var projectDropDownMenu = $("#project_dropDownMenu")[0],
        moduleDropDownMenu = $("#module_dropDownMenu")[0],
        selectedIndex = projectDropDownMenu.selectedIndex;

    moduleDropDownMenu.options.length = 0;
    moduleDropDownMenu.options.add(new Option("--请选择--", "请选择"));

    if(selectedIndex == 0 ) return;
    var moduleNames = projectDropDownMenu.options[selectedIndex].moduleNames;
    for(var i = 0, len = moduleNames.length; i < len; ++i) {
        moduleDropDownMenu.options.add(new Option(moduleNames[i], moduleNames[i]));
    }

    if(typeof(defaultModuleName) != "undefined") {
        setDropDownMenuDefault(moduleDropDownMenu, defaultModuleName);
    }
}

function setDropDownMenuDefault(dropDownMenuObj, defaultValue) {
    for(var i = 0, len = dropDownMenuObj.options.length; i < len; ++i) {
        if(dropDownMenuObj.options[i].value == defaultValue) {
            dropDownMenuObj.selectedIndex = i;
        }
    }
}

function debugCase() {
    var requestData = {
        "url": $("#req_url").val(),
        "method": $("input[name='req_method']:checked").val(),
        "paramType": $("input[name='req_type']:checked").val(),
        "headers": $("#req_header").val() === ""? "{}" : $("#req_header").val(),
        "params": $("#req_parameter").val() === ""? "{}" : $("#req_parameter").val()
    };

    if(!isRequestDataValid(requestData)) return false;

    $("#result").text("");
    $.ajax({
        type: "post",
        url: "/interface/debug_case/",
        data: requestData,
        async:false,        //IE浏览器必须设为false，否则会报错
        success: function(data) {
            //$("#result").html(data.data);
            data.success == "true"? $("#result").text(data.data) : showTips(data.message);
        }
    });
}


function saveCase(type, id) {
    var requestData = {
        "name": $("#req_name").val(),
        "url": $("#req_url").val(),
        "method": $("input[name='req_method']:checked").val(),
        "paramType": $("input[name='req_type']:checked").val(),
        "headers": $("#req_header").val() === ""? "{}" : $("#req_header").val(),
        "params": $("#req_parameter").val() === ""? "{}" : $("#req_parameter").val(),
        "moduleName": $("#module_dropDownMenu").val(),
        "assertText": $("#assert_text").val()
    };

    if(!isRequestDataValid(requestData, true)) return false;
    if(type == "update" && typeof(id) == "undefined")   showTips("没有指定用例ID");

    $.ajax({
        type: "post",
        url: type == "update"? "/interface/update_case/" + id + "/" : "/interface/save_case/",
        data: requestData,
        async:false,        //IE浏览器必须设为false，否则会报错
        success: function(data) {
            showTips(data.message);
        }
    });
}

function assertResult() {
    var responseResult = $("#result").val(),
        assertText = $("#assert_text").val();

    if(responseResult === "" || assertText === "") {
        showTips("验证数据或者响应结果不能为空！");
        return;
    }

    $.ajax({
        type: "post",
        url: "/interface/assert_result/",
        data: {
            "response_result": responseResult,
            "assert_text": assertText
        },
        async:false,        //IE浏览器必须设为false，否则会报错
        success: function(data) {
            showTips(data.message);
        }
    });
}


function deleteCase(name, id){
    deleteConfirmDialog(name, "/interface/delete_case/" + id + "/");
}

function isRequestDataValid(requestData, isForSavingCase){
    var errorStr = "";
    var num = 1;
    errorStr += (requestData.url === "")? "<p>" + (num++) + ". 请求的URL不能为空！</p>" : "";

    //调试时用例名称和模块名称可以不填，但是保存时必须要填
    if(!!isForSavingCase){
        errorStr += requestData.name === ""? "<p>" + (num++) + ". 用例名称不能为空！</p>" : "";
        errorStr += requestData.moduleName === "请选择"? "<p>" + (num++) + ". 必须选择所属模块！</p>" : "";
    }

    if(errorStr !== "") {
        showTips(errorStr);
        return false;
    }
    return true;
}

function showTips(data){
    $("#dialog-tips").html(data);
    $("#dialog-tips").dialog({
        autoOpen: true,
        modal: true,
        resizable: false,
        width: 350,
        height: 220,
        title: "提示信息",
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

function getTestCaseInfoById(id) {
    $.ajax({
        type: "get",
        url: "/interface/get_case_info/" + id + "/",
        dataType: "json",
        success: function(data) {
            (data.success == "true")? initTestCase(data.data) : showTips(data.message);
        }
    });
}

function initTestCase(data) {
    $("#req_name").val(data.name);
    $("#req_url").val(data.url);
    $("#req_header").val((data.headers === "{}")? "" : data.headers);
    $("#req_parameter").val((data.params === "{}")? "" : data.params);
    $("#assert_text").val(data.assertText);

    data.method === "GET"? $("#get").prop("checked", true) : $("#post").prop("checked", true);
    data.paramsType === "JSON"? $("#json").prop("checked", true) : $("#form").prop("checked", true);

    initDropDownMenu(data.projectName, data.moduleName);
}


