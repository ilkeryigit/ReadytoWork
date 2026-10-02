# ReadytoWork

**Windows 托盘启动器：程序、文件夹、文档和网址，一键直达。**

[English](README.md) · [Türkçe](README.tr.md) · [中文](README.zh.md) · [Deutsch](README.de.md) · [Italiano](README.it.md)

---

## 为什么？

每天早上你都会打开同样的几样东西：正在写的文档、文献管理器、存放资料的文件夹、
一个仪表盘。ReadytoWork 把它们集中在一个托盘菜单里，一键全部打开，不必再去开始
菜单和桌面翻找。

这是一个小而诚实的小工具：无需账号、没有云端、没有遥测、不产生后台网络流量。
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

## 隐私

没有统计分析、没有网络请求、没有用户追踪。安装目录之外唯一被写入的文件是
`%APPDATA%\ReadytoWork\config.json`，其中保存你自己创建的条目。测试套件包含一项
自动检查，确保仓库中不会混入个人路径、用户名或邮箱地址。

## 许可协议

[MIT](LICENSE) © 2026 ilkeryigit