#!/usr/bin/python3
# coding=utf-8
################################################################################
#Function: 点击坐标、截图、文字识别、结果检查
#Platform:ALL
#Author: Pengfei Wang
#Date: 2021/12/12
#Company: Kylin Software Co.,Ltd.
################################################################################
import os
import time
import requests
import sys
import json
import pyautogui

#--------------------------------------------------------应用方法--------------------------------------------------------------
def startApp(app_name) ->bool:
    """
    启动应用方法
    Parameters:
     param1 - 应用名称
    Returns:
        True:启动成功
        False：启动失败
    """
    os.system(f'xdotool exec {app_name}')
    res = os.system(f'ps -ef|grep {app_name}|grep -v grep')
    if res == 0:
        print('-----------------应用启动成功--------------------')
        return True
    else:
        print('-----------------应用启动失败--------------------')
        return False


def closeApp(app_name) ->bool:
    """
    关闭应用方法
    Parameters:
     param1 - 应用名称
    Returns:
        True:关闭成功
        False：关闭失败
    """
    os.system(f"ps -ef|grep {app_name}|grep -v grep|awk "+"'{print \"kill -9 \"$2}'"+"|sh")
    res = os.system(f'ps -ef|grep {app_name}|grep -v grep')
    if res == 0:
        print('-----------------应用关闭失败--------------------')
        return False
    else:
        print('-----------------应用关闭成功--------------------')
        return True

def restartApp(app_name) -> bool:
    """
    重启应用方法
    Parameters:
     param1 - 应用名称
    Returns:
        True:重启成功
        False：重启失败
    """
    os.system(f"ps -ef|grep {app_name}|grep -v grep|awk " + "'{print \"kill -9 \"$2}'" + "|sh")
    os.system(f'xdotool exec {app_name}')
    res = os.system(f'ps -ef|grep {app_name}|grep -v grep')
    if res == 0:
        print('-----------------应用重启成功--------------------')
        return True
    else:
        print('-----------------应用启动失败--------------------')
        return False

#--------------------------------------------------------窗口方法--------------------------------------------------------------
def pidGetWid(pid) ->str:
    """
    根据进程ID获取窗口ID
    Parameters:
     param1 - 进程ID
    Returns:
        str:窗口ID
    """
    res = os.popen(f'xdotool search --pid {pid}')
    res_ID = res.read()[:-1:]
    if res_ID =='':
        print('没有找到对应的窗口ID')
        return None
    return res_ID


def winNameGetWid(window_name) ->str:
    """
    根据窗口名称获取窗口ID
    Parameters:
     param1 - 窗口名称
    Returns:
        str:窗口ID
    """
    res = os.popen(f'xdotool search -n {window_name}| tail -1')
    res_ID = res.read()[:-1:]
    if res_ID =='':
        print('没有找到正在运行的窗口',window_name)
        return None
    return res_ID


def appNameGetWid(app_name) ->str:
    """
    根据应用名称获取窗口ID
    Parameters:
     param1 - 应用名称
    Returns:
        str:窗口ID
    """
    pid = os.popen(f"ps -ef | grep {app_name}"+"| grep -v grep | awk '{ print $2 }'").readline()[:-1:]
    if pid =='':
        print('没有找到正在运行的程序',app_name)
        return None
    res = os.popen(f'xdotool search --pid {pid}')
    return res.read()[:-1:]


def mouseGetWid() ->str:
    """
    获取鼠标当前位置的窗口ID
    Parameters:None
    Returns:
        str:窗口ID
    """
    res = os.popen("xdotool getmouselocation").readline()[:-1:].split(" ")
    window_id = res[3][res[3].index(':')+1::]
    return window_id


def getPid(window_id) ->str:
    """
    根据窗口ID获取进程ID
    Parameters:
     param1 - 窗口ID
    Returns:
        str:进程ID
    """
    pid = os.popen(f"xdotool getwindowpid {window_id}").readline()[:-1:]
    if pid == '':
        print('没有找到对应的进程ID')
        return None
    return pid


def getWinName(window_id) ->str:
    """
    根据窗口ID获取窗口名称
    Parameters:
     param1 - 窗口ID
    Returns:
        str:窗口名称
    """
    window_name = os.popen(f"xdotool getwindowname {window_id}").readline()[:-1:]
    if window_name == '':
        print('没有找到对应的窗口ID')
        return None
    return window_name


def getScreenSize() ->list:
    """
    获取屏幕分辨率
    Parameters:None
    Returns:
        list:[宽度, 高度]
    """
    screen_size = os.popen("xdotool getdisplaygeometry").readline()[:-1:].split(' ')
    return screen_size


def getWindowSize(window_id) ->list:
    """
    根据窗口ID获取窗口尺寸
    Parameters:
     param1 - 窗口ID
    Returns:
        list:[窗口宽度, 窗口高度]
    """
    window_width = os.popen(
        f"xdotool getwindowgeometry {window_id} | grep Geometry | sed -r \"s/[^0-9]*([0-9]+)x([0-9]+)/\\1/g\"").readline()[:-1:]
    if window_width=='':
        print('没有找到对应的窗口ID')
        return None
    window_height = os.popen(
        f"xdotool getwindowgeometry {window_id} | grep Geometry | sed -r \"s/[^0-9]*([0-9]+)x([0-9]+)/\\2/g\"").readline()[:-1:]
    return [window_width, window_height]


def topWindow(window_id):
    """
    置顶窗口
    Parameters:
     param1 - 窗口ID
    """

    os.system(f"xdotool windowactivate {window_id}")


def moveWindow(window_id, width, height):
    """
    将窗口移动到某处
    Parameters:
     param1 - 窗口ID
     param2 - 横坐标
     param3 - 纵坐标
    """
    os.system(f"xdotool windowmove {window_id} {width} {height}")


def minimizeWindow(window_id):
    """
    最小化窗口
    Parameters:
     param1 - 窗口ID
    """
    os.system(f"xdotool windowminimize {window_id}")


def setWindowSize(window_id, width, height):
    """
    设置窗口大小
    Parameters:
     param1 - 窗口ID
     param2 - 宽度
     param3 - 高度
    """
    os.system(f"xdotool windowsize {window_id} {width} {height}")


def switchWindow(window_id):
    """
    切换到指定窗口
    Parameters:
     param1 - 窗口ID
    """
    os.system(f"xdotool windowfocus {window_id}")


#--------------------------------------------------------鼠标操作方法--------------------------------------------------------------
def getMouseLocation() ->list:
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


def mouseClick(option, repeat=1):
    """
    鼠标点击(左键/右键/滚轮)
    鼠标点击左键 mouseClick left
    鼠标点击右键 mouseClick right
    鼠标点击滚轮 mouseClick wheel
    Parameters:
     param1 - 选项(左键/右键/滚轮)
     param2 - 重复操作次数，不输入则默认为1
    """
    if option=='left':
        os.system(f"xdotool click -repeat {repeat} 1")
    elif option=='wheel':
        os.system(f"xdotool click -repeat {repeat} 2")
    elif option=='right':
        os.system(f"xdotool click -repeat {repeat} 3")
    else:
        print('选项输入错误，点击失败')


def mouseDown(option):
    """
    鼠标按下(左键/右键/滚轮)
    鼠标按下左键 mouseClick left
    鼠标按下右键 mouseClick right
    鼠标按下滚轮 mouseClick wheel
    Parameters:
     param1 - 选项(左键/右键/滚轮)
    """
    if option=='left':
        os.system("xdotool mousedown 1")
    elif option=='wheel':
        os.system("xdotool mousedown 2")
    elif option=='right':
        os.system("xdotool mousedown 3")
    else:
        print('选项输入错误，按下失败')


def mouseUp(option):
    """
    鼠标松开(左键/右键/滚轮)
    鼠标松开左键 mouseClick left
    鼠标松开右键 mouseClick right
    鼠标松开滚轮 mouseClick wheel
    Parameters:
     param1 - 选项(左键/右键/滚轮)
    """
    if option=='left':
        os.system("xdotool mouseup 1")
    elif option=='wheel':
        os.system("xdotool mouseup 2")
    elif option=='right':
        os.system("xdotool mouseup 3")
    else:
        print('选项输入错误，松开失败')


def mouseScroll(option, repeat=1):
    """
    滚轮滚动(向上/向下)
    鼠标滚轮向上滚动 mouseScroll up
    鼠标滚轮向下滚动 mouseScroll down
    Parameters:
     param1 - 选项(向上/向下)
     param2 - 重复操作次数，不输入则默认为1
    """
    if option=='up':
        os.system(f"xdotool click -repeat {repeat} 4")
    elif option=='down':
        os.system(f"xdotool click -repeat {repeat} 5")
    else:
        print('选项输入错误，滚动失败')


def mouseMoveAbslute(width,height):
    """
    鼠标移动到绝对位置
    Parameters:
     param1 - 横坐标
     param2 - 纵坐标
    """
    os.system(f"xdotool mousemove {width} {height}")


def mouseMoveRelative(width,height):
    """
    鼠标移动到相对位置
    Parameters:
     param1 - 横向偏移量(负值向左，正值向右)
     param2 - 纵向偏移量(负值向上，正值向下)
    """
    os.system(f"xdotool mousemove_relative {width} {height}")


#--------------------------------------------------------键盘操作方法--------------------------------------------------------------
def keyInput(key):
    """
    键盘输入某个键('a')或组合键('ctrl+a')
    Parameters:
     param1 - 键盘上的某个键或组合键
    """
    os.system(f"xdotool key {key}")


def keyDown(key):
    """
    按下键盘某个键
    Parameters:
     param1 - 键盘上的某个键
    """
    os.system(f"xdotool keydown {key}")


def keyUp(key):
    """
   松开键盘某个键
    Parameters:
     param1 - 键盘上的某个键
    """
    os.system(f"xdotool keyup {key}")


def inputString(string):
    """
   自动输入字符串
    Parameters:
     param1 - 字符串
    """
    os.system(f"xdotool type {string}")


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
    if filepath == './':
        path = os.getcwd()
        scrot = f"scrot '{filename}' -e 'echo $f'"
        file = os.popen(scrot).readline()[:-1:]
        return path+'/'+file
    else:
        scrot = f"scrot '{filename}' -e 'mv $f {filepath};echo $f'"
        file = os.popen(scrot).readline()[:-1:]
        return filepath+'/'+file


def screenshotWindow(filename='%Y-%m-%d-%s_$wx$h.png', filepath='./') ->str:
    """
   截取当前窗口
    Parameters:
     param1 - 文件名称(默认为时间戳_分辨率.png)
     param2 - 文件存储的绝对路径(默认为当前目录)
    Returns:
        str:截图的绝对路径
    """
    if filepath == './':
        path = os.getcwd()
        scrot = f"scrot -u '{filename}' -e 'echo $f'"
        file = os.popen(scrot).readline()[:-1:]
        return path+'/'+file
    else:
        scrot = f"scrot -u '{filename}' -e 'mv $f {filepath};echo $f'"
        file = os.popen(scrot).readline()[:-1:]
        return filepath+'/'+file


def screenshotCustom(region, filename='截图'+str(int(time.time()))+'.png', filepath='./') ->str:
    """
   截取选择的窗口或矩形
    Parameters:
     param1 - 矩形列表[起点的横坐标,起点的纵坐标,矩形的宽度,矩形的高度]
     param2 - filename:文件名称(默认为时间戳_分辨率.png)
     param3 - filepath:文件存储的绝对路径(默认为当前目录)
    Returns:
        str:截图的绝对路径
    """
    if filepath == './':
        image_filename = os.getcwd()+'/'+filename
    else:
        image_filename = filepath+'/'+filename
    region_list = region
    pyautogui.screenshot(imageFilename=image_filename, region=region_list)
    return image_filename
#--------------------------------------------------------文字识别方法--------------------------------------------------------------
def getALLCoordinates(image_path, url) ->dict:
    """
   输入图片返回所有文字坐标
    Parameters:
     param1 - 图片的绝对路径
     param2 - 访问接口的url
    Returns:
        dict:包含文字及坐标的字典
    """
    file = open(image_path, 'rb')
    files = {'file': file}
    r = requests.post(url=url, files=files)
    res = r.json()
    return res['main']


def getCoordinate(string, coordinate_dict,fuzzy=False):
    """
   输入单个字符串返回字典中该字符串的坐标
    Parameters:
     param1 - 字符串
     param2 - getALLCoordinates方法获得的字典
     param3 - 检查模式(默认为精准查询，fuzzy=True时为模糊查询)
    Returns:
        dict:包含坐标的字典
    """
    res_key = checkExist(string, coordinate_dict,fuzzy)
    if res_key:
        return coordinate_dict[res_key]
    else:
        return None
#--------------------------------------------------------断言方法--------------------------------------------------------------
def checkExist(string, coordinate_dict, fuzzy=False) ->bool:
    """
   检查字典中是否存在该字符串(精准查询,模糊查询)
    Parameters:
     param1 - 字符串
     param2 - getALLCoordinates方法获得的字典
     param3 - 检查模式(默认为精准查询，fuzzy=True时为模糊查询)
    Returns:
        str：key(若存在，返回字典中与该字符串相匹配的key)
        bool：False(若不存在，返回False)
    """
    if fuzzy:
        for key in coordinate_dict.keys():
            if string in key:
                return key
        else:
            return False
    else:
        if string in coordinate_dict.keys():
            return string
        else:
            return False




#--------------------------------------------------------复合方法--------------------------------------------------------------
def checkExistbyImage(string, image_path, url,  fuzzy=False) ->bool:
    """
   检查图片中是否存在该字符串(精准查询,模糊查询)
    Parameters:
     param1 - 字符串
     param2 - 图片的绝对路径
     param3 - 访问接口的url
     param4 - 检查模式(默认为精准查询，fuzzy=True时为模糊查询)
    Returns:
        str：key(若存在，返回字典中与该字符串相匹配的key)
        bool：False(若不存在，返回False)
    """
    coordinate = getALLCoordinates(image_path, url)
    return checkExist(string, coordinate, fuzzy)


def getCoordinatebyImage(string, image_path, url,  fuzzy=False):
    """
   输入单个字符串返回图片中该字符串的坐标
    Parameters:
     param1 - 字符串
     param2 - 图片的绝对路径
     param3 - 访问接口的url
     param4 - 检查模式(默认为精准查询，fuzzy=True时为模糊查询)
    Returns:
        dict:包含坐标的字典
    """
    coordinate_dict = getALLCoordinates(image_path, url)
    res_key = checkExist(string, coordinate_dict,fuzzy)
    if res_key:
        return coordinate_dict[res_key]
    else:
        return None


def clickLocation(window_id, x_coordinate, y_coordinate):
    """
    点击指定窗口的指定位置(左键点击一次)
    Parameters:
     param1 - 窗口ID
     param2 - 需要点击的横坐标
     param3 - 需要点击的纵坐标
    """
    os.system(f"xdotool mousemove -w {window_id} {x_coordinate} {y_coordinate} click 1")


def getLocationClick(string, coordinate_dict, window_id, fuzzy=False):
    """
    获得坐标并点击该位置
    Parameters:
     param1 - 窗口ID
     param2 - 需要点击的横坐标
     param3 - 需要点击的纵坐标
    """
    res_dict = getCoordinate(string, coordinate_dict, fuzzy)
    os.system(f"xdotool mousemove -w {window_id} {res_dict['width']} {res_dict['height']} click 1")
