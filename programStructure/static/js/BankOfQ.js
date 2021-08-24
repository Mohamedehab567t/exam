$(document).ready(function(){

$('#SearchQ').on('click' , function(){
var AndExpression = GetKeyOfSearch()
var BankQ = $('#BankQ')
if($.isEmptyObject(AndExpression)){
alert('لا يوجد شئ للبحث عنه')
}else{
$.ajax({
type: 'POST',
url: '/GetFilteredQuestion',
data: JSON.stringify(AndExpression),
contentType: 'application/json;charset=UTF-8',
beforeSend : function(){
$(BankQ).fadeOut(1000)
$('#SearchQ').text('جاري البحث ...')
},
complete: function(){
$(BankQ).fadeIn(1000)
$('#SearchQ').text('بحث')
},
success : function(data){
$(BankQ).html(data)
}
});
}


})

$('#NameOfQuestion').on('keyup' , function(){
        var Titles = Array.from($('body').find('.titles'))
        Titles.forEach(e => {
        var IndexOF = e.value.trim().indexOf($("#NameOfQuestion").val())
            if(IndexOF > -1 ){
            var card = $(e).closest('.card')
            $(card).attr('style' , 'display:block !important')
            }else if (IndexOF == -1 ){
            var card = $(e).closest('.card')
            $(card).attr('style' , 'display:none !important')
            }
        })
})

$(window).on('click' , function(e){
if($(e.target).hasClass('UpdateQ')){
var id = $(e.target).data('sid')
var title = $('#'+id+'title').val()
var ChoicesDiv = Array.from($('.'+id+'choice'))
var ScoreDiv = Array.from($('.'+id+'score'))
var Choices = []

var Score = []

ChoicesDiv.forEach(e => {
var value = $(e).val()
var choice = []
choice.push(value)
Choices.push(choice)
})


ScoreDiv.forEach(e => {
var value = $(e).val()
Score.push(parseInt(value))
})

var UQFB = {
'title' : title,
'Choices' : Choices,
'score' : Score
}

var MyCard = $('#'+id+'card .card-body')
$(MyCard).fadeOut(1000)

$.ajax({
type: 'POST',
url: '/UpdateQuestionFromBank/'+id,
data: JSON.stringify(UQFB),
contentType: 'application/json;charset=UTF-8',
success : function(data){
$(MyCard).fadeIn(1000)
$(MyCard).html(data)
}
});

}else if ($(e.target).hasClass('DeleteQ')){
var id = $(e.target).data('sid')
var AndExpression = GetKeyOfSearch()
var BankQ = $('#BankQ')
if($.isEmptyObject(AndExpression)){
$.ajax({
type: 'POST',
url: '/DeleteBankQ',
data: JSON.stringify({'id' : id}),
contentType: 'application/json;charset=UTF-8',
beforeSend : function(){
$(BankQ).fadeOut(1000)
},
complete: function(){
$(BankQ).fadeIn(1000)
},
success : function(data){
$(BankQ).html(data)
}
});
}else{
$.ajax({
type: 'POST',
url: '/DeleteBankQ',
data: JSON.stringify({'id' : id , 'AndExpression' : AndExpression}),
contentType: 'application/json;charset=UTF-8',
beforeSend : function(){
$(BankQ).fadeOut(1000)
},
complete: function(){
$(BankQ).fadeIn(1000)
},
success : function(data){
$(BankQ).html(data)
}
});
}

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

})