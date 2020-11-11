以下为本程序的使用说明，

图片显示有问题去这个链接看 https://blog.csdn.net/GuDoerr/article/details/109632917

## 第一步：下载浏览器驱动

程序用的是selenium, 模拟浏览器的，所以要有你电脑上谷歌浏览器的对应版本驱动

![image-20201111214030662](https://gitee.com/ma_tung_zhou/imageuse1/raw/master/imgg/image-20201111214030662.png)

我是86.0.4240.193版本，在下表找到对应的驱动版本，然后去网站上找对应版本下载（http://chromedriver.storage.googleapis.com/index.html），下载完成后和代码目录放在一起

| chromedriver版本 | 支持的Chrome版本 |
| ---------------- | :--------------: |
| v2.46            |      v71-73      |
| v2.45            |      v70-72      |
| v2.44            |      v69-71      |
| v2.43            |      v69-71      |
| v2.42            |      v68-70      |
| v2.41            |      v67-69      |
| v2.40            |      v66-68      |
| v2.39            |      v66-68      |
| v2.38            |      v65-67      |
| v2.37            |      v64-66      |
| v2.36            |      v63-65      |
| v2.35            |      v62-64      |
| v2.34            |      v61-63      |
| v2.33            |      v60-62      |
| v2.32            |      v59-61      |
| v2.31            |      v58-60      |
| v2.30            |      v58-60      |
| v2.29            |      v56-58      |
| v2.28            |      v55-57      |
| v2.27            |      v54-56      |
| v2.26            |      v53-55      |
| v2.25            |      v53-55      |
| v2.24            |      v52-54      |
| v2.23            |      v51-53      |
| v2.22            |      v49-52      |
| v2.21            |      v46-50      |
| v2.20            |      v43-48      |
| v2.19            |      v43-47      |
| v2.18            |      v43-46      |
| v2.17            |      v42-43      |
| v2.13            |      v42-45      |
| v2.15            |      v40-43      |
| v2.14            |      v39-42      |
| v2.13            |      v38-41      |
| v2.12            |      v36-40      |
| v2.11            |      v36-40      |
| v2.10            |      v33-36      |
| v2.9             |      v31-34      |
| v2.8             |      v30-33      |
| v2.7             |      v30-33      |
| v2.6             |      v29-32      |
| v2.5             |      v29-32      |
| v2.4             |      v29-32      |

## 第二步：下载Fiddler抓包软件

https://www.telerik.com/fiddler 官网下载，也可以去垃圾网站下载快点http://www.downza.cn/soft/234727.html

下载完成一路安装完成，第一次打开 需要设置一下，以后就不用了

在Tools-Options里按如下勾选

![image-20201111214924296](https://gitee.com/ma_tung_zhou/imageuse1/raw/master/imgg/image-20201111214924296.png)

设置完成，下面看一下怎么抓取授权

### 第三步：抓取授权信息

首先在电脑微信上打开 抓取授权用的连链接（不要填写该问卷，否则失效），如下，先不要点击“一键登录”

![image-20201111215137304](https://gitee.com/ma_tung_zhou/imageuse1/raw/master/imgg/image-20201111215813440.png)

先在Fidder软件内使用`Ctrl+X`快捷键清空页面，再在微信点击“`一键登录`”

在Fiddler中找到如下open.weixin.qq.com的这条记录，一般选择在www.wjx.cn下面这条

![image-20201111215720738](https://gitee.com/ma_tung_zhou/imageuse1/raw/master/imgg/image-20201111215137304.png)

在右边的Inspectors窗口内就有我们要的授权

![image-20201111215813440](https://gitee.com/ma_tung_zhou/imageuse1/raw/master/imgg/image-20201111215720738.png)

![image-20201111215950139](https://gitee.com/ma_tung_zhou/imageuse1/raw/master/imgg/image-20201111215950139.png)

复制好授权信息，替换`setting_config.yaml`中的url即可，其他设置见`setting_config.yaml`中的注释