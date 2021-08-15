$(document).ready(function(){
    $('.StudentInformation').on('submit' , function(e){
        var elements = Array.from($('.StudentInformation *'))
        var arr = CheckIfEmpty(elements)
        UpdateInformation(arr)
        e.preventDefault()
    })


    $('#langChange').on('click' , function(){
    var textLang = $(this).text()
    if(textLang == 'AR'){
    setCookie('Language' , 'Arabic' , 100000)
    window.location.reload()
    }else if (textLang == 'EN'){
    setCookie('Language' , 'English' , 100000)
    window.location.reload()
    }
    })

  function setCookie(cname, cvalue, exdays) {
  const d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  let expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

})
function CheckIfEmpty(el){
var eVal = []
el.forEach(e => {
if($(e).is('input') || $(e).is('select')){
var val = $(e).val()
eVal.push(val)
}
})
return eVal
}

function UpdateInformation(arrayOfVal){
var bool = true
for(var i =0; i < arrayOfVal.length; i++){
if(arrayOfVal[i] == ""){
alert("Please fill all your information")
bool = false
break
}
}
if(bool){
var Information = {}
var elements = Array.from($('.StudentInformation .Adi'))

elements.forEach(e => {
var val = $(e).val()
Information[$(e).data('label')] = val
})


$.ajax({
type: 'POST',
url: '/UpdateInformation',
data: JSON.stringify(Information),
contentType: 'application/json;charset=UTF-8',
success : function(data){
alert(data)
window.location.reload()
},
    error: function (jqXHR, exception) {
        var msg = '';
        if (jqXHR.status === 0) {
            msg = 'Not connect.\n Verify Network.';
        } else if (jqXHR.status == 404) {
            msg = 'Requested page not found. [404]';
        } else if (jqXHR.status == 500) {
            msg = 'Internal Server Error [500].';
        } else if (exception === 'parsererror') {
            msg = 'Requested JSON parse failed.';
        } else if (exception === 'timeout') {
            msg = 'Time out error.';
        } else if (exception === 'abort') {
            msg = 'Ajax request aborted.';
        } else {
            msg = 'Uncaught Error.\n' + jqXHR.responseText;
        }
        alert(msg);
    }
});
}
}


