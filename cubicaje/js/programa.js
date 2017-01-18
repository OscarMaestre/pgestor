$(document).ready(inicio)


function informe_dimensiones(ancho_caja, largo_caja, ancho_pale, largo_pale){
    texto="Dimensiones caja:"+ancho_caja+" x "+largo_caja +"<br/> Dimensiones palé:"+ancho_pale+" x "+largo_pale;
    return texto;
}

function informe_superficies(ancho_caja, largo_caja, ancho_pale, largo_pale){
    var superficie_caja=ancho_caja * largo_caja;
    var superficie_pale=ancho_pale * largo_pale;
    var cantidad_cajas=superficie_pale / superficie_caja;
    
    var texto="Superficie de la caja:"+superficie_caja;
    texto+=", Superficie del pale:"+superficie_pale;
    texto+="<br/>Cantidad de cajas: "+superficie_pale+" / "+superficie_caja+" = <b>"+cantidad_cajas+" cajas</b>";
    return texto;
}


function dibujar_caja(p, r, g, b, x0, y0, ancho, largo){
    for (var i = x0; i < x0+ancho; i++) {
        
            p.buffer[p.index(i, y0)] = p.color(0xcc, 0x00, 0x44);
            
        
    }
    return p;
}
function generar_graficos(ancho_caja, largo_caja, ancho_pale, largo_pale){
    var p = new PNGlib(640, 480, 256); // construcor takes height, weight and color-depth
    var background = p.color(0, 0, 0, 0); // set the background transparent
    
    p=dibujar_caja(p, 0xcc, 0x00, 0x44, 20, 20, ancho_caja*10, largo_caja*10);
    
    
    $("#grafico").html('<img src="data:image/png;base64,'+p.getBase64()+'">');

}
function calcular(){
    var ancho_caja=parseInt($("#ancho_caja").val());
    var largo_caja=parseInt($("#largo_caja").val());
    var ancho_pale=parseInt($("#ancho_pale").val());
    var largo_pale=parseInt($("#largo_pale").val());
    
    
    $("#dimensiones").html( informe_dimensiones(ancho_caja, largo_caja, ancho_pale, largo_pale) );
    $("#superficies").html( informe_superficies(ancho_caja, largo_caja, ancho_pale, largo_pale) );
    
    //generar_graficos(ancho_caja, largo_caja, ancho_pale, largo_pale)
}

function inicio(){
    $("#ancho_caja").val(3);
    $("#largo_caja").val(2);
    $("#ancho_pale").val(30);
    $("#largo_pale").val(20);
    $("#ancho_pale").change(calcular);
    $("#largo_pale").change(calcular);
    $("#ancho_caja").change(calcular);
    $("#largo_caja").change(calcular);
    calcular();
}