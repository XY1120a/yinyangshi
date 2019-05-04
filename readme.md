# yinyangshi
* YYS自动刷怪脚本
* 利用adb实现控制安卓手机。
* 需要根据打怪的速度及手机加载场景的速度调整timer参数
* 在命令行中使用
* 使用前需开启手机的开发者模式及USB DEBUG
* 本程序仅在华为荣耀7中测试，能正常使用，其余机型涉及屏幕分辨率问题，可能无法正常使用
使用方法：
1. 下载安装python 3.7
2. 在python安装目录中打开命令行工具，输入命令 *pip install \project_path\requirement.txt* project_path为项目目录
3. 启动游戏，手动进入 *离岛* 战斗准备画面
4. 输入命令 *python \project_path\yinyangshi.py* 启动本程序，根据提示操作

* 需勾选 **取消** 截图分享 
* 可选参数
    * --btype TEXT     战斗的种类 jinbi yuhun
    * --count INTEGER  战斗次数
    * --wifi           是否选用无线连接

## 2019-05-03更新
* 加入图像匹配，自动根据战斗画面进入下步操作
## 2019-05-04更新
* 使用subprocess替换os.system及os.popen
* 更新配置逻辑