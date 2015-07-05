
$(document).ready(function()  {

var usr_form_input = document.getElementById("id_username");

    if (usr_form_input !== null) {
        usr_form_input.setAttribute("placeholder","Username*");
	usr_form_input.setAttribute("width","100%");
	}

});


$(document).ready(function()  {

var pass_form_input = document.getElementById("id_password");

    if (pass_form_input !== null) {
        pass_form_input.setAttribute("placeholder","Password*");
    }


});



$(document).ready(function()  {

var pass_form_input = document.getElementById("id_device");

    if (pass_form_input !== null) {
        pass_form_input.setAttribute("style","display:none");
    }


});


$(document).ready(function()  {

var pass_form_input = document.getElementById("id_description");

    if (pass_form_input !== null) {
        pass_form_input.setAttribute("style","display:none");
    }


});




$(document).ready(function()  {

var pass_form_input = document.getElementById("id_password");

    if (pass_form_input !== null) {
        pass_form_input.setAttribute("style","display:none");
    }


});



$(document).ready(function()  {

var pass_form_input = document.getElementById("BuSu");

    if (pass_form_input !== null) {
        pass_form_input.setAttribute("style","display:none");
    }


});


$(document).ready(function()  {

var pass_form_input = document.getElementById("BuRe");

    if (pass_form_input !== null) {
        pass_form_input.setAttribute("style","display:none");
    }


});
/*
$(document).ready(function()  {

var usr_form_input = document.getElementById("id_username");

    if (usr_form_input !== null) {
        usr_form_input.setAttribute("placeholder","Username*");
	usr_form_input.setAttribute("width","100%");
	}

});
*/

function show_hide_upload(passage){
	if(passage==0){
		document.getElementById("sel").style.display = 'block';
		document.getElementById("dropzone-previews").style.display = 'block';
		document.getElementById("Experiment_schifo").style.display = 'block';
	} else{
		document.getElementById("dropzone-previews").style.display = 'none';
		document.getElementById("sel").style.display = 'none';
		document.getElementById("Experiment_schifo").style.display = 'none';
	}
	if(passage==1){
		document.getElementById("id_description").style.display = 'block';
		document.getElementById("id_device").style.display = 'block';
	} else {
		document.getElementById("id_description").style.display = 'none';
		document.getElementById("id_device").style.display = 'none';
	}
	if(passage==2){
		document.getElementById("id_password").style.display = 'block';
		document.getElementById("BuSu").style.display = 'block';
		document.getElementById("BuRe").style.display = 'block';
		document.getElementById("button1").style.display = 'none';
	}else{
		document.getElementById("id_password").style.display = 'none';
		document.getElementById("BuSu").style.display = 'none';
		document.getElementById("BuRe").style.display = 'none';
		document.getElementById("button1").style.display = 'block';
	}
}

passage=0
function increase_passage(){
	passage +=1
	show_hide_upload(passage)
}

