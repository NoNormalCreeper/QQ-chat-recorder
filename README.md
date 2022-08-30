# QQ Chat Recorder

**中文** | English (WIP)

腾讯QQ客户端经常会吞掉我们的聊天记录，有可能几天前的群聊聊天记录都找不到了，而我也因此丢掉了一些重要的私聊信息，我十分不满，于是该项目应运而生。

## 安装

#### 下载项目源文件

```bash
git clone https://github.com/NoNormalCreeper/QQ-chat-recorder.git
cd QQ-chat-recorder
```

#### 安装 `pip` 包

```bash
pip install -r requirements.txt
```

#### 配置 go-cqhttp

在 [此处](https://github.com/Mrs4s/go-cqhttp/releases/) 下载最新的 release 版本。

首次启动 go-cqhttp，应有如下提示，输入 `23` 以创建正向、反向 Websocket 通信。

```plaintext
未找到配置文件，正在为您生成配置文件中！
请选择你需要的通信方式:
> 0: HTTP通信
> 1: 云函数服务
> 2: 正向 Websocket 通信
> 3: 反向 Websocket 通信
请输入你需要的编号(0-9)，可输入多个，同一编号也可输入多个(如: 233)
您的选择是:
```

输入 `23` 后，应有如下提示：

```plaintext
您的选择是:23
默认配置文件已生成，请修改 config.yml 后重新启动!
```

修改 `config.yml` 中的账号、密码。

```yml
account: # 账号相关
  uin: 123345 # QQ账号
  password: ''
```

修改 `config.yml` 中注释处的 Websocket 配置。

```yml
servers:
  - ws:
      address: 127.0.0.1:8080 # 修改正向ws端口
      middlewares:
        <<: *default
  - ws-reverse:
      universal: ws://localhost:8081 # 修改添加反向ws端口
```

使用如 screen, tmux 的工具在后台运行 go-cqhttp。

#### 配置

复制 `config-config.json` 到 `config.json`。

修改 `config.json` 中 `port-send` 字段为 go-cqhttp 中配置的正向ws端口，`port` 字段为 go-cqhttp 中配置的反向ws端口。

```json
{
    "general": {},
    "ws": {
        "host": "localhost",
        "port-send": 9601,
        "port": 9602
    }
}
```

## 用法

```bash
python main.py [-h] {send,stop,start,call,get-image} ...
```

### 参数

```bash
positional arguments:
  {send,stop,start,call,get-image}
    send                Send a message to a user or group.
    stop                Stop the recorder.
    start               Start the recorder.
    call                Call an API of go-cqhtttp.
    get-image           Get the image of chat history.

optional arguments:
  -h, --help            show this help message and exit.
```

### 开始 / 停止

```bash
python main.py start  # 也可不加start
python main.py stop
```

### 发送信息

```bash
python main.py send [-h] -m MESSAGE [-u USER] [-g GROUP]
optional arguments:
  -m MESSAGE, --message MESSAGE
                        Content of message
  -u USER, --user USER  User ID
  -g GROUP, --group GROUP
                        Group ID
```

其中 `User ID` 与 `Group ID` 中应指定一个，若同时指定则以 `Group ID` 为准。

### 调用 API

```bash
python main.py call [-h] -a ACTION -p ...
optional arguments:
  -h, --help            show this help message and exit
  -a ACTION, --action ACTION
                        API name
  -p ..., --params ...  API parameters
```

其中 `params` 应指定为 `key=value` 的形式，若有多个参数则应用空格分隔。

### 获取图片信息

```bash
python main.py get-image [-h] -n NAME
optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  file name
```

其中 `file name` 为图片缓存的文件名，通常以 `.image` 后缀结尾。

### 获取 用户/群组/消息 信息
```bash
python main.py get-info [-h] [-u USER] [-g GROUP] [-m MESSAGE]
optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  user ID
  -g GROUP, --group GROUP
                        group ID
  -m MESSAGE, --message MESSAGE
                        message ID
```

## 运行示例

#### 启动记录器

```bash
python main.py
```

#### 发送消息

给用户 `114514` 发送一条私聊消息以表示喜爱。

```bash
python main.py send -u 114514 --message "[CQ:face,id=318] suki"
```

![发送效果](image/README/suki_to_114514.png)

返回如下提示：

```json
Response < 
{
    "data": {
        "message_id": -207246359
    },
    "echo": "send_mannually_by_cmd_1661696305.9210277",
    "retcode": 0,
    "status": "ok"
}
```

返回值中 `"status": "ok"` 说明发送成功。

#### 调用 API

- API 参考：https://docs.go-cqhttp.org/api/

在群组 `1919810` 中禁言用户 `114514` 5 分钟。

```bash
python main.py call -a set_group_ban -p group_id=1919810 user_id=114514 duration=300
```

返回如下提示：

```json
Response < 
{
    "data": null,
    "echo": "call_mannually_by_cmd_1661834289.8971636",
    "retcode": 0,
    "status": "ok"
}
```

#### 获取图片信息

一天，我在看聊天记录的时候看到了这样一条消息：

```plaintext
114514 in 1919810 > [CQ:image,file=0d9312dedaa9bcb7fa9007c0d3a53aad.image,subType=0]草
```

我很好奇，想看看这张图到底是什么东西，所以我可以运行如下命令：

```bash
python main.py get-image -n 0d9312dedaa9bcb7fa9007c0d3a53aad.image
```

返回如下提示：

```plaintext
Image info < 
{0D9312DE-DAA9-BCB7-FA90-07C0D3A53AAD}.jpg    1.91 kB
https://gchat.qpic.cn/gchatpic_new/2560359315/798891715-2463410492-0D9312DEDAA9BCB7FA9007C0D3A53AAD/0?term=3
```

太好了！我点进去下面那个链接就可以看到图片了！

#### 获取群成员信息

获取群组 `1919810` 中群成员 `114514` 的信息。

```bash
python main.py get-info -g 1919810 -u 114514
```

返回如下提示：

```json
Info < 
{
    "age": 24,
    "area": "",
    "card": "",
    "card_changeable": false,
    "group_id": 1917810,
    "join_time": 1658881615,
    "last_sent_time": 1661692053,
    "level": "19",
    "nickname": "qwq",
    "role": "member",
    "sex": "male",
    "shut_up_timestamp": 0,
    "title": "",
    "title_expire_time": 0,
    "unfriendly": false,
    "user_id": 114514
}
```

可以看出来，他叫`qwq`，今年`24`岁，`男`，群名片`未设置`，`19`级，`普通成员`，最后一次发消息时间是`今天`(时间戳为`1661692053`)。

## 贡献

欢迎大家贡献代码、改进文档、寻找bug、提出新功能建议等。

## 关于
