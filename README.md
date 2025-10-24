# characterLive-patch

characterLive 补丁，当前可实现无用歌曲删除。

## 功能特性

- 🎯 **智能搜索**：递归搜索指定目录中包含歌名的所有文件
- 💾 **配置保存**：自动保存项目路径，下次启动时自动加载
- 📊 **实时输出**：终端窗口实时显示搜索和删除进度
- 🔒 **安全确认**：删除前需要用户确认，防止误操作
- 🎨 **友好界面**：简洁直观的图形界面

## 搜索范围

工具会在以下目录中递归搜索包含歌名的文件：

1. `characterLive项目/songs`
2. `singsong项目/songs`
3. `singsong项目/output`

> 注意：so-vits-svc项目路径已预留，可根据需要在代码中添加搜索目录

## 使用方法

### 方法一：直接运行Python脚本

1. 确保已安装Python 3.7+
2. 运行以下命令：

   ```bash
   python file_cleaner_app.py
   ```

### 方法二：打包为EXE可执行文件

1. 安装PyInstaller：

   ```bash
   pip install pyinstaller
   ```

2. 打包为单个exe文件：

   ```bash
   pyinstaller build.spec
   ```

   或者使用命令行方式：

   ```bash
   pyinstaller --onefile --windowed --name="characterLive-patch" file_cleaner_app.py
   ```

3. 打包完成后，exe文件位于 `dist` 文件夹中

4. 双击 `characterLive-patch.exe` 即可运行

## 界面说明

### 输入区域

1. **characterLive项目**：选择characterLive项目的根目录
2. **singsong项目**：选择singsong项目的根目录
3. **so-vits-svc项目**：选择so-vits-svc项目的根目录
4. **歌名**：输入要删除的歌名（文件名包含此文本的文件将被删除）

### 输出区域

- 显示搜索进度
- 显示找到的文件列表
- 显示删除结果和统计信息

## 配置文件

应用程序会在同级目录下创建 `config.json` 配置文件，用于保存项目路径。首次点击"删除"按钮后自动创建。

配置文件格式：

```json
{
    "characterlive_path": "路径1",
    "singsong_path": "路径2",
    "sovits_path": "路径3"
}
```

## 注意事项

⚠️ **重要提示**：

1. 删除操作**不可撤销**，请谨慎操作
2. 建议在删除前先备份重要文件
3. 首次使用请仔细检查项目路径是否正确
4. 文件匹配规则：文件名**包含**歌名即会被删除（不区分大小写的部分匹配）

## 系统要求

- Windows 7 或更高版本
- Python 3.7+ (如果运行源码)
- 约 20MB 磁盘空间 (打包后的exe)

## 开发信息

- 开发语言：Python 3
- GUI框架：tkinter (Python标准库)
- 打包工具：PyInstaller

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 更新日志

### v1.0.0 (2025-10-24)

- ✨ 初始版本发布
- ✨ 支持三个项目路径配置
- ✨ 递归搜索和删除功能
- ✨ 配置文件自动保存
- ✨ 实时终端输出
- ✨ 多线程异步删除
