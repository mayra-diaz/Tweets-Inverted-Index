function buscar(){
    var cantidad = $('#numElement').val();

    var str = $('#searchString').val();
    var res = str;

    var message = JSON.stringify({
            "values": res,
            "cantidad": cantidad
        });

    $.ajax({
        url:'/consulta',
        type:'POST',
        contentType: 'application/json',
        data : message,
        dataType:'json',
        success: function(response){
            $("#titulo").html("<h1 class='mt-5'>Resultados</h1>")
            $("#resultados").html("");

            $.each(response, function(key, value) {
                console.log(value);
                var parsedDate = new Date(value.date);
                var time = parsedDate.toLocaleTimeString(); 
                var date = parsedDate.toLocaleDateString('en-GB'); 
                
                var string = "";             
                string += "<article class='card mb-4'>"
                string += "<header class='card__header'>"
                string +=     "<div class='card__userinfo'>"
                string +=        "<h2 class='card__name'>"+ value.userName +"</h2>"
                string +=     "</div>"
                string += "</header>"
                
                string += "<div class='card__text'>"
                string +=     "<p class='card__paragraph'>"+ value.body +"</p>"
                string +=     "<span class='card__date'>" + date + " - " + time + "</span>"
                string += "</div>"
                
                string += "<footer class='card__footer'>"
                string +=     "<span class='fas fa-comment'></span>"
                string +=     "<span class='fas fa-redo'></span>"
                string +=     "<span class='fas fa-heart'></span>"
                string +=     "<span class='fas fa-share'></span>"
                string += "</footer>"
                string += "</article>"

                $("#resultados").append(string);
            });
        },
        error: function(response){
            alert("Hubo un problema de comunicación con la base de datos!");
        }
    });
}

$("#loading").hide();

function loading(){
    $("#loading").show();
    $("#uploader").hide();       
}