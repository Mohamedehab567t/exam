$(document).ready(function(){

$('.formToJoin').on('submit' , function(e){
//    var examTwo = $(this).find('#EXAM').text().replace(/'/g,'"')
//    var exam = JSON.parse(examTwo)
//    var bu = $(this).find('#join')
//    $.ajax({
//    type: 'POST',
//    url: '/GoToExam',
//    data: JSON.stringify({'id' : exam['_id']}),
//    contentType: 'application/json;charset=UTF-8',
//    beforeSend : function(){
//    $(bu).text('Joining . . .')
//    },success : function(){
//    window.location = '/StudentExam/'+exam['_id']
//    }
//    });

var examTwo = $(this).find('#EXAM').text().replace(/'/g,'"')
var exam = JSON.parse(examTwo)
var current_time = new Date()
var current_Date = moment(current_time).format('YYYY-MM-DD')
var current_hour = current_time.getHours()
var current_minutes = current_time.getMinutes()
var EndOfExamHours = exam['ExamInformation']['To'].split('T')
var EndOfExamMinutes = exam['ExamInformation']['To'].split('T')
//var current_id = $(this).find('#EXAM').data('sid')
//var MSG = $(this).find('#msg')

console.log(examTwo)
console.log(exam)
console.log(current_Date == '2021-08-09' ? true : false)
console.log(current_hour+":"+current_minutes)
console.log(EndOfExamHours[1])
console.log(EndOfExamMinutes[1])

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



//function CheckForErrors(form){
//var examTwo = $(form).find('#EXAM').text().replace(/'/g,'"')
//var exam = JSON.parse(examTwo)
////var current_time = new Date()
////var current_hour = current_time.getHours()
////var current_minutes = current_time.getMinutes()
////var EndOfExamHours = parseInt(exam['ExamInformation']['To'].split(':')[0])
////var EndOfExamMinutes = parseInt(exam['ExamInformation']['To'].split(':')[1])
//var current_id = $(form).find('#EXAM').data('sid')
//var MSG = $(form).find('#msg')
//
//    $.ajax({
//    type: 'POST',
//    url: '/CheckIfAttending',
//    data: JSON.stringify({'id' : exam['_id']}),
//    contentType: 'application/json;charset=UTF-8',
//    success : function(data){
//    $(MSG).text(data).css({'color' : 'red' , 'display' : 'block'})
//    }
//    });
//}



})