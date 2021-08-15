$(document).ready(function(){

$('.formToJoin').on('submit' , function(e){


var examTwo = $(this).find('#EXAM').text().replace(/'/g,'"')
var exam = JSON.parse(examTwo)
var EndOfExamHours = exam['ExamInformation']['From'].split('T')
var o = CheckTime(EndOfExamHours)

if(o){
   var bu = $(this).find('#join')
   $.ajax({
   type: 'POST',
   url: '/GoToExam',
   data: JSON.stringify({'id' : exam['_id']}),
   contentType: 'application/json;charset=UTF-8',
   beforeSend : function(){
   $(bu).text('Joining . . .')
   },success : function(){
   window.location = '/StudentExam/'+exam['_id']
   }
   });
}else{
var MSG = $(this).find('#msg')
var IsHere = checkCookie('Language')
if(IsHere){
var Cookie = getCookie('Language')
if(Cookie == "English"){
MSG.text('The exam does not start yet')
}else if (Cookie == "Arabic"){
MSG.text('لم يبدأ الامتحان بعد')
}
}else{
MSG.text('The exam does not start yet')
}
}
e.preventDefault()
})

$('.deleteMSG').on('click' , function(){
    var bu = $(this)
    var Parent = $(bu).parent()
    var examTwo = $(Parent).find('#EXAM').text().replace(/'/g,'"')
    console.log(examTwo)
    var exam = JSON.parse(examTwo)
    $.ajax({
    type: 'POST',
    url: '/DeleteMSG',
    data: JSON.stringify({'id' : exam['_id']}),
    contentType: 'application/json;charset=UTF-8',
    beforeSend : function(){
    $(bu).text('Deleting . . .')
    },
    success : function(data){
        alert(data)
        window.location.reload()
    }
    });
})




function CheckTime(from){
var DateFrom = from[0]
var TimeFrom = from[1]

var partsFrom = DateFrom.split('-')
var partsFromTime = TimeFrom.split(':')

var FromDate = new Date(partsFrom[0], partsFrom[1] - 1 , partsFrom[2],partsFromTime[0] , partsFromTime[1])
var Current = new Date()
if (FromDate > Current){
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

})