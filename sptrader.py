import cffi
from ctypes import *
import ctypes
import atexit
import os
location = os.path.dirname(os.path.realpath(__file__))
dll_location = os.path.join(location, "dll")
ctypes.windll.LoadLibrary(os.path.join(dll_location, "libeay32.dll"))
ctypes.windll.LoadLibrary(os.path.join(dll_location, "ssleay32.dll"))
ctypes.windll.LoadLibrary(os.path.join(dll_location, "spapidllm32.dll"))
sp = ctypes.windll.spapidllm32
sp.SPAPI_SetLanguageId(0)
sp.SPAPI_Initialize()
LOGIN_FUNC = WINFUNCTYPE(None, c_long, c_char_p)
# Remember to convert unicode strings to byte strings otherwise
# ctypes will assume that the characters are wchars and not
# ordinary characters

class SPTrader(object):
    def __init__(self,
                 host,
                 port,
                 license,
                 app_id,
                 user_id,
                 password):
        self.user = user_id.encode("utf-8")
        sp.SPAPI_SetLoginInfo(host.encode("utf-8"),
                              port,
                              license.encode("utf-8"),
                              app_id.encode("utf-8"),
                              user_id.encode("utf-8"),
                              password.encode("utf-8"))
    def login(self, callback=None):
        sp.SPAPI_Login()
        if callback != None:
            sp.SPAPI_RegisterLoginReply(callback)
    def get_login_status(self, status_id):
        return sp.SPAPI_GetLoginStatus(self.user, status_id)
    def logout(self):
        return sp.SPAPI_Logout(self.user)
    
        
#def cleanup():
#    sp.SPAPI_Uninitialize()

#atexit.register(cleanup)
