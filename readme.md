# yinyangshi
## YYS自动刷怪脚本
## 利用adb实现控制安卓手机。
## 需要根据打怪的速度及手机加载场景的速度调整timer参数
## 在命令行中使用
## 使用前需开启手机的开发者模式及USB DEBUG
使用方法：
* 启动游戏，进入离岛战斗准备画面
* 手机USB连接电脑
* 可选WiFi模式，需手机与电脑在同一局域网下
* python yinyangshi.py lidao
* 需勾选 **取消** 截图分享 
* 可选参数
    * --btype TEXT     战斗的种类 jinbi yuhun
    * --count INTEGER  战斗次数
    * --wifi BOOLEAN   是否选用无线连接

## 2019-05-03更新
* 加入图像匹配，自动根据战斗画面进入下步操作
