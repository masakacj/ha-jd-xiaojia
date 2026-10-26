# 京东小家净水器 — Home Assistant 集成（私人维护版）

本项目基于 [orangeboyChen/ha-jd-smart](https://github.com/orangeboyChen/ha-jd-smart)（MIT 许可）增加京东小家净水器的只读状态展示与可选的冲洗控制。**不是京东官方产品，不保证所有型号兼容。**

## 当前支持

- 保留原项目京东小家账号认证、令牌续期、设备发现、设备状态轮询及空调支持。
- 根据设备名称/分类识别净水器，显示云端实际返回的状态字段；已从小程序代码确认的部分字段使用友好的名称：
  - `PureTDS` — 纯水 TDS（ppm）
  - `Filter1Life` / `Filter2Life` — 一级/二级滤芯剩余寿命（%）
  - `State` / `Wash` / `Offline` — 工作状态、冲洗状态、设备状态原始值
  - `ResetFilter` — 滤芯复位状态（**仅只读显示，绝不自动复位**）
- 目标设备：用户确认「二楼净水器」为 600G Pro；此型号的**实际设备 ID 与云端写入命令尚未完成验证**。
- 只有填入**从目标设备实际成功调用中确认的** `flush_feed_id`、`flush_stream_id`、`flush_value` 后，才会在 HA 生成一键冲洗按钮。**不预设控制值、不执行定时冲洗、不自动写设备。**

## 通过 HACS 安装

1. 打开 Home Assistant → **HACS → 右上角菜单 → 自定义仓库（Custom repositories）**。
2. 仓库地址填写 `https://github.com/masakacj/ha-jd-xiaojia`，类型选择 **Integration（集成）**，点击添加。
3. 在 HACS 中找到 **JD Xiaojia / 京东小家净水器**，下载安装。若没有立即显示，可刷新 HACS 页面。
4. **如果已经安装原版 `ha-jd-smart`，请先备份**：两者集成域名都是 `jd_smart`，不能同时存在。
5. 重启 Home Assistant，在「设置 → 设备与服务 → 添加集成」搜索 `JD Smart / JD Xiaojia`。
6. 按你自己的已授权京东小家会话配置参数（Cookie、tgt 等）与设备信息。**这些私密信息仅填写在自己的 HA 内，不要上传到公开 GitHub。**
7. 添加后先验证只读状态。600G Pro 自动冲洗操作尚待真实设备写入与云端接口验证，默认不启用。

也可以通过 [Releases](https://github.com/masakacj/ha-jd-xiaojia/releases) 下载 ZIP，手动复制其中的 `custom_components/jd_smart` 到 HA 配置目录的 `custom_components/jd_smart`。

## 测试与兼容性边界

- 源码包含 `tests_offline` 的脱离 HA 环境的逻辑测试。
- **目前仅完成离线测试，未在实际 Home Assistant 系统进行完整集成测试。**
- 京东云端 API 不是官方公开承诺的稳定接口，可能随版本变化。
- 曾在京东小家 App 中观察到两台不同控制界面的净水器，不能假定它们的控制字段完全一致。
- 与 Home Assistant 正式运行无关的 MuMu 实验、抓包、认证数据均**不在本仓库的发布清单中**。

## 许可与来源

本项目保留 [ha-jd-smart](https://github.com/orangeboyChen/ha-jd-smart) 的 MIT 许可证和免责声明，详见 `LICENSE` 与 `DISCLAIMER.md`。
