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
                string += "<article class='tweet mb-4'>"
                string += "<header class='my_header'>"
                string +=     "<h2 class='my_username'>"+ value.user_name +"</h2>"
                string += "</header>"
                
                string += "<div class='my_text'>"
                string +=     "<p class='my_paragraph'>"+ value.body +"</p>"
                string +=     "<span class='my_date'>" + date + " - " + time + "</span>"
                string += "</div>"
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