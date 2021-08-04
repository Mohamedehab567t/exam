$(document).ready(function(){
// main settings

    $('.mainform').on('submit' , function(e){
    var SelectedLang = $('#lang').val()
    setCookie('Language' , SelectedLang , 1000000)
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

    e.preventDefault()
    })



 // cookie function
  function setCookie(cname, cvalue, exdays) {
  const d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  let expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}
})