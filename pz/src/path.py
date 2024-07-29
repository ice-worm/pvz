import os
import sys  
  
# 假设你有一个函数来获取资源文件夹的路径  
def get_resource_path(relative_path):  
    try:  
        # PyInstaller 创建了一个临时目录，并将所有文件放入其中  
        # 你可以通过 sys._MEIPASS 来访问这些文件（但请注意，这仅在打包后有效）  
        base_path = sys._MEIPASS  
    except AttributeError:  
        # 如果不是通过 PyInstaller 运行的，则使用当前工作目录  
        base_path = os.path.abspath(".")  
      
    return os.path.join(base_path, relative_path)  
  