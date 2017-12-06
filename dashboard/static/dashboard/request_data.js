$(document).ready(function(){
    setInterval(function(){
        $.ajax({
        type: "GET",
        dataType: 'json',
        url: "/dashboard/ajax/get_sensordata/",
        success: function(data){
            $("#Date").text(data.date_time);
            $("#isConnecting_div").hide();
            if (data.is_server_connected){
                if (data.is_client_connected) {
                    $("#isConnected_div").show();
                    $("#isClientDisconnected_div").hide();
                    $("#isServerDisconnected_div").hide();
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
    }, 2000);
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
function request_testemail(){
    $.ajax({
    type: "GET",
    dataType: 'json',
    url: "/dashboard/ajax/testemail/",
    success: function(data){
        if (data.isConnected) {             
        } 
        else {
        }
    }
  });
}
function latency_test(){
        var t1 = Date.now();
        $("#time_sent").text(t1+" ms");
        $.ajax({
        type: "GET",
        dataType: 'json',
        url: "/dashboard/ajax/get_sensordata/",
        success: function(data){
        var t2 = Date.now();
        $("#rawdata").text("[S1:"+data.S1+", S2:"+data.S2+", S3:"+data.S3+", S4:"+data.S4+", S5:"+data.S5+", S6:"+data.S6+"]");
        if (data.is_server_connected){
            if (data.is_client_connected){
                $("#time_received").text(t2+" ms");
                var diff = t2-t1;
                $("#time_diff").text(diff+" ms");    
                }
            else{
                $("#time_received").text("Connection error!");
                $("#time_diff").text("Connection error!");    
            }
        }
        else{
            $("#time_received").text("Connection error!");
            $("#time_diff").text("Connection error!");    
            }
        }
    }); 
}