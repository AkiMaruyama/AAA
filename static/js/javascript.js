function toggleCheckbox(){
    var x = document.getElementById("myDIV");
    
    if (x.style.display === "none") {
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