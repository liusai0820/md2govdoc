#!/bin/bash

echo "======================================"
echo "  Markdown转政府公文格式 Web服务"
echo "======================================"
echo ""
echo "正在检查依赖..."

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python"
    exit 1
fi

# 检查并安装依赖
echo "安装/更新依赖包..."
pip3 install -r requirements.txt -q

echo ""
echo "✅ 依赖检查完成"
echo ""
echo "启动Web服务..."
echo "服务地址: http://localhost:5000"
echo "按 Ctrl+C 停止服务"
echo ""

# 启动Flask服务
python3 app.py
