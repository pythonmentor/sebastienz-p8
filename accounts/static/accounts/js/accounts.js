$(function(){

    //************************** Resize masterhead ******************************************************************
    function resize_masthead() {
        var title = $(document).prop('title');
        if (title !== "Pur Beurre - Accueil") {
            $('.masthead').height($('form').height()+ $('.navbar').height()+ $('h1').height()+ $('footer').height());
        }
    }

    $(window).resize(function(){
        resize_masthead();
    });

    $(document).ready(function(){
        resize_masthead();
    });

    //****************** Toggle button for account edition mode ******************************************************
    $(function() {
        $('#edit-toggle').bootstrapToggle({
            on: 'Activé',
            off: 'Désactivé'
        });
    });
    //***************** Activate/Désactivate edition mode for account page *******************************************
    $('#edition').click(function () {
        console.log('cliqué');
        if ($('#edition .toggle').hasClass('off')) {
            console.log("ON");
            $('#account .form-control').attr('disabled', false);
            $('#save-btn').removeClass('d-none');
        } else {
            console.log("OFF");
            $('#account .form-control').attr('disabled', true);
            $('#save-btn').addClass('d-none');
        }
    });

});
