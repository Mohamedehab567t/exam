$(document).ready(function(){
    $('.StudentInformation').on('submit' , function(e){
        var elements = Array.from($('.StudentInformation *'))
        var arr = CheckIfEmpty(elements)
        UpdateInformation(arr)
        e.preventDefault()
    })


    $('#langChange').on('click' , function(){
    var textLang = $(this).text()
    if(textLang == 'AR'){
    setCookie('Language' , 'Arabic' , 100000)
    window.location.reload()
    }else if (textLang == 'EN'){
    setCookie('Language' , 'English' , 100000)
    window.location.reload()
    }
    })

    $('#SearchQ').on('click' , function(){
            var AndExpression = GetKeyOfSearch()
            if($.isEmptyObject(AndExpression)){
            alert('لا يوجد شئ للبحث عنه')
            }else{
            $.ajax({
            type: 'POST',
            url: '/GetFilteredStudentRankedStudent',
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

  function setCookie(cname, cvalue, exdays) {
  const d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  let expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

})
function CheckIfEmpty(el){
var eVal = []
el.forEach(e => {
if($(e).is('input') || $(e).is('select')){
var val = $(e).val()
eVal.push(val)
}
})
return eVal
}

function UpdateInformation(arrayOfVal){
var bool = true
for(var i =0; i < arrayOfVal.length; i++){
if(arrayOfVal[i] == ""){
alert("Please fill all your information")
bool = false
break
}
}
if(bool){
var Information = {}
var UPDATE = {}
var elements = Array.from($('.StudentInformation .Adi'))
var First = $('.StudentInformation').find('#f').val()
var last = $('.StudentInformation').find('#l').val()
var phone = $('.StudentInformation').find('#p').val()
var gender = $('.StudentInformation').find('#g').val()
elements.forEach(e => {
var val = $(e).val()
Information[$(e).data('label')] = val
})

UPDATE['i'] = Information
UPDATE['f'] = First
UPDATE['l'] = last
UPDATE['p'] = phone
UPDATE['g'] = gender

$.ajax({
type: 'POST',
url: '/UpdateInformation',
data: JSON.stringify(UPDATE),
contentType: 'application/json;charset=UTF-8',
success : function(data){
alert(data)
window.location.reload()
},
    error: function (jqXHR, exception) {
        var msg = '';
        if (jqXHR.status === 0) {
            msg = 'Not connect.\n Verify Network.';
        } else if (jqXHR.status == 404) {
            msg = 'Requested page not found. [404]';
        } else if (jqXHR.status == 500) {
            msg = 'Internal Server Error [500].';
        } else if (exception === 'parsererror') {
            msg = 'Requested JSON parse failed.';
        } else if (exception === 'timeout') {
            msg = 'Time out error.';
        } else if (exception === 'abort') {
            msg = 'Ajax request aborted.';
        } else {
            msg = 'Uncaught Error.\n' + jqXHR.responseText;
        }
        alert(msg);
    }
});
}
}
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


