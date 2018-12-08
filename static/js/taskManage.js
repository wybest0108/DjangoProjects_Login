//删除指定的id的任务
function deleteTask(name, id){
    deleteConfirmDialog(name, "/interface/delete_task/" + id + "/");
}

//从后台获取数据，初始化“可选用例树”和“已选用例树”
function initZTree() {
    $.ajax({
        type: "get",
        url: "/interface/get_cases_for_ztree/",
        dataType: "json",
        success: function(data) {
            if(data.success == "true") {
                initZTreeOfAllCases(data.data.ztreeNodesForAllCases);
                initZTreeOfSelectedCases(data.data.ztreeNodesForSelectedCases);
            }
            else {
                showTips(data.message);
            }
        }
    });
}

//初始化“可选用例树”
function initZTreeOfAllCases(zNodes) {
    var setting = {
        view: {
            selectedMulti: true,
            showIcon: false
        },
        data: {
            simpleData: {
                enable: true,
                idKey: "zId",
                pidKey: "pId"
            }
        },
        callback: {
            onCheck: onCheckForZTreeOfAllCases
        },
        check: {
            enable: true,
            chkboxType: { "Y": "ps", "N": "ps" }
        }
    };

    $.fn.zTree.init($("#ztree_all_cases"), setting, zNodes);
}

//初始化“已选用例树”
function initZTreeOfSelectedCases(zNodes) {
    var setting = {
        view: {
            selectedMulti: true,
            showIcon: false
        },
        data: {
            simpleData: {
                enable: true,
                idKey: "zId",
                pidKey: "pId"
            }
        },
        callback: {
            onCheck: onCheckForZTreeOfSelectedCases
        },
        check: {
            enable: true,
            chkboxType: { "Y": "ps", "N": "ps" }
        }
    };
    $.fn.zTree.init($("#ztree_selected_cases"), setting, zNodes);
}

//定义“可选用例树”勾选/取消勾选事件
//勾选“可选用例树”上节点时，将对应节点添加到“已选用例树”上；取消勾选“可选用例树”上节点时，将“已选用例树”上对应的节点移除
function onCheckForZTreeOfAllCases(e, treeId, treeNode) {
    var zTreeObjOfSelectedCases = $.fn.zTree.getZTreeObj("ztree_selected_cases"),
        level = treeNode.level,
        rootNode = zTreeObjOfSelectedCases.getNodeByParam("UID", "0_0_0", null);

    if(treeNode.checked) {
        switch (level) {
            case 0:
                zTreeObjOfSelectedCases.removeChildNodes(rootNode);
                zTreeObjOfSelectedCases.addNodes(rootNode, treeNode.children);
                break;
            case 1:
                var targetProjectNode = zTreeObjOfSelectedCases.getNodeByParam("UID", treeNode.UID, null);
                if(!!targetProjectNode) {
                    zTreeObjOfSelectedCases.removeNode(targetProjectNode);
                }
                zTreeObjOfSelectedCases.addNodes(rootNode, treeNode);
                break;
            case 2:
                var srcProjectNode = treeNode.getParentNode();
                var targetProjectNode = zTreeObjOfSelectedCases.getNodeByParam("UID", srcProjectNode.UID, null),
                    targetModuleNode = zTreeObjOfSelectedCases.getNodeByParam("UID", treeNode.UID, null);
                if(!!targetModuleNode) {
                    zTreeObjOfSelectedCases.removeNode(targetModuleNode);
                }
                if(!targetProjectNode) {
                    targetProjectNode = zTreeObjOfSelectedCases.addNodes(rootNode, {zId: srcProjectNode.zId, pId: srcProjectNode.pId, name: srcProjectNode.name, checked: true, UID: srcProjectNode.UID })[0];
                }
                zTreeObjOfSelectedCases.addNodes(targetProjectNode, treeNode);
                break;
            case 3:
                var srcModuleNode = treeNode.getParentNode(),
                    srcProjectNode = srcModuleNode.getParentNode();

                var targetProjectNode = zTreeObjOfSelectedCases.getNodeByParam("UID", srcProjectNode.UID, null),
                    targetModuleNode = zTreeObjOfSelectedCases.getNodeByParam("UID", srcModuleNode.UID, null);

                if(!targetProjectNode) {
                    targetProjectNode = zTreeObjOfSelectedCases.addNodes(rootNode, {zId: srcProjectNode.zId, pId: srcProjectNode.pId, name: srcProjectNode.name, checked: true, UID: srcProjectNode.UID })[0];
                }
                if(!targetModuleNode) {
                    targetModuleNode = zTreeObjOfSelectedCases.addNodes(targetProjectNode, {zId: srcModuleNode.zId, pId: srcModuleNode.pId, name: srcModuleNode.name, checked: true, UID: srcModuleNode.UID })[0];
                }
                zTreeObjOfSelectedCases.addNodes(targetModuleNode, treeNode);
                break;
        }
        zTreeObjOfSelectedCases.checkNode(rootNode, true, false);
    }
    else {
        removeNodes(zTreeObjOfSelectedCases, zTreeObjOfSelectedCases.getNodeByParam("UID", treeNode.UID, null));
    }
}

//定义“已选用例树”勾选/取消勾选事件
function onCheckForZTreeOfSelectedCases(e, treeId, treeNode) {
    var zTreeObjOfSelectedCases = $.fn.zTree.getZTreeObj("ztree_selected_cases"),
        zTreeObjOfAllCases = $.fn.zTree.getZTreeObj("ztree_all_cases");
    if(!treeNode.checked) {
        zTreeObjOfAllCases.checkNode(zTreeObjOfAllCases.getNodeByParam("UID", treeNode.UID, null), false, true);
        removeNodes(zTreeObjOfSelectedCases, treeNode);
    }
}

//删除节点，如果其父节点不再有子节点，则删除其父节点；依次类推，直至到根节点
function removeNodes(zTreeObj, node) {
    if(node.level === 0) {
        zTreeObj.removeChildNodes(node);
        zTreeObj.checkNode(node, false, true);
        return;
    }
    var parentNode = node.getParentNode();
    zTreeObj.removeNode(node);
    if(parentNode.children.length === 0) {
        removeNodes(zTreeObj, parentNode);
    }
    else {
        return;
    }
}


function saveTask(type, id) {
    var name = $("#task_name").val();
    if(name === "") {
        $("#error-tip").text("任务名称不能为空").show();
        return;
    }

    var taskData = {
        "name": name,
        "description": $("#task_description").val(),
        "caseIds": ""
    };

    var zTreeObjOfSelectedCases = $.fn.zTree.getZTreeObj("ztree_selected_cases"),
        checkedNodes = zTreeObjOfSelectedCases.getCheckedNodes();
    for(var i = 0, len = checkedNodes.length; i < len; ++i) {
        if(!checkedNodes[i].isParent) {
            taskData.caseIds += (checkedNodes[i].caseId + ",");
        }
    }
    taskData.caseIds = (taskData.caseIds === "")? taskData.caseIds : taskData.caseIds.substring(0, taskData.caseIds.length -1); //删除最后一个“，”
    $("#error-tip").text("").hide();

    $.ajax({
        type: "post",
        url: type == "update"? "/interface/update_task/" + id + "/" : "/interface/save_task/",
        data: taskData,
        async:false,        //IE浏览器必须设为false，否则会报错
        success: function(data) {
            showTips(data.message);
        }
    });
}


function getTestTaskInfoById(id) {
    $.ajax({
        type: "get",
        url: "/interface/get_task_info/" + id + "/",
        dataType: "json",
        success: function(data) {
            (data.success == "true")? initTestTask(data.data) : showTips(data.message);
        }
    });
}


function initTestTask(data) {
    $("#task_name").val(data.name);
    $("#task_description").val(data.description);

    initZTreeOfAllCases(data.ztreeNodesForAllCases);
    initZTreeOfSelectedCases(data.ztreeNodesForSelectedCases);

    //解决初始化半勾选问题
    var zTreeObjOfAllCases = $.fn.zTree.getZTreeObj("ztree_all_cases"),
        checkNodes = zTreeObjOfAllCases.getCheckedNodes(true);
    for(var i = 0, len = checkNodes.length; i < len; ++i) {
        zTreeObjOfAllCases.checkNode(checkNodes[i], true, true);
    }

    if(data.ztreeNodesForSelectedCases.length >1 ) {
        var zTreeObjOfSelectedCases = $.fn.zTree.getZTreeObj("ztree_selected_cases");
        zTreeObjOfSelectedCases.checkNode(zTreeObjOfSelectedCases.getNodeByParam("UID", "0_0_0", null), true, true);
    }
}