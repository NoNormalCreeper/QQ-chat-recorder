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
python main.py [-h] {send,stop,start} ...
```

### 参数

```bash
positional arguments:
  {send,stop,start}
    send             Send a message to a user or group.
    stop             Stop the recorder.
    start            Start the recorder.

options:
  -h, --help         show this help message and exit
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

其中 `User ID` 与 `Group ID` 中应指定一个，若同时指定则以 `Group ID` 为准

## 运行示例

#### 启动记录器

```bash
python main.py
```

### 发送一条私聊消息

给用户 `114514` 发送一条私聊消息以表示喜爱。

```bash
python main.py send -u 114514 --message "[CQ:face,id=318] suki"
```

![发送效果](image/README/suki_to_114514.png)

返回如下提示：

```plaintext
2022-08-28 22:18:25.945 | INFO     | src.log:write_log:16 - Response < 
{
    "data": {
        "message_id": -207246359
    },
    "echo": "send_mannually_by_cmd_1661696305.9210277",
    "retcode": 0,
    "status": "ok"
}
```

## 贡献

欢迎大家贡献代码、改进文档、寻找bug、提出新功能建议等。

## 关于
