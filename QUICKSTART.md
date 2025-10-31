# 快速开始指南

## 🎯 选择使用方式

### 1. 仅本地使用 → 命令行工具
最简单，直接运行Python脚本

### 2. 本地Web界面 → Streamlit或Flask
更友好的界面体验

### 3. 公网访问 → Streamlit Cloud部署
让任何人都能通过网址使用

---

## 💻 本地使用（命令行）

**适合：** 熟悉命令行，批量处理文档

```bash
# 1. 安装依赖
pip3 install python-docx

# 2. 转换文档
python3 md2gov_docx.py input.md output.docx

# 完成！
```

---

## 🌐 本地使用（Streamlit Web）

**适合：** 喜欢图形界面，本地或内网使用

```bash
# 1. 安装依赖
pip3 install streamlit python-docx

# 2. 启动应用
streamlit run streamlit_app.py
# 或使用快捷脚本
./run_streamlit.sh

# 3. 浏览器打开
# http://localhost:8501
```

**界面特点：**
- 干净的蓝白配色
- 支持文件上传和文本粘贴
- 双标签页切换
- 可折叠的帮助说明

---

## ☁️ 公网部署（5分钟搞定）

**适合：** 需要分享给他人使用，随时随地访问

### 最简单的方法：Streamlit Cloud（免费）

#### 步骤1: 准备GitHub仓库

```bash
# 初始化git（如果还没有）
git init
git add .
git commit -m "Initial commit"

# 推送到GitHub
# 先在GitHub创建新仓库，然后：
git remote add origin https://github.com/你的用户名/你的仓库名.git
git push -u origin main
```

#### 步骤2: 部署到Streamlit Cloud

1. 访问 https://streamlit.io/cloud
2. 用GitHub账号登录
3. 点击"New app"
4. 选择你的仓库
5. 主文件路径填: `streamlit_app.py`
6. 点击"Deploy"

⏱️ **等待2-3分钟部署完成**

✅ **完成！** 你会得到一个公网URL，比如:
```
https://your-app-name.streamlit.app
```

现在任何人都可以通过这个网址使用你的工具了！

---

## 📱 使用教程

### 上传文件模式

1. 选择"上传文件"标签页
2. 点击或拖拽Markdown文件
3. 点击"转换并下载"按钮
4. 浏览器自动下载Word文档

### 粘贴文本模式

1. 选择"粘贴文本"标签页
2. 在文本框中粘贴或输入Markdown内容
3. 点击"转换并下载"按钮
4. 浏览器自动下载Word文档

---

## 📝 Markdown示例

```markdown
# 关于加强公文格式管理的通知

## 一、总体要求

各单位要高度重视公文格式规范化工作，严格按照标准执行。

## 二、具体措施

### 1. 字体要求

正文采用**仿宋_GB2312字体**，字号为三号（16磅）。

### 2. 页面设置

页边距设置如下：
- 上边距：37毫米
- 下边距：35毫米
- 左边距：28毫米
- 右边距：26毫米

### （一）加强培训

各部门要组织*专题培训*，确保工作人员熟练掌握标准。

### （二）严格把关

建立审核机制，对不规范的公文**一律退回修改**。
```

---

## 🎨 格式效果

转换后的Word文档会自动应用：

| 元素 | 字体 | 字号 | 样式 |
|------|------|------|------|
| 主标题 | 方正小标宋简体 | 22磅 | 加粗居中 |
| 一级标题 | 黑体 | 16磅 | 常规 |
| 二级标题 | 楷体_GB2312 | 16磅 | 加粗 |
| 正文 | 仿宋_GB2312 | 16磅 | 常规 |

**页面设置：**
- 行距：固定值28.8磅
- 首行缩进：2字符
- 段前段后：0

完全符合《党政机关公文格式》GB/T 9704-2012标准

---

## ❓ 常见问题

### Q: 生成的文档字体不正确？
A: 系统需要安装中文字体：仿宋_GB2312、楷体_GB2312、黑体、方正小标宋简体

**macOS用户：** 
- 打开"字体册"应用检查
- 可从Windows系统复制字体文件

**Windows用户：**
- 通常已预装所需字体

### Q: Streamlit Cloud部署失败？
A: 检查：
1. requirements.txt是否包含所有依赖
2. Python代码是否有语法错误
3. GitHub仓库是否为public

### Q: 能同时给多人使用吗？
A: 
- Streamlit Cloud免费版支持多用户同时访问
- 但有资源限制（1GB内存）
- 如需更高性能，考虑升级plan

---

## 📚 更多资源

- **完整功能说明**: [README.md](README.md)
- **部署详细教程**: [DEPLOY.md](DEPLOY.md)
- **Flask版本说明**: [WEB_USAGE.md](WEB_USAGE.md)

---

## 🆘 需要帮助？

遇到问题可以：
1. 查看对应的文档说明
2. 检查错误提示信息
3. 确认文件格式和内容是否正确

---

**祝使用愉快！** 🎉
