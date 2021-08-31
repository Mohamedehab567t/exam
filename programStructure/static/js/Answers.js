$('.QA span').hide()
$(document).ready(function(){
var QuestionsText = Array.from($('.TextQ'))
var QuestionsImage = Array.from($('.ImageQ'))
var Answers = ReturnJson($('#a'))

var i = 0
QuestionsText.forEach(e => {
if($(e).hasClass('QUES')){
var ChoiceDiv = $(e).find('.choices')
var Score = Answers[$(e).find('.Qid').data('sid')]['mark']
if(Score > 0) {
$(e).find('.Qid').attr('style' , 'color : white; text-align:center; background-color:green')
}else{
$(e).find('.Qid').attr('style' , 'color : white; text-align:center; background-color:red')
}
var qa = $(e).find('.QA span')
$(qa).text('الطالب اختار : '+ Answers[$(e).find('.Qid').data('sid')]['selected'])
$(qa).show()
}else if ($(e).hasClass('Passage')){
var dict = Answers[$(e).siblings('.PID').data('sid')]
var PQ = Array.from($(e).find('.PQ'))
PQ.forEach(el =>{
var ChoiceDiv = $(el).find('.choices')
var Score = dict[$(el).find('.title').data('sid')]['mark']
console.log(Score)
if(Score > 0) {
$($(el).find('.title')).attr('style' , 'color : white; text-align:center; background-color:green')
}else{
$($(el).find('.title')).attr('style' , 'color : white; text-align:center; background-color:red')
}
var qa = $(el).find('.QA span')
$(qa).text('الطالب اختار : '+ dict[$(el).find('.title').data('sid')]['selected'])
$(qa).show()
})


}
})


var Spans = Array.from($('.htmlOfP'))
Spans.forEach(e => {
var getEditor = $(e).siblings('.editor-text')
$(getEditor).html($(e).text())
})

})

function ReturnJson(a){
var OBJ2 = $(a).text().split('')

OBJ2.forEach(e => {
if(e == "'"){
var index = OBJ2.indexOf(e)
OBJ2[index] = '"'
}
})
var Dict = OBJ2.join('')
var exam = JSON.parse(Dict)
return exam
}