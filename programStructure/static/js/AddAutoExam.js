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




 $('.AddExamForm').on('submit',function(e){
        e.preventDefault()
    var si_addition = Array.from($('.si-addition'))
    var bool = CheckIfEmpty(si_addition)
        if(bool == false)
        {
        alert('Fill All Information')
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
                $.ajax({
                type: 'POST',
                url: '/AddAutoExam',
                data: JSON.stringify(Exam_Information),
                contentType: 'application/json;charset=UTF-8',
                beforeSend : function(){
                $('#AddQToDataBase').text('Loading . . .')
                },
                complete: function(){
                $('#AddQToDataBase').text('Done')
                },
                success : function(data){
                    window.location.reload()
                }
                });
        }
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
})