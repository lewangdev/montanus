静态资源发布工具
===============

## 原则

### 二进制资源优先

支持的二进制文件类型：

```python
IMAGE_FILE_EXTS = [
    'svg', 'tif', 'tiff', 'wbmp',
    'png', 'bmp', 'fax', 'gif',
    'ico', 'jfif', 'jpe', 'jpeg',
    'jpg', 'woff', 'cur', 'webp',
    'swf', 'ttf', 'eot'
    ]
```

### 文本文件递归解析

支持的文本文件类型：

```python
TEXT_FILE_EXTS = [
    'css', 'tpl', 'js', 'php',
    'txt', 'json', 'xml', 'htm',
    'text', 'xhtml', 'html', 'md',
    'coffee', 'less', 'sass', 'jsp'
    ]
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





