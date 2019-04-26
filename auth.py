from flask import session
from functools import wraps

def requires_auth_role(role):
	def auth_decorator(func):
		@wraps(func)
		def auth_wrapper(*args, **kwargs):
			if 'auth_role' in session and session['auth_role'] == role:
				return func(*args, **kwargs)
			else:
				return '403 Forbidden', 403
		return auth_wrapper
	return auth_decorator
