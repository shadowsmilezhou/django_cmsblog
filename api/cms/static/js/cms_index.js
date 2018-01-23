/**
 * Created by Administrator on 2017/10/9/009.
 */


$(document).ready(function () {
    //1.获取当前url
    var c_url = window.location.href;
    console.log(c_url);
    console.log(c_url.indexOf('add_artical'));
    var c_index = 0;
    if (c_url.indexOf('add_artical') >0){
        c_index = 1;
    }else if(c_url.indexOf('settings') >0 ){
        c_index = -1;
    } else{
        c_index = 0;
    }
    var ulTag = $('.menu-li');
    if (c_index >= 0) {
        ulTag.children().eq(c_index).addClass('active').siblings().removeClass('active');
    }else{
        ulTag.children().removeClass('active');
    }
});