
$(document).ready(function(){

$('.Loading').attr('style' , 'display : none !important;')
    $('#SNumber').on('click' , function(){
        ShowStudents()
    })

        $('#WsNUMBER').on('click' , function(){
                $.ajax({
                type: 'POST',
                url: '/Waiting_Students',
                contentType: 'application/json;charset=UTF-8',
                beforeSend : function(){
                $('.Loading').attr('style' , '')},
                complete: function(){
                $('.Loading').attr('style' , 'display : none !important;')
                },
                success : function(data){
                    $('.parent').fadeOut(100).fadeIn(100)
                    $('.parent').html(data['temp'])
                    $('head').html(data['AdminHead'])
                }
                });
    })



    $(document).on('keyup' , function(e){
    if($(e.target).attr('id') == 'NameOfStudent'){
        var Names = Array.from($('body').find('.Names'))
        Names.forEach(e => {
        var IndexOF = e.textContent.trim().indexOf($("#NameOfStudent").val())
            if(IndexOF > -1 ){
            var ws = $(e).closest('.ws')
            $(ws).attr('style' , 'display:block !important')
            }else if (IndexOF == -1 ){
            var ws = $(e).closest('.ws')
            $(ws).attr('style' , 'display:none !important')
            }
        })
    }
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
                var AndExpression = GetKeyOfSearch()
                if($.isEmptyObject(AndExpression)){
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
                    $('#S_NUM').text(data['num2'])
                    $('head').html(data['AdminHead'])
                }
                });
                }else{
                $.ajax({
                type: 'POST',
                url: '/deletestudent',
                data: JSON.stringify({'id' : $(e.target).data('sid') , 'AndExpression' : AndExpression}),
                contentType: 'application/json;charset=UTF-8',
                success : function(data){
                    $('.container-of-ws').fadeOut(100).fadeIn(100)
                    $('#WsNUMBER').fadeOut(100).fadeIn(100)
                    $('#SNumber').fadeOut(100).fadeIn(100)
                    $('.container-of-ws').html(data['temp2'])
                    $('#SNumber').text(data['Nav'])
                    $('#S_NUM').text(data['num2'])
                    $('head').html(data['AdminHead'])
                }
                });
                }

        }else if ($(e.target).hasClass('showST')){
            window.open('/StudentInformation/'+$(e.target).data('sid'),'_blank')
        }else if ($(e.target).hasClass('SearchQ')){
            var AndExpression = GetKeyOfSearch()
            if($.isEmptyObject(AndExpression)){
            alert('لا يوجد شئ للبحث عنه')
            }else{
            $.ajax({
            type: 'POST',
            url: '/GetFilteredStudent',
            data: JSON.stringify(AndExpression),
            contentType: 'application/json;charset=UTF-8',
            beforeSend : function(){
            $('.SearchQ').text('جاري البحث ...')
            },
            complete: function(){
            $('.SearchQ').text('بحث')
            },
            success : function(data){
            $('.container-of-ws').fadeOut(100).fadeIn(100)
            $('.container-of-ws').html(data['temp2'])
            $('head').html(data['AdminHead'])
            $('#S_NUM').text(data['num2'])
            }
            });
            }
        }else if ($(e.target).hasClass('All')){
            ShowStudents()
        }
    })

function GetKeyOfSearch(){
var Inputs = Array.from($('.SearchDiv').children())
var AndExpression = {}
Inputs.forEach(e => {
if($(e).is('input')){
if($(e).val() != ""){
var key = $(e).attr('placeholder')
AndExpression[key] = $(e).val()
}
}else if ($(e).is('select')){
if($(e).val() != ""){
var key = $(e).attr('name')
AndExpression[key] = $(e).val()
}
}
})
return AndExpression
}
function ShowStudents(){
                $.ajax({
                type: 'POST',
                url: '/Students',
                contentType: 'application/json;charset=UTF-8',
                beforeSend : function(){
                $('.Loading').attr('style' , '')},
                complete: function(){
                $('.Loading').attr('style' , 'display : none !important;')
                },
                success : function(data){
                    $('.parent').fadeOut(100).fadeIn(100)
                    $('.parent').html(data['temp'])
                    $('head').html(data['AdminHead'])

                }
                });
}
})