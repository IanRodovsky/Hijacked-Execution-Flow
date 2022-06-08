import os
import winreg


def read_path_value(reg_hive, reg_path):
    reg = winreg.ConnectRegistry(None, reg_hive)
    key = winreg.OpenKey(reg, reg_path, access=winreg.KEY_READ)
    index = 0
    while True:
        try:
            val = winreg.EnumValue(key, index)
            if val[0] == 'Path':
                return val[1]
            index += 1
        except OSError:
            break


def edit_path_value(reg_hive, reg_path, target_dir):
    path = read_path_value(reg_hive, reg_path)
    new_path = f'{target_dir};{path}'
    reg = winreg.ConnectRegistry(None, reg_hive)
    key = winreg.OpenKey(reg, reg_path, access=winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path)


target_dir = os.getcwd()

# Modify USER path
reg_hive = winreg.HKEY_CURRENT_USER
reg_path = 'Environment'

# Modify SYSTEM path
# reg_hive = winreg.HKEY_LOCAL_SYSTEM
# reg_path = 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'

edit_path_value(reg_hive, reg_path, target_dir)
