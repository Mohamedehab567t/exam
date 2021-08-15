$(document).ready(function(){




$('.C').on('click' , function(){
    $(this).attr('data-selected' , true)
    $(this).siblings().attr('data-selected' , false)
    if($(this).hasClass('choice')){
        $(this).siblings().addClass('disabeld').removeClass('choice')
    }else if ($(this).hasClass('disabeld')){
        $(this).addClass('choice').removeClass('disabeld').siblings().addClass('disabeld').removeClass('choice')
    }
})

$('.M').on('click' , function(){
var clicked = $(this)
$(clicked).attr('data-selected' , 'true')
var mSiblings = Array.from($(this).siblings())
mSiblings.forEach(e => {
if($(e).hasClass('M')){
$(e).attr('data-selected' , 'false')
$(e).css('background-color' , '#83ff77')
}
})
$(clicked).css('background-color' , 'green')
})




$('#SENDEXAM').on('click' , function(){
SubmitFunction()
})

var IDInterval = setInterval(myFunc , 1000)
function myFunc(){
var text = parseInt($('#timer').text())
var New = text - 1
$('#timer').text(New)
if(text <= 0){
clearInterval(IDInterval)
$('#timer').text(0)
SubmitFunction()
}
}

function SubmitFunction(){
var score = 0
var Children = Array.from($('#ExamCon *'))
Children.forEach(e =>{
if($(e).hasClass('C') || $(e).hasClass('M')){
if($(e).attr('data-selected') == 'true' ){
var eScore = parseInt($(e).data('score'))
score += eScore
}
}
})
    var exam = $('#EXID').data('sid')
    $.ajax({
    type: 'POST',
    url: '/SendingSubmitting',
    data: JSON.stringify({'id' : exam , 'score' : score}),
    contentType: 'application/json;charset=UTF-8',
    beforeSend : function(){
    $('#SENDEXAM').text('Submitting . . .')
    },success : function(){
    window.location = '/profile'
    }
    });
}

})