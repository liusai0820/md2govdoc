#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask API for Vercel Serverless Functions
Markdown转政府公文格式 - API服务
"""

from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import tempfile
import sys
import re
from pathlib import Path

# 添加父目录到路径以导入md2gov_docx
sys.path.insert(0, str(Path(__file__).parent.parent))
from md2gov_docx import convert_markdown_to_gov_docx
from docx import Document as DocxDocument

app = Flask(__name__)
CORS(app)

# 临时文件目录
TEMP_DIR = tempfile.gettempdir()


def extract_title_from_markdown(content):
    """从Markdown内容中提取标题作为文件名"""
    lines = content.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            title = line[2:].strip()
            title = re.sub(r'[#*`\[\]()]', '', title).strip()
            if title:
                return sanitize_filename(title)
    
    for line in lines:
        line = line.strip()
        if line.startswith('## '):
            title = line[3:].strip()
            title = re.sub(r'[#*`\[\]()]', '', title).strip()
            if title:
                return sanitize_filename(title)
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            title = re.sub(r'[#*`\[\]()]', '', line).strip()
            if title:
                title = title[:50]
                return sanitize_filename(title)
    
    return "公文格式文档"


def sanitize_filename(filename):
    """清理文件名，移除不合法字符"""
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = filename.strip()
    if len(filename) > 50:
        filename = filename[:50]
    return filename if filename else "公文格式文档"


def read_docx_as_markdown(docx_path):
    """读取docx文件内容"""
    doc = DocxDocument(docx_path)
    content = []
    for paragraph in doc.paragraphs:
        content.append(paragraph.text)
    return '\n'.join(content)


@app.route('/')
def index():
    """API根路径"""
    return jsonify({
        'status': 'ok',
        'message': 'Markdown转政府公文格式 API',
        'version': '1.0.0',
        'endpoints': {
            '/api/convert': 'POST - 转换Markdown到Word文档',
            '/api/health': 'GET - 健康检查'
        }
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({'status': 'ok', 'message': '服务运行正常'})


@app.route('/api/convert', methods=['POST'])
def convert_markdown():
    """
    转换Markdown到Word文档
    支持三种方式：
    1. 上传.md文件
    2. 上传.docx文件（内容为markdown格式）
    3. 直接提交文本内容
    """
    try:
        import uuid
        file_id = str(uuid.uuid4())
        input_path = os.path.join(TEMP_DIR, f"{file_id}.md")
        output_path = os.path.join(TEMP_DIR, f"{file_id}.docx")
        
        markdown_content = None
        original_filename = None
        
        # 处理文件上传
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': '未选择文件'}), 400
            
            original_filename = file.filename
            file_ext = os.path.splitext(original_filename)[1].lower()
            
            if file_ext == '.md' or file_ext == '.markdown' or file_ext == '.txt':
                file.save(input_path)
                with open(input_path, 'r', encoding='utf-8') as f:
                    markdown_content = f.read()
            
            elif file_ext == '.docx':
                temp_docx_path = os.path.join(TEMP_DIR, f"{file_id}_temp.docx")
                file.save(temp_docx_path)
                
                try:
                    markdown_content = read_docx_as_markdown(temp_docx_path)
                    with open(input_path, 'w', encoding='utf-8') as f:
                        f.write(markdown_content)
                finally:
                    if os.path.exists(temp_docx_path):
                        os.remove(temp_docx_path)
            
            else:
                return jsonify({'error': '不支持的文件格式，请上传.md、.txt或.docx文件'}), 400
        
        # 处理文本内容
        elif 'text' in request.form:
            markdown_content = request.form['text']
            if not markdown_content.strip():
                return jsonify({'error': '文本内容不能为空'}), 400
            
            with open(input_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
        
        else:
            return jsonify({'error': '请提供文件或文本内容'}), 400
        
        # 转换文档
        success = convert_markdown_to_gov_docx(input_path, output_path)
        
        if not success:
            return jsonify({'error': '转换失败，请检查Markdown格式'}), 500
        
        # 从markdown内容中提取标题作为文件名
        doc_title = None
        
        # 优先从markdown内容提取标题
        if markdown_content and markdown_content.strip():
            doc_title = extract_title_from_markdown(markdown_content)
        
        # 如果没有提取到标题，使用原文件名
        if not doc_title or doc_title == "公文格式文档":
            if original_filename:
                doc_title = os.path.splitext(original_filename)[0]
                doc_title = sanitize_filename(doc_title)
        
        # 最后的默认值
        if not doc_title:
            doc_title = "公文格式文档"
        
        download_filename = f"{doc_title}.docx"
        
        # 返回生成的文件
        response = send_file(
            output_path,
            as_attachment=True,
            download_name=download_filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
        # 清理临时文件
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
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500


# Vercel需要这个
if __name__ != '__main__':
    # 在Vercel上运行
    application = app
else:
    # 本地开发
    app.run(debug=True, host='0.0.0.0', port=5555)
