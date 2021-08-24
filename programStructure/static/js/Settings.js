$(document).ready(function(){
// main settings

    $('.mainform').on('submit' , function(e){
    var SelectedLang = $('#lang').val()
    if(SelectedLang != ""){
        setCookie('Language' , SelectedLang , 1000000)
    }else{
        setCookie('Language' , 'Arabic' , 1000000)
    }
    var ShowPiece = $('#ShowPiece').is(":checked") ? true : false
    var SettingsUpdate = {
    'ShowPiece' : ShowPiece
    }
    $.ajax({
    type: 'POST',
    url: '/CheckSettings',
    data: JSON.stringify(SettingsUpdate),
    contentType: 'application/json;charset=UTF-8',
    success : function(data){
        alert('تم التغيير')
    },
    error : function(data){
        alert('هناك خطأ ما')
    }
    });


    })

  // addition information settings

    $('#si-addition-input-for-students').on('change' , function(){
        if(this.value == 'select'){
            $('.SelectValues').addClass('show')
            if($('.SelectValues').hasClass('hide')){
            $('.SelectValues').removeClass('hide')
            }
        }else{
        $('.SelectValues').addClass('hide').removeClass('show')
        }
    })

    $('.AdditionStudentInformationForm').on('submit' , function(e){
    var labelValue = $('#labelValue').val()
    var typeValue = $('#si-addition-input-for-students').val()
    var InfoValue = $('#si-addition-input-for').val()


    var si_addition = Array.from($('.Stu'))
    var bool = CheckIfEmpty(si_addition)
    if(bool == false){
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
    }else{
    if(typeValue =='select'){
    var Values = $('#ValuesOfSelectBox').val().split("  ")

    $.ajax({
    type: 'POST',
    url: '/Addition',
    data: JSON.stringify({
    'label' : labelValue,
    'type'  : typeValue,
    'InfoValue'  : InfoValue,
    'values': Values
    }),
    contentType: 'application/json;charset=UTF-8',
    success : function(data){
        alert(data)
    }
    });
    }else {
    $.ajax({
    type: 'POST',
    url: '/Addition',
    data: JSON.stringify({
    'label' : labelValue,
    'type'  : typeValue,
    'InfoValue'  : InfoValue
    }),
    contentType: 'application/json;charset=UTF-8',
    success : function(data){
        alert(data)
    }
    });
    }
    }


    e.preventDefault()
    })

// QuestionConfiguration

$('#si-addition-input-for-Q').on('change' , function(){
        if(this.value == 'select'){
            $('.SelectValues2').addClass('show')
            if($('.SelectValues2').hasClass('hide')){
            $('.SelectValues2').removeClass('hide')
            }
        }else{
        $('.SelectValues2').addClass('hide').removeClass('show')
        }
    })

    $('.AdditionQuestionsConfigurationForm').on('submit' , function(e){
    var labelValue = $('#labelValue2').val()
    var typeValue = $('#si-addition-input-for-Q').val()

    var si_addition = Array.from($('.Que'))
    var bool = CheckIfEmpty(si_addition)
    if(bool == false){
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
    }else{

    if(typeValue =='select'){
    var Values = $('#ValuesOfSelectBox2').val().split("  ")

    $.ajax({
    type: 'POST',
    url: '/QConfiguration',
    data: JSON.stringify({
    'label' : labelValue,
    'type'  : typeValue,
    'values': Values
    }),
    contentType: 'application/json;charset=UTF-8',
    success : function(data){
        alert(data)
    }
    });
    }else {
    $.ajax({
    type: 'POST',
    url: '/QConfiguration',
    data: JSON.stringify({
    'label' : labelValue,
    'type'  : typeValue
    }),
    contentType: 'application/json;charset=UTF-8',
    success : function(data){
        alert(data)
    }
    });
    }
    }

    e.preventDefault()
    })

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

 // cookie function
  function setCookie(cname, cvalue, exdays) {
  const d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  let expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
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