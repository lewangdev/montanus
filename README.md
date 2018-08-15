静态资源发布工具
===============

## 原则

### 二进制资源优先

支持的二进制文件类型：

```python
 __binary_file_exts = [
        '.png', '.bmp', '.gif', '.ico',
        '.jfif', '.jpe', '.jpeg', '.jpg'
    ]

```

### 文本文件递归解析

支持的文本文件类型：

```python
  __text_file_exts = ['.css', '.js']
```

模版后缀：

```python
  __templates_exts = ['.jsp', '.html']
```

#### 示例

index.html

```html
<html>
    <head>
        <link rel="apple-touch-icon" sizes="144x144" href="/apple-touch-icon-144.png">
        <link href="layout.css" media="all" rel="stylesheet" type="text/css">
    </head>
    <body>
        <img src="li.png" alt="li" />
        <script type="text/javascript" src="jquery.js"></script>
        <script type="text/javascript">
            var dialog = require('dialog/dialog.js');
            dialog.alert("I am a dialog!");
        </script>
    </body>
</html>
```

layout.css

```css
.bg{background: url(bg.png)}
```

#### 递归深度

index.html &#62; layout.css &#62; bg.png

index.html &#60; layout_987cb34ea2.css &#60; bg_087b4e5f67.png


### CDN

CSS

```css
@import url(path)
background:url(path)
background-image:url(path)
filter[Only IE]
```

JS

AMD require，或者自定义
避免直接 document.write img

HTML 包括 JSP，PHP 以及一些模版语言

```html
<script src="path">
<link href="path">
<img src="path">
```

## HowTo

-----------

### Installation

-----------

```shell
sudo apt-get install python-pip
git clone https://github.com/thisiswangle/montanus.git
cd montanus
sudo pip install .
```


### Usage

-----------

```shell
(montanus)➜  montanus git:(master) ./montanus.py -h
Montanus.

Usage:
    montanus.py <templates_path> [--with-static-files-path=<p> | --with-protocol=<p> | --with-domains=<l> | --with-md5-len=<l> | --with-md5-concat-by=<c> | --with-conf=<f> | -d]
    montanus.py (-h | --help)
montanus.py (-v | --version)

    Options:
    -h --help                          Show this help message
    -v --version                       Show version
    -d --delete                        Delete all sources
    --with-static-files-path=<p>       Set static file path. If not set, the value will be the same as template_path
    --with-protocol=<p>                Set protocol [Default: http]
    --with-domains=<d>                 Set CDN domains[Default: ]
    --with-md5-len=<l>                 Set MD5 Length [Default: 10]
    --with-md5-concat-by=<c>           Set MD5 concatenator [Default: -]
    --with-conf=<f>                    Set config file path

```

```shell
montanus 'awesome_project/src/main/webapp'
```
    
### How to work with Jenkins

-----------

在合适的时机执行脚本即可，如在构建之前添加

```shell
WEB_HOME=${WORKSPACE}/src/main/webapp
echo "Goto ${WEB_HOME} to build a version tag for all static files"
montanus ${WEB_HOME} --with-domains=s0.awesome-domain.com,s1.awesome-domain.com
```

在构建之后添加

```shell
pwd
git clean -df
```
