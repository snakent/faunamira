/**
 * Created by Max on 10.08.2017.
 */

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

function get_animal_results(offset=0) {
    var kind = $('#pet #id_kind select').val(),
        breed = $('#pet #autocomplete-1').val(),
        gender = $('#pet #id_gender select').val(),
        age_from = $('#pet #id_age-from input').val(),
        age_before = $('#pet #id_age-before input').val(),
        status = $('#pet #id_status select').val(),
        city = $('#pet #autocomplete-2').val(),
        csrf = getCookie('csrftoken'),
        data = {
            'offset' : offset,
            'kind' : kind,
            'breed' : breed,
            'status' : status,
            'gender' : gender,
            'age' : age_from+(age_from || age_before)?'-':''+age_before,
            'city': city,
            'csrfmiddlewaretoken' : csrf
        };
    $.ajax(
        {
            url : 'animal_results/',
            type : 'POST',
            data : data,
            dataType: 'json',
            success: function (response) {
                $('#block_content').html(response.html_content);

                $('.moar').click(function (e) {
                    e.preventDefault();
                    if( $('.moar').attr('searchtype') == 'p'){
                        get_people_results( $('.moar').val() );
                    }
                    else{
                        get_animal_results( $('.moar').val() );
                    }
                });
            },
            error: function (xhr, status, error) {
                console.log('error =', error);
            }
        }
    )
}


// результаты фильтрации по людям
function get_people_results(offset=0) {
    var gender = $('#owner #id_wtf .initialized, #owner #id_wtf .browser-default').val(),
        age_from = $('#owner #id_age-from input').val(),
        age_before = $('#owner #id_age-before input').val(),
        city = $('#owner #autocomplete-0').val(),
        purpose = $('#owner #id_target .initialized, #owner #id_target .browser-default').val(),
        csrf = getCookie('csrftoken'),
        data = {
            'offset' : offset,
            'gender' : gender,
            'age' : age_from+(age_from || age_before)?'-':''+age_before,
            'city' : city,
            'purpose': purpose,
            'csrfmiddlewaretoken' : csrf
        };
    $.ajax(
        {
            url : 'people_results/',
            type : 'POST',
            data : data,
            dataType : 'json',
            success: function (response) {
                $('#block_content').html(response.html_content);

                $('.moar').click(function (e) {
                    e.preventDefault();
                    if( $('.moar').attr('searchtype') == 'p'){
                        get_people_results( $('.moar').val() );
                    }
                    else{
                        get_animal_results( $('.moar').val() );
                    }
                });
            },
            error: function (xhr, status, error) {
                console.log('error =', error);
            }

        }
    )
}

// remove options from selectbox
function removeOptions(selectbox){
    var i;
    for(i = selectbox.options.length - 1 ; i >= 0 ; i--)
    {
        selectbox.remove(i);
    }
}

function setAutocompleteBreeds(breed_data){
    $('#autocomplete-1').tinyAutocomplete({
        minChars:1,
        data: breed_data,
        showNoResults: true,
        noResultsTemplate: '<li class="autocomplete-item">Ничего не найдено по запросу "{{title}}"</li>',
        onSelect: function(el, val) {
            if(val == null) {
                $('.results').html('All results for "' + $(this).val() + '" would go here');
            }
            else {
                $(this).val( val.title );
            }
        }
    });
}

$(document).ready(function () {

    $('#owner #people_filter_button').click(function (e) {
        e.preventDefault();
        get_people_results(  );
    });

    $('#pet #animal_filter_button').click(function (e) {
        e.preventDefault();
        get_animal_results( );
    });

    //for autocomplete
    var breed_data = [];

    //get animals json
    var animals=[];
    $.ajax({
        url: '/animal/getAnimals',
    }).done( json_result => {
        animals = json_result;

        //populate kind
        $("#id_kind select").material_select("destroy");
        $.each(animals,function(key, value){
            $("#id_kind select").append('<option value=' + key + '>' + key + '</option>');
        });
        $("#id_kind select").material_select();

        //populate breed from kind selected
        $("#id_kind select").change( e => {
            breed_data = [];
            $('#autocomplete-1').removeAttr('disabled');
            //$("#id_breed select").material_select("destroy");
            //removeOptions($("#id_breed select")[0]);
            //$("#id_breed select").append('<option value="" disabled selected>Порода</option>');
            $.each(animals[e.currentTarget.value]['Порода'],function(key, value){
                //$("#id_breed select").append('<option value="' + value + '">' + value + '</option>');
                var poroda = {
                    "title": value,
                    "id": key
                };            
                breed_data.push(poroda);
            });
            setAutocompleteBreeds(breed_data);
            //$("#id_breed select").material_select();
        });        

    });

    setAutocompleteBreeds(breed_data);


    $('#autocomplete-0').tinyAutocomplete({
        minChars:1,
        data: city_data,
        showNoResults: true,
        noResultsTemplate: '<li class="autocomplete-item">Ничего не найдено по запросу "{{title}}"</li>',
        onSelect: function(el, val) {
            if(val == null) {
                $('.results').html('All results for "' + $(this).val() + '" would go here');
            }
            else {
                $(this).val( val.title );
            }
        }
    });

    $('#autocomplete-2').tinyAutocomplete({
        minChars:1,
        data: city_data,
        showNoResults: true,
        noResultsTemplate: '<li class="autocomplete-item">Ничего не найдено по запросу "{{title}}"</li>',
        onSelect: function(el, val) {
            if(val == null) {
                $('.results').html('All results for "' + $(this).val() + '" would go here');
            }
            else {
                $(this).val( val.title );
            }
        }
    });

})