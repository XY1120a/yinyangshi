import os
import random
import time
import click

LIDAO_TIMER = {
	# [按战斗按钮后切换到战斗场景的时间， 战斗经过时间，战斗结束播放获取奖励画面的时间， 退出战斗场景时间]
    "jinbi_timer": [16, 130, 2, 10],
    "yuhun_timer": [16, 200, 2, 10]
}


@click.group()
def yys():
    pass

def auto_fight(timer):
    x = random.randrange(1600, 1700)
    y = random.randrange(760, 900)
    os.system(f'adb shell input tap {x} {y}')  # 点击挑战
    time.sleep(timer[0] + random.randrange(0, 5, 1))
    x = random.randrange(1600, 1850)
    y = random.randrange(760, 930)
    os.system(f'adb shell input tap {x} {y}')  # 点击准备
    time.sleep(timer[1] + random.randrange(0, 10, 1))
    x = random.randrange(1500, 1850)
    y = random.randrange(200, 930)
    os.system(f'adb shell input tap {x} {y}')  # 点击屏幕，确认
    time.sleep(timer[2] + random.randrange(0, 1, 1))
    x = random.randrange(1500, 1850)
    y = random.randrange(200, 930)
    os.system(f'adb shell input tap {x} {y}')  # 点击屏幕，返回
    time.sleep(timer[3] + random.randrange(0, 10, 1))


@click.command()
@click.option("--type", help="战斗的种类 jinbi yuhun", type=str)
@click.option("--count", default=100, help="战斗次数", type=int)
def lidao(type, count):
    timer = LIDAO_TIMER.get(type+"_timer")
    if not timer:
        click.echo(f"No such a fight type {type}.Types avaliable: jinbi, yuhun")
        exit(0)
    click.echo(f"Program is running fight {type}, {count}")
    while count:
        auto_fight(timer)
        count -= 1
        print(f"剩余 {count} 次")


yys.add_command(lidao)

if __name__ == '__main__':
    yys()
