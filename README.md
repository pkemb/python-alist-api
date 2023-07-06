## 项目描述

[Alist](https://github.com/alist-org/alist) 的 python api。Alist api的说明可以参考[API Document](https://alist-doc.nn.ci/docs/api)。

仅支持Alist v2。

## 安装

```shell
pip install python-alist-api
```

## 使用方法

### 示例1：创建alist客户端

匿名登录，只能使用`/public` API。

```python
from alist import AlistClient
client = AlistClient('https://your.alist.domain')
```

使用密码或授权码登录，能使用`/public`和`/admin` API。

```python
from alist import AlistClient
client = AlistClient('https://your.alist.domain', password='xxxxx')
# 或者
client = AlistClient('https://your.alist.domain', authorization='xxxxx')
```

### 示例2：获取alist版本号

```python
version = client.public.settings.version()
```

### 示例3：获取文件列表。

```python
result = client.public.path('/xxxxx')
```

### 示例4：打开搜索

需要使用密码或授权码登录客户端。

```python
client.admin.settings.enable_search(True)
```

### 示例5：上传文件

需要使用密码或授权码登录客户端，或开启了游客上传。

```python
client.public.upload(['path/to/file1', 'path/to/file2'], '/target/path')
```
