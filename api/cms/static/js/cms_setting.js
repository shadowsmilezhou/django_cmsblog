
'use strict';

$(function() {
	var domain = 'http://oxrm6w8zc.bkt.clouddn.com/';
	
	var uploader=xtqiniu.setUp({

		'browse_button':'pickfiles',
		'success':function(up,file,info){
			var avatar = domain + file.name;
			$('#pickfiles').attr('src',avatar);
		},
		'error':function(up,err,errTip){
			console.log(err);

		}
	});


	// var domain = 'http://oxrm6w8zc.bkt.clouddn.com/';
	// var uploader = Qiniu.uploader({
	// 	runtimes: 'html5,flash,html4', //上传模式，依次退化
	// 	browse_button: 'pickfiles', //上传选择的点选按钮，必须
	// 	container: 'container',	//上传区域DOM的ID，默认是browse_button的父元素
	// 	drop_element: 'container', //拖曳上传区域元素的ID，拖曳文件或文件夹后可触发上传
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
	// 			$('#pickfiles').attr('src',avatar)
	// 			},
			
	// 		'Error': function(up,err,errTip) {
	// 			console.log('error:'+err);
	// 		}
	// 	},
	
	//点击按钮提交事件
	
	$('.submit-btn').click(function(event) {
		event.preventDefault();
		console.log('haha');
		var username = $('.username-input').val();
		//说明有图片上传了
		var avatar = null;

		if(uploader.files.length > 0){
			//src代表的就是上传的头像url
			avatar = $('#pickfiles').attr('src');
		}
		// 说明客户端没有修改图片
			// 此时直接修改用户名就可以了
		var data = {'username':username};
		if (avatar){
			data['avatar'] = avatar; 
		}
		console.log(data['avatar']);
		// $.ajax({
		// 	'url': '/cms/update_profile/',
		// 	'method': 'post',
		// 	'data':data,
		// 	'success': function(data) {
		// 		console.log(data['code'])
		// 		if(data['code'] == 200){
		// 			var alert = $('.alert-success');
		// 			alert.html('更新成功');
		// 			alert.show();
		// 		}
		// 	},
		// 	'error': function(error) {
		// 		console.log(error);
		// 	},
		// 	'beforeSend':function(xhr,settings) {
		// 		var csrftoken = getCookie('csrftoken');
		// 		//2.在header当中设置csrf_token的值
		// 		xhr.setRequestHeader('X-CSRFToken',csrftoken);
		// 	}
		// });
		xtajax.ajax({

			'url': '/cms/update_profile/',
			'method': 'post',
			'data':data,
			'success': function(data) {
				console.log(data['code'])
				if(data['code'] == 200){
					var alert = $('.alert-success');
					alert.html('更新成功');
					alert.show();
				}
			},
			'error': function(error) {
				console.log(error);
			},


		});
	});
});



