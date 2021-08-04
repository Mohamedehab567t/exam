$(document).ready(function(){
$('.Loading').attr('style' , 'display : none !important;')

$('#Active').on('click' , function(){
    $.ajax({
    type: 'POST',
    url: '/returnExams',
    contentType: 'application/json;charset=UTF-8',
    beforeSend : function(){
    $('.Loading').attr('style' , '')
    },
    complete: function(){
    $('.Loading').attr('style' , 'display : none !important;')
    },
    success : function(data){
    $('#ExamCon').html(data['temp'])
    }
    });
})

$('#Published').on('click' , function(){
    $.ajax({
    type: 'POST',
    url: '/returnExams',
    contentType: 'application/json;charset=UTF-8',
    beforeSend : function(){
    $('.Loading').attr('style' , '')},
    complete: function(){
    $('.Loading').attr('style' , 'display : none !important;')
    },
    success : function(data){
    $('#ExamCon').html(data['temp2'])
    }
    });
})

$('#Submitted').on('click' , function(){
    $.ajax({
    type: 'POST',
    url: '/returnExams',
    contentType: 'application/json;charset=UTF-8',
    beforeSend : function(){
    $('.Loading').attr('style' , '')},
    complete: function(){
    $('.Loading').attr('style' , 'display : none !important;')
    },
    success : function(data){
    $('#ExamCon').html(data['temp3'])
    }
    });
})

})