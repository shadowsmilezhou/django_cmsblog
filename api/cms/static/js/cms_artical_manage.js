'use strtic';

$(function(){
	$('.delete-artical-btn').click(function(event){
		console.log('hahaha')
		event.preventDefault();
		var result = confirm("您确定要删除吗？");
		if (result){
			var trTag = $(this).parent().parent();
			var uid = trTag.attr('data-artical-id');

			xtajax.post({
				'url':'/cms/delete_artical/',
				'data':{
					'uid':uid
				},
				'success':function(result){
					if(result['code']==200){
						trTag.hide(1000,function(){
							trTag.remove();
							
						});
					}else{
						alert(result['message']);
					}
				},
				'error':function(error){
					alert(error);
				}
			});
		}
	});
});


//置顶文章的执行函数

$(function(){
	$('.top-artical-btn').click(function(event){
		event.preventDefault();
		var self = $(this);
		var trTag = $(this).parent().parent();
		var uid = trTag.attr('data-artical-id'); 
		var url = '/cms/top_artical/';
		if (self.html().indexOf('取消置顶') >= 0){
			url = '/cms/untop_artical/';
		}
		xtajax.post({
			'url':url,
			'data':{
				'uid':uid
			},
			'success':function(result){
				if(result['code']==200){
					//1.在标题前面添加[置顶]
					// var span = $('<span class="top-title-word">[置顶]</span>');
					// var titleTag = $(self).parent().siblings().first().children().eq(0);
					// var title = titleTag.text();
					// titleTag.html('');
					// titleTag.append(span);
					// titleTag.append(title);
					// self.html('取消置顶')
					window.location = '/cms/'

				}else{
					alert(result['message'])
				}
			},
			'error':function(){
				alert('error')
			},

		})
	});
});

$(function(){
	$('#category-select').change(function(){
		var categoryId = $(this).val();
		console.log(categoryId)
		window.location = '/cms/artical_manage/1/' + categoryId +'/'

	});
});