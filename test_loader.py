import cffi
import os
import ctypes
location = os.path.dirname(os.path.realpath(__file__))
dll_location = os.path.join(location, "dll")
print ("Testing loader")
print ("Loading dlls from directory '%s'" % dll_location)
ctypes.windll.LoadLibrary(os.path.join(dll_location, "libeay32.dll"))
ctypes.windll.LoadLibrary(os.path.join(dll_location, "ssleay32.dll"))
ctypes.windll.LoadLibrary(os.path.join(dll_location, "spapidllm32.dll"))
print(ctypes.windll.spapidllm32)

sptrader = ctypes.windll.spapidllm32;
print(sptrader.SPAPI_Initialize())

input("Press any key to exit")

