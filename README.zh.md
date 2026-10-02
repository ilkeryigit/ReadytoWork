# ReadytoWork

**Windows 托盘启动器：程序、文件夹、文档和网址，一键直达。**

[English](README.md) · [Türkçe](README.tr.md) · [中文](README.zh.md) · [Deutsch](README.de.md) · [Italiano](README.it.md)

---

## 适合谁？

博士生、硕士生、大学生和办公室职员——简而言之，任何每天上班都要先打开同一批
工具的人。

## 为什么？

你是否每天早上都要先打开几十个文件、程序和网址，才能开始工作？在开始菜单和
桌面里翻找浪费掉的那些分钟，是否在一点点削弱你的专注力、消耗你的真实时间？

如果答案是肯定的，这个工具就是为你准备的。只需一次点击，全部同时打开——
你不必再花时间收集工具，而是可以直接开始工作，别再把一天的开始浪费在寻找上。

这是一个小而诚实的小工具：无需账号、没有云端、没有遥测、没有后台网络流量。
你的列表就保存在本机的一个 JSON 文件里。

## 功能

- **托盘菜单** — 列出全部条目，并提供 *全部打开*，一键开启新一天
- **四种条目类型** — 程序、文件夹、文档、网址
- **五种语言** — English、Türkçe、Deutsch、Italiano、中文，随时切换
- **设置持久保存** — 存放在 `%APPDATA%\ReadytoWork\config.json`，采用原子写入，
  崩溃或磁盘写满都不会损坏设置
- **排序与重命名** — 上下移动条目，就地编辑
- **浏览器选择** — 用系统默认浏览器、Chrome、Firefox 或 Edge 打开网址
- **单实例运行** — 重复启动不会有任何反应，不会叠加多个进程
- **原生安装程序** — 开始菜单和桌面快捷方式、可选的开机自启、卸载时一并清除设置

## 安装

从 [Releases 页面](https://github.com/ilkeryigit/ReadytoWork/releases) 下载安装
程序，运行 `ReadytoWork-Setup-1.0.0.exe` 并按需勾选选项。

> 安装程序未做代码签名，首次运行时 Windows SmartScreen 可能提示警告。选择
> *更多信息 → 仍要运行*。

## 使用

1. 启动 ReadytoWork。首次运行会自动打开设置窗口。
2. 点击 **添加**，选择类型、填写名称并选择路径（或粘贴网址）。
3. 点击 **保存**。该条目已进入托盘菜单。
4. 右键点击托盘图标 → *全部打开*。

卸载应用时，设置会一并删除。

## 从源码构建

需要 Windows 上的 Python 3.10+。

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# 以源码方式运行
.\.venv\Scripts\python.exe readytowork.py

# 运行测试
.\.venv\Scripts\python.exe -m pytest tests -v

# 生成单文件可执行程序 -> dist\ReadytoWork.exe
.\.venv\Scripts\python.exe -m PyInstaller --clean --noconfirm ReadytoWork.spec

# 生成安装程序 -> dist\ReadytoWork-Setup-1.0.0.exe   （需要 Inno Setup 6）
& "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe" installer.iss
```

## 翻译

所有界面文案都存放在 `lang/<代码>.json`。新增语言的步骤见
[CONTRIBUTING.md](CONTRIBUTING.md)。

## 参与贡献

欢迎贡献——问题反馈、翻译、小功能都能帮上忙。这是一个仅支持 Windows 的工具，
除 `pystray` 和 `Pillow` 外没有运行时依赖，我们希望保持这一点。

- **缺陷与想法：** 提一个 issue。提交前请先看看是否已有同类 issue。
- **小修复与翻译：** 优先查看带有
  [`good first issue`](https://github.com/ilkeryigit/ReadytoWork/labels/good%20first%20issue)
  标签的 issue——它们的范围经过刻意控制，适合作为第一次贡献。
- **较大的改动：** 请先提 issue 讨论方案，再动手写代码。

环境搭建、基本规则以及新增语言的步骤见 [CONTRIBUTING.md](CONTRIBUTING.md)。
所有参与者都需遵守[行为准则](CODE_OF_CONDUCT.md)。

## 隐私

没有统计分析、没有网络请求、没有用户追踪。安装目录之外唯一被写入的文件是
`%APPDATA%\ReadytoWork\config.json`，其中保存你自己创建的条目。测试套件包含一项
自动检查，确保仓库中不会混入个人路径、用户名或邮箱地址。

## 许可协议

[MIT](LICENSE) © 2026 ilkeryigit