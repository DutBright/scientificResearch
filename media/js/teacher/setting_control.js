$(document).ready(function(){
    if($("#alert-bar").length == 0){
        alert("alert-bar");
        if($("#id_name").val() && $("#id_card").val()) {
            $("#id_name").attr("readonly", "true");
            $("#id_card").attr("readonly", "true");
        }
    }
});