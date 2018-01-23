/**
 * Created by Administrator on 2017/10/10/010.
 *
 **/

$(function () {
    $('.captcha-imgs').click(function () {

        var old_src = $(this).attr('src');
        var src = old_src + '?' + Math.random();
        $(this).attr('src',src);
    });
});
