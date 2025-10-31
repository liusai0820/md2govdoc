# 部署指南

## 🚀 本地运行

### 安装依赖

```bash
pip3 install streamlit python-docx
```

### 启动应用

```bash
streamlit run streamlit_app.py
```

应用将在 `http://localhost:8501` 启动

---

## ☁️ 云平台部署

### 方式1: Streamlit Cloud（推荐，免费）

Streamlit Cloud是官方提供的免费部署平台，最简单快捷。

#### 步骤：

1. **准备GitHub仓库**
   ```bash
   # 在项目目录初始化git（如果还没有）
   git init
   git add .
   git commit -m "Initial commit"
   
   # 推送到GitHub
   git remote add origin <你的GitHub仓库URL>
   git push -u origin main
   ```

2. **访问Streamlit Cloud**
   - 打开 https://streamlit.io/cloud
   - 使用GitHub账号登录

3. **部署应用**
   - 点击 "New app"
   - 选择你的GitHub仓库
   - 主文件选择: `streamlit_app.py`
   - 点击 "Deploy"

4. **等待部署完成**
   - 部署通常需要2-5分钟
   - 完成后会得到一个公网URL，如: `https://your-app.streamlit.app`

#### 优点：
- ✅ 完全免费
- ✅ 自动SSL证书
- ✅ 自动从GitHub更新
- ✅ 无需服务器管理

#### 注意：
- 免费版有资源限制（1GB内存）
- 不活跃应用会进入休眠，访问时需要唤醒

---

### 方式2: Heroku

Heroku是流行的PaaS平台，支持免费tier。

#### 步骤：

1. **安装Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # 或访问 https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **创建必要文件**

   创建 `Procfile`:
   ```
   web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

   创建 `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "[server]
   headless = true
   port = $PORT
   enableCORS = false
   " > ~/.streamlit/config.toml
   ```

3. **部署到Heroku**
   ```bash
   # 登录
   heroku login
   
   # 创建应用
   heroku create your-app-name
   
   # 推送代码
   git push heroku main
   
   # 打开应用
   heroku open
   ```

#### 优点：
- ✅ 支持自定义域名
- ✅ 丰富的插件生态
- ✅ 良好的文档

#### 缺点：
- ⚠️ 免费tier限制较多
- ⚠️ 不活跃应用会休眠

---

### 方式3: Railway

Railway是新兴的部署平台，界面友好。

#### 步骤：

1. **访问Railway**
   - 打开 https://railway.app
   - 使用GitHub账号登录

2. **部署应用**
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择你的仓库
   - Railway会自动检测并部署

3. **配置启动命令**
   - 在设置中添加启动命令:
   ```
   streamlit run streamlit_app.py --server.port=$PORT
   ```

4. **生成域名**
   - 在设置中生成公网域名

#### 优点：
- ✅ 界面简洁现代
- ✅ 部署快速
- ✅ 免费额度充足

---

### 方式4: 自建服务器（VPS/云服务器）

适合需要完全控制的场景。

#### 步骤：

1. **准备服务器**
   - 购买VPS（阿里云、腾讯云、AWS等）
   - 确保Python 3.8+已安装

2. **上传代码**
   ```bash
   scp -r . user@your-server:/path/to/app
   ```

3. **安装依赖**
   ```bash
   ssh user@your-server
   cd /path/to/app
   pip3 install -r requirements.txt
   ```

4. **使用systemd守护进程**
   
   创建 `/etc/systemd/system/streamlit.service`:
   ```ini
   [Unit]
   Description=Streamlit App
   After=network.target

   [Service]
   Type=simple
   User=your-user
   WorkingDirectory=/path/to/app
   ExecStart=/usr/bin/python3 -m streamlit run streamlit_app.py --server.port=8501
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   启动服务:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable streamlit
   sudo systemctl start streamlit
   ```

5. **配置Nginx反向代理**
   
   `/etc/nginx/sites-available/streamlit`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

6. **配置SSL（可选）**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

---

## 🔧 环境变量配置

如果需要配置环境变量（如API密钥），在不同平台的方法：

### Streamlit Cloud
在应用设置 → Secrets中添加

### Heroku
```bash
heroku config:set KEY=value
```

### Railway
在设置 → Variables中添加

---

## 📊 性能优化建议

1. **字体文件处理**
   - 考虑将常用字体打包到项目中
   - 或提供字体安装脚本

2. **缓存优化**
   ```python
   @st.cache_data
   def convert_markdown(text):
       # 转换逻辑
       pass
   ```

3. **资源限制**
   - 限制上传文件大小
   - 添加请求频率限制

4. **错误处理**
   - 完善错误提示
   - 添加日志记录

---

## 🛡️ 安全建议

1. **文件上传限制**
   ```python
   # 限制文件大小
   if uploaded_file.size > 10 * 1024 * 1024:  # 10MB
       st.error("文件过大")
   ```

2. **输入验证**
   - 验证文件类型
   - 防止恶意代码注入

3. **HTTPS**
   - 生产环境必须使用HTTPS
   - Streamlit Cloud自动提供

---

## 📝 部署检查清单

部署前确认：

- [ ] requirements.txt包含所有依赖
- [ ] 测试过本地运行正常
- [ ] 添加了.gitignore（排除临时文件）
- [ ] 更新了README文档
- [ ] 测试了文件上传和文本转换功能
- [ ] 检查了字体依赖问题
- [ ] 配置了合适的错误处理

---

## ❓ 常见问题

### Q: 部署后字体显示不正确？
A: 云平台可能缺少中文字体，需要：
1. 将字体文件包含在项目中
2. 在代码中动态加载字体
3. 或使用系统自带字体替代

### Q: Streamlit Cloud部署失败？
A: 检查：
1. requirements.txt是否正确
2. Python版本是否兼容（建议3.9-3.11）
3. 查看部署日志中的错误信息

### Q: 应用运行缓慢？
A: 
1. 使用@st.cache_data缓存结果
2. 优化文件处理逻辑
3. 考虑升级到付费plan

---

## 🔗 相关链接

- Streamlit文档: https://docs.streamlit.io
- Streamlit Cloud: https://streamlit.io/cloud
- Heroku文档: https://devcenter.heroku.com
- Railway文档: https://docs.railway.app

---

**推荐部署顺序**: Streamlit Cloud > Railway > Heroku > 自建服务器
