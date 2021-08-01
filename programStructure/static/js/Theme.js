$(document).ready(function(){

var Ishere = checkCookie('Theme')
var color
if(Ishere){
color = getCookie('Theme').split('-')
ChangeTheme(color[0] , color[1])
}

    $('.nav-item').on('click' , function(e){
    var anchor = $(this).children()
    if(! $(e.target).hasClass('dropdown')){
    if(!Ishere){
        $(this).addClass("active").siblings().removeClass("active");
    }else{
        $(anchor).css("color" , ""+color[1])
        $(this).siblings().children().css("color" , "rgba(0,0,0,0.5)")
    }
    }
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
            $(e).attr("style" , "color :" +SelectedColor+" !important")
        }else if ($(e).hasClass('active')){
            $(e).attr("style" , "color :"+SelectedColor+" !important")
            console.log('Is active')
        }else if ($(e).hasClass('container-of-ws')){
            $(e).attr("style" , "border : 2px solid "+SelectedColor)
        }
    })
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
})