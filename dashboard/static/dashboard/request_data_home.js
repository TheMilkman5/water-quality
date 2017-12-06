$(document).ready(function(){
    setInterval(function(){
        $.ajax({
        type: "GET",
        dataType: 'json',
        url: "/dashboard/ajax/get_sensordata/",
        success: function(data){
	        $("#S1").text(data.S1);
	        $("#S2").text(data.S2);
	        $("#S3").text(data.S3);
            $("#TDS").text(data.S3*0.5);
	        $("#S4").text(data.S4);
	        $("#S5").text(data.S5);
	        $("#S6").text(data.S6);
	        $("#Date").text(data.date_time);
            $("#isConnecting_div").hide();

            //pH
            if (data.S1 > 8.5){
                document.getElementById("S1").style.color = "red";
            }
            else if (data.S1 < 6.5){
                document.getElementById("S1").style.color = "red";
            }
            else{
                document.getElementById("S1").style.color = "black";
            }   

            //Conductivity
            if (data.S3 > 1250){
                document.getElementById("S3").style.color = "red";
                document.getElementById("TDS").style.color = "red";
            }
            else{
                document.getElementById("S3").style.color = "black";
                document.getElementById("TDS").style.color = "black";
            }  

            //Turbidity
            if (data.S4 > 1){
                document.getElementById("S4").style.color = "red";
            }
            else{
                document.getElementById("S4").style.color = "black";
            }

            //Flow rate
            if (data.S6 > 15){
                document.getElementById("S6").style.color = "red";
            }
            else if ((data.S6 < 2.5) && (data.S6 > 0)){
                document.getElementById("S6").style.color = "red";
            }
            else{
                document.getElementById("S6").style.color = "black";
            }

            if (data.is_server_connected)
            {
                if (data.is_client_connected) {
                    $("#isConnected_div").show();
                    $("#isClientDisconnected_div").hide();
                    $("#isServerDisconnected_div").hide();

                    if (parseInt(data.S2)>=650){
                        $("#coliform").text("<30s");
                        $("#ecoli").text("<10s");
                        $("#salmonella").text("<20s");
                    }
                    else if(parseInt(data.S2)>=485 && parseInt(data.S2<650)){
                        $("#coliform").text(">48h");
                        $("#ecoli").text("<60s");
                        $("#salmonella").text(">300s");
                    }
                    else {
                        $("#coliform").text(">48h");
                        $("#ecoli").text(">300s");
                        $("#salmonella").text(">300s");
                    }
                } 
                else {
                    $("#isConnected_div").hide();
                    $("#isClientDisconnected_div").show();
                    $("#isServerDisconnected_div").hide();
                }
            }
            else {
                $("#isConnected_div").hide();
                $("#isClientDisconnected_div").hide();
                $("#isServerDisconnected_div").show();
            }
    	}
        }); 
    }, 500);
});
function request_stop(){
    $.ajax({
    type: "GET",
    dataType: 'json',
    url: "/dashboard/ajax/close_flow/",
    success: function(data){
        if (data.isConnected) {             
        } 
        else {
        }
    }
  });
}
function request_open(){
    $.ajax({
    type: "GET",
    dataType: 'json',
    url: "/dashboard/ajax/open_flow/",
    success: function(data){
        if (data.isConnected) {             
        } 
        else {
        }
    }
  });
}
