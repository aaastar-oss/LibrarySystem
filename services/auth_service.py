from db.database_user import get_user_by_username, create_user
import hashlib
import traceback
import secrets
from typing import Optional, Dict

ADMIN_SECRET_CODE = "ADMIN123"  # 管理员注册密码
MIN_PASSWORD_LENGTH = 8  # 最小密码长度
MAX_PASSWORD_LENGTH = 32  # 最大密码长度

def _secure_compare(a: str, b: str) -> bool:
    """安全比较两个字符串，防止时序攻击"""
    if len(a) != len(b):
        return False
        
    result = 0
    for x, y in zip(a, b):
        result |= ord(x) ^ ord(y)
    return result == 0

def _hash_password(password: str, salt: str = None) -> str:
    """密码哈希处理"""
    salt = salt or secrets.token_hex(16)  # 使用更安全的
    salted_password = salt + password
    return f"{salt}${hashlib.sha256(salted_password.encode()).hexdigest()}"

def authenticate(username: str, password: str) -> Optional[Dict[str, str]]:
    """
    认证用户
    :param username: 用户名
    :param password: 密码
    :return: 用户信息字典或None
    :raises: ValueError 当输入无效时
    """
    if not isinstance(username, str) or not username.strip():
        raise ValueError("无效的用户名")
    
    if not isinstance(password, str) or not password.strip():
        raise ValueError("无效的密码")
    
    try:
        user = get_user_by_username(username.strip())
        if not user or 'password' not in user:
            return None
        
        # 解析存储的密码 (格式: salt$hash)
        stored_parts = user['password'].split('$')
        if len(stored_parts) != 2:
            return None
            
        salt, stored_hash = stored_parts
        hashed_input = hashlib.sha256((salt + password).encode()).hexdigest()
        
        if not _secure_compare(hashed_input, stored_hash):
            return None
        
        return {
            'username': user['username'],
            'role': user.get('role', 'user')  # 默认普通用户
        }
        
    except Exception as e:
        print(f"[AUTH ERROR] 认证出错: {str(e)}")
        print(traceback.format_exc())
        return None

def register(username: str, password: str, phone: str, email: str, 
            is_admin: bool = False, admin_secret: str = None) -> bool:
    """
    注册新用户
    :param username: 用户名 (4-20字符)
    :param password: 密码 (8-32字符)
    :param phone: 电话
    :param email: 邮箱
    :param is_admin: 是否管理员
    :param admin_secret: 管理员验证码
    :return: 是否注册成功
    :raises: ValueError 当输入无效时
    """
    # 参数验证
    if not all(isinstance(x, str) for x in [username, password, phone, email]):
        raise ValueError("所有字段都必须为字符串")
    
    username = username.strip()
    if len(username) < 4 or len(username) > 20:
        raise ValueError("用户名长度需在4-20个字符之间")
    
    if len(password) < MIN_PASSWORD_LENGTH or len(password) > MAX_PASSWORD_LENGTH:
        raise ValueError(f"密码长度需在{MIN_PASSWORD_LENGTH}-{MAX_PASSWORD_LENGTH}个字符之间")
    
    if is_admin and (not admin_secret or admin_secret != ADMIN_SECRET_CODE):
        raise ValueError("管理员验证码错误")
    
    try:
        # 检查用户名是否已存在
        if get_user_by_username(username):
            raise ValueError("用户名已存在")
        
        # 密码加密
        hashed_pwd = _hash_password(password)
        
        # 创建用户
        success = create_user(
            username=username,
            password=hashed_pwd,
            phone=phone.strip(),
            email=email.strip(),
            role='admin' if is_admin else 'user',
            max_borrow=10 if is_admin else 2
        )
        
        if not success:
            raise RuntimeError("数据库创建用户失败")
            
        return True
        
    except ValueError:
        raise  # 重新抛出已知错误
    except Exception as e:
        print(f"[REGISTER ERROR] 注册出错: {str(e)}")
        print(traceback.format_exc())
        raise RuntimeError("注册过程中发生系统错误") from e

def validate_password_strength(password: str) -> bool:
    """验证密码强度"""
    if len(password) < MIN_PASSWORD_LENGTH:
        return False
        
    # 检查是否包含数字、字母和特殊字符
    has_digit = any(c.isdigit() for c in password)
    has_letter = any(c.isalpha() for c in password)
    has_special = any(not c.isalnum() for c in password)
    
    return has_digit and has_letter and has_special