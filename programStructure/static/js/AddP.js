$(document).ready(function(){
    var Passage = {}
    var PassageQ = []
// AddQ
    var count = -1
    $('#Q-type').on('change' , function(){
        if(this.value == 'text'){
            $('#AddChoiceBtn').addClass('show')
            if($('#AddChoiceBtn').hasClass('hide')){
            $('#AddChoiceBtn').removeClass('hide')
            }

            $('.QChoices').addClass('show')
            if($('.QChoices').hasClass('hide')){
            $('.QChoices').removeClass('hide')
            }


            $('.ImagePurpose').addClass('hide')
            if($('.ImagePurpose').hasClass('show')){
            $('.ImagePurpose').removeClass('show')
            }

        }else if(this.value == 'images'){

            $('#AddChoiceBtn').addClass('show')
            if($('#AddChoiceBtn').hasClass('hide')){
            $('#AddChoiceBtn').removeClass('hide')
            }

            $('.QChoices').addClass('show')
            if($('.QChoices').hasClass('hide')){
            $('.QChoices').removeClass('hide')
            }

            $('.ImagePurpose').addClass('show')
            if($('.ImagePurpose').hasClass('hide')){
            $('.ImagePurpose').removeClass('hide')
            }

        }
        else{
        $('#AddChoiceBtn').addClass('hide').removeClass('show')
        $('.QChoices').addClass('hide').removeClass('show')

                    $('.ImagePurpose').addClass('hide')
            if($('.ImagePurpose').hasClass('show')){
            $('.ImagePurpose').removeClass('show')
            }
        }

        var DeleteChildes = Array.from($('.QChoices').children())
        DeleteChildes.forEach(e=>{
        $(e).remove()
        })
    })
    var x = 0
    $('#AddChoiceBtn').on('click' , function(){

        // ConForSingleChoice
        var q_con = document.createElement('div')
        $(q_con).addClass('ConForSingleChoice')


     // Q choice
        var q_choice = document.createElement('input')
        $(q_choice).attr('placeholder' , 'another choice')
        $(q_choice).addClass('form-control')
     // Q delete
        var q_delete = document.createElement('button')
        $(q_delete).addClass('btn btn-danger DeleteSiblingChoice')
        $(q_delete).attr('type' , 'button')
        var q_delete_i = document.createElement('i')
        $(q_delete_i).addClass('fa fa-times-circle DeleteSiblingChoice')
        q_delete.append(q_delete_i)

    // Q Right

        var q_right = document.createElement('button')
        $(q_right).addClass('btn btn-success MakeItRight')
        $(q_right).attr('type' , 'button')

        var IsHere = checkCookie('Language')
        if(IsHere){
        var Cookie = getCookie('Language')
        if(Cookie == "English"){
        $(q_right).text('Right')
        }else if (Cookie == "Arabic"){
        $(q_right).text('صح')
        }
        }else{
       $(q_right).text('Right')
        }


        $(q_right).css({"margin-left" : "5px" ,
        "font-size" : "11px"})


        if($('#Q-type').val() != 'text'){
        x++
        }
        var q_file = document.createElement('input')
        $(q_file).attr('type' , 'file')
        $(q_file).attr('name' , 'ChoiceImage'+x)
        $(q_file).addClass('ImagePurpose')

        if($('#Q-type').val() == 'images'){
        q_con.append(q_file)
        q_con.append(q_choice)
        q_con.append(q_delete)
        q_con.append(q_right)
        }else{
        q_con.append(q_choice)
        q_con.append(q_delete)
        q_con.append(q_right)
        }

        $('.QChoices').append(q_con)
    })


    $(window).on('click' , function(e){
        DeleteParentOrParentOfParent(e)
        if($(e.target).hasClass('MakeItRight')){
                MakeItRight(e , 'MakeItRight' , count )
        }
    })




    $('#AddQOfPToDataBase').on('click' , function(e){
    var si_addition = Array.from($('.si-addition'))
    var bool = CheckIfEmpty(si_addition)
    if(bool == false ){
    alert("Fill question data")
    }
    else{
    if($('#Q-type').val() == "text"){
            AddTextedQuestion()
    }else{
            AddImagedQuestion()
    }
    }
    e.preventDefault()
    })

$('#AddPToDataBase').on('click' , function(){
Passage['_id'] = Math.floor(Math.random() * 1000000000)
Passage['P-title'] = $('#PTitle').val()
Passage['P-content'] = $('#editor-text').html()
var divChild = Array.from($('.P-Configuration *'))

divChild.forEach(e =>{
if($(e).is('input') || $(e).is('select') ){
var eID = $(e).attr('id')
var eVal = $(e).val()
Passage[eID] = eVal
}
})
Passage['P-Questions'] = PassageQ
       if(PassageQ.length > 0){
        $.ajax({
        type: 'POST',
        url: '/AddPtoDataBase',
        data: JSON.stringify(Passage),
        contentType: 'application/json;charset=UTF-8',
        beforeSend : function(){
        $('#AddPToDataBase').text('Loading . . .')
        },
        complete: function(){
        $('#AddPToDataBase').text('اضافة قطعة')
        },
        success : function(data){
        alert(data)
        $('#exampleFormControlTextarea1').val('')
        $('body').find('.ConForSingleChoice').remove()
        }
        });
            }else{
            alert('اضف علي الاقل سؤال واحد')
            }
})
    function MakeItRight(e , className , count){

    var classArray = Array.from($('.'+className))
    for(var i = 0; i < classArray.length; i++){
        $(classArray[i]).prop('disabled' , true)
    }

    if($('Q-type') == "text"){
    if($(e.target).is('button')){
    $(e.target).prop('disabled' , true)
    $(e.target).css('border' , '0.5px solid black')
    var Parent = $(e.target).parent()
    var SiblingInput = Parent.find('input')
    SiblingInput.data('score' , 1)
    }
    }else{
    if($(e.target).is('button')){
    $(e.target).prop('disabled' , true)
    $(e.target).css('border' , '0.5px solid black')
    var Parent = $(e.target).parent()
    Parent.data('score' , 1)
    }
    }

}
    function DeleteParentOrParentOfParent(e){
     if($(e.target).is('button')){
    var className = $(e.target).attr('class'),
        lastClass = className.substr(className.lastIndexOf(' ') + 1);
        if(lastClass == 'DeleteSiblingChoice'){
            $(e.target).parent().remove()
        }
     }else if($(e.target).is('i')){
    var className = $(e.target).attr('class'),
        lastClass = className.substr(className.lastIndexOf(' ') + 1);
        if(lastClass == 'DeleteSiblingChoice'){
           var directP =  $(e.target).parent()
           $(directP).parent().remove()
        }
     }
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



function AddTextedQuestion(){
    Q = {}
    Q['_id'] = Math.floor(Math.random() * 1000000)
    ChoicesArray = []
    score = []
    var divChild = Array.from($('.Q-Configuration *'))
    var ChoicesDiv = Array.from($('.ConForSingleChoice'))

    divChild.forEach(e =>{
    if($(e).is('input') || $(e).is('select') ){
    var eID = $(e).attr('id')
    var eVal = $(e).val()
    Q[eID] = eVal
    }
    })


    ChoicesDiv.forEach(e => {
    var Choice = []
    var input = Array.from($(e).children())
    input.forEach(e => {
    if($(e).is('input')){
    if($(e).val() != ""){
        Choice.push($(e).val())
    }
    }
    })
       ChoicesArray.push(Choice)
       if($(e).data('score')){
       score.push(1)
       }else{
       score.push(0)
       }
    })
        Q['Choices'] = ChoicesArray
        Q['score'] = score
        Passage['kind'] = 'P'
        if(confirm("Do you want to add this question ?")){
        var ValOBJ = QValidation(ChoicesArray , score)
        if (!ValOBJ['go']){
        alert(ValOBJ['message'])
        }else{
        PassageQ.push(Q)
        $('#Q-title').val('')
        $('body').find('.ConForSingleChoice').remove()
}
 }
        else{
        console.log('you Canceled')
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

function checkCookie(cname) {
  let username = getCookie(cname);
  if (!username) {
   return false
  } else {
    return true
    }
  }
function GetTotal(total , num){
return total + num
}
function QValidation(Array1,Array2){
        if(Array1.length < 2) {
        return {'go' : false , 'message' : 'يجب اضافة اكثر من اختيار واحد علي الاقل'}
        }else if (Array2.reduce(GetTotal) == 0){
        return {'go' : false , 'message' : 'يجب تحديد اي من الاجابات صحيحه'}
        }else{
        return {'go' : true}
        }
}
})

