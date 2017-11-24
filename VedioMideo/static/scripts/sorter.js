$(function(){

    function videos_by_(filter){
        return `<!-- Videos -->
        <div class="row">
            {% for video in videos_by_`+filter+` %}
            <div class="col-lg-4 col-md-6 portfolio-item">
                <article class="card h-100">
                    <header class="card-header">
                        {{ video.id_user.username }}
                    </header>
                    <figure>
                        <a href="{% url 'userprofiles:video_details' video.pk %}">
                            <img class="img img-responsive" style="width:100%" src="{{ video.thumbnail.url }}" alt="{{ video.title }}">
                        </a>
                        </video>
                    </figure>
                    <div class="card-body">
                        <h4 class="card-title">
                            <!-- Contribución de Osvaldo -->
                            <a href="{% url 'userprofiles:video_details' video.pk %}">{{ video.title }}</a>
                            <!-- - - - - - - - - - - - - -->
                        </h4>
                        <p class="card-text">{{ video.sumary }}</p>
                    </div>
                    <footer class="card-footer text-muted">
                        Subido el {{ video.date|localtime|date:'Y-m-d \a \l\a\s H:i' }}hrs
                    </footer>
                </article>
            </div>
            {% endfor %}
        </div>
        <!-- /.row -->`
    }

    $('#sorter').click(function(){
        $('#sorter').animateRotate(-180, 300);
        $('.oculto').slideToggle(300, function(){
            $(this).animateRotate(-180, 300);
        });
    });

    $('#date,#searched,#views').each(function(){
       $(this).click(function(ev){
            /*$('#card').animate({
                
            }, 1000);*/
            $('#videos').html(videos_by_(ev.target.id));
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