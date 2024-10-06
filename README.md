# 编码转换工具

![License](https://img.shields.io/badge/license-MIT-blue.svg)

**编码转换工具** 是一款用户友好的桌面应用程序，旨在高效地转换文本文件的字符编码。无论您处理不同语言的编码，还是需要标准化文件格式，这个工具都能通过直观的图形界面简化您的工作流程。

## 功能

- **多语言支持**
  - 轻松切换语言，满足不同地区用户的需求。
  
- **批量转换**
  - 选择多个文件或整个文件夹进行批量编码转换。
  
- **自动检测编码**
  - 自动检测文件的源编码，确保准确转换。
  
- **进度跟踪**
  - 通过可视化的进度条实时监控转换状态。
  
- **自定义编码选项**
  - 从多种源编码和目标编码中选择，满足不同需求。
  
- **全选功能**
  - 快速选择或取消选择所有文件进行转换。

## 截图

![编码转换工具截图](https://github.com/user-attachments/assets/19555e6d-98d8-42a6-b12e-47ceede3d93d)

*展示编码转换工具界面的截图。*

## 安装

### 前提条件

- **Python 3.7 或更高版本**
  - 确保已安装 Python。可从 [python.org](https://www.python.org/downloads/) 下载。

### 步骤

1. **克隆仓库**

    ```bash
    git clone https://github.com/yourusername/encoding-converter.git
    cd encoding-converter

2. **安装依赖**

    ```bash
    pip install -r requirements.txt
    ```

3. **运行应用**

    ```bash
    python main.py
    ```

## 使用指南

1. **选择文件或文件夹**

    - 点击“选择文件”按钮选择单个或多个文件。
    - 点击“选择文件夹”按钮选择整个文件夹进行批量转换。

2. **选择编码选项**

    - **源编码（源编码）**: 选择文件的当前编码。如果不确定，可以选择“自动识别”。
    - **目标编码（目标编码）**: 选择希望转换成的编码格式。

3. **过滤文件（可选）**

    - **过滤文件**: 指定要包含在转换中的文件扩展名。
    - **排除文件**: 指定不希望包含在转换中的文件扩展名。

4. **搜索和全选**

    - 使用搜索栏根据文件名过滤文件。
    - 使用“全选”复选框快速选择或取消选择所有文件。

5. **开始转换**

    - 点击“开始转换”按钮启动编码转换过程。
    - 通过进度条监控转换进度，并在完成后收到通知。

## 项目结构

    encoding_converter/
    ├── utils/
    │   ├── window_util.py 
    │   ├── image_util.py 
    │   ├── chardet_util.py 
    │   └── event_bus.py 
    ├── widgets/
    │   ├── multi_select_dropdown.py 
    │   ├── progress_bar.py 
    │   ├── scrollable_frame.py 
    │   ├── icon_checkbox.py 
    │   └── tooltip.py 
    │   └── underlined_frame.py 
    ├── res/ 
    │   └── icon/ 
    │       ├── waiting.png 
    │       ├── error.png 
    │       ├── success.png 
    │       ├── checkbox_uncheck.png 
    │       ├── checkbox_checked.png 
    │       └── filter.png 
    ├── settings/ 
    │   ├── encoding_options.py 
    │   └── filter_options.py 
    │   └── search_filter_options.py 
    ├── views/ 
    │   └── file_list_view.py 
    ├── managers/ 
    │   ├── progress_manager.py 
    │   ├── file_manager.py
    │   ├── LanguageManager.py
    │   └── conversion_manager.py 
    ├── locales/ 
    │   ├── zh_CN/ 
    │   │   └── LC_MESSAGES/ 
    │   │   ├── messages.po 
    │   │   └── messages.mo
    ├── main.py
    ├── .gitignore
    ├── requirements.txt
    └── README.md
