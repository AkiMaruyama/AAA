function toggleCheckbox(elem){
    var x = document.getElementById("myDIV");
    
    if (elem.checked) {
        x.style.display = "block";
        let elems = document.getElementsByClassName("form-control");
        for(let i=0;i<elems.length;i++){
          elems[i].required = true;
        }
    } else {
        x.style.display = "none";
        let elems = document.getElementsByClassName("form-control");
        for(let i=0;i<elems.length;i++){
          elems[i].required = false;
        }
    }
}

$(document).ready(function(){
    $('input:checkbox').prop('checked', false);
 }); 