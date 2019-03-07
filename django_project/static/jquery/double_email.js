jQuery(document).ready(function() {
        $('#id_email').keyup(function() {
        $('#id_username').val($(this).val());
    });
});