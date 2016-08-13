from cffi import FFI
import atexit
import os
location = os.path.dirname(os.path.realpath(__file__))
dll_location = os.path.join(location, "..", "dll")
ffi = FFI()
ffi.cdef("""
typedef void (__stdcall *LoginReplyAddr)(long ret_code, char* ret_msg);
typedef void (__stdcall *AccountLoginReplyAddr)(char *accNo, long ret_code, char* ret_msg);
typedef void (__stdcall *AccountLogoutReplyAddr)(long ret_code, char *ret_msg);

int SPAPI_SetLanguageId(int langid);
int SPAPI_Initialize();
void SPAPI_SetLoginInfo(char *host, int port, char *license, char *app_id, char *user_id, char *password);
int SPAPI_Login();
int SPAPI_GetLoginStatus(char *user_id, short host_id);
void SPAPI_RegisterLoginReply(LoginReplyAddr addr);
int SPAPI_Logout(char *user_id);
void SPAPI_RegisterAccountLoginReply(AccountLoginReplyAddr addr);
void SPAPI_RegisterAccountLogoutReply(AccountLogoutReplyAddr addr);
void SPAPI_Uninitialize();
""")
ffi.dlopen(os.path.join(dll_location, "libeay32.dll"))
ffi.dlopen(os.path.join(dll_location, "ssleay32.dll"))
sp = ffi.dlopen(os.path.join(dll_location, "spapidllm32.dll"))
sp.SPAPI_SetLanguageId(0)
sp.SPAPI_Initialize()

# Remember to convert unicode strings to byte strings otherwise
# ctypes will assume that the characters are wchars and not
# ordinary characters

class SPTrader(object):
    ffi = ffi
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
