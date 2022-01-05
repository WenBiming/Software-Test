import os

from libs.untils.functions import *
import time
import sys
import shutil

if __name__ == '__main__':
    # 绝对路径
    abs_path = os.getcwd()
    # 时间戳
    times = str(int(time.time()))
    # 字典(名称:选项)
    scanner_dict = {'设备':'Hewlett', '类型':'馈纸式', '色彩':'彩色', '分辨率':'600', '尺寸':'A5', '格式':'png'}
    # 重启应用
    exec_res = restartApp('kylin-scanner')
    # 判断是否启动成功
    if exec_res:
        print('应用启动成功')
    else:
        print('应用启动失败')
        sys.exit()
    # 等待扫描设备
    time.sleep(12)
    # 获取窗口ID
    window_id = winNameGetWid('扫描')
    # 置顶窗口
    topWindow(window_id)
    # 最初截图
    time.sleep(1)
    file_path = screenshotWindow()
    # 识别图片
    res_dict = getALLCoordinates(file_path, "http://172.17.31.212:5000/ocr_web")
    # 删除图片
    os.remove(file_path)
    # 检查传入参数是否正确
    for i in scanner_dict.keys():
        if checkExist(i, res_dict):
            print(i,'存在')
        else:
            print(i, '不存在')
            sys.exit()
    # 点击所有坐标
    for i in scanner_dict:
        # 遍历参数字典
        # 获得key坐标
        if i=='设备':
            coordinate = getCoordinate(i, res_dict, fuzzy=True)
        else:
            coordinate = getCoordinate(i, res_dict)
        print(coordinate)
        # 点击key对应的下拉框坐标
        clickLocation(window_id, coordinate['width']+100, coordinate['height'])
        # 等待1秒后截图
        time.sleep(1)
        each_image_path = screenshotWindow()
        # 对截图进行识别
        each_dict = getALLCoordinates(each_image_path,"http://172.17.31.212:5000/ocr_web")
        # 删除图片
        os.remove(each_image_path)
        # 获得key对应的选项坐标
        each_value_coordinate = getCoordinate(scanner_dict[i],each_dict, fuzzy=True)
        print(scanner_dict[i])
        print(each_value_coordinate)
        # 点击key对应的选项
        clickLocation(window_id,each_value_coordinate['width'], each_value_coordinate['height'])
    # 输入名称
    # 获得名称的坐标
    name_coordinate = getCoordinate('名称', res_dict)
    print(name_coordinate)
    # 点击名称所对应的输入框位置
    clickLocation(window_id, name_coordinate['width']+100, name_coordinate['height'])
    # 全选输入框内内容
    keyInput('ctrl+a')
    # 输入内容
    result_name = 'case1'+times
    inputString(result_name)
    # 最终结果检查
    # 等待1秒后截图
    time.sleep(1)
    final_file_path = screenshotWindow('最终检查结果'+times+'.png', abs_path+'/screenshot')
    # 识别图片
    final_res_dict = getALLCoordinates(final_file_path, "http://172.17.31.212:5000/ocr_web")
    # 查看参数字典的键和值是否都在图片中
    for i in scanner_dict.keys():
        if checkExist(i, final_res_dict) and checkExist(scanner_dict[i], final_res_dict,fuzzy=True):
            print(i,'=',scanner_dict[i],'正确')
        else:
            print(i,'=',scanner_dict[i],'不正确')
            sys.exit()
    # 最终检查通过后点击扫描
    scanner_coordinate = getCoordinate('扫描', final_res_dict)
    clickLocation(window_id, scanner_coordinate['width'], scanner_coordinate['height'])
    # 等待扫描时间
    time.sleep(15)
    # 获得文件保存路径
    final_path = checkExist('/home', final_res_dict, fuzzy=True)
    result_format = scanner_dict['格式']
    if final_path:
        result_path = final_path+'/'+result_name+'.'+result_format
        dst_path = f'{abs_path}/result/'
        print(result_path)
        # 结果保存到result文件夹下
        shutil.move(result_path, dst_path)

