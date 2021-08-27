$(document).ready(function(){
var Exam_Information = {}
$('.ShowQ').hide()
$('#Q-no').on('keyup' , function(){
    num = $(this).data("number")
    if(this.value > num){
        $(this).css('border' , '0.5px solid red')
        $('#msg').text('This number is out of range')
        $('#msg').css('color' , 'red')
        $('#AddQToDataBase').prop('disabled' , true)
    }else if (this.value < num && this.value != 0 || this.value == num ){
        $(this).css('border' , '0.5px solid green')
        $('#msg').text('Valid Number')
        $('#msg').css('color' , 'green')
        $('#AddQToDataBase').prop('disabled' , false)
    }else if (this.value == 0) {
        $(this).css('border' , '0.5px solid grey')
        $('#msg').text('We do not accept zero')
        $('#msg').css('color' , 'red')
        $('#AddQToDataBase').prop('disabled' , true)
    }
})

$('.si-addition').on('change' , function(){
if($(this).is('select')){
var SmallClass = $(this).attr('id')
$('.'+SmallClass).text($('.'+SmallClass).text() +"  "+this.value)
if(this.value == ""){
$('.'+SmallClass).text("")
}
}
})

$('#bu').hide()
var E_ID;
 $('.AddExamForm').on('submit',function(e){
        e.preventDefault()
    var si_addition = Array.from($('.si-addition'))
    var bool = CheckIfEmpty(si_addition)
        if(bool == false)
        {
        var IsHere = checkCookie('Language')
        if(IsHere){
        var Cookie = getCookie('Language')
        if(Cookie == "English"){
        alert('Fill All Information')
        }else if (Cookie == "Arabic"){
        alert('املئ كل الخانات')
        }
        }else{
        alert('Fill All Information')
        }
        }
        else {
        var Question_Information = {}
        var Student_Information = {}
        No = $('#Q-no').val()
        duration = $('#Du').val()
        from = $('#from').val()
        to = $('#to').val()
        title = $('#Q-title').val()
        QuestionPartInputs = Array.from($('.QuestionPart').children())
        StudentPart = Array.from($('.StudentPart').children())

        QuestionPartInputs.forEach(e => {
        if($(e).is('input')){
        Question_Information[$(e).attr('id')] = $(e).val()
        }else if($(e).is('select')){
        var SmallClass = $(e).attr('id')
        ArrOfContent = $('.'+SmallClass).text().split("  ")
        ArrOfContent.splice(0,1)
        Question_Information[$(e).attr('id')] = ArrOfContent
        }
        })

        StudentPart.forEach(e => {
        if($(e).is('input')){
        Student_Information[$(e).attr('id')] = $(e).val()
        }else if($(e).is('select')){
        var SmallClass = $(e).attr('id')
        ArrOfContent = $('.'+SmallClass).text().split("  ")
        ArrOfContent.splice(0,1)
        Student_Information[$(e).attr('id')] = ArrOfContent
        }
        })
        Exam_Information["NoQ"] = No
        Exam_Information["title"] = title
        Exam_Information["duration"] = duration
        Exam_Information["from"] = from
        Exam_Information["to"] = to
        Exam_Information["Question_Part"] = Question_Information
        Exam_Information["Student_Part"] = Student_Information
        var LISTQ;
        var f = from.split('T')
        var t = to.split('T')
        var o = CheckTime(f,t)
        if(o){
            $.ajax({
            type: 'POST',
            url: '/AddManualExam',
            data: JSON.stringify(Exam_Information),
            contentType: 'application/json;charset=UTF-8',
            beforeSend : function(){
            $('#AddQToDataBase').text('Searching . . .')
            },
            complete: function(){
            $('#AddQToDataBase').text($('#AddQToDataBase').attr('data-text'))
            },
            success : function(Data){
            LISTQ = {
            'list' : Data['list']
            }
            E_ID = Data['id']
           $.ajax({
            type: 'POST',
            url: '/GetQuestions',
            data: JSON.stringify(LISTQ),
            contentType: 'application/json;charset=UTF-8',
            beforeSend : function(){
            $('#AddQToDataBase').text('Getting Questions . . .')
            },
            complete: function(){
            $('#AddQToDataBase').text($('#AddQToDataBase').attr('data-text'))
            },
            success : function(data){
            $('#QuestionChoose').html(data)
            $('#bu').show()
            $('.ShowQ').show()
            }
            });
            }
            });
        }else{
        var IsHere = checkCookie('Language')
        if(IsHere){
        var Cookie = getCookie('Language')
        if(Cookie == "English"){
        alert('There is error in data')
        }else if (Cookie == "Arabic"){
        alert('هناك خطأ في التاريخ')
        }
        }else{
        alert('There is error in data')
        }
        }

        }
        })

$(window).on('click' , function(e){
if($(e.target).hasClass('ManAdd')){
var Non = $('body').find('#NoNAdded')
var NotNon = $('#AddedQ')
var TR = $(e.target).parents("tr:first");
$(Non).append(TR)
$(NotNon).prepend(TR)
$('#NumberOFAdded').text('('+Array.from($(NotNon).children('tr')).length+')')
$(e.target).addClass('ManDelete').removeClass('ManAdd')
$(e.target).addClass('btn-danger').removeClass('btn-success')
    var IsHere = checkCookie('Language')
    if(IsHere){
    var Cookie = getCookie('Language')
    if(Cookie == "English"){
    $(e.target).text('Delete')
    }else if (Cookie == "Arabic"){
    $(e.target).text('حذف')
    }
    }else{
    $(e.target).text('حذف')
    }
}else if($(e.target).hasClass('ManDelete')){
var Non = $('body').find('#NoNAdded')
var NotNon = $('#AddedQ')
var TR = $(e.target).parents("tr:first");

$(NotNon).append(TR)
$(Non).prepend(TR)
$('#NumberOFAdded').text('('+Array.from($(NotNon).children('tr')).length+')')
$(e.target).addClass('ManAdd').removeClass('ManDelete')
$(e.target).addClass('btn-success').removeClass('btn-danger')
        var IsHere = checkCookie('Language')
        if(IsHere){
        var Cookie = getCookie('Language')
        if(Cookie == "English"){
        $(e.target).text('Add')
        }else if (Cookie == "Arabic"){
        $(e.target).text('اضافة')
        }
        }else{
        $(e.target).text('اضافة')
        }
}

})


$('#addExam').on('click' , function(){
var btn = Array.from($('#AddedQ').find('.ManDelete'))
var Array_od_ids = []
btn.forEach(e => {
Array_od_ids.push($(e).data('sid'))
})
var DATA = {
'list' : Array_od_ids ,
'id' : E_ID
}
console.log(Array_od_ids)
             $.ajax({
              type: 'POST',
              url: '/UpQOfManToMongo',
              data: JSON.stringify(DATA),
              contentType: 'application/json;charset=UTF-8',
              beforeSend : function(){
              $('#addExam').text('Uploading  . . .')
              },
              complete: function(){
              $('#addExam').text('Add exam')
              },
              success : function(data){
              window.location = '/exams'
              }
              });

})

function DeleteEmptyValue(arr){
var indexOfEmpty = 0
for(var i = 0; i < arr.length; i++){
if(arr[i] = ""){
indexOfEmpty = arr.indexOf(arr[i])
}
}
arr.splice(indexOfEmpty , 1)
return arr
}

function CheckIfEmpty(el){
var eVal = []
var bool = true
el.forEach(e => {
if($(e).is('input') || $(e).is('select')){
var val = $(e).val()
eVal.push(val)
}
})
for(var i = 0; i < eVal.length; i++){
if(eVal[i] == ""){
bool = false
break
}
}
return bool
}

function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}
function CheckTime(from , to){
var DateFrom = from[0]
var TimeFrom = from[1]
var DateTo = to[0]
var TimeTo = to[1]
var partsFrom = DateFrom.split('-')
var partsTo = DateTo.split('-')
var partsFromTime = TimeFrom.split(':')
var partsToTime = TimeTo.split(':')

var FromDate = new Date(partsFrom[0], partsFrom[1] - 1 , partsFrom[2],partsFromTime[0] , partsFromTime[1])
var ToDate = new Date(partsTo[0], partsTo[1] - 1 , partsTo[2],partsToTime[0] , partsToTime[1])
var Current = new Date()
if (ToDate < FromDate || FromDate < Current){
return false
}else{
return true
}


}
function checkCookie(cname) {
  let username = getCookie(cname);
  if (!username) {
   return false
  } else {
    return true
    }
  }
})