# Flask + Vercel/Render 部署指南

这个分支使用前后端分离架构，实现秒开体验：
- **前端**：静态HTML部署在Vercel（秒开）
- **后端**：Flask API部署在Render（按需启动）

## 架构优势

✅ **前端秒开**：用户打开网页立即看到界面  
✅ **完全免费**：Vercel和Render都有免费额度  
✅ **全球CDN**：Vercel提供全球加速  
✅ **自动部署**：推送代码自动部署  

---

## 方案一：前端Vercel + 后端Render（推荐）

### 第一步：部署后端API到Render

1. **注册Render账号**
   - 访问 https://render.com
   - 使用GitHub账号登录

2. **创建Web Service**
   - 点击 "New +" → "Web Service"
   - 连接你的GitHub仓库
   - 选择 `flask-vercel-deploy` 分支

3. **配置服务**
   ```
   Name: md2govdoc-api
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn api.index:app
   ```

4. **部署**
   - 点击 "Create Web Service"
   - 等待部署完成（约2-3分钟）
   - 记录你的API地址，例如：`https://md2govdoc-api.onrender.com`

### 第二步：部署前端到Vercel

1. **注册Vercel账号**
   - 访问 https://vercel.com
   - 使用GitHub账号登录

2. **导入项目**
   - 点击 "Add New..." → "Project"
   - 选择你的GitHub仓库
   - 选择 `flask-vercel-deploy` 分支

3. **配置项目**
   ```
   Framework Preset: Other
   Root Directory: ./
   Build Command: (留空)
   Output Directory: public
   ```

4. **部署**
   - 点击 "Deploy"
   - 等待部署完成（约1分钟）

5. **更新API地址**
   - 部署完成后，编辑 `public/index.html`
   - 找到第 442 行：
     ```javascript
     const API_BASE_URL = window.location.hostname === 'localhost' 
         ? 'http://localhost:5000'
         : 'https://your-api.onrender.com';  // 替换这里
     ```
   - 将 `https://your-api.onrender.com` 替换为你的Render API地址
   - 提交并推送代码，Vercel会自动重新部署

### 完成！

访问你的Vercel域名（例如：`https://your-project.vercel.app`），即可使用！

---

## 方案二：全部部署在Vercel（实验性）

Vercel也支持Python Serverless函数，但有限制：
- ⚠️ 函数执行时间限制10秒（免费版）
- ⚠️ 可能不适合大文件转换

### 部署步骤

1. **导入项目到Vercel**（同上）

2. **Vercel会自动识别配置**
   - 读取 `vercel.json` 配置
   - 自动部署前端和API

3. **测试**
   - 访问 `https://your-project.vercel.app`
   - 测试转换功能

如果遇到超时问题，建议使用方案一（Render后端）。

---

## 本地开发

### 启动后端API

```bash
# 安装依赖
pip install -r requirements.txt

# 启动Flask开发服务器
python api/index.py
# 或使用gunicorn
gunicorn api.index:app
```

后端运行在 http://localhost:8000

### 启动前端

直接用浏览器打开 `public/index.html`，或使用简单HTTP服务器：

```bash
# Python 3
python -m http.server 8080 --directory public

# 或使用Node.js
npx serve public
```

前端运行在 http://localhost:8080

---

## 环境变量配置

### Render环境变量

在Render Dashboard中可以设置：
- `PYTHON_VERSION`: 3.11.0
- `PORT`: 10000（Render自动设置）

### Vercel环境变量

通常不需要额外配置。

---

## 故障排查

### 问题1：CORS错误

确保后端API已启用CORS：
```python
from flask_cors import CORS
CORS(app)
```

### 问题2：API超时

Render免费版冷启动需要50秒-2分钟，首次访问会较慢。

### 问题3：文件上传失败

检查：
1. 文件大小是否超过限制（Render免费版建议<10MB）
2. API地址是否正确配置

### 问题4：Vercel部署失败

检查：
1. `vercel.json` 配置是否正确
2. Python版本是否兼容（建议3.9-3.11）

---

## 成本估算

### 完全免费方案

- **Vercel**：免费额度足够个人使用
  - 100GB带宽/月
  - 无限请求
  
- **Render**：免费额度
  - 750小时/月（足够一个应用24/7运行）
  - 15分钟不活跃会休眠

### 付费升级（可选）

- **Render Pro**：$7/月
  - 始终在线，无休眠
  - 更快的启动速度
  
- **Vercel Pro**：$20/月
  - 更多带宽和构建时间
  - 团队协作功能

---

## 性能对比

| 方案 | 首次加载 | 转换速度 | 成本 |
|------|---------|---------|------|
| Streamlit Cloud | 30-120秒 | 快 | 免费 |
| Vercel前端 + Render后端 | 前端秒开<br>后端首次50-120秒 | 快 | 免费 |
| Vercel全栈 | 秒开 | 可能超时 | 免费 |
| VPS自建 | 秒开 | 最快 | ￥24-50/月 |

---

## 推荐配置

**个人使用**：Vercel前端 + Render后端（免费）  
**团队使用**：Vercel前端 + Render Pro后端（$7/月）  
**高频使用**：VPS自建（￥24-50/月）

---

## 技术支持

遇到问题？
1. 查看 [Vercel文档](https://vercel.com/docs)
2. 查看 [Render文档](https://render.com/docs)
3. 提交GitHub Issue

---

## 更新日志

- 2025-11-05：创建Flask + Vercel/Render部署方案
- 支持自动序号功能
- 支持智能文件命名
- 支持.md、.txt、.docx格式上传
