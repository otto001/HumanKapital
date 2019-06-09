$(document).ready(function(){
    $(".modal-close").each(function(index,element){
        $(element).on("click",function(event){
            $(element).closest(".modal").css("display","none");
            event.preventDefault();
            return false;
        });
    });
});