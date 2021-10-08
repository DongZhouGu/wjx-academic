## 前言

由于问卷星更新了，里面加了阿里云智能验证的接口，所以之前的方法使用 selnium 不行了。

前端通过简单的判断就可以知道是不是 webdriver，解决的办法可以使用中间代理过滤掉 webdrvier 中的指纹信息，太过繁琐且不太好移植

**:smile: 因此使用puppeteer的V2.0来了！**



## 使用说明

###  新建python工程

建议使用 IDE Pycharm ， 工程目录如下

![image-20201130155501104](https://gitee.com/ma_tung_zhou/imageuse1/raw/master/imgg/20201130161359.png)



## 安装环境

### Requirements

- Python 3.5+
- time
- pyyaml
- pypuppter(https://github.com/miyakogi/pyppeteer)

```
python3 -m pip install pyppeteer -i https://pypi.tuna.tsinghua.edu.cn/simple
```

也可以直接在 Pycharm 中安装此包

安装包完成后，接着，修改下图所示的

![image-20201130160506924](https://gitee.com/ma_tung_zhou/imageuse1/raw/master/imgg/20201130161357.png)

的  `pyppeteer/_init_.py` 的文件，修改第14行代码为 

```
__chromium_revision__ = '818858'
```

![image-20201130160601402](https://gitee.com/ma_tung_zhou/imageuse1/raw/master/imgg/20201130161355.png)

😥 我就是因为这里的坑停滞了许久许久……………………,因为低版本的不支持Input.insertText 这个函数，没有这个函数 所有的中文字段都不能输入。

### 开始使用

第一次运行，会下载chromium，如果慢的话百度 `pyppeteer下载chromium慢`

也可以下载我下载好的 放在下面的路径，`local-chromium` 文件夹没有的话请自己新建

![image-20201130175842517](https://gitee.com/ma_tung_zhou/imageuse1/raw/master/imgg/20201130180242.png)



> 链接：https://pan.baidu.com/s/1SAkLTAnOjwo1Eg9_oIJ6fQ 
> 提取码：s64h 
> 复制这段内容后打开百度网盘手机App，操作更方便哦



其他的设置和之前一样，在 `setting_config_yaml` 里设置，同样需要抓包软件，之前的chromdriver不需要了

详情见 `setting_config_yaml`中的解释



## 附：Fiddler抓包软件

https://www.telerik.com/fiddler 官网下载，也可以去垃圾网站下载快点http://www.downza.cn/soft/234727.html

下载完成一路安装完成，第一次打开 需要设置一下，以后就不用了

在Tools-Options里按如下勾选

![image-20201111214924296](https://gitee.com/ma_tung_zhou/imageuse1/raw/master/imgg/image-20201111214924296.png)

设置完成，下面看一下怎么抓取授权

### 抓取授权信息

首先在电脑微信上打开 抓取授权用的连链接（不要填写该问卷，否则失效），如下，先不要点击“一键登录”

![image-20201111215137304](https://gitee.com/ma_tung_zhou/imageuse1/raw/master/imgg/image-20201111215813440.png)

先在Fidder软件内使用`Ctrl+X`快捷键清空页面，再在微信点击“`一键登录`”

![image-20201111215720738](https://gitee.com/ma_tung_zhou/imageuse1/raw/master/imgg/image-20201111215137304.png)

在Fiddler中找到如下open.weixin.qq.com的这条记录，一般选择在www.wjx.cn下面这条

在右边的Inspectors窗口内就有我们要的授权

![image-20201111215813440](https://gitee.com/ma_tung_zhou/imageuse1/raw/master/imgg/image-20201111215720738.png)

![image-20201111215950139](https://gitee.com/ma_tung_zhou/imageuse1/raw/master/imgg/image-20201111215950139.png)

复制好授权信息，替换`setting_config.yaml`中的url即可，其他设置见`setting_config.yaml`中的注释

