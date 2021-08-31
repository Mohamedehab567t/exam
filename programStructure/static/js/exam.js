$(document).ready(function(){
$('.Loading').attr('style' , 'display : none !important;')

$('.ShowAnswer').on('click' , function(){
var OBJ = $(this).closest('td')
var BTN = $(this)
var answers = ReturnJson(OBJ)
    $.ajax({
    type: 'POST',
    url: '/ShowStudentAnswer',
    data: JSON.stringify(answers),
    contentType: 'application/json;charset=UTF-8',
    beforeSend : function(){
    $(BTN).html('<i class="fa fa-spinner fa-spin" style="color:white" ></i>')
    },
    complete: function(){
    $(BTN).html('<i class="fa fa-eye" style="color:white"></i>')
    },
    success : function(data){
    window.open('/ShowStudentAnswer','_blank')
    }
    });
})

$('#Active').on('click' , function(){
    $.ajax({
    type: 'POST',
    url: '/returnExams',
    contentType: 'application/json;charset=UTF-8',
    beforeSend : function(){
    $('.Loading').attr('style' , '')
    },
    complete: function(){
    $('.Loading').attr('style' , 'display : none !important;')
    },
    success : function(data){
    $('#ExamCon').html(data['temp'])
    }
    });
})

$('#Published').on('click' , function(){
    $.ajax({
    type: 'POST',
    url: '/returnExams',
    contentType: 'application/json;charset=UTF-8',
    beforeSend : function(){
    $('.Loading').attr('style' , '')},
    complete: function(){
    $('.Loading').attr('style' , 'display : none !important;')
    },
    success : function(data){
    $('#ExamCon').html(data['temp2'])
    }
    });
})

$('#Submitted').on('click' , function(){
    $.ajax({
    type: 'POST',
    url: '/returnExams',
    contentType: 'application/json;charset=UTF-8',
    beforeSend : function(){
    $('.Loading').attr('style' , '')},
    complete: function(){
    $('.Loading').attr('style' , 'display : none !important;')
    },
    success : function(data){
    $('#ExamCon').html(data['temp3'])
    }
    });
})
$('#ActiveAddStudent').on('click' , function(){
var action = $('.Action')[0]
action.style.display = 'block'
})

$('#PublishedAddStudent').on('click' , function(){
var action = $('.Action')[0]
action.style.display = 'block'
})

$('#close').on('click' , function(){
var action = $('.Action')[0]
action.style.display = 'none'
window.location.reload()
})


$('.AddStudent').on('click' , function(){
    var SID = $(this).data('sid')
    var EID = $(this).data('eid')
    var Status = $(this).data('status')
    var btn = $(this)
    $.ajax({
    type: 'POST',
    url: '/AddStudentToExam',
    contentType: 'application/json;charset=UTF-8',
    data : JSON.stringify({'Sid' : SID , 'Eid' : EID , 'status' : Status}),
    beforeSend : function(){
    $(btn).text('جاري الاضافة')
    },
    complete: function(){
    $(btn).text('تم')
    },
    success : function(data){
    var tr = $(btn).parents('tr')
    $(tr).fadeOut(1000).remove()
    $('#AbsentStudent').html(data)
    }
    });
})


})
function ReturnJson(text){
var OBJ2 = $(text).siblings('.ObjText').text().split('')

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

