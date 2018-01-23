'use strict';

$(function(){
	var dialog = $('#category-modal')
	$('.edit-category-btn').click(function(event){
		event.preventDefault();
		dialog.modal('show');
		var categoryId = $(this).parent().parent().attr('data-category-id');
		console.log(categoryId)
		$('#category-submit-btn').attr('data-category-id',categoryId);

	});

	$('#category-submit-btn').click(function(){
		var categoryId = $('#category-submit-btn').attr('data-category-id');
		var name = $('#category-input').val();
		console.log('categoryId '+ categoryId +',name '+ name);
		xtajax.post({
			'url':'/cms/edit_category/',
			'data':{
				'category_id':categoryId,
				'name':name
			},
			'success':function(result){
				if (result['code'] == 200){
					$('.category-tr').each(function(){
						if($(this).attr("data-category-id") == categoryId){
							$(this).children().eq(0).html(name);
						}
					});
				}else{
					alert(result['message'])
				}
			},
			'error':function(err){
				alert(err)
			},
			'complete':function(){
				dialog.modal('hide')
			}
		});
	});
});


$(function(){
	$('.delete-category-btn').click(function(event){
		event.preventDefault();
		console.log('success...');
		var trTag = $(this).parent().parent();
		var categoryId = trTag.attr('data-category-id');
		var result = confirm('您确定要删除这个分类吗？');
		if (result){
			xtajax.post({
			'url':'/cms/delete_category/',
			'data':{
					'category_id':categoryId,
				},
			'success':function(res){
				if(res['code'] == 200){
					trTag.remove();
				}else{
					alert(res['message']);
				}

			},
			'error':function(err){
				alert(err);
			}
		
			
		
			});
		}
	});
});