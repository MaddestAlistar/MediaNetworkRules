# 家庭影音连接排查清单

## 1. 确认连接地址与协议

- 确认使用的是 **你自己或已获授权** 的服务器域名、端口、路径（Emby / Jellyfin / NAS）。
- 内外网是否切换、系统 DNS 是否解析到可达 IP、证书是否可信？
- HTTPS 反向代理是否转发 Host / WebSocket，路径重写与端口映射是否正确？

## 2. 典型现象

| 现象 | 优先检查 |
|---|---|
| 网页能进、媒体不能播 | 授权、转码、媒体路径、Range 请求、音视频解码能力 |
| 内网正常、外网超时 | 端口映射、CGNAT、DNS 解析与访问策略 |
| 首帧慢或高码率缓冲 | 直连/代理路径、服务器带宽、是否发生转码 |
| TLS 错误 | 证书链、域名、系统时间、HTTPS 混用 |
| CarPlay 等客户端异常 | App 自身适配、音视频格式、客户端 UA 与日志 |

## 3. 逐层测量（仅自有服务器）

```bash
python3 scripts/diagnose.py --host media.example.test
python3 scripts/diagnose.py --url https://media.example.test/
```

网页打开不等于真实视频可播放。记录测试客户端、系统版本、媒体格式、错误码、测试网络和时间，注意隐去密码与 Token。
