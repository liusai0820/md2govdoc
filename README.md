# Markdown转政府公文格式工具

一键将Markdown文件转换为符合国家标准的政府公文格式Word文档。

## ✨ 功能特性

- ✅ **完全符合国标**：按照《党政机关公文格式》GB/T 9704-2012标准
- ✅ **自动格式化**：自动应用字体、字号、行距、页边距等格式
- ✅ **支持多级标题**：支持主标题、一级、二级、三级标题
- ✅ **行内格式**：支持加粗、斜体等Markdown语法
- ✅ **列表支持**：支持无序列表和任务列表
- ✅ **简单易用**：单个命令即可完成转换

## 📋 格式规范

### 页面设置
- 上边距：37mm
- 下边距：35mm
- 左边距：28mm
- 右边距：26mm

### 字体字号
| 元素 | 字体 | 字号 | 样式 | 对齐 |
|------|------|------|------|------|
| 主标题（#） | 方正小标宋简体 | 22磅（二号） | 加粗 | 居中 |
| 一级标题（##） | 黑体 | 16磅（三号） | 常规 | 两端对齐 |
| 二级标题（###） | 楷体_GB2312 | 16磅（三号） | 加粗 | 两端对齐 |
| 三级标题（####） | 楷体_GB2312 | 16磅（三号） | 常规 | 两端对齐 |
| 正文 | 仿宋_GB2312 | 16磅（三号） | 常规 | 两端对齐 |

### 段落格式
- 行距：固定值28.8磅
- 首行缩进：2字符（约32磅）
- 段前段后间距：0

## 🚀 快速开始

### 方式1：Streamlit Web应用（推荐，可公网部署）

```bash
# 安装依赖
pip3 install streamlit python-docx

# 启动应用
streamlit run streamlit_app.py
# 或使用启动脚本
./run_streamlit.sh
```

然后在浏览器中打开：**http://localhost:8501**

🌟 **Streamlit版本特点**：
- ✅ 干净纯色设计，简洁专业
- ✅ 支持文件上传和文本粘贴
- ✅ 一键部署到Streamlit Cloud（免费）
- ✅ 支持多云平台部署

🚀 **公网部署**：详细步骤请查看 [DEPLOY.md](DEPLOY.md)

### 方式2：Flask Web服务（本地使用）

```bash
# 安装依赖
pip3 install flask flask-cors python-docx

# 启动Web服务
python3 app.py
```

然后在浏览器中打开：**http://localhost:5000**

详细说明请查看 [WEB_USAGE.md](WEB_USAGE.md)

### 方式2：命令行

```bash
# 安装依赖
pip install python-docx

# 转换文档
python md2gov_docx.py input.md output.docx

# 示例
python md2gov_docx.py example.md example_formatted.docx
```

## 📝 Markdown语法支持

### 标题

```markdown
# 主标题（文档标题，只能有一个）
## 一级标题
### 二级标题
#### 三级标题
```

### 正文

```markdown
普通正文内容，会自动应用首行缩进和合适的行距。
```

### 列表

```markdown
- 无序列表项1
- 无序列表项2
* 也支持星号
☑ 任务列表项
```

### 行内格式

```markdown
这是**加粗文本**
这是*斜体文本*
```

### 分隔线

```markdown
---
***
___
```

## 📁 项目结构

```
docx-formatter/
├── streamlit_app.py        # Streamlit Web应用（推荐，可公网部署）
├── md2gov_docx.py          # 核心转换逻辑
├── app.py                  # Flask Web服务（本地使用）
├── .streamlit/
│   └── config.toml         # Streamlit配置
├── static/
│   └── index.html          # Flask前端页面
├── example.md              # 示例Markdown文件
├── README.md               # 主说明文档
├── DEPLOY.md               # 公网部署指南
├── WEB_USAGE.md            # Flask服务说明
├── requirements.txt        # Python依赖
├── run_streamlit.sh        # Streamlit启动脚本
├── start_server.sh         # Flask启动脚本
├── .gitignore              # Git忽略文件
├── convert_and_format.py   # 旧版本
├── format_docx_v4.py       # 旧版本
└── md_to_docx.py           # 旧版本
```

## ⚠️ 注意事项

### 字体安装

本工具使用以下字体，请确保系统已安装：

- **仿宋_GB2312**
- **楷体_GB2312**
- **黑体**
- **方正小标宋简体**

#### macOS用户

1. 打开"字体册"应用
2. 搜索所需字体
3. 如果缺少，可从以下途径获取：
   - 从Windows系统复制字体文件
   - 下载对应的字体包
   - 使用替代字体（需修改代码中的字体常量）

#### Windows用户

Windows系统通常已预装所需中文字体。

### 常见问题

**Q: 生成的文档字体不正确？**  
A: 请检查系统是否已安装所需字体。可以在"字体册"（macOS）或"字体设置"（Windows）中确认。

**Q: 格式不符合要求？**  
A: 请确保Markdown文件使用正确的语法标记。可以参考`example.md`示例文件。

**Q: 支持表格和图片吗？**  
A: 当前版本暂不支持表格和图片，如有需要可联系开发者添加功能。

## 🔄 版本历史

### v1.0.0 (当前版本)
- ✅ 完整的Markdown解析
- ✅ 精确的公文格式控制
- ✅ 行内格式支持（加粗、斜体）
- ✅ 多级标题支持
- ✅ 列表项支持
- ✅ 完善的错误处理
- ✅ 友好的命令行界面

## 📄 许可证

本项目仅供个人学习和内部使用。

## 🤝 贡献

欢迎提出问题和改进建议！

---

**开发者**: Qibaoba  
**最后更新**: 2025-10-31
