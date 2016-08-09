import cffi
import ctypes
print ("Testing loader")
ctypes.windll.LoadLibrary("dll\\libeay32.dll")
ctypes.windll.LoadLibrary("dll\\ssleay32.dll")
ctypes.windll.LoadLibrary("dll\\spapidllm32.dll")
print(ctypes.windll.spapidllm32)

input("Press any key to exit")

