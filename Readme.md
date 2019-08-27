# Fingerprint

一个CMS指纹识别工具，捎带着识别了开发语言和Web组件。
我从网上搜集了2K+CMS指纹，而且没有使用多线程，识别起来可能有些耗时。

## 安装
您需要Python 2.7，不再需要别的了
>git clone --depth 1 https://github.com/Lewiswu1209/fingerprint.git

## 使用
>python fingerprint.py http://www.baidu.com/

因为使用单线程，所以识别耗时，默认开启了快速模式，识别到一个匹配的指纹立即退出。
如果想尝试匹配全部指纹，可以修改fingerprint.py：
>rs_web  = web.scan(sys.argv[1], True)
为：
>rs_web  = web.scan(sys.argv[1], False)
这将匹配全部指纹信息，大约需要10到15分钟

如果您愿意帮我更新指纹库，或者修bug，给我pull request或者提issue。
