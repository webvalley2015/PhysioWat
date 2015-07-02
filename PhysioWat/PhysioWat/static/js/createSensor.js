/**
 * Created by federico on 02/07/15.
 */

function getValue() {
    var e = document.getElementById("id_Sensors");
    var boxNumb = e.value - 1;
    for (var c = 0; c <= boxNumb; c++) {
        document.getElementById("coupIn" + c).style.display = 'block';
    }
    for (var c = boxNumb + 1; c <= 25; c++) {
        document.getElementById("coupIn" + c).style.display = 'none';
    }
}