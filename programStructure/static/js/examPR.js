$(document).ready(function(){



$('.SHOWPHOTO').hide()
$('.SHOWCHOICEPHOTO').hide()
$('.SHOWCHOICEPHOTOBOTH').hide()

$('.ImageContainer').on('click' , function(){
    var ClassName = $(this).attr('class').substr($(this).attr('class').lastIndexOf(" "))
    var ClassNamaArray = ClassName.split(" ")
    $('#'+ClassNamaArray[1]).show()
})

$('.Showing').on('click' , function(){
    var ClassName = $(this).attr('class').substr($(this).attr('class').lastIndexOf(" "))
    var ClassNamaArray = ClassName.split(" ")
    var ele = document.getElementById(ClassNamaArray[1])
    $(ele).show()
})

$(window).on('click' , function(e){
    if($(e.target).hasClass('SHOWPHOTO') || $(e.target).hasClass('SHOWCHOICEPHOTO') ||$(e.target).hasClass('SHOWCHOICEPHOTOBOTH') ){
        $(e.target).hide()
    }
})
coloring()
function coloring(){
var D = []
var Container = Array.from($('.container').children())
Container.forEach(e => {
if($(e).hasClass('TextQ') || $(e).hasClass('ImageQ')){
D.push(e)
}
})
D.forEach(e => {
var index = D.indexOf(e)
if(index % 2 == 0 ){
$(e).css('background-color' , 'aliceblue')
}
})
}

})