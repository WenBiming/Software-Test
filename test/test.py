from libs.untils.functions import *
from libs.config import SCREENSHOT_DIR
if __name__ == '__main__':
    # res = start_app('xdotool exec kylin-scanner')
    # res = close_app('wechat')
    # res = restart_app('xdotool exec wechat')
    # res = get_window_id_with_window_name('扫描')
    # res = get_window_id_with_mouse_location()
    # res = get_pid_with_window_id(130036844)
    # res = get_window_name_with_window_id('130036844')
    # res = get_screen_size()
    # res = get_window_size(130036844)
    # res = top_window(182452239)
    # res = move_window(127926291, 200, 100)
    # res = minimize_window(127926291)
    # res = get_mouse_location()
    # res = mouse_click('left',2)
    # res = mouse_click('right', 3)
    # res = mouse_click('wheel')
    # res = mouse_click('aaa')
    # res = mouse_move_absolute(100,200)
    # res = mouse_move_relative(100,-200)
    # res = key_input('a')
    # res = key_input('ctrl+a')
    # res1 = key_down('a')
    # res2 = key_up('a')
    # res = screenshot(filename='1.png')
    # res = screenshot_window()
    # res = screenshot_custom([50,50,50,50])
    # res = get_all_coordinates('/home/wangpengfei/桌面/111111.png')
    # res2 = get_coordinate('扫描', res)
    # res3 = check_exist('美化', res, fuzzy=True)
    # res4 = check_exist('美化', res)
    # res5 = check_exist('扫描', res)
    # res = check_exist_by_image('美化', '/home/wangpengfei/桌面/111111.png')
    # res2 = check_exist_by_image('美化', '/home/wangpengfei/桌面/111111.png',fuzzy=True)
    # res3 = check_exist_by_image('扫描', '/home/wangpengfei/桌面/111111.png')
    # res = get_coordinate_by_image('美化', '/home/wangpengfei/桌面/111111.png')
    # res2 = get_coordinate_by_image('美化', '/home/wangpengfei/桌面/111111.png',fuzzy=True)
    # res3 = get_coordinate_by_image('扫描', '/home/wangpengfei/桌面/111111.png')
    # res2 = click_location(182452239, 100, 100)
    # print(res)
    final_file_path = screenshot_window('最终检查结果.png', SCREENSHOT_DIR)
    print(final_file_path)
    # print(res2)

