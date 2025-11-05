# 公文格式转换器 - Flask版本

> 这是 `flask-vercel-deploy` 分支，使用前后端分离架构，实现秒开体验。

## 🚀 快速开始

### 在线使用

- **前端（秒开）**：部署在Vercel
- **后端API**：部署在Render

### 本地开发

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动后端API
gunicorn api.index:app

# 3. 打开前端
# 用浏览器打开 public/index.html
```

## 📦 部署

详细部署指南请查看：[DEPLOY_VERCEL_RENDER.md](./DEPLOY_VERCEL_RENDER.md)

### 快速部署步骤

1. **后端部署到Render**
   - 访问 https://render.com
   - 连接GitHub仓库
   - 选择 `flask-vercel-deploy` 分支
   - 自动部署

2. **前端部署到Vercel**
   - 访问 https://vercel.com
   - 连接GitHub仓库
   - 选择 `flask-vercel-deploy` 分支
   - 修改 `public/index.html` 中的API地址
   - 自动部署

## ✨ 特性

- ✅ 前端秒开，无等待
- ✅ 自动添加标题序号（一、二、三、或（一）（二）（三））
- ✅ 智能文件命名
- ✅ 支持.md、.txt、.docx格式
- ✅ 符合GB/T 9704-2012标准
- ✅ 完全免费

## 📁 项目结构

```
.
├── api/
│   └── index.py          # Flask API（后端）
├── public/
│   └── index.html        # 静态前端
├── md2gov_docx.py        # 核心转换模块
├── requirements.txt      # Python依赖
├── vercel.json          # Vercel配置
├── render.yaml          # Render配置
└── DEPLOY_VERCEL_RENDER.md  # 部署指南
```

## 🔄 与main分支的区别

| 特性 | main分支（Streamlit） | flask-vercel-deploy分支 |
|------|---------------------|------------------------|
| 技术栈 | Streamlit | Flask + 静态HTML |
| 部署平台 | Streamlit Cloud | Vercel + Render |
| 首次加载 | 30-120秒 | 前端秒开 |
| 用户体验 | 需要等待启动 | 立即可用 |
| 成本 | 免费 | 免费 |

## 📝 License

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！
