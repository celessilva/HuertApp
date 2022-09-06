$(document).ready(function(){
    // function ajax_login(){
    //     $.ajax({
    //         url:'/ajax-login',
    //         data: $('form').serialize(),
    //         type: 'POST',
    //         success: function(res){
    //             console.log(res);
    //         },
    //         error: function(e){
    //             console.log(e);
    //         },
    //     });
    // };
    // $('#login-form').submit(function(event){
    //     event.preventDefault();
    //     ajax_login();
    // })
    setTimeout(function() {
        $(".alert").not('section[name="banner"]').fadeOut(800);
    }, 15000); // <-- time in milliseconds

});