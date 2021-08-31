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
sessionStorage.setItem("Timer", $('#timer').text());
$('#timer').text(New)
if(text <= 0){
clearInterval(IDInterval)
$('#timer').text(0)
SubmitFunction()
}
}
var QuestionScore = {}
var QIDS = Array.from($('.Qid'))
function SubmitFunction(){
var score = 0
var Children = Array.from($('#ExamCon *'))
var i = 0
Children.forEach(e =>{
if($(e).hasClass('QUES')){
var Choices = Array.from($(e).find('.choice'))
Choices.forEach(el => {
if($(el).hasClass('C') || $(el).hasClass('M')){
if($(el).attr('data-selected') == 'true' ){
var eScore = parseInt($(el).data('score'))
score += eScore
QuestionScore[$(QIDS[i]).data('sid')] = {'mark' : eScore , 'selected' : $(el).text().trim()}
i++;
}
}
})
}else if ($(e).hasClass('Passage')){
var ques = Array.from($(e).find('.Pid'))
var PQ = {}
var o = 0
var ChoicesOfQP = Array.from($(e).find('.choice'))
console.log(ChoicesOfQP)
ChoicesOfQP.forEach(er => {
if($(er).hasClass('C')){
if($(er).attr('data-selected') == 'true' ){
var eScore = parseInt($(er).data('score'))
score += eScore
PQ[$(ques[o]).data('sid')] = {'mark' : eScore , 'selected' : $(er).text().trim()}
o++;
}
}
})

QuestionScore[$(QIDS[i]).data('sid')] = PQ
i++;
}

})
console.log(QuestionScore)
    var exam = $('#EXID').data('sid')
    $.ajax({
    type: 'POST',
    url: '/SendingSubmitting',
    data: JSON.stringify({'id' : exam , 'score' : score , 'QuestionScore' : QuestionScore}),
    contentType: 'application/json;charset=UTF-8',
    beforeSend : function(){
    $('#SENDEXAM').text('Submitting . . .')
    $('#SENDEXAM').prop('disabled' , true)
    },success : function(){
    window.location = '/profile'
    }
    });
}
const pageAccessedByReload = (
  (window.performance.navigation && window.performance.navigation.type === 1) ||
    window.performance
      .getEntriesByType('navigation')
      .map((nav) => nav.type)
      .includes('reload')
);
if(pageAccessedByReload){
$('#timer').text(sessionStorage.getItem("Timer"))
}

var Spans = Array.from($('.htmlOfP'))
Spans.forEach(e => {
var getEditor = $(e).siblings('.editor-text')
$(getEditor).html($(e).text())
})
})