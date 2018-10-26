function deleteModule(name, id){
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
                window.location.href="/manage/delete_module/" + id + "/";
                $(this).dialog("close");
            },
            '取消':function(){
                $(this).dialog("close");
            }
        }
    });

}
