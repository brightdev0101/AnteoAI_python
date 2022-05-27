var menu_status = false;

$(document).on('click', '#nav_menu_button', function (e) {
    if(menu_status){
        $('#nav_collaps_menu').toggleClass('hidden visible');
        menu_status = false;
    }else{
        $('#nav_collaps_menu').toggleClass('visible hidden')
        menu_status = true;
    }
});

// Manage go to top button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    if (document.body.scrollTop > 500 || document.documentElement.scrollTop > 500) {
        $("#go-top").show();
    } else {
        $("#go-top").hide();
    }
}

function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}


/* A function to arrange the navbar according the page.

Available pages:
    home
    form
    hiw (HowItWorks)
    trends
    custom
    account
*/
function arrangeNavbar(page){
    if(logged){
        $('#nav_menu_account').toggleClass('hidden visible');
        $('#nav_menu_login').toggleClass('visible hidden');
        $('#nav_menu_custom').toggleClass('hidden visible');
        
        $('#nav_collaps_account').toggleClass('hidden visible');
        $('#nav_collaps_login').toggleClass('visible hidden');
        $('#nav_collaps_custom').toggleClass('hidden visible');
    };
    
    switch (page) {
        case 'form':
            break;
        case 'hiw':
            break;
        case 'trends':
            break;
        case 'custom':
            break;
        case 'account':
            break;
    }
};

