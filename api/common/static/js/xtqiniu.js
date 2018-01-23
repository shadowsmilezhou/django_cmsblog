'use strict';
//var agrs = {'browser_button':'xxx','success':function(){},'error':function(){}}


var xtqiniu = {
	'setUp':function(args){
		var domain = 'http://oxrm6w8zc.bkt.clouddn.com/';
		var params = {
			runtimes: 'html5,flash,html4', //上传模式，依次退化
			// browse_button: 'thumbnail-btn', //上传选择的点选按钮，必须
			
			max_file_size: '500mb', //文件最大允许的尺寸
			dragdrop: false, //是否开启拖拽上传
			chunk_size: '4mb', //分块上传时，每片的大小
			uptoken_url: '/cms/get_token/', //ajax请求token的url
			domain: domain, //图片下载时候的域名
			get_new_uptoken: false, //是否每次上传文件都要从业务服务器获取token
			auto_start: true, //是否自动上传
			log_level: 5, //log级别
			init:{
				'FileUploaded': function(up,file,info) {
					if (args['success']){
						var success = args['success'];
						success(up,file,info);
					}
				},
			
			'Error': function(up,err,errTip) {
				if (args['error']){
					var error = args['error'];
					error(up,err,errTip);
					}
				
				}
			},

		};
		for (var key in args){
			params[key] = args[key];
		}
		var uploader = Qiniu.uploader(params);
		return uploader;
	}
};