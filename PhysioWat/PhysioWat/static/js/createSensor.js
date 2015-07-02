/**
 * Created by federico on 02/07/15.
 */

function getValue() {
    var e = document.getElementById("id_Sensors");
    var boxNumb = e.value - 1;
    for (var c = 0; c <= boxNumb; c++) {
        document.getElementById("nameIn" + c).style.display = 'block';
        document.getElementById("typeIn" + c).style.display = 'block';
    }
    for (var c = boxNumb + 1; c <= 25; c++) {
        document.getElementById("nameIn" + c).style.display = 'none';
        document.getElementById("typeIn" + c).style.display = 'none';
    }
}