#coding:utf-8
#这是一个将密码设置成加密状态的函数

import hashlib
import configs

def make_password(raw_password,salt=None):
	if not salt:
		salt = configs.PASSWORD_SALT

	hash_password = hashlib.md5(salt+raw_password).hexdigest()
	return hash_password


def check_password(raw_password,hash_password):
	if not raw_password:
		return False

	tmp_password = make_password(raw_password)
	if tmp_password == hash_password:
		return True
	else:
		return False

