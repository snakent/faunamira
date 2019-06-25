$(document).ready(function () {

    //get animals json
    var animals=[];
    $.ajax({
        url: '/animal/getAnimals',
    }).done( json_result => {
        animals = json_result;

        //get animal kind
        var get_kind = $('#get_kind').val();

        //get attr
        var get_attr = $('#id_attr option:selected').text();
        if(get_attr && get_attr!="---------"){
            $('#id_value').removeAttr('disabled');
            $("#id_value")
                .find('option')
                .remove()
                .end()

            $.each(animals[get_kind][get_attr],function(key, value){
                $("#id_value").append('<option value="' + key + '">' + value + '</option>'); 
            });
        }


        //populate breed from kind selected
        $("#id_attr").change( e => {

            $('#id_value').removeAttr('disabled');
            get_attr = $('#id_attr option:selected').text();
            $("#id_value")
                .find('option')
                .remove()
                .end()

            $.each(animals[get_kind][get_attr],function(key, value){
                $("#id_value").append('<option value="' + key + '">' + value + '</option>'); 
            });

        });        

    });

});