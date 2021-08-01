$(document).ready(function(){

    $('#SNumber').on('click' , function(){
                $.ajax({
                type: 'POST',
                url: '/Students',
                contentType: 'application/json;charset=UTF-8',
                success : function(data){
                    $('.parent').fadeOut(100).fadeIn(100)
                    $('.parent').html(data['temp'])
                    $('head').html(data['AdminHead'])
                }
                });
    })

        $('#WsNUMBER').on('click' , function(){
                $.ajax({
                type: 'POST',
                url: '/Waiting_Students',
                contentType: 'application/json;charset=UTF-8',
                success : function(data){
                    $('.parent').fadeOut(100).fadeIn(100)
                    $('.parent').html(data['temp'])
                    $('head').html(data['AdminHead'])
                }
                });
    })

    $(document).on('click' , function(e){
        if($(e.target).hasClass('accept_WS')){
            $.ajax({
                type: 'POST',
                url: '/acceptstudent',
                data: JSON.stringify({'id' : $(e.target).data('sid')}),
                contentType: 'application/json;charset=UTF-8',
                success : function(data){

                    $('.container-of-ws').fadeOut(100).fadeIn(100)
                    $('#WsNUMBER').fadeOut(100).fadeIn(100)
                    $('#SNumber').fadeOut(100).fadeIn(100)
                    $('.container-of-ws').html(data['temp'])
                    $('#WsNUMBER').text(data['num1'])
                    $('#SNumber').text(data['num2'])
                    $('head').html(data['AdminHead'])
                }
                });
        }
                else if($(e.target).hasClass('refuse_WS')){
                $.ajax({
                type: 'POST',
                url: '/refusestudent',
                data: JSON.stringify({'id' : $(e.target).data('sid')}),
                contentType: 'application/json;charset=UTF-8',
                success : function(data){
                    $('.container-of-ws').fadeOut(100).fadeIn(100)
                    $('#WsNUMBER').fadeOut(100).fadeIn(100)
                    $('#SNumber').fadeOut(100).fadeIn(100)
                    $('.container-of-ws').html(data['temp'])
                    $('#WsNUMBER').text(data['num1'])
                    $('#SNumber').text(data['num2'])
                    $('head').html(data['AdminHead'])
                }
                });
    }else if ($(e.target).hasClass('deleteSt')){
                $.ajax({
                type: 'POST',
                url: '/deletestudent',
                data: JSON.stringify({'id' : $(e.target).data('sid')}),
                contentType: 'application/json;charset=UTF-8',
                success : function(data){
                    $('.container-of-ws').fadeOut(100).fadeIn(100)
                    $('#WsNUMBER').fadeOut(100).fadeIn(100)
                    $('#SNumber').fadeOut(100).fadeIn(100)
                    $('.container-of-ws').html(data['temp2'])
                    $('#WsNUMBER').text(data['num1'])
                    $('#SNumber').text(data['num2'])
                    $('head').html(data['AdminHead'])
                }
                });
        }
    })


})