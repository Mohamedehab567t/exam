$(document).ready(function(){
// main settings
    $('.c').on('click' , function(){
      $(this).addClass('SelectedColor').siblings().removeClass("SelectedColor");
      color = $(this).data('color')
      ChangeTheme(color,'SelectedColor')
    })
    $('.mainform').on('submit' , function(e){
      var SiteName = $('#exampleInputEmail1').val()
      var ColorsDivArray = Array.from($('.colors').children())
      var SelectedColor
      var color
      ColorsDivArray.forEach(e => {
        if($(e).hasClass('SelectedColor')){
            var arrayS = $(e).attr('class')
          SelectedColor = arrayS.split(" ")[1]
          color = $('.SelectedColor').css('background-color')
        }
      })
                $.ajax({
                type: 'POST',
                url: '/Changing',
                data: JSON.stringify({'SiteName' : SiteName}),
                contentType: 'application/json;charset=UTF-8',
                success : function(data){

                }
                });
          setCookie('Theme' , ""+SelectedColor+"-"+color , 1000000)
    })

    function ChangeTheme(color , SelectedColor){
    var element = Array.from($("*"));
    element.forEach(e => {
        if($(e).hasClass('alert-success') ||
         $(e).hasClass('alert-danger') ||
         $(e).hasClass('alert-info') ||
         $(e).hasClass('alert-warning')||
         $(e).hasClass('alert-secondary')){
            if(color == 'green'){
            var arrayS = $(e).attr('class')
            $(e).removeClass(arrayS.split(" ")[2]);
            $(e).addClass('alert-success')
            }else if (color == 'blue'){
            var arrayS = $(e).attr('class')
            $(e).removeClass(arrayS.split(" ")[2]);
            $(e).addClass('alert-info')
            }else if (color == 'yellow'){
            var arrayS = $(e).attr('class')
            $(e).removeClass(arrayS.split(" ")[2]);
            $(e).addClass('alert-warning')
            }else if (color == 'black'){
            var arrayS = $(e).attr('class')
            $(e).removeClass(arrayS.split(" ")[2]);
            $(e).addClass('alert-secondary')
            }else if (color == 'red') {
            var arrayS = $(e).attr('class')
            $(e).removeClass(arrayS.split(" ")[2]);
            $(e).addClass('alert-danger')
            }
        }else if ($(e).hasClass('btn-success') ||
        $(e).hasClass('btn-warning') ||
        $(e).hasClass('btn-danger')||
        $(e).hasClass('btn-info') ||
        $(e).hasClass('btn-secondary')){
            if(color == 'green'){
            var arrayS = $(e).attr('class')
            $(e).removeClass(arrayS.split(" ")[1]);
            $(e).addClass('btn-success')
            }else if (color == 'blue'){
            var arrayS = $(e).attr('class')
            $(e).removeClass(arrayS.split(" ")[1]);
            $(e).addClass('btn-info')
            }else if (color == 'yellow'){
            var arrayS = $(e).attr('class')
            $(e).removeClass(arrayS.split(" ")[1]);
            $(e).addClass('btn-warning')
            }else if (color == 'black'){
            var arrayS = $(e).attr('class')
            $(e).removeClass(arrayS.split(" ")[1]);
            $(e).addClass('btn-secondary')
            }else if (color == 'red') {
            var arrayS = $(e).attr('class')
            $(e).removeClass(arrayS.split(" ")[1]);
            $(e).addClass('btn-danger')
            }
        }else if ($(e).hasClass('Variable')){
            $(e).attr("style" , "color :"+$("."+SelectedColor).css('background-color')+" !important")
        }else if ($(e).hasClass('active')){
            $(e).attr("style" , "color :"+$("."+SelectedColor).css('background-color')+" !important")
        }
    })
    }




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