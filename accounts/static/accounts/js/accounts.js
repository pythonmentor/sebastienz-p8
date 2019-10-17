$(function(){

    function resize_masthead() {
        var title = $(document).prop('title');
        if (title !== "Pur Beurre - Accueil") {
            $('.masthead').height($('form').height()+ $('.navbar').height()+ $('h1').height()+ $('footer').height());
        }
    }
    $(function() {
        $('#edit-toggle').bootstrapToggle({
            on: 'Activé',
            off: 'Désactivé'
        });
    });

    if ($('#edit-toggle').attr('checked')=== true){
        // $('#account .form-control').removeAttr('disabled');
        $('#account .form-control').attr('disabled', true);
    }
    else{
         $('#account .form-control').attr('disabled', true);
        //$('#account .form-control').removeAttr('disabled');
    }

    $(window).resize(function(){
        resize_masthead();
    });

    $(document).ready(function(){
        resize_masthead();
        //$('#account .form-control').attr('disabled', true);
    });

    $('#logout').on('click', function(){

    });



});
