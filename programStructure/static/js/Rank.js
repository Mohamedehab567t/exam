$(document).ready(function(){
$('#SearchQ').on('click' , function(){
            var AndExpression = GetKeyOfSearch()
            if($.isEmptyObject(AndExpression)){
            alert('لا يوجد شئ للبحث عنه')
            }else{
            $.ajax({
            type: 'POST',
            url: '/GetFilteredStudentRankedAdmin',
            data: JSON.stringify(AndExpression),
            contentType: 'application/json;charset=UTF-8',
            beforeSend : function(){
            $('#SearchQ').text('جاري البحث ...')
            },
            complete: function(){
            $('#SearchQ').text('بحث')
            },
            success : function(data){
            $('.ConOfRanked').fadeOut(100).fadeIn(100)
            $('.ConOfRanked').html(data['temp2'])
            }
            });
            }
})
})
////////////////////////////////////
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