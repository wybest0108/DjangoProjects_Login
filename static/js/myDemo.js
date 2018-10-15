function deleteProject(name, id){
    $("#delete-target").text(name);
    $("#dialog-confirm-delete").dialog({
        autoOpen: true,
        modal: true,
        resizable: false,
        width: 350,
        height: 200,
        title: "确认删除",
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
                window.location.href="/manage/delete_project/" + id + "/";
                $(this).dialog("close");
            },
            '取消':function(){
                $(this).dialog("close");
            }
        }
    });

}

function createProject() {
    resetProjectForm();
    $( "#dialog-form-project" ).dialog({
        autoOpen: true,
        modal: true,
        resizable: false,
        width: 400,
        height: 300,
        title: "新建项目",
        position: {
            using: function (pos) {
                var topOffset = $(this).css(pos).offset().top;
                if (topOffset = 0||topOffset>0) {
                    $(this).css('top', ($(window).height() - 300) / 2);
                }
            }
        },
        buttons: {
            "提交": function() {
                var projectName = $("#name").val(),
                    isValid = isProjectNameValid(projectName);
                if(isValid) {
                    $("#error-tip").hide();
                    var form = $("#form-project");
                    form.attr("action", "/manage/add_project/");
                    form.submit();
                    $( this ).dialog( "close" );
                }
                else {
                    $("#error-tip").show();
                }
            },
            取消: function() {
                $( this ).dialog( "close" );
            }
        }
    });
}

function resetProjectForm() {
    $("#name").val("");
    $("#description").val("");
    $("#error-tip").hide();
    $("#status").prop("checked", true);
}

function isProjectNameValid(projectName) {
    var errorTipElem = $("#error-tip");
    if(projectName === ""){
        errorTipElem.text("项目名称不能为空");
        return false;
    }
    else if(projectName.length > 100){
        errorTipElem.text("项目名称长度不能大于100!");
        return false;
    }
    return true;
}


function editProject(id){
    $.ajax({
        type: "get",
        url: "/manage/edit_project/" + id + "/",
        dataType: "json",
        success: function(data) {
            showProjectInfo(data, id);
        }
    });
}


function showProjectInfo(data, id) {
    var projectInfo = eval(data);
    $("#name").val(projectInfo.name);
    $("#description").val(projectInfo.description);
    $("#error-tip").hide();
    $("#status").prop("checked", projectInfo.status);

    $( "#dialog-form-project" ).dialog({
        autoOpen: true,
        modal: true,
        resizable: false,
        width: 400,
        height: 300,
        title: "编辑项目",
        position: {
            using: function (pos) {
                var topOffset = $(this).css(pos).offset().top;
                if (topOffset = 0||topOffset>0) {
                    $(this).css('top', ($(window).height() - 300) / 2);
                }
            }
        },
        buttons: {
            "保存": function() {
                var projectName = $("#name").val(),
                    isValid = isProjectNameValid(projectName);
                if(isValid) {
                    $("#error-tip").hide();
                    var form = $("#form-project");
                    form.attr("action", "/manage/edit_project_save/" + id + "/");
                    form.submit();
                    $( this ).dialog( "close" );
                }
                else {
                    $("#error-tip").show();
                }
            },
            取消: function() {
                $( this ).dialog( "close" );
            }
        }
    });
}
