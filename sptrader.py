import cffi
import ctypes
import atexit
import os
location = os.path.dirname(os.path.realpath(__file__))
dll_location = os.path.join(location, "dll")
ctypes.windll.LoadLibrary(os.path.join(dll_location, "libeay32.dll"))
ctypes.windll.LoadLibrary(os.path.join(dll_location, "ssleay32.dll"))
ctypes.windll.LoadLibrary(os.path.join(dll_location, "spapidllm32.dll"))
sp = ctypes.windll.spapidllm32
sp.SPAPI_Initialize()

class SPTrader(object):
    def __init__(self,
                 host,
                 port,
                 license,
                 app_id,
                 user_id,
                 password):
        self.user = user_id
        sp.SPAPI_SetLoginInfo(host,
                              port,
                              license,
                              app_id,
                              user_id,
                              password)
    def login(self):
        return sp.SPAPI_Login()
    def get_login_status(self, host_id):
        return sp.SPAPI_GetLoginStatus(self.user, host_id)
    def logout(self):
        return sp.SPAPI_Logout(self.user)
    
        
#def cleanup():
#    sp.SPAPI_Uninitialize()

#atexit.register(cleanup)
