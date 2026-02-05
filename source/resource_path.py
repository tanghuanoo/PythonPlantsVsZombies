"""
资源路径辅助模块

支持 PyInstaller 打包后的资源路径解析。
打包后资源会被解压到临时目录，需要使用 sys._MEIPASS 获取正确路径。
"""

import os
import sys


def get_base_path():
    """获取资源基础路径

    Returns:
        str: 打包后返回临时目录路径，开发环境返回项目根目录
    """
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后的运行环境
        return sys._MEIPASS
    else:
        # 开发环境，返回项目根目录
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def resource_path(*paths):
    """获取资源文件的绝对路径

    Args:
        *paths: 相对于项目根目录的路径组件

    Returns:
        str: 资源文件的绝对路径

    Example:
        resource_path('resources', 'graphics')
        resource_path('source', 'data', 'map', 'level_1.json')
    """
    return os.path.join(get_base_path(), *paths)


def get_user_data_path():
    """获取用户数据目录路径（用于存储配置、存档等可写文件）

    打包后资源目录是只读的，需要将配置文件等写入用户目录。

    Returns:
        str: 用户数据目录路径
    """
    if getattr(sys, 'frozen', False):
        # 打包后使用 exe 所在目录
        return os.path.dirname(sys.executable)
    else:
        # 开发环境使用项目根目录
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def user_data_path(*paths):
    """获取用户数据文件的绝对路径

    Args:
        *paths: 相对于用户数据目录的路径组件

    Returns:
        str: 用户数据文件的绝对路径
    """
    return os.path.join(get_user_data_path(), *paths)


def is_frozen():
    """检查是否在打包环境中运行

    Returns:
        bool: 打包环境返回 True，开发环境返回 False
    """
    return getattr(sys, 'frozen', False)
