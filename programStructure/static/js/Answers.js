$(document).ready(function(){
var QuestionsText = Array.from($('.TextQ'))
var QuestionsImage = Array.from($('.ImageQ'))
var Answers = ReturnJson($('#a'))

var i = 0
QuestionsText.forEach(e => {
var ChoiceDiv = $(e).find('.choices')
var Score = Answers[$(e).find('.Qid').data('sid')]

if(Score > 0) {
$(e).find('.Qid').attr('style' , 'color : white; text-align:center; background-color:green')
}else{
$(e).find('.Qid').attr('style' , 'color : white; text-align:center; background-color:red')
}


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