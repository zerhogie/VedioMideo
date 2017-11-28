$(function(){
    function buscar() {
        var buscador = encodeURI($('#buscador').val().trim());
        if(buscador) {
            $("#videos_mostrados").load('/mostrando/'+buscador); 
        } else {
            css = $('#buscador').css('border-color');
            $('#buscador').css("border", "1px solid #ff0000").animate({
                'border-color': '#ff0000'
            }, 4000, function(){
                $('#buscador').css("border", "1px solid "+css).animate({
                    'border-color': css
                }, 1000);
            }); 
        }
    }
    $('#btnBuscar').click(function(){
        buscar();
    });
    $('#buscador').keydown(function(key){
        if(key.which==13) {
            buscar();
        }
    });
});