import enum
from flask_login import current_user

class Permissions(enum.Enum):
    no_permissions = 0
    default_account = 1
    admin_account = 2
    dev_account = 3

def role_to_text(role: int) -> str:
    '''Convert role to text'''
    if role == Permissions.no_permissions.value:
        return 'Нет разрешений'
    elif role == Permissions.default_account.value:
        return 'Стандартный аккаунт'
    elif role == Permissions.admin_account.value:
        return 'Администратор'
    elif role == Permissions.dev_account.value:
        return 'Аккаунт разработчика'
    else:
        return 'Не установленные разрешения'
    
def get_user_role():
    '''Gets current user role'''
    if current_user.is_authenticated:
        return current_user.role
    else:
        return 0
    
def is_admin(role):
    '''Returns True if user is admin or dev'''
    if role == 2 or role == 3:
        return True
    return False

def is_current_user_admin():
    '''Returns True if current user is admin or dev'''
    return is_admin(get_user_role())