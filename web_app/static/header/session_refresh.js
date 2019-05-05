const interval = 290000;  // milliseconds
$(document).ready(doAjax());
//Refresh session every interval
function doAjax(){
    $.ajax({
        type: 'GET',
        url: '/session',
        complete: function () {
            setTimeout(doAjax, interval);
        }
    });
}