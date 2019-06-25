// функция получения csrf_token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// получение списка блогов
function get_blog_results(user='',offset=0,search='') {
    var csrf = getCookie('csrftoken'),
        data = {
            'offset' : offset,
            'csrfmiddlewaretoken' : csrf,
            'search': search,
        };
    $.ajax(
        {
            url : '/blog/getBlogs/'+(user?user+'/':''),
            type : 'POST',
            data : data,
            success: function (response) {
                if(response.trim()){
                    $('.blog-moar').parent().before(response);
                }
                else{
                    $('.blog-moar').parent().hide();
                }
                $('.section-found-article .article img').addClass('responsive-img');
            },
            error: function (xhr, status, error) {
                console.log('error =', error);
            }

        }
    )
}


function findGetParameter(parameterName) {
    var result = null,
        tmp = [];
    var items = location.search.substr(1).split("&");
    for (var index = 0; index < items.length; index++) {
        tmp = items[index].split("=");
        if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
    }
    return result;
}


$(document).ready(function () {

    var offset=0,
    user = $('.blog-moar').val();
    var search = findGetParameter('search');

    $('.blog-moar').click(function (e) {
        e.preventDefault();
        offset+=3;
        get_blog_results( user, offset, search );
    });


    $('.section-search-blog button').click(function (e) {
        e.preventDefault;
        var searchval = $('#autocomplete-input').val();
        if(searchval){
            window.location.href = location.protocol + '//' + location.host + location.pathname + '?search=' + searchval;
        }
    });

    $('#autocomplete-input').keypress(function (e) {
        var key = e.which;
        if(key == 13){
            $('.section-search-blog button').click();
            return false;  
        }
    });   

})