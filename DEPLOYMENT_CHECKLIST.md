# 🚀 部署检查清单

## 准备工作

- [ ] 注册Render账号：https://render.com
- [ ] 注册Vercel账号：https://vercel.com
- [ ] 确保GitHub仓库已推送 `flask-vercel-deploy` 分支

---

## 第一步：部署后端到Render（5分钟）

### 1. 创建Web Service

- [ ] 登录Render Dashboard
- [ ] 点击 "New +" → "Web Service"
- [ ] 连接GitHub仓库
- [ ] 选择 `flask-vercel-deploy` 分支

### 2. 配置服务

```
Name: md2govdoc-api
Environment: Python 3
Region: Singapore (或选择离你最近的)
Branch: flask-vercel-deploy
Build Command: pip install -r requirements.txt
Start Command: gunicorn api.index:app
```

- [ ] 选择 "Free" 计划
- [ ] 点击 "Create Web Service"

### 3. 等待部署

- [ ] 等待2-3分钟，直到状态变为 "Live"
- [ ] 复制你的API地址（例如：`https://md2govdoc-api.onrender.com`）
- [ ] 测试API：访问 `https://你的地址.onrender.com/api/health`
- [ ] 应该看到：`{"status":"ok","message":"服务运行正常"}`

✅ **后端部署完成！**

---

## 第二步：部署前端到Vercel（3分钟）

### 1. 导入项目

- [ ] 登录Vercel Dashboard
- [ ] 点击 "Add New..." → "Project"
- [ ] 选择你的GitHub仓库
- [ ] 选择 `flask-vercel-deploy` 分支

### 2. 配置项目

```
Framework Preset: Other
Root Directory: ./
Build Command: (留空)
Output Directory: public
Install Command: (留空)
```

- [ ] 点击 "Deploy"
- [ ] 等待1分钟部署完成

### 3. 更新API地址

- [ ] 在GitHub上编辑 `public/index.html`
- [ ] 找到第442行左右的代码：
  ```javascript
  const API_BASE_URL = window.location.hostname === 'localhost' 
      ? 'http://localhost:5000'
      : 'https://your-api.onrender.com';  // 👈 修改这里
  ```
- [ ] 将 `https://your-api.onrender.com` 替换为你的Render API地址
- [ ] 提交更改
- [ ] Vercel会自动重新部署（约30秒）

✅ **前端部署完成！**

---

## 第三步：测试（2分钟）

- [ ] 访问你的Vercel域名（例如：`https://your-project.vercel.app`）
- [ ] 页面应该立即加载（秒开）
- [ ] 测试粘贴文本转换功能
- [ ] 测试文件上传转换功能
- [ ] 检查下载的Word文档格式是否正确

✅ **全部完成！**

---

## 可选：自定义域名

### Vercel自定义域名

- [ ] 在Vercel项目设置中点击 "Domains"
- [ ] 添加你的域名
- [ ] 按照提示配置DNS记录

### Render自定义域名

- [ ] 在Render服务设置中点击 "Custom Domain"
- [ ] 添加你的API域名
- [ ] 按照提示配置DNS记录

---

## 故障排查

### ❌ 前端加载正常，但转换失败

**原因**：API地址配置错误

**解决**：
1. 检查 `public/index.html` 中的 `API_BASE_URL` 是否正确
2. 确保Render服务状态为 "Live"
3. 测试API健康检查：`https://你的API地址/api/health`

### ❌ Render部署失败

**原因**：依赖安装失败

**解决**：
1. 检查 `requirements.txt` 是否正确
2. 查看Render的构建日志
3. 确保Python版本兼容（3.9-3.11）

### ❌ CORS错误

**原因**：跨域配置问题

**解决**：
1. 确保 `api/index.py` 中有 `CORS(app)`
2. 检查Render环境变量

### ❌ 首次访问API很慢

**原因**：Render免费版冷启动

**解决**：
- 这是正常现象，免费版15分钟不活跃会休眠
- 首次访问需要50-120秒启动
- 升级到Render Pro ($7/月) 可以保持始终在线

---

## 成本

- **Vercel**：完全免费
- **Render**：完全免费（有冷启动）
- **总计**：$0/月 🎉

---

## 下一步

- [ ] 分享你的应用链接
- [ ] 收集用户反馈
- [ ] 考虑升级到付费版（如果需要更快的响应）

---

## 需要帮助？

- 查看详细文档：[DEPLOY_VERCEL_RENDER.md](./DEPLOY_VERCEL_RENDER.md)
- 提交Issue：https://github.com/你的用户名/你的仓库/issues
