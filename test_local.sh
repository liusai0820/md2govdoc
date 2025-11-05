#!/bin/bash
# 本地测试脚本

echo "================================"
echo "本地测试 Flask API"
echo "================================"
echo ""
echo "1. 确保已安装依赖："
echo "   pip install -r requirements.txt"
echo ""
echo "2. 启动后端API..."
echo ""

# 启动Flask API
export FLASK_APP=api/index.py
export FLASK_ENV=development

echo "后端API启动在: http://localhost:5000"
echo ""
echo "3. 打开前端："
echo "   用浏览器打开 public/index.html"
echo "   或运行: python -m http.server 8080 --directory public"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

python -m flask run --port 5000
