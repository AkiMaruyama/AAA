function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            document.getElementById('blah').setAttribute("src", e.target.result);
            // $('blah')
            //     .attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}

// $(document).ready(function(){
//     $("#rowClick > tr").click(function(){
//         $(this).toggleClass("active");
//     });
// });

$(document).ready(function () {
    $('tr').click(function () {
        //Check to see if background color is set or if it's set to white.
        if(this.style.background == "" || this.style.background =="white") {
            $(this).css('background', '#3fafd7');
        }
        else {
            $(this).css('background', 'white');
        }
    });
});