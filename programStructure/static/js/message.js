$(document).ready(function(){
history.pushState(null,  document.title, location.href);
$('.formToJoin').on('submit' , function(e){


var examTwo = $(this).find('#EXAM').text().replace(/'/g,'"')
var exam = JSON.parse(examTwo)
var StartOfExamHours = exam['ExamInformation']['From'].split('T')
var EndOfExamHours = exam['ExamInformation']['To'].split('T')
var o = CheckTime(StartOfExamHours,EndOfExamHours)

if(o['join']){
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
MSG.text(''+o['MessageE'])
}else if (Cookie == "Arabic"){
MSG.text(''+o['MessageA'])
}
}else{
MSG.text(''+o['MessageE'])
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




function CheckTime(from,to){
var DateFrom = from[0]
var TimeFrom = from[1]

var DateTo = to[0]
var TimeTo = to[1]

var partsFrom = DateFrom.split('-')
var partsFromTime = TimeFrom.split(':')

var partsTo = DateTo.split('-')
var partsToTime = TimeTo.split(':')

var FromDate = new Date(partsFrom[0], partsFrom[1] - 1 , partsFrom[2],partsFromTime[0] , partsFromTime[1])

var ToDate = new Date(partsTo[0], partsTo[1] - 1 , partsTo[2],partsToTime[0] , partsToTime[1])

var Current = new Date()
if (FromDate > Current){
return {'join' : false , 'MessageE' : 'The exam doesnt start yet' , 'MessageA' : 'الامتحان لم يبدأ بعد'}
}else if (ToDate < Current){
return {'join' : false , 'MessageE' : 'The exam finished' , 'MessageA' : 'لقد انتهي وقت الامتحان'}
}else{
return {'join' : true}
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