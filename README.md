# SubdomainX

## 参数说明

```shell
# 参数
-d   --domain     待查询域名
-z   --zoomeye    使用zoomeye知道创宇网络空间雷达
-b   --brute      子域名爆破/字典遍历
-l   --list       破解字典，默认为自带字典subname_base.txt
-e   --engine     搜索引擎更换，可在探测存活时使用
-r   --reptile    使用浏览器site功能进行查找，默认使用bing搜索引擎
-p   --pages      浏览器site的页数范围，默认为10页
```

## 使用方法

### 子域名探测

#### zoomeye网络空间雷达

```shell
python3 subdomainX.py -d baidu.com -z
```

#### 搜索引擎查询

```shell
# 常规方法
python3 subdomainX.py -d baidu.com -r 

# 调控页数
python3 subdomainX.py -d baidu.com -r  -p 20
```

### 子域名爆破

```shell
# 常规方法
python3 subdomainX.py -d baidu.com -b

# 自定义字典爆破
python3 subdomainX.py -d baidu.com -b -l <file_name>

# 切换浏览器
python3 subdomainX.py -d baidu.com -b -e https://cn.bing.com/
```

### 子域名存活探测

```shell
# 获取子域名
python3 subdomainX.py -d baidu.com -z
# 探测存活 
修改results.txt为list.txt（避免文件覆盖）
python3 subdomainX.py -d baidu.com -b -l list.txt
```

