# 良友影音网络规则库 · MediaNetworkRules

[← 返回良友资源中心](https://maddestalistar.github.io/LiangYou-ResourceHub/) · 首版 2026-10-23

面向 **Emby / Jellyfin / NAS / WebDAV / 家庭影音** 的安全网络配置**模板**，支持 Surge、Clash/Mihomo、Quantumult X 三类规则格式，以及基础故障检查清单。

## 仓库已准备内容

- [Surge 规则片段](generated/surge-rules.conf) —— 复制到已有配置的 `[Rule]` 中（勿重复插入节头）。
- [Clash/Mihomo 直连规则集](generated/clash-direct.yaml) 和 [代理规则集](generated/clash-proxy.yaml) —— **按 DIRECT / PROXY 分开**，以防同一 Provider 中的域名被错误地统一套用策略；另有 [拒绝规则集](generated/clash-reject.yaml)（目前为空）。这些 `payload` 都不是完整可启动的 `config.yaml`，须在主配置的 `rule-providers` / `rules` 中为每组分别指定对应策略。
- [Quantumult X 规则片段](generated/quanx-filter.conf) —— 包含 `[filter_local]` 区段，不要直接覆盖现有配置。
- [域名源 CSV](rules/domains.csv)、[私网地址清单](rules/lan-cidrs.txt)。
- `scripts/build.py`：修改域名后可重新生成 Surge、Quantumult X 和按策略分类的 Clash/Mihomo 规则。
- [连接排查清单](docs/troubleshooting.md) 与 `scripts/diagnose.py`：不主动扫描网段，只检查手动指定的域名或 URL。

## 必须先做的两件事

1. 把 `rules/domains.csv` 内的 `*.example.test` 全部改成自己的主机域名；它们是保留的**虚构演示域名**，无法直接提供流媒体访问。
2. 先分清 **DIRECT / PROXY** 的含义以及设备所在网络。像 `plex.tv`、`jellyfin.org` 这种项目官网域名**不等于**你的媒体服务器域名，不能笼统要求直连。

在仓库根目录执行：

```bash
python3 scripts/build.py
python3 scripts/diagnose.py --host media.your-domain.example
# 或针对你自己的服务 URL
python3 scripts/diagnose.py --url https://media.your-domain.example/
```

## 原则

**不包含代理节点、付费线路、白名单绕过规则或未获授权服务器域名。** 不自动添加第三方影视服务域名，避免错误劫持/分流。三种配置语法不完全一致，需要在自己的客户端、网络与环境中逐项测试。不要把账号、Cookie、Token 或含凭据的完整订阅 URL 提交 Issue。

先验证 DNS → TCP/TLS → HTTP → 反代路径 → 媒体客户端，详见 [排查清单](docs/troubleshooting.md)。
