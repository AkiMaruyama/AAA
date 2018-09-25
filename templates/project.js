/*
	IFB398 Project for Tanda:
	1. Tom Dowling n8312303
	2. Sarah Deriche n9683542
	3. Jinhao Li 
	4. Aki Maruyama n9534041
*/

window.onload = function() {

    //Check File API support
    if (window.File && window.FileList && window.FileReader) {
        var filesInput = document.getElementById("files");

        filesInput.addEventListener("change", function(event) {

            var files = event.target.files; //FileList object
            var output = document.getElementById("result");

            for (var i = 0; i < files.length; i++) {
                var file = files[i];

                //Only plain text
                if (!file.type.match('plain')) continue;

                var picReader = new FileReader();

                picReader.addEventListener("load", function(event) {

                    var textFile = event.target;

                    var div = document.createElement("div");

                    div.innerText = textFile.result;

                    output.insertBefore(div, null);

                });

                //Read the text file
                picReader.readAsText(file);
            }

        });
    }
    else {
        console.log("Your browser does not support File API");
    }
}