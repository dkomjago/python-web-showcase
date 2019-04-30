const maxLength = document.getElementById('message').getAttribute('maxlength');
$('textarea').bind('input', function() {
    let length = $(this).val().length;
    length = maxLength-length;
    $('#chars').text(length);
});