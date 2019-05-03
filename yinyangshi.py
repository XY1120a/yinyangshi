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


@click.group()
def yys():
    pass


def auto_fight():
    x = random.randrange(1600, 1700)
    y = random.randrange(760, 900)
    wait_for_pattern("start_fight.png")
    os.system(f'adb shell input tap {x} {y}')  # 点击挑战
    # 按战斗按钮后切换到战斗场景的时间
    x = random.randrange(1600, 1850)
    y = random.randrange(760, 930)
    wait_for_pattern("ready.png")
    os.system(f'adb shell input tap {x} {y}')  # 点击准备
    x = random.randrange(1500, 1850)
    y = random.randrange(200, 930)
    wait_for_pattern("end_fight.png")
    os.system(f'adb shell input tap {x} {y}')  # 点击屏幕，返回


@click.command()
@click.option("--btype", default="jinbi", help="战斗的种类", type=click.Choice(['jinbi', 'yuhun']))
@click.option("--count", default=20, help="战斗次数", type=int)
@click.option("--wifi/--usb", default=False, help="是否选用无线连接")
def lidao(btype, count, wifi):
    draw_pic("sc.png")
    if wifi:
        connect_wireless_device()
    click.echo(f"Program is running fight {btype}, {count}")
    while count:
        auto_fight()
        count -= 1
        print(f"剩余 {count} 次")
    print("自动脚本结束")


def screen_shot():
    os.system("adb shell screencap -p /sdcard/sc.png")
    os.system("adb pull /sdcard/sc.png")


def connect_wireless_device():
    click.echo("请用USB连接您的手机")
    ip = input("确认手机已连接后，输入手机ip地址：\n")
    failed_count = 2
    while not check_ip(ip) and failed_count:
        ip = input("输入的IP地址不合法，请重新输入\n")
        failed_count -= 1
    if failed_count == 0 and not check_ip(ip):
        print("输入错误次数过多，退出程序!!!")
        exit(0)
    os.popen("adb kill-server")
    result = os.popen("adb tcpip 5555").readlines()[-1]
    print(result)
    if "restarting in TCP mode port: 5555" not in result:
        click.echo("请检查手机USB连接或是否已打开开发者模式")
        exit(0)
    input("请断开USB连接，按回车继续")
    result = os.popen(f"adb connect {ip}").readlines()[-1]
    if "connected to" not in result:
        click.echo(f"保证手机与电脑在同一局域网内并确认手机IP输入正确\n{ip}")
        exit(0)
    print("手机无线连接成功")


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
    if max_val > 0.95:
        return True
    else:
        return False


def wait_for_pattern(pattern):
    while not match_pic(pattern):
        screen_shot()
        time.sleep(2)
    time.sleep(1 + random.randrange(0, 10, 1)/10)


def draw_pic(src):
    empty_image = numpy.zeros((1, 2, 3), numpy.uint8)
    cv2.imwrite(f"./{src}", empty_image)


yys.add_command(lidao)


if __name__ == '__main__':
    yys()
    # connect_wireless_device()
    # screen_shot()
    # print(match_pic("3.png"))#,"2 - 副本.png"))
    # draw_pic("sc.png")