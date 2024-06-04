import json
import ctypes

lib = './crashMe.so'
funcs = ctypes.cdll.LoadLibrary(lib)

# void init()
init = funcs.init

# int setString(char *data);
setString = funcs.setString
setString.argtypes = [ctypes.c_char_p]
setString.restype = ctypes.c_int

# # int getString();

# getString = funcs.getString
# getString.restype = ctypes.c_int

# # int delString();
# delString = funcs.delString
# delString.restype = ctypes.c_int

# # int setNum(uint64_t data);
# setNum = funcs.setNum
# setNum.argtypes = [ctypes.c_uint64]
# setNum.restype = ctypes.c_int

# # int getNum();
# getNum = funcs.getNum
# getNum.restype = ctypes.c_int

# # int delNum();
# delNum = funcs.delNum
# delNum.restype = ctypes.c_int

# init()
# print("Hello! CrashMe!")

# while True:
#     argc = 0
#     args = None
#     received = input()
#     try:
#         received = json.loads(received)
#         if received['callNum'] is None:
#             raise Exception("Invalid Parameter")

#         callNum = received['callNum']
#         if received['args'] is not None:
#             argc = len(received['args'])
#             args = received['args']
        
#         if callNum == 1:
#             if argc != 1:
#                 raise Exception("Invalid Parameter")
#             data = ctypes.c_char_p(args[0].encode())
#             setString(data)

#         elif callNum == 2:
#             getString()

#         elif callNum == 3:
#             delString()

#         elif callNum == 4:
#             if argc != 1:
#                 raise Exception("Invalid Parameter")
#             setNum(ctypes.c_uint64(args[0]))

#         elif callNum == 5:
#             getNum()

#         elif callNum == 6:
#             delNum()

#         else:
#             raise Exception("Invalid Parameter")
#         print("Done")

#     except json.decoder.JSONDecodeError:
#         print("The input must be in JSON format")
#         exit()
        
#     except Exception as e:
#         print(e)
#         exit()

print(init)