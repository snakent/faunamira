$(document).ready(function () {    

    $('#id_city').val(current_city_id);
    $('#id_city_fake').val(current_city_name);

    $('#id_city_fake').tinyAutocomplete({
        minChars:1,
        data: city_data,
        showNoResults: true,
        noResultsTemplate: '<li class="autocomplete-item">Ничего не найдено по запросу "{{title}}"</li>',
        onSelect: function(el, val) {
            if(val != null) {
                $(this).val( val.title );
                $('#id_city').val( val.id );
            }
        }
    });

});