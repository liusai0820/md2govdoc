#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown转政府公文格式 - Web服务后端
提供文件上传和文本转换API
"""

from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import tempfile
from pathlib import Path
from md2gov_docx import convert_markdown_to_gov_docx
import uuid

app = Flask(__name__, static_folder='static')
CORS(app)  # 允许跨域请求

# 临时文件目录
TEMP_DIR = tempfile.gettempdir()


@app.route('/')
def index():
    """返回主页"""
    return app.send_static_file('index.html')


@app.route('/api/convert', methods=['POST'])
def convert_markdown():
    """
    转换Markdown到Word文档
    支持两种方式：
    1. 上传文件 (file)
    2. 直接提交文本内容 (text)
    """
    try:
        # 生成唯一的文件名
        file_id = str(uuid.uuid4())
        input_path = os.path.join(TEMP_DIR, f"{file_id}.md")
        output_path = os.path.join(TEMP_DIR, f"{file_id}.docx")
        
        # 处理文件上传
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': '未选择文件'}), 400
            
            # 保存上传的文件
            file.save(input_path)
        
        # 处理文本内容
        elif 'text' in request.form:
            text_content = request.form['text']
            if not text_content.strip():
                return jsonify({'error': '文本内容不能为空'}), 400
            
            # 保存文本到临时文件
            with open(input_path, 'w', encoding='utf-8') as f:
                f.write(text_content)
        
        else:
            return jsonify({'error': '请提供文件或文本内容'}), 400
        
        # 转换文档
        success = convert_markdown_to_gov_docx(input_path, output_path)
        
        if not success:
            return jsonify({'error': '转换失败，请检查Markdown格式'}), 500
        
        # 返回生成的文件
        response = send_file(
            output_path,
            as_attachment=True,
            download_name='公文格式文档.docx',
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
        # 清理临时文件（在后台）
        @response.call_on_close
        def cleanup():
            try:
                if os.path.exists(input_path):
                    os.remove(input_path)
                if os.path.exists(output_path):
                    os.remove(output_path)
            except:
                pass
        
        return response
        
    except Exception as e:
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({'status': 'ok', 'message': '服务运行正常'})


if __name__ == '__main__':
    # 创建static目录
    os.makedirs('static', exist_ok=True)
    
    print("\n" + "="*60)
    print("Markdown转政府公文格式 Web服务")
    print("="*60)
    print("\n服务地址: http://localhost:5000")
    print("按 Ctrl+C 停止服务\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
