$(function(){

    $('#sorter').click(function(){
        $('#sorter').animateRotate(-180, 300);
        $('.oculto').slideToggle(300, function(){
            $(this).animateRotate(-180, 300);
        });
    });

    $('#date,#searched,#views').each(function(){
       $(this).click(function(ev){
            $("#videos_mostrados").load('/mostrando/'+ev.target.id, function(response, stats){
                if(stats == "success") {
                    console.log("Cambio realizado");
                }
                if(stats == "error") {
                    console.log("Error al desplegar los datos");
                }
            });
       });
    });

    $.fn.animateRotate = function(angle, duration, easing, complete) {
        var args = $.speed(duration, easing, complete);
        var step = args.step;
        return this.each(function(i, e) {
            args.complete = $.proxy(args.complete, e);
            args.step = function(now) {
            $.style(e, 'transform', 'rotate(' + now + 'deg)');
            if (step) return step.apply(e, arguments);
            };
        
            $({deg: 0}).animate({deg: angle}, args);
        });
    };
});