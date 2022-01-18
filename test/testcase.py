from libs.untils.functions import *
import time
import sys
import shutil
def res_check(result,pass_print,fail_print):
    """
    断言方法 判断result是否为True
    Args:
        result: 需要检查的结果
        pass_print: result为True时打印的信息
        fail_print: result为False时打印的信息

    Returns:

    """
    if result:
        print(pass_print)
    else:
        print(fail_print)
        sys.exit()

if __name__ == '__main__':
    #----------------------------------------------------初始化参数------------------------------------------------------
    # 截图文件夹路径
    root_path = os.path.abspath(os.path.dirname(__file__)).split('test')[0]
    screenshot_dir = f'{root_path}screenshot'
    # 绝对路径
    abs_path = os.getcwd()
    # 时间戳
    times = str(int(time.time()))
    # 字典(名称:选项)
    scanner_dict = {'设备':'Hewlett', '类型':'馈纸式', '色彩':'彩色', '分辨率':'600', '尺寸':'A5', '格式':'png'}
    #----------------------------------------------打开置顶应用并初始化检查-------------------------------------------------
    # 重启应用
    exec_res = restart_app('xdotool exec kylin-scanner')
    # 判断是否启动成功
    res_check(exec_res, '应用启动成功', '应用启动失败')
    # 等待扫描设备
    time.sleep(12)
    # 获取窗口ID
    window_id = int(get_window_id_with_window_name('扫描'))
    #判断是否获取到窗口ID
    res_check(window_id, f'获取窗口ID成功{window_id}', f'获取窗口ID失败{window_id}')
    # 置顶窗口
    top_window_res = top_window(window_id)
    # 判断是否置顶成功
    res_check(top_window_res, '置顶窗口成功', '置顶窗口失败')
    # 最初截图
    time.sleep(1)
    file_path = screenshot_window()
    # 判断是否截图成功
    res_check(file_path, f'截图成功，路径为{file_path}', '截图失败')
    # 识别图片
    res_dict = get_all_coordinates(file_path)
    # 判断是否识别成功
    res_check(res_dict, '最初截图识别成功', '最初截图识别失败')
    # 删除图片
    os.remove(file_path)
    # 检查传入参数是否正确
    for i in scanner_dict.keys():
        res_check(check_exist(i, res_dict), f'{i}存在', f'{i}不存在')
    #--------------------------------------------------选择与输入选项-----------------------------------------------------
    # 点击所有坐标
    for i in scanner_dict:
        # 遍历参数字典
        # 获得key坐标
        if i=='设备':
            # “设备”采用模糊查询方式
            coordinate = get_coordinate(i, res_dict, fuzzy=True)
        else:
            coordinate = get_coordinate(i, res_dict)
        # 判断是否获得key坐标
        res_check(coordinate, f'{i}坐标为{coordinate}', f'没有获得{i}坐标')
        # 点击key对应的下拉框坐标
        click_res = click_location(window_id, coordinate['width']+100, coordinate['height'])
        # 判断是否点击下拉框成功
        res_check(click_res, f'点击{i}下拉框成功', f'点击{i}下拉框失败')
        # 等待1秒后截图
        time.sleep(1)
        each_image_path = screenshot_window()
        # 判断是否截图成功
        res_check(each_image_path, f'{i}下拉框截图成功', f'{i}下拉框截图失败')
        # 对截图进行识别
        each_dict = get_all_coordinates(each_image_path)
        # 判断是否识别成功
        res_check(each_dict, f'截图识别成功{each_dict}', '截图识别失败')
        # 删除图片
        os.remove(each_image_path)
        # 获得key对应的选项坐标
        each_value_coordinate = get_coordinate(scanner_dict[i],each_dict, fuzzy=True)
        # 判断是否获得value坐标
        res_check(each_value_coordinate, f'{scanner_dict[i]}坐标为{each_value_coordinate}', f'没有获得{scanner_dict[i]}坐标')
        # 点击key对应的选项
        value_click_res = click_location(window_id,each_value_coordinate['width'], each_value_coordinate['height'])
        # 判断是否点击成功
        res_check(value_click_res, f'点击{scanner_dict[i]}成功', f'点击{scanner_dict[i]}失败')
    # 输入名称
    # 获得名称的坐标
    name_coordinate = get_coordinate('名称', res_dict)
    # 判断是否获得名称坐标
    res_check(name_coordinate, f'获取名称坐标成功{name_coordinate}', '获取名称坐标失败')
    # 点击名称所对应的输入框位置
    click_name_res = click_location(window_id, name_coordinate['width']+100, name_coordinate['height'])
    # 判断是否点击名称输入框位置
    res_check(click_name_res, '点击名称输入框成功', '点击名称输入框失败')
    # 全选输入框内内容
    key_input_res = key_input('ctrl+a')
    # 判断是否全选输入框内容
    res_check(key_input_res, '全选输入框内容成功', '全选输入框内容失败')
    # 输入内容
    result_name = f'case{times}'
    input_string_res = input_string(result_name)
    # 判断是否输入成功
    res_check(input_string_res, f'{result_name}输入成功', f'{result_name}输入失败')
    #----------------------------------------------------最终结果检查-----------------------------------------------------
    # 等待1秒后截图
    time.sleep(1)
    final_file_path = screenshot_window('最终检查结果'+times+'.png', screenshot_dir)
    # 判断最终截图结果
    res_check(final_file_path, f'最终截图成功，保存路径为{final_file_path}', '最终截图失败')
    # 识别图片
    final_res_dict = get_all_coordinates(final_file_path)
    # 判断最终识别结果
    res_check(final_res_dict, '最终识别成功', '最终识别失败')
    # 判断参数字典的键和值是否都在图片中
    for i in scanner_dict.keys():
        res_check((check_exist(i, final_res_dict) and check_exist(scanner_dict[i], final_res_dict,fuzzy=True)),
                  f'{i}={scanner_dict[i]}正确', f'{i}={scanner_dict[i]}不正确')
    #------------------------------------------------------开始扫描------------------------------------------------------
    # 获取'扫描按钮'坐标
    scanner_coordinate = get_coordinate('扫描', final_res_dict)
    # 判断是否获取扫描按钮坐标
    res_check(scanner_coordinate, f'获取扫描按钮坐标成功{scanner_coordinate}','获取扫描按钮坐标失败')
    # 点击扫描按钮
    scanner_click_res = click_location(window_id, scanner_coordinate['width'], scanner_coordinate['height'])
    # 判断是否点击成功
    res_check(scanner_click_res, '扫描按钮点击成功', '扫描按钮点击失败')
    # 等待扫描时间
    time.sleep(15)
    # 获得文件保存路径
    #-----------------------------------------------------结果保存-------------------------------------------------------
    final_path = check_exist('/home', final_res_dict, fuzzy=True)
    result_format = scanner_dict['格式']
    if final_path:
        result_path = final_path+'/'+result_name+'.'+result_format
        dst_path = f'{root_path}result/'
        # 结果保存到result文件夹下
        shutil.move(result_path, dst_path)
        print(f'最终结果保存在{dst_path}')

