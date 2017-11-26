$(function(){
        $('#btnBuscar').click(function(){
            var buscador = $('#buscador').val().trim();
            if(buscador) {
                $("#videos_mostrados").load('/mostrando/'+encodeURI(buscador), function(response, stats){
                    if(stats == "success") {
                        console.log("Cambio realizado");
                    }
                    if(stats == "error") {
                        console.log("Error al desplegar los datos");
                    }
                }); 
            } else {
                css = $('#buscador').css('border-color');
                $('#buscador').css('border-color', 'red');   
            }
        });
});