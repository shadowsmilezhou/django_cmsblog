'use strict';

$(function(){
	var editor,toolbar;
	toolbar = ['title','bold','italic','underline','strikethrough','fontScale','color','ol'    ,        'ul'     ,       'blockquote','code',    'link','image','hr',            'indent','outdent','alignment',];
	Simditor.locale = 'zh-CN';
	editor = new Simditor({
		textarea:$('#simditor'),
		toolbar:toolbar,
		pasteImage:true
	});
	//加到window上去，其他地方才能访问到这个变量
	window.editor = editor;
});

$(function(){
	var dialog = $('#category-modal')
	$('#category-btn').click(function(){
		dialog.modal('show')
	});

	$('#category-submit-btn').click(function(){
		
		var categoryInput = $('#category-input');
		var categoryName = categoryInput.val();
		
		xtajax.post({
			'url':'/cms/add_category/', 
			'data':{'categoryname':categoryName},
			'success':function(result){
				
				if (result['code'] == 200){
					var data = result['code'];
					var data = result['data'];  //一定要获取啊啊啊啊啊啊
					var select = $('#category-select');
					dialog.modal('hide');
					var option = $('<option></option>');
					option.attr('value',data['id']);
					option.html(data['name']);
					console.log(data['name']);
					select.append(option);
					select.children().last().attr('selected','selected').siblings().removeAttr('selected');

				}else{

				}
			},
			'error':function(error){
				console.log(error);
			}
			
		});

	});

});

$(function(){
	var dialog = $('#tag-modal')
	$('#tag-btn').click(function(){
		dialog.modal('show');
		console.log('coming');
		//弹出一个模态对话框
	});
	function addLableTag(){var data=result['data'];
		var label = $("<label class='checkbox-inline'></label>");
		var input = $("<input type='checkbox' />");
		input.val(data['id']);
		input.attr('checked','checked');
		label.append(input);
		label.append(data['name']);
		$('#tag-box').append(label);
	}
	$('#tag-submit-btn').click(function(){
		var tagElement = $('#tag-input');
		var tagname = tagElement.val();
		//提交到服务器
		xtajax.post({
			'url':'/cms/add_tag/', 
			'data':{'tagname':tagname},
			'success':function(result){
				
				if (result['code'] == 200){
					//1.原始的dom操作
					//请求正常
					//addLableTag()
					//2.第二种方式是通过aattemplate模板的方式进行创建
					var data = result['data'];
					var tpl = template('cms_tag_template',{'id':data['id'],'name':data['name']});
					$('#tag-box').append(tpl);
					dialog.modal('hide');
				}else{
					console.log(result['message'])

				}
			},
			'error':function(error){
				console.log(error);
			}
	});
});


//上传图片执行函数
$(function() {
	var domain = 'http://oxrm6w8zc.bkt.clouddn.com/';
	// var uploader = Qiniu.uploader({
	// 	runtimes: 'html5,flash,html4', //上传模式，依次退化
	// 	browse_button: 'thumbnail-btn', //上传选择的点选按钮，必须
		
	// 	max_file_size: '500mb', //文件最大允许的尺寸
	// 	dragdrop: true, //是否开启拖拽上传
	// 	chunk_size: '4mb', //分块上传时，每片的大小
	// 	uptoken_url: '/cms/get_token/', //ajax请求token的url
	// 	domain: domain, //图片下载时候的域名
	// 	get_new_uptoken: false, //是否每次上传文件都要从业务服务器获取token
	// 	auto_start: true, //是否自动上传
	// 	log_level: 5, //log级别
	// 	init:{
	// 		'FilesAdded': function(up,files) {
	// 			console.log('file added');
	// 		},
	// 		'BeforeUpload': function(up,file) {
	// 			console.log('before upload');
	// 		},
	// 		'UploadProgress': function() {
	// 			console.log('upload progress');
	// 		},
	// 		'FileUploaded': function(up,file,info) {
	// 			console.log('file uploaded-----------');
	// 			//发送文件名到服务器
	// 			var avatar = domain + file.name;//设置图片的完整路径
	// 			//把图片地址加入到src里面
	// 			console.log(avatar)
	// 			$('#thumbnail-input').val(avatar)
	// 			},
			
	// 		'Error': function(up,err,errTip) {
	// 			console.log('error:'+err);
	// 		}
	// 	},
	// });
	var uploader = xtqiniu.setUp({
	'browse_button':'thumbnail-btn',
	'success':function(up,file,info){
		var avatar = domain + file.name;
		$('#thumbnail-input').val(avatar);
	},
	'error':function(up,err,errTip){
		console.log(err);
	}
});



$(function(){
	$('#submit-artical-btn').click(function(){
		var titleElement = $('#title-input');
		var categoryElement = $('#category-select');
		var descElement = $('#desc-input');
		var thumbnailElement = $('#thumbnail-input');
		var tagElement = $('.tag-checkbox');

		//取值
		var title = titleElement.val();
		var category = categoryElement.val();
		var desc = descElement.val();
		var thumbnail = thumbnailElement.val();
		var tags = [];
		tagElement.each(function(){
			if ($(this).is(':checked')){
				var tagId = $(this).val();
				console.log(tagId)
				tags.push(tagId);
			}
		});

		var content_html = editor.getValue();
		var data = {
			'title':title,
			'category':category,
			'desc':desc,
			'thumbnail':thumbnail,
			'tags[]':tags,
			'content_html':content_html,
			'uid':titleElement.attr('data-artical-id'),
		};


		xtajax.post({
			'url':window.location.href,
			'data':data,

			'success':function(result){
				console.log(result['code'])
				if (result['code']==200){

					$('#submit-success-modal').modal('show');
					titleElement.val('');
					descElement.val('');
					thumbnailElement.val('');
					tagElement.removeAttr('checked');
					editor.setValue('');
				}else{
					alert(result['message']);
				}
			},
			'error':function(err){
				console.log(err)
			}
		});
	});
	$('#back-home-btn').click(function(){
		window.location = '/cms/';
	});	
	$('#write-again-btn').click(function(){
		$('#submit-success-modal').modal('hide');
		window.location = '/cms/add_artical/';
	});
});	
});	
});	

