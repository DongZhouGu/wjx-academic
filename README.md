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

修改下图所示的

![image-20201130160506924](https://gitee.com/ma_tung_zhou/imageuse1/raw/master/imgg/20201130161357.png)

的  `pyppeteer/_init_.py` 的文件，修改第14行代码为 

```
__chromium_revision__ = '818858'
```

![image-20201130160601402](https://gitee.com/ma_tung_zhou/imageuse1/raw/master/imgg/20201130161355.png)

😥 我就是因为这里的坑停滞了许久许久……………………,因为低版本的不支持Input.insertText 这个函数，没有这个函数 所有的中文字段都不能输入。

### 开始使用

第一次运行，会下载chromium，如果慢的话百度 `puppeteer下载chromium慢`

其他的设置和之前一样，在 `setting_config_yaml` 里设置

详情见 `setting_config_yaml`中的解释