// Max. Length display component
const maxLength = document.getElementById('message').getAttribute('maxlength');

//Adjust in accordance with length of text in textfield
$('textarea').bind('input', function() {
    let length = $(this).val().length;
    length = maxLength-length;
    $('#chars').text(length);
});