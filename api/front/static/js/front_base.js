'use strict'

$(function(){
	var url = window.location.href;

	if (url.indexOf('artical_list') > 0){
		var urlArray = url.split('/');
		var categoryId = urlArray[4];
		var liTag = $('#category-box').children('[data-category-id='+categoryId+']');
		console.log(liTag)
		liTag.addClass('active').siblings().removeClass('active');

	}else if(url.indexOf('artical_detail') > 0){
			var categoryId = $('h2.artical-title').attr('data-category-id');
			var liTag = $('#category-box').children('[data-category-id='+categoryId+']');
			liTag.addClass('active').siblings().removeClass('active');
		
	}else{
		$('#category-box').children().eq(0).addClass('active').siblings().removeClass('active');

	}
});