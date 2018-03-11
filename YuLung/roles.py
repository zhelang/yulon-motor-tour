from rolepermissions.roles import AbstractUserRole

class Staff(AbstractUserRole):
    
    available_permissions = {
            'view_site_admin':True,
            'edit_site_admin':True
        }
    
    
class Manager(AbstractUserRole):
    
    available_permissions = {
            'view_site_admin':True,
            'edit_site_admin':False
        }