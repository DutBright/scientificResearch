if(!String.prototype.format) {
    String.prototype.format = function() {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function(match, number) {
            return typeof args[number] != 'undefined'
                ? args[number] : match;
        });
    };
}

var glob_path;

function clear_check_box(){
    $("input[type='checkbox']").each(function(){ 
        this.checked = false;
    });
}
$(document).ready(function(){
    $("#button_operator_cancel").hide(); 

    glob_path = window.location.pathname.split('/')[2];
});

$("#alloc_tab").click(function(){
    clear_check_box();
    $("#button_operator_cancel").toggle();
    $("#button_operator_alloc").toggle();
    //$("#id_div_expert").hide();

});
$("#unalloc_tab").click(function(){
    clear_check_box();
    $("#button_operator_cancel").hide(); 
    $("#button_operator_alloc").show();
    //$("#id_div_expert").show();
});


$(document).on("click", ".select_all", function(){
    var state = this.checked;
    target = "[name='{0}']".format($(this).attr("arg"));
    $(target).each(function(){
        this.checked = state;  
    });
});

var glob_project_college_id = "-1";
var glob_project_special_id = "-1";

$("#project_filter_button").click(function(){
    glob_project_college_id = $("#project_filter_form #id_colleges").val();
    glob_project_special_id = $("#project_filter_form #id_specials").val();
    Dajaxice.school.getProjectList(getProjectListCallback, {"college_id": glob_project_college_id, 
                                                            "special_id": glob_project_special_id,
                                                            "path": glob_path,});
});
function getProjectListCallback(data){
    $("#alloced-section").html(data.html_alloc);
    $("#unalloced-section").html(data.html_unalloc);
}


$(document).on("click", "#unalloc_paginator .item_page", function(){
    page = $(this).attr("arg");   
    Dajaxice.school.getUnallocProjectPagination(getUnallocCallback, {"page": page,
                                                                     "college_id": glob_project_college_id,
                                                                     "special_id": glob_project_special_id,
                                                                     "path": glob_path,}); 
});
function getUnallocCallback(data){
    $("#unalloced-section").html(data.html);
}

$(document).on("click", "#alloc_paginator .item_page", function(){
    page = $(this).attr("arg");   
    Dajaxice.school.getAllocProjectPagination(getAllocCallback, {"page": page,
                                                                 "college_id": glob_project_college_id,
                                                                 "special_id": glob_project_special_id,
                                                                 "path": glob_path,}); 

});
function getAllocCallback(data){
    $("#alloced-section").html(data.html);
}

var glob_expert_college_id = "-1";

$(document).on("click", "#alloc_expert_paginator .item_page", function(){
    page = $(this).attr("arg");
    Dajaxice.school.getAllocExpertPagination(getAllocExpertCallback, {"page": page,
                                                                      "id": glob_expert_college_id,
                                                                      "path": glob_path,});
});
function getAllocExpertCallback(data){
    $("#expert_list_div").html(data.html);
}

$("#expert_filter_button").click(function(){
    glob_expert_college_id = $("#expert_filter_form #id_colleges").val();
    Dajaxice.school.getExpertList(getExpertListCallback, {"id": glob_expert_college_id, 
                                                          "path": glob_path,});
});
function getExpertListCallback(data){
    $("#expert_list_div").html(data.html);
}

function refresh(){
    var page1 = $("#alloc_expert_paginator .disabled").val()
    var page2 = $("#alloc_paginator .disabled").val()
    var page3 = $("#unalloc_paginator .disabled").val()
    Dajaxice.school.getUnallocProjectPagination(getUnallocCallback, {"page": page3,
                                                                     "college_id": glob_project_college_id,
                                                                     "special_id": glob_project_special_id,
                                                                     "path": glob_path, }); 
    Dajaxice.school.getAllocProjectPagination(getAllocCallback, {"page": page2,
                                                                     "college_id": glob_project_college_id,
                                                                     "special_id": glob_project_special_id,
                                                                     "path": glob_path,}); 

    Dajaxice.school.getAllocExpertPagination(getAllocExpertCallback, {"page": page1,
                                                                      "id": glob_expert_college_id,
                                                                      "path": glob_path,});

}

$("#button_operator_alloc button").click(function(){
    var expert_list = []
    var project_list = []
    $("#expert_box tbody").find("tr").each(function(){
        expert_list.push($(this).attr("args"));   
    })
    $("input[name='checkbox_unalloc_project']:checkbox:checked").each(function(){ 
        project_list.push($(this).val());
    });
    Dajaxice.school.allocProjectToExpert(allocProjectToExpertCallback, {"project_list": project_list,
                                                                        "expert_list": expert_list,
                                                                        "path": glob_path,});
});

function allocProjectToExpertCallback(data){
    if(data.message == "ok"){
        refresh();
        alert("分配成功！");
    }
    else if(data.message == "no project"){
        alert("选中的项目集合为空！");
    }
    else{
        alert("选中的评审集合为空！");
    }
}


$("#button_operator_cancel button").click(function(){
    var project_list = []
    $("input[name='checkbox_alloc_project']:checkbox:checked").each(function(){ 
        project_list.push($(this).val());
    });
    Dajaxice.school.cancelProjectAlloc(cancelProjectAllocCallback, {"project_list": project_list,
                                                                    "path": glob_path,});
});
function cancelProjectAllocCallback(data){
    if(data.message == "ok"){
        refresh();
        alert("操作成功！");
    }
    else{
        alert("选中的项目集合为空！");
    }
}

$(document).on("click", ".query_info", function(){
    project_id = $(this).attr("arg");
    Dajaxice.school.queryAllocedExpert(queryAllocedExpertCallback, {"project_id": project_id, 
                                                                    "path": glob_path,});
});
function queryAllocedExpertCallback(data){
    $("#query_modal .modal-body").html(data.html);
}


$(document).on("click", ".append_alloc", function(){
    project_id = $(this).attr("arg");
    var expert_list = []
    $("#expert_box tbody").find("tr").each(function(){
        expert_list.push($(this).attr("args"));   
    })
    if(expert_list.length > 1){
        alert("选中的专家数量超过1！");
    }
    else{
        Dajaxice.school.appendAlloc(appendAllocCallBack, {"project_id": project_id,
                                                          "expert_list": expert_list,
                                                          "path": glob_path,});
    }
});

function appendAllocCallBack(data){
    if(data.message == "ok"){
        refresh();
        alert("操作成功！");
    }
    else if(data.message == "redundance"){
        alert("选中的专家已被该项目分配！");
    }
    else{
        alert("选中的专家数量不为1！");
    }
}

function exist(userid){
    var flag = false;
    $("#expert_box").find("tr").each(function(){
        if($(this).attr("args") == userid) flag = true;
    });
    return flag;
}
$(document).on("click", ".btn-addon", function(){
    var pr_row = $(this).parent().parent();
    var userid = pr_row.attr("args");
    if(exist(userid)){
        alert("该专家已经添加");       
    }
    else{
        var name = pr_row.find("td").eq(0).html();
        var school = pr_row.find("td").eq(1).html();
        new_tr_html = "<tr args='{0}'><td>{1}</td><td>{2}</td><td><button class='btn btn-primary btn-remove'>移除</button></td></tr>".format(userid, name, school);
        $("#expert_box").append(new_tr_html);
    }
});

$(document).on("click", ".btn-remove", function(){
    var pr_row = $(this).parent().parent();
    pr_row.remove();
});

$(document).on("click", ".btn-clear", function(){
    $("#expert_box tbody").find("tr").each(function(){
        $(this).remove();
    });
});

$("#expert_add_button").click(function(){
    var name = $("#expert_search_input").val();
    Dajaxice.school.searchExpert(searchCallBack, {"name": name, });    
});
function searchCallBack(data){
    if(data.message == "no expert exist"){
        alert("未查询到该专家存在");
    }
    else{
        $("#expert_box").append(data.html);
    }
}
