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

## 私有仓库安装须知

> **HACS 官方不支持直接安装 private GitHub 仓库。** 本仓库按 private 保存，可作为私人源码及更新存档；如果你需要在 Home Assistant 中安装，请使用以下手动安装办法。未来如果愿意将不含私密数据的源码仓库设为 public，才可以按 HACS 的「自定义仓库」流程添加。请勿把 GitHub Token、京东 Cookie 或设备凭据上传 Git。

1. 在 GitHub 登录有权限访问本 private 仓库的账号，下载最新 Release 附件 `jd-xiaojia-ha-<版本号>.zip`。
2. 解压后将 `custom_components/jd_smart` 文件夹复制到 Home Assistant 配置目录下的 `custom_components/jd_smart`（例如 HAOS 的 `/config/custom_components/jd_smart`）。
3. **如果已经安装原版 `ha-jd-smart`，请先备份**：两者集成域名都是 `jd_smart`，不能同时存在。
4. 重启 Home Assistant，然后在「设置 → 设备与服务 → 添加集成」中搜索 `JD Smart / JD Xiaojia`。
5. 需要配置你自己的已授权京东小家请求参数（Cookie、tgt 等），以及目标设备信息。**请仅在你自己的 HA 中配置凭据，勿将登录凭据发到聊天或提交到 Git。**
6. 成功添加后先验证只读状态，再单独验证目标 600G Pro 的控制协议；未经验证，请保持冲洗按钮禁用。

如需后续从 private GitHub 自动更新，可选用具备私有仓库凭据支持的第三方更新工具，但那**不是 HACS 原生安装**，需要自行维护 GitHub 最小权限 Token。

## 测试与兼容性边界

- 源码包含 `tests_offline` 的脱离 HA 环境的逻辑测试。
- **目前仅完成离线测试，未在实际 Home Assistant 系统进行完整集成测试。**
- 京东云端 API 不是官方公开承诺的稳定接口，可能随版本变化。
- 曾在京东小家 App 中观察到两台不同控制界面的净水器，不能假定它们的控制字段完全一致。
- 与 Home Assistant 正式运行无关的 MuMu 实验、抓包、认证数据均**不在本仓库的发布清单中**。

## 许可与来源

本项目保留 [ha-jd-smart](https://github.com/orangeboyChen/ha-jd-smart) 的 MIT 许可证和免责声明，详见 `LICENSE` 与 `DISCLAIMER.md`。
