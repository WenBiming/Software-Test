#!/usr/bin/python3
# coding=utf-8
################################################################################
#Function: 本框架主要将文字识别技术与Linux系统中模拟键盘输入和鼠标操作的方法相结合，
# 提供了基于xdotool实现对应用操作(启动应用，关闭应用，重启应用)、窗口操作(获取窗口ID，获取窗口名称，移动窗口，最小化窗口，置顶窗口等)，
# 基于Scrot+PyAutoGUI实现截图操作(截取全屏，截取窗口，截取指定大小矩形等)以及基于PaddleOCR实现文字识别操作，该框架环境搭建简单，通用性强，语法简单，
# 对于不同的软件都可达到自动化测试用例快速开发的目的。
#Platform:ALL
#Author: Pengfei Wang
#Date: 2022/01/18
#Company: Kylin Software Co.,Ltd.
################################################################################
import os
import time
import requests
import sys
import json
import pyautogui
from libs.config import OCR_URL

#--------------------------------------------------------应用方法--------------------------------------------------------------
def start_app(exec_commend) ->bool:
    """
    启动应用方法
    Parameters:
     param1 - 启动命令
    Returns:
        True:启动成功
        False:启动失败
    """
    # 判断是否为字符串
    if not isinstance(exec_commend,str):
        print('启动命令输入错误,启动命令应为字符串类型！')
        return False
    # 执行启动命令
    start_res = os.system(exec_commend)
    # 查进程
    res = os.system(f'ps -ef|grep {exec_commend.split()[-1]}|grep -v grep')
    # 判断是否启动成功
    if res == 0 and start_res == 0:
        print('-----------------应用启动成功--------------------')
        return True
    else:
        print('-----------------应用启动失败--------------------')
        return False


def close_app(app_name) ->bool:
    """
    关闭应用方法
    Parameters:
     param1 - 应用名称
    Returns:
        True:关闭成功
        False:关闭失败
    """
    # 判断是否为字符串
    if not isinstance(app_name,str):
        print('启动命令输入错误,启动命令应为字符串类型！')
        return False
    # 查杀进程
    os.system(f"ps -ef|grep {app_name}|grep -v grep|awk "+"'{print \"kill -9 \"$2}'"+"|sh")
    # 查结果
    res = os.system(f'ps -ef|grep {app_name}|grep -v grep')
    # 结果判断
    if res == 0:
        print('-----------------应用关闭失败--------------------')
        return False
    else:
        print('-----------------应用关闭成功--------------------')
        return True

def restart_app(exec_commend) -> bool:
    """
    重启应用方法
    Parameters:
     param1 - 启动命令
    Returns:
        True:重启成功
        False：重启失败
    """
    # 判断是否为字符串
    if not isinstance(exec_commend, str):
        print('启动命令输入错误,启动命令应为字符串类型！')
        return False
    # 查杀进程
    os.system(f"ps -ef|grep {exec_commend.split()[-1]}|grep -v grep|awk " + "'{print \"kill -9 \"$2}'" + "|sh")
    # 查看查杀结果
    res1 = os.system(f'ps -ef|grep {exec_commend.split()[-1]}|grep -v grep')
    # 查杀结果判断
    if res1 == 0:
        print('-----------------应用关闭失败--------------------')
        return False
    else:
        # 启动应用
        os.system(exec_commend)
        # 査进程
        res2 = os.system(f'ps -ef|grep {exec_commend.split()[-1]}|grep -v grep')
        # 判断启动结果
        if res2 == 0:
            print('-----------------应用重启成功--------------------')
            return True
        else:
            print('-----------------应用启动失败--------------------')
            return False


#--------------------------------------------------------窗口方法--------------------------------------------------------------
def _get_window_id_with_pid(pid) ->str:
    """
    根据进程ID获取窗口ID(一个进程ID对应多个窗口ID时可能导致结果不准确)
    Parameters:
     param1 - 进程ID
    Returns:
        str:窗口ID
    """
    pid = str(pid)
    if pid.isdigit():
        res = os.popen(f'xdotool search --pid {pid}')
        res_ID = res.read()[:-1:]
        if res_ID =='':
            print('没有找到对应的窗口ID')
            return  ''
        return res_ID
    else:
        return ''



def get_window_id_with_window_name(window_name) ->str:
    """
    根据窗口名称获取窗口ID
    Parameters:
     param1 - 窗口名称
    Returns:
        str:窗口ID
    """
    # 判断是否为字符串
    if not isinstance(window_name, str):
        print('窗口名称输入错误,启动命令应为字符串类型！')
        return ''
    # 获得窗口ID数组
    res = os.popen(f'xdotool search -n {window_name}| tail -1')
    # 获得窗口ID
    res_ID = res.read()[:-1:]
    # 结果判断
    if res_ID =='':
        print('没有找到正在运行的窗口',window_name)
        return ''
    return res_ID


def _get_window_id_with_start_command(start_command) ->str:
    """
    根据启动命令获取窗口ID(一个进程ID对应多个窗口ID时可能导致结果不准确)
    Parameters:
     param1 - 应用名称
    Returns:
        str:窗口ID
    """
    pid = os.popen(f"ps -ef | grep {start_command.split()[-1]}"+"| grep -v grep | awk '{ print $2 }'").readline()[:-1:]
    if pid =='':
        print('没有找到正在运行的程序',start_command)
        return ''
    res = os.popen(f'xdotool search --pid {pid}')
    return res.read()[:-1:]


def get_window_id_with_mouse_location() ->str:
    """
    获取鼠标当前位置的窗口ID
    Parameters:None
    Returns:
        str:窗口ID
    """
    res = os.popen("xdotool getmouselocation").readline()[:-1:].split(" ")
    window_id = res[3][res[3].index(':')+1::]
    return window_id


def get_pid_with_window_id(window_id) ->str:
    """
    根据窗口ID获取进程ID
    Parameters:
     param1 - 窗口ID
    Returns:
        str:进程ID
    """
    # 判断是否为数字
    window_id_str = str(window_id)
    if window_id_str.isdigit():
        # 获取进程ID
        pid = os.popen(f"xdotool getwindowpid {window_id}").readline()[:-1:]
        # 判断结果
        if pid == '':
            print('没有找到对应的进程ID')
            return ''
        return pid
    else:
        print(window_id,'输入错误，window_id应为数字')
        return ''


def get_window_name_with_window_id(window_id) ->str:
    """
    根据窗口ID获取窗口名称
    Parameters:
     param1 - 窗口ID
    Returns:
        str:窗口名称
    """
    # 判断是否为数字
    window_id_str = str(window_id)
    if window_id_str.isdigit():
        # 获取窗口名称
        window_name = os.popen(f"xdotool getwindowname {window_id}").readline()[:-1:]
        # 结果判断
        if window_name == '':
            print('没有找到对应的窗口ID')
            return ''
        return window_name
    else:
        print(window_id, '输入错误，window_id应为数字')
        return ''


def get_screen_size() ->list:
    """
    获取屏幕分辨率
    Parameters:None
    Returns:
        list:[宽度, 高度]
    """
    screen_size = os.popen("xdotool getdisplaygeometry").readline()[:-1:].split(' ')
    return screen_size


def get_window_size(window_id) ->list:
    """
    根据窗口ID获取窗口尺寸
    Parameters:
     param1 - 窗口ID
    Returns:
        list:[窗口宽度, 窗口高度]
    """
    window_id_str = str(window_id)
    # 判断是否为数字
    if window_id_str.isdigit():
        # 获取宽度
        window_width = os.popen(
            f"xdotool getwindowgeometry {window_id} | grep Geometry | sed -r \"s/[^0-9]*([0-9]+)x([0-9]+)/\\1/g\"").readline()[:-1:]
        # 结果判断
        if window_width=='':
            print('没有找到对应的窗口ID')
            return []
        # 获取高度
        window_height = os.popen(
            f"xdotool getwindowgeometry {window_id} | grep Geometry | sed -r \"s/[^0-9]*([0-9]+)x([0-9]+)/\\2/g\"").readline()[:-1:]
        # 结果判断
        if window_height == '':
            print('没有找到对应的窗口ID')
            return []
        return [window_width, window_height]
    else:
        print(window_id, '输入错误，window_id应为数字')
        return []


def top_window(window_id) -> bool:
    """
    置顶窗口
    Parameters:
     param1 - 窗口ID
    Returns:
        置顶成功:True
        置顶失败:False
    """
    # 判断是否为数字
    window_id_str = str(window_id)
    if window_id_str.isdigit():
        # 置顶窗口
        res = os.system(f"xdotool windowactivate {window_id}")
        # 结果判断
        if res == 0:
            print(f"{window_id}置顶成功")
            return True
        else:
            print(f"{window_id}置顶失败")
            return False
    else:
        print(window_id, '输入错误，window_id应为数字')
        return False


def move_window(window_id, width, height):
    """
    将窗口移动到某处
    Parameters:
     param1 - 窗口ID
     param2 - 横坐标
     param3 - 纵坐标
    Returns:
        移动成功:True
        移动失败:False
    """
    if not str(window_id).isdigit():
        print(window_id, '输入错误，window_id应为数字')
        return False
    elif not str(width).isdigit():
        print(width, '输入错误，width应为数字')
        return False
    elif not str(height).isdigit():
        print(height, '输入错误，height应为数字')
        return False
    else:
        res = os.system(f"xdotool windowmove {window_id} {width} {height}")
        if res == 0:
            print(f'{window_id}窗口移动成功')
            return True
        else:
            print(f'{window_id}窗口移动失败')
            return False


def minimize_window(window_id):
    """
    最小化窗口
    Parameters:
     param1 - 窗口ID
    Returns:
        最小化窗口成功:True
        最小化窗口失败:False
    """
    # 判断是否为数字
    if str(window_id).isdigit():
        # 最小化窗口
        res = os.system(f"xdotool windowminimize {window_id}")
        # 结果判断
        if res == 0:
            print(f'{window_id}最小化窗口成功')
            return True
        else:
            print(f'{window_id}最小化窗口失败')
            return False
    else:
        print(window_id, '输入错误，window_id应为数字')
        return False


def _set_window_size(window_id, width, height):
    """
    设置窗口大小(内核版本过高可能导致方法失效)
    Parameters:
     param1 - 窗口ID
     param2 - 宽度
     param3 - 高度
    """
    if not str(window_id).isdigit():
        print(window_id, '输入错误，window_id应为数字')
    elif not str(width).isdigit():
        print(width, '输入错误，width应为数字')
    elif not str(height).isdigit():
        print(height, '输入错误，height应为数字')
    else:
        os.system(f"xdotool windowsize {window_id} {width} {height}")


# def switchWindow(window_id):
#     """
#     切换到指定窗口
#     Parameters:
#      param1 - 窗口ID
#     """
#     os.system(f"xdotool windowfocus {window_id}")


#--------------------------------------------------------鼠标操作方法--------------------------------------------------------------
def get_mouse_location() ->list:
    """
    获取鼠标当前位置坐标
    Parameters:None
    Returns:
        list:[横坐标, 纵坐标]
    """
    res = os.popen("xdotool getmouselocation").readline()[:-1:].split(" ")
    res_x = res[0][res[0].index(':')+1::]
    res_y = res[1][res[1].index(':')+1::]
    return [res_x, res_y]


def mouse_click(option, repeat=1):
    """
    鼠标点击(左键/右键/滚轮)
    鼠标点击左键 mouse_click left
    鼠标点击右键 mouse_click right
    鼠标点击滚轮 mouse_click wheel
    Parameters:
     param1 - 选项(左键/右键/滚轮)
     param2 - 重复操作次数，不输入则默认为1
    Returns:
        点击成功:True
        点击失败:False
    """
    if not str(repeat).isdigit():
        print(repeat, '输入错误，repeat应为数字')
        return False
    else:
        if option=='left':
            res = os.system(f"xdotool click -repeat {repeat} 1")
            if res == 0:
                print(f'点击鼠标左键{repeat}次成功')
                return True
            else:
                print(f'点击鼠标左键{repeat}次失败')
                return False
        elif option=='wheel':
            res = os.system(f"xdotool click -repeat {repeat} 2")
            if res == 0:
                print(f'点击鼠标滚轮{repeat}次成功')
                return True
            else:
                print(f'点击鼠标滚轮{repeat}次失败')
                return False
        elif option=='right':
            res = os.system(f"xdotool click -repeat {repeat} 3")
            if res == 0:
                print(f'点击鼠标右键{repeat}次成功')
                return True
            else:
                print(f'点击鼠标右键{repeat}次失败')
                return False
        else:
            print('选项输入错误，点击失败')
            return False


def mouse_down(option):
    """
    鼠标按下(左键/右键/滚轮)
    鼠标按下左键 mouse_down left
    鼠标按下右键 mouse_down right
    鼠标按下滚轮 mouse_down wheel
    Parameters:
     param1 - 选项(左键/右键/滚轮)
    Returns:
        按下成功:True
        按下失败:False
    """
    if option=='left':
        res = os.system("xdotool mousedown 1")
        if res == 0:
            print(f'按下鼠标左键成功')
            return True
        else:
            print(f'按下鼠标左键失败')
            return False
    elif option=='wheel':
        res = os.system("xdotool mousedown 2")
        if res == 0:
            print(f'按下鼠标滚轮成功')
            return True
        else:
            print(f'按下鼠标滚轮失败')
            return False
    elif option=='right':
        res = os.system("xdotool mousedown 3")
        if res == 0:
            print(f'按下鼠标右键成功')
            return True
        else:
            print(f'按下鼠标右键失败')
            return False
    else:
        print('选项输入错误，按下失败')
        return False


def mouse_up(option):
    """
    鼠标松开(左键/右键/滚轮)
    鼠标松开左键 mouse_up left
    鼠标松开右键 mouse_up right
    鼠标松开滚轮 mouse_up wheel
    Parameters:
     param1 - 选项(左键/右键/滚轮)
    Returns:
        松开成功:True
        松开失败:False
    """
    if option == 'left':
        res = os.system("xdotool mouseup 1")
        if res == 0:
            print(f'松开鼠标左键成功')
            return True
        else:
            print(f'松开鼠标左键失败')
            return False
    elif option == 'wheel':
        res = os.system("xdotool mouseup 2")
        if res == 0:
            print(f'松开鼠标滚轮成功')
            return True
        else:
            print(f'松开鼠标滚轮失败')
            return False
    elif option == 'right':
        res = os.system("xdotool mouseup 3")
        if res == 0:
            print(f'松开鼠标右键成功')
            return True
        else:
            print(f'松开鼠标右键失败')
            return False
    else:
        print('选项输入错误，松开失败')
        return False


def mouse_scroll(option, repeat=1):
    """
    滚轮滚动(向上/向下)
    鼠标滚轮向上滚动 mouse_scroll up
    鼠标滚轮向下滚动 mouse_scroll down
    Parameters:
     param1 - 选项(向上/向下)
     param2 - 重复操作次数，不输入则默认为1
    Returns:
        滚动成功:True
        滚动失败:False
    """
    if not str(repeat).isdigit():
        print(repeat, '输入错误，repeat应为数字')
    else:
        if option=='up':
            res = os.system(f"xdotool click -repeat {repeat} 4")
            if res == 0:
                print(f'鼠标向前滚动{repeat}次成功')
                return True
            else:
                print(f'鼠标向前滚动{repeat}次失败')
                return False
        elif option=='down':
            res = os.system(f"xdotool click -repeat {repeat} 5")
            if res == 0:
                print(f'鼠标向后滚动{repeat}次成功')
                return True
            else:
                print(f'鼠标向后滚动{repeat}次失败')
                return False
        else:
            print('选项输入错误，滚动失败')
            return False


def mouse_move_absolute(width,height):
    """
    鼠标移动到绝对位置
    Parameters:
     param1 - 横坐标
     param2 - 纵坐标
    Returns:
        移动成功:True
        移动失败:False
    """
    if not isinstance(width,int):
        print(width, '输入错误，width应为数字')
        return False
    elif not isinstance(height, int):
        print(height, '输入错误，height应为数字')
        return False
    else:
        res = os.system(f"xdotool mousemove {width} {height}")
        if res == 0:
            print(f'鼠标移动成功')
            return True
        else:
            print(f'鼠标移动失败')
            return False


def mouse_move_relative(width,height):
    """
    鼠标移动到相对位置
    Parameters:
     param1 - 横向偏移量(负值向左，正值向右)
     param2 - 纵向偏移量(负值向上，正值向下)
    Returns:
        移动成功:True
        移动失败:False
    """
    if not isinstance(width, int):
        print(width, '输入错误，width应为数字')
        return False
    elif not isinstance(height, int):
        print(height, '输入错误，height应为数字')
        return False
    else:
        res = os.system(f"xdotool mousemove_relative -- {width} {height}")
        if res == 0:
            print(f'鼠标移动成功')
            return True
        else:
            print(f'鼠标移动失败')
            return False


#--------------------------------------------------------键盘操作方法--------------------------------------------------------------
def key_input(key):
    """
    键盘输入某个键('a')或组合键('ctrl+a')
    Parameters:
     param1 - 键盘上的某个键或组合键
     Returns:
        输入成功:True
        输入失败:False
    """

    if not isinstance(key, str):
        print(key, '输入错误，应为字符串')
        return False
    res = os.system(f"xdotool key {key}")
    if res == 0:
        print(f'{key}输入成功')
        return True
    else:
        print(f'{key}输入失败')
        return False


def key_down(key):
    """
    按下键盘某个键
    Parameters:
     param1 - 键盘上的某个键
    Returns:
        按下成功:True
        按下失败:False
    """
    if not isinstance(key, str):
        print(key, '输入错误，应为字符串')
        return False
    res = os.system(f"xdotool keydown {key}")
    if res == 0:
        print(f'{key}按下成功')
        return True
    else:
        print(f'{key}按下失败')
        return False


def key_up(key):
    """
   松开键盘某个键
    Parameters:
     param1 - 键盘上的某个键
    Returns:
        松开成功:True
        松开失败:False
    """
    if not isinstance(key, str):
        print(key, '输入错误，应为字符串')
        return False
    res = os.system(f"xdotool keyup {key}")
    if res == 0:
        print(f'{key}松开成功')
        return True
    else:
        print(f'{key}松开失败')
        return False


def input_string(string):
    """
   自动输入字符串
    Parameters:
     param1 - 字符串
    Returns:
        输入成功:True
        输入失败:False
    """
    if not isinstance(string, str):
        print(string, '输入错误，应为字符串')
        return False
    res = os.system(f"xdotool type {string}")
    if res == 0:
        print(f'{string}输入成功')
        return True
    else:
        print(f'{string}输入失败')
        return False


#--------------------------------------------------------截图方法--------------------------------------------------------------
def screenshot(filename='%Y-%m-%d-%s_$wx$h.png', filepath='./') ->str:
    """
   截取全屏
    Parameters:
     param1 - 文件名称(默认为时间戳_分辨率.png)
     param2 - 文件存储的绝对路径(默认为当前目录)
    Returns:
        str:截图的绝对路径
    """
    if not isinstance(filename, str):
        print(filename, '输入错误，应为字符串')
        return ''
    elif not isinstance(filepath, str):
        print(filepath, '输入错误，应为字符串')
        return ''
    else:
        if filepath == './':
            path = os.getcwd()
            scrot = f"scrot '{filename}' -e 'echo $f'"
            file = os.popen(scrot).readline()[:-1:]
            if file == '':
                return ''
            return path+'/'+file
        else:
            scrot = f"scrot '{filename}' -e 'mv $f {filepath};echo $f'"
            file = os.popen(scrot).readline()[:-1:]
            if file == '':
                return ''
            return filepath+'/'+file


def screenshot_window(filename='%Y-%m-%d-%s_$wx$h.png', filepath='./') ->str:
    """
   截取当前窗口
    Parameters:
     param1 - 文件名称(默认为时间戳_分辨率.png)
     param2 - 文件存储的绝对路径(默认为当前目录)
    Returns:
        str:截图的绝对路径
    """
    if not isinstance(filename, str):
        print(filename, '输入错误，应为字符串')
        return ''
    elif not isinstance(filepath, str):
        print(filepath, '输入错误，应为字符串')
        return ''
    else:
        if filepath == './':
            path = os.getcwd()
            scrot = f"scrot -u '{filename}' -e 'echo $f'"
            file = os.popen(scrot).readline()[:-1:]
            if file == '':
                return ''
            return path+'/'+file
        else:
            scrot = f"scrot -u '{filename}' -e 'mv $f {filepath};echo $f'"
            file = os.popen(scrot).readline()[:-1:]
            if file == '':
                return ''
            return filepath+'/'+file


def screenshot_custom(region, filename='截图'+str(int(time.time()))+'.png', filepath='./') ->str:
    """
   截取选择的窗口或矩形
    Parameters:
     param1 - 矩形列表[起点的横坐标,起点的纵坐标,矩形的宽度,矩形的高度]
     param2 - filename:文件名称(默认为时间戳_分辨率.png)
     param3 - filepath:文件存储的绝对路径(默认为当前目录)
    Returns:
        str:截图的绝对路径
    """
    if not isinstance(filename, str):
        print(filename, '输入错误，应为字符串')
        return ''
    elif not isinstance(filepath, str):
        print(filepath, '输入错误，应为字符串')
        return ''
    if len(region) !=4:
        print(region,'输入错误，region列表应包含4个元素')
        return ''
    else:
        for i in region:
            if not isinstance(i, int):
                print(region, '输入错误，region列表元素应为数字')
                return ''
        if filepath == './':
            image_filename = os.getcwd()+'/'+filename
        else:
            image_filename = filepath+'/'+filename
        region_list = region
        pyautogui.screenshot(imageFilename=image_filename, region=region_list)
        return image_filename
#--------------------------------------------------------文字识别方法--------------------------------------------------------------
def get_all_coordinates(image_path) ->dict:
    """
   输入图片返回所有文字坐标
    Parameters:
     param1 - 图片的绝对路径
    Returns:
        dict:包含文字及坐标的字典
    """
    if not isinstance(image_path, str):
        print(image_path, '输入错误，应为字符串')
        return {}
    file = open(image_path, 'rb')
    files = {'file': file}
    r = requests.post(url=OCR_URL, files=files)
    res = r.json()
    return res['main']


def get_coordinate(string, coordinate_dict, fuzzy=False):
    """
   输入单个字符串返回字典中该字符串的坐标
    Parameters:
     param1 - 字符串
     param2 - get_all_coordinates方法获得的字典
     param3 - 检查模式(默认为精准查询，fuzzy=True时为模糊查询)
    Returns:
        dict:包含坐标的字典
    """
    if not isinstance(string, str):
        print(string, '输入错误，应为字符串')
        return {}
    elif not isinstance(coordinate_dict, dict):
        print(coordinate_dict, '输入错误，应为字典')
        return {}
    elif not isinstance(fuzzy, bool):
        print(fuzzy, '输入错误，应为布尔类型')
        return {}
    else:
        res_key = check_exist(string, coordinate_dict,fuzzy)
        if res_key:
            return coordinate_dict[res_key]
        else:
            return {}
#--------------------------------------------------------断言方法--------------------------------------------------------------
def check_exist(string, coordinate_dict, fuzzy=False) ->str:
    """
   检查字典中是否存在该字符串(精准查询,模糊查询)
    Parameters:
     param1 - 字符串
     param2 - get_all_coordinates方法获得的字典
     param3 - 检查模式(默认为精准查询，fuzzy=True时为模糊查询)
    Returns:
        str：key(若存在，返回字典中与该字符串相匹配的key)
        str：''(若不存在，返回'')
    """
    if not isinstance(string, str):
        print(string, '输入错误，应为字符串')
        return ''
    elif not isinstance(coordinate_dict, dict):
        print(coordinate_dict, '输入错误，应为字典')
        return ''
    elif not isinstance(fuzzy, bool):
        print(fuzzy, '输入错误，应为布尔类型')
        return ''
    if fuzzy:
        for key in coordinate_dict.keys():
            if string in key:
                return key
        else:
            return ''
    else:
        if string in coordinate_dict.keys():
            return string
        else:
            return ''




#--------------------------------------------------------复合方法--------------------------------------------------------------
def check_exist_by_image(string, image_path, fuzzy=False) ->str:
    """
   检查图片中是否存在该字符串(精准查询,模糊查询)
    Parameters:
     param1 - 字符串
     param2 - 图片的绝对路径
     param3 - 检查模式(默认为精准查询，fuzzy=True时为模糊查询)
    Returns:
        str：key(若存在，返回字典中与该字符串相匹配的key)
        str：''(若不存在，返回'')
    """
    coordinate = get_all_coordinates(image_path)
    return check_exist(string, coordinate, fuzzy)


def get_coordinate_by_image(string, image_path, fuzzy=False):
    """
   输入单个字符串返回图片中该字符串的坐标
    Parameters:
     param1 - 字符串
     param2 - 图片的绝对路径
     param3 - 检查模式(默认为精准查询，fuzzy=True时为模糊查询)
    Returns:
        dict:包含坐标的字典
    """
    coordinate_dict = get_all_coordinates(image_path)
    res_key = check_exist(string, coordinate_dict,fuzzy)
    if res_key:
        return coordinate_dict[res_key]
    else:
        return {}


def click_location(window_id, x_coordinate, y_coordinate)->bool:
    """
    点击指定窗口的指定位置(左键点击一次)
    Parameters:
     param1 - 窗口ID
     param2 - 需要点击的横坐标
     param3 - 需要点击的纵坐标
    Returns:
        bool:True 点击成功
            False 点击失败
    """
    if not isinstance(window_id, int):
        print(window_id, '输入错误，应为数字')
        return False
    elif not isinstance(x_coordinate, int):
        print(x_coordinate, '输入错误，应为数字')
        return False
    elif not isinstance(y_coordinate, int):
        print(y_coordinate, '输入错误，应为数字')
        return False
    else:
        res = os.system(f"xdotool mousemove -w {window_id} {x_coordinate} {y_coordinate} click 1")
        if res == 0:
            print('点击成功')
            return True
        else:
            print('点击失败')
            return False

def get_location_click(string, coordinate_dict, window_id, fuzzy=False)->bool:
    """
    获得坐标并点击该位置
    Parameters:
     param1 - 需要点击的字符串
     param2 - get_all_coordinates方法获得的字典
     param3 - 窗口ID
     param4 - 检查模式(默认为精准查询，fuzzy=True时为模糊查询)
    """
    res_dict = get_coordinate(string, coordinate_dict, fuzzy)
    if res_dict:
        res = os.system(f"xdotool mousemove -w {window_id} {res_dict['width']} {res_dict['height']} click 1")
        if res == 0:
            print('点击成功')
            return True
        else:
            print('点击失败')
            return False
    else:
        print('没有在图中找到该字符串')
        return False