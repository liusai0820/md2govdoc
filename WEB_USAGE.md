# Web服务使用说明

## 🚀 快速启动

### 1. 安装依赖

```bash
pip3 install -r requirements.txt
```

### 2. 启动服务

```bash
python3 app.py
```

服务将在 `http://localhost:5000` 启动

### 3. 使用Web界面

在浏览器中打开：**http://localhost:5000**

## 📱 功能说明

### 上传文件模式
1. 点击"上传文件"标签页
2. 拖拽Markdown文件到上传区域，或点击选择文件
3. 点击"转换并下载"按钮
4. 浏览器将自动下载生成的Word文档

### 粘贴文本模式
1. 点击"粘贴文本"标签页
2. 在文本框中粘贴或输入Markdown内容
3. 点击"转换并下载"按钮
4. 浏览器将自动下载生成的Word文档

## 🌐 API接口

### 转换接口

**端点**: `POST /api/convert`

**支持两种方式**:

#### 方式1: 上传文件
```bash
curl -X POST http://localhost:5000/api/convert \
  -F "file=@example.md" \
  --output output.docx
```

#### 方式2: 提交文本
```bash
curl -X POST http://localhost:5000/api/convert \
  -F "text=# 标题
正文内容..." \
  --output output.docx
```

### 健康检查

**端点**: `GET /api/health`

```bash
curl http://localhost:5000/api/health
```

响应:
```json
{
  "status": "ok",
  "message": "服务运行正常"
}
```

## 🎨 界面特性

- ✅ 现代化渐变紫色主题
- ✅ 支持拖拽上传
- ✅ 双标签页切换（文件上传/文本粘贴）
- ✅ 实时状态提示
- ✅ 响应式设计，支持移动端
- ✅ 内置Markdown语法参考

## 📝 支持的文件格式

- `.md` - Markdown文件
- `.markdown` - Markdown文件
- `.txt` - 纯文本文件

## ⚙️ 配置说明

### 修改端口

编辑 `app.py` 文件最后一行：

```python
app.run(debug=True, host='0.0.0.0', port=5000)  # 修改port参数
```

### 修改临时文件目录

编辑 `app.py` 文件：

```python
TEMP_DIR = tempfile.gettempdir()  # 修改为自定义路径
```

## 🔒 安全注意事项

1. **开发模式**: 当前配置为开发模式（`debug=True`），仅适合本地使用
2. **生产部署**: 如需部署到生产环境，请：
   - 关闭debug模式
   - 使用生产级WSGI服务器（如gunicorn、uwsgi）
   - 添加认证机制
   - 限制文件上传大小
   - 配置HTTPS

### 生产部署示例（使用gunicorn）

```bash
# 安装gunicorn
pip3 install gunicorn

# 启动服务
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🛠️ 故障排查

### 问题1: 端口被占用

**错误**: `Address already in use`

**解决**:
```bash
# 查找占用端口的进程
lsof -i :5000

# 杀死进程
kill -9 <PID>
```

### 问题2: 字体不正确

**原因**: 系统缺少所需字体

**解决**: 
- 安装仿宋_GB2312、楷体_GB2312、黑体、方正小标宋简体
- 或修改`md2gov_docx.py`中的字体常量

### 问题3: 转换失败

**检查**:
1. Markdown语法是否正确
2. 查看后端控制台错误信息
3. 检查是否安装了python-docx库

## 📊 性能优化

- 临时文件自动清理
- 支持并发请求
- 文件流式传输
- 内存优化处理

## 🔗 相关文件

- `app.py` - Flask后端服务
- `static/index.html` - 前端页面
- `md2gov_docx.py` - 核心转换逻辑
- `requirements.txt` - Python依赖

## 💡 提示

- 建议使用Chrome、Edge、Safari等现代浏览器
- 文件上传大小建议不超过10MB
- 转换速度取决于文档大小和复杂度
- 支持同时处理多个请求

---

**技术栈**: Python + Flask + HTML5 + CSS3 + JavaScript  
**开发者**: Qibaoba  
**更新日期**: 2025-10-31
