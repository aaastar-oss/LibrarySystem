# services/auth_service.py
from db.database_user import get_user_by_username, create_user
import hashlib

ADMIN_SECRET_CODE = "ADMIN123"  # 管理员注册密码

def authenticate(username: str, password: str) -> dict:
    """认证用户"""
    user = get_user_by_username(username)
    if not user or 'password' not in user:
        return None
    
    # 验证密码
    hashed_input = hashlib.sha256(password.encode()).hexdigest()
    if hashed_input != user['password']:
        return None
    
    return {
        'username': user['username'],
        'role': user['role']
    }

def register(username: str, password: str, phone: str, email: str, is_admin: bool = False, admin_secret: str = None) -> bool:
    """注册新用户"""
    # 检查用户名是否已存在
    if get_user_by_username(username):
        return False
    
    # 如果是管理员注册，验证管理员密码
    if is_admin and admin_secret != ADMIN_SECRET_CODE:
        return False
    
    # 密码加密
    hashed_pwd = hashlib.sha256(password.encode()).hexdigest()
    
    # 创建用户
    return create_user(
        username=username,
        password=hashed_pwd,
        phone=phone,
        email=email,
        role='admin' if is_admin else 'user',
        max_borrow=10 if is_admin else 5  # 管理员借阅上限更高
    )