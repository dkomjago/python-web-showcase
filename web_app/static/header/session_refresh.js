const interval = 290000;  // milliseconds
$(document).ready(doAjax());
function doAjax(){
    $.ajax({
        type: 'GET',
        url: '/session',
        complete: function () {
            setTimeout(doAjax, interval);
        }
    });
}