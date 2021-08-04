$(document).ready(function(){

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
        var Exam_Information = {}
        var Question_Information = {}
        var Student_Information = {}
        No = $('#Q-no').val()
        duration = $('#Du').val()
        from = $('#from').val()
        to = $('#to').val()
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
        Exam_Information['NoQ'] = No
        Exam_Information['duration'] = duration
        Exam_Information['from'] = from
        Exam_Information['to'] = to
        Exam_Information['Question_Part'] = Question_Information
        Exam_Information['Student_Part'] = Student_Information
        var LISTQ;
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
                $('#AddQToDataBase').text('Add exam')
                },
                success : function(data){
                $('#QuestionChoose').html(data)
                $('#bu').show()
                }
                });
                }
                });

        }
        })

$(window).on('click' , function(e){
if($(e.target).hasClass('ManAdd')){
var Qid = $(e.target).data('sid')
var te = $('#Array_of_Question').text()
if(te == ""){
$('#Array_of_Question').text(Qid)
}else{
$('#Array_of_Question').text($('#Array_of_Question').text() +"  "+Qid )
}
}

})


$('#addExam').on('click' , function(){
var Array_od_ids = $('#Array_of_Question').text().split("  ")
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
              window.location.reload()
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

function checkCookie(cname) {
  let username = getCookie(cname);
  if (!username) {
   return false
  } else {
    return true
    }
  }
})