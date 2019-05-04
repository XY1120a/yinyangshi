"""
author:jianglz
email:lovejianglz@qq.com
data:
"""
import os
import random
import time
import click
import re
import cv2
import numpy
import subprocess


@click.group()
def yys():
    pass


def auto_fight():
    x = random.randrange(1600, 1700)
    y = random.randrange(760, 900)
    wait_for_pattern("start_fight.png")
    exc_adb_command(f'shell input tap {x} {y}')  # 点击挑战
    # 按战斗按钮后切换到战斗场景的时间
    x = random.randrange(1600, 1850)
    y = random.randrange(760, 930)
    wait_for_pattern("ready.png")
    exc_adb_command(f'shell input tap {x} {y}')  # 点击准备
    time.sleep(5)
    x = random.randrange(866, 880)
    y = random.randrange(208, 246)
    exc_adb_command(f'shell input tap {x} {y}')# 点击主怪
    x = random.randrange(1500, 1850)
    y = random.randrange(200, 930)
    wait_for_pattern("end_fight.png")
    exc_adb_command(f'shell input tap {x} {y}')  # 点击屏幕，返回


@click.command()
@click.option("--btype", default="jinbi", help="战斗的种类", type=click.Choice(['jinbi', 'yuhun']))
@click.option("--count", default=20, help="战斗次数", type=int)
@click.option("--wifi/--usb", default=False, help="是否选用无线连接")
def lidao(btype, count, wifi):
    if connect_device(wifi):
        click.echo(f"Program is running fight {btype}, {count}")
        while count:
            auto_fight()
            count -= 1
            print(f"剩余 {count} 次")
        print("自动脚本结束")
    exc_adb_command("kill-server")
    exit(0)


def screen_shot():
    exc_adb_command("shell screencap -p /sdcard/sc.png")
    exc_adb_command("pull /sdcard/sc.png")


def exc_adb_command(command):
    adb = subprocess.Popen(f"adb {command}", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    adb.wait()
    result = adb.communicate()
    return result[0].decode("utf-8"), result[1].decode("utf-8")


def connect_device(wifi):
    # todo 1. 用 adb devices查看当前已激活的手机
    #      2. 若存在 wifi 已连接的直接跳过连接步骤
    #      3. 检查USB是否连接好
    #      4. 配置连接WIFI
    result, error = exc_adb_command("devices")
    if error:
        print(error)
        return False
    # 先检查设备列表中的第一项是否含有IP地址
    device = result.split("\r\n")[1]
    reg = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    reg = re.compile(reg)
    result = re.search(reg, device)
    if result:
        click.echo("已通过WIFI连接手机")
        return True
    # 如果设备列表为空，提示连接手机
    if "device" not in device:
        input("请用USB连接你的手机，按回车继续")
    # 如果选择了WIFI选项，则进入WIFI配置
    if wifi:
        if connect_wireless_device():
            return True
    # 上述配置结束后，检查设备是否成功连接
    result, _ = exc_adb_command("devices")
    if "device" in result.split("\r\n")[1]:
        return True
    return False


def connect_wireless_device():
    exc_adb_command("kill-server")
    result, _ = exc_adb_command("tcpip 5555")
    if "restarting in TCP mode port: 5555" not in result:
        click.echo("请检查手机USB连接或是否已打开开发者模式")
        return False
    ip = input("确认手机已连接后，输入手机ip地址：\n")
    failed_count = 2
    while not check_ip(ip) and failed_count:
        ip = input("输入的IP地址不合法，请重新输入\n")
        failed_count -= 1
    if failed_count == 0 and not check_ip(ip):
        print("输入错误次数过多，退出程序!!!")
        return False
    input("请断开USB连接，按回车继续")
    result, _ = exc_adb_command(f"connect {ip}")
    if "connected to" not in result:
        click.echo(f"保证手机与电脑在同一局域网内并确认手机IP输入正确\n{ip}")
        return False
    print("手机无线连接成功")
    return True


def check_ip(ip_addr):
    compile_ip = re.compile(r'^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9]).'
                            r'(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d).'
                            r'(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d).'
                            r'(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    if compile_ip.match(ip_addr):
        return True
    else:
        return False


def match_pic(temp, target="sc.png"):
    imgsr = cv2.imread(f"./{target}")
    imgtm = cv2.imread(f"./{temp}")
    res = cv2.matchTemplate(imgsr, imgtm, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # print(max_val)
    if max_val > 0.95:
        return True
    else:
        return False


def wait_for_pattern(pattern):
    screen_shot()
    while not match_pic(pattern):
        screen_shot()
        time.sleep(5)
    time.sleep(1 + random.randrange(0, 10, 1) / 10)


def draw_pic(src):
    empty_image = numpy.zeros((1080, 960, 3), numpy.uint8)
    cv2.imwrite(f"./{src}", empty_image)


yys.add_command(lidao)

if __name__ == '__main__':
    yys()
    # lidao()
    # print(exc_adb_command("devices").split("\r\n"))#=="List of devices attached\r\n")
    # connect_wireless_device()
    # connect_device(1)
    # screen_shot()
    # print(match_pic("start_fight.png"))#,"2 - 副本.png"))
    # draw_pic("sc.png")
    # print(wait_for_pattern("end_fight.png"))
