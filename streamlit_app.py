#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GovDoc - 政府公文格式转换工具
专业的Markdown到公文格式转换服务
"""

import streamlit as st
import tempfile
import os
import re
from pathlib import Path
from md2gov_docx import convert_markdown_to_gov_docx
from docx import Document

# 页面配置
st.set_page_config(
    page_title="公文格式转换器 - AI输出一键转公文",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "公文格式转换器 - 把AI输出一键转换成标准公文 | 符合GB/T 9704-2012标准"
    }
)

# 专业设计CSS
st.markdown("""
<style>
    /* 隐藏默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 全局样式 */
    .main {
        background: linear-gradient(to bottom, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Logo和标题区域 */
    .app-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        margin-bottom: 2rem;
    }
    
    .app-logo {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    .app-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a365d;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .app-subtitle {
        font-size: 1rem;
        color: #718096;
        font-weight: 400;
    }
    
    /* 特色卡片 */
    .feature-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    /* 标题样式 */
    h1 {
        color: #1a365d;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }
    
    h2 {
        color: #2d3748;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #4a5568;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* 标签页样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background-color: #f7fafc;
        border-radius: 8px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 6px;
        padding: 12px 24px;
        font-weight: 500;
        color: #4a5568;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
        color: #2b6cb0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: #3182ce;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #2c5aa0;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(49, 130, 206, 0.3);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        background: #2a4365;
    }
    
    /* 下载按钮特殊样式 */
    .stDownloadButton > button {
        background: #38a169;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.2s ease;
    }
    
    .stDownloadButton > button:hover {
        background: #2f855a;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(56, 161, 105, 0.3);
    }
    
    /* 文本框样式 */
    .stTextArea textarea {
        font-family: 'SF Mono', 'Monaco', 'Courier New', monospace;
        font-size: 14px;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        transition: border-color 0.3s;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* 文件上传器 */
    .uploadedFile {
        border: 2px dashed #cbd5e0;
        border-radius: 12px;
        padding: 2rem;
        background: #f7fafc;
        text-align: center;
        transition: all 0.3s;
    }
    
    .uploadedFile:hover {
        border-color: #3182ce;
        background: #edf2f7;
    }
    
    /* 隐藏文件上传的英文提示 */
    [data-testid="stFileUploader"] label {
        display: none;
    }
    
    /* 信息框样式 */
    .stAlert {
        border-radius: 8px;
        border: none;
        padding: 1rem;
    }
    
    /* 成功消息 */
    .stSuccess {
        background-color: #f0fff4;
        border-left: 4px solid #48bb78;
    }
    
    /* 错误消息 */
    .stError {
        background-color: #fff5f5;
        border-left: 4px solid #f56565;
    }
    
    /* 信息消息 */
    .stInfo {
        background-color: #ebf8ff;
        border-left: 4px solid #4299e1;
    }
    
    /* Expander样式 */
    .streamlit-expanderHeader {
        background-color: #f7fafc;
        border-radius: 8px;
        font-weight: 600;
        color: #2d3748;
    }
    
    /* 代码块 */
    code {
        background-color: #edf2f7;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        color: #667eea;
        font-family: 'SF Mono', 'Monaco', monospace;
        font-size: 0.9em;
    }
    
    /* 分隔线 */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, #cbd5e0, transparent);
    }
    
    /* Sidebar样式 */
    .css-1d391kg {
        background-color: #f7fafc;
    }
</style>
""", unsafe_allow_html=True)


def extract_title_from_markdown(content):
    """
    从Markdown内容中提取标题作为文件名
    优先级：# 标题 > ## 标题 > 第一行非空文本
    """
    lines = content.strip().split('\n')
    
    # 查找第一个一级标题
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            title = line[2:].strip()
            # 移除markdown格式符号
            title = re.sub(r'[#*`\[\]()]', '', title).strip()
            if title:
                return sanitize_filename(title)
    
    # 查找第一个二级标题
    for line in lines:
        line = line.strip()
        if line.startswith('## '):
            title = line[3:].strip()
            title = re.sub(r'[#*`\[\]()]', '', title).strip()
            if title:
                return sanitize_filename(title)
    
    # 使用第一行非空文本
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            title = re.sub(r'[#*`\[\]()]', '', line).strip()
            if title:
                # 限制长度
                title = title[:50]
                return sanitize_filename(title)
    
    return "公文格式文档"


def sanitize_filename(filename):
    """
    清理文件名，移除不合法字符
    """
    # 移除Windows和Unix不允许的文件名字符
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # 移除前后空格
    filename = filename.strip()
    # 限制长度
    if len(filename) > 50:
        filename = filename[:50]
    # 如果清理后为空，返回默认名称
    return filename if filename else "公文格式文档"


def read_docx_as_markdown(docx_path):
    """
    读取docx文件内容，假设其中包含markdown格式的文本
    """
    doc = Document(docx_path)
    content = []
    for paragraph in doc.paragraphs:
        content.append(paragraph.text)
    return '\n'.join(content)


def main():
    # 简洁的头部
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 0.5rem 0;">
        <h1 style="color: #1a365d; font-size: 2.2rem; margin-bottom: 0.5rem; font-weight: 700;">公文格式转换器</h1>
        <p style="color: #4a5568; font-size: 1rem; margin-bottom: 0.3rem; font-weight: 500;">把AI输出一键转换成标准公文，省去排版烦恼</p>
        <p style="color: #a0aec0; font-size: 0.85rem; margin-bottom: 0;">符合 GB/T 9704-2012 标准</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 创建标签页（默认显示粘贴文本）
    tab1, tab2 = st.tabs(["📝 粘贴文本", "📁 上传文件"])
    
    # 标签页1: 粘贴文本（默认）
    with tab1:
        st.markdown("")
        st.info("💡 提示：可直接在下方文本框中粘贴或输入Markdown内容。标题会自动添加序号（一、二、三、或（一）（二）（三））")
        
        markdown_text = st.text_area(
            "Markdown内容",
            height=450,
            placeholder="# 关于加强公文格式管理的通知\n\n## 总体要求\n\n各单位要高度重视公文格式规范化工作，严格按照标准执行。\n\n## 具体措施\n\n### 字体要求\n\n正文采用**仿宋_GB2312字体**，字号为三号（16磅）。\n\n### 页面设置\n\n页边距设置如下：\n- 上边距：37毫米\n- 下边距：35毫米\n\n注：标题会自动添加序号（一、二、三、或（一）（二）（三））",
            help="支持标准Markdown语法，包括标题、列表、表格、加粗、斜体等",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if st.button("🗑️ 清空", key="clear_text", use_container_width=True):
                st.rerun()
        
        with col2:
            if st.button("🚀 转换并下载", key="convert_text", use_container_width=True, type="primary"):
                if not markdown_text.strip():
                    st.error("❌ 请输入Markdown文本")
                else:
                    with st.spinner("正在转换中..."):
                        # 从内容中提取标题作为文件名
                        doc_title = extract_title_from_markdown(markdown_text)
                        download_filename = f"{doc_title}.docx"
                        
                        # 创建临时文件
                        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as tmp_input:
                            tmp_input.write(markdown_text)
                            input_path = tmp_input.name
                        
                        output_path = input_path.replace('.md', '.docx')
                        
                        # 转换文档
                        success = convert_markdown_to_gov_docx(input_path, output_path)
                        
                        if success:
                            # 读取生成的文件
                            with open(output_path, 'rb') as f:
                                docx_data = f.read()
                            
                            st.success(f"✅ 转换成功！文件名：{download_filename}")
                            
                            # 直接下载，不需要再点击
                            st.download_button(
                                label="📥 下载Word文档",
                                data=docx_data,
                                file_name=download_filename,
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                use_container_width=True
                            )
                            
                            # 清理临时文件
                            try:
                                os.remove(input_path)
                                os.remove(output_path)
                            except:
                                pass
                        else:
                            st.error("❌ 转换失败，请检查Markdown格式是否正确")
    
    # 标签页2: 上传文件
    with tab2:
        st.markdown("""
        <div style="text-align: center; margin: 1rem 0; padding: 1rem; background: #ebf8ff; border-radius: 8px;">
            <p style="margin: 0; color: #2c5282; font-size: 0.95rem;">📁 拖拽文件到下方区域，或点击选择文件</p>
            <p style="margin: 0.3rem 0 0 0; color: #718096; font-size: 0.85rem;">支持 .md、.markdown、.txt、.docx 格式</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "选择文件",
            type=['md', 'markdown', 'txt', 'docx'],
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            st.success(f"✅ 已选择文件：**{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚀 转换并下载", key="convert_file", use_container_width=True):
                with st.spinner("正在转换中..."):
                    file_ext = os.path.splitext(uploaded_file.name)[1].lower()
                    markdown_content = None
                    
                    # 根据文件类型处理
                    if file_ext == '.docx':
                        # 保存临时docx文件
                        with tempfile.NamedTemporaryFile(mode='wb', suffix='.docx', delete=False) as tmp_docx:
                            tmp_docx.write(uploaded_file.getvalue())
                            temp_docx_path = tmp_docx.name
                        
                        try:
                            # 读取docx中的markdown内容
                            markdown_content = read_docx_as_markdown(temp_docx_path)
                            
                            # 保存为md文件
                            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as tmp_input:
                                tmp_input.write(markdown_content)
                                input_path = tmp_input.name
                        finally:
                            # 清理临时docx文件
                            if os.path.exists(temp_docx_path):
                                os.remove(temp_docx_path)
                    else:
                        # 处理md/txt文件
                        with tempfile.NamedTemporaryFile(mode='wb', suffix='.md', delete=False) as tmp_input:
                            tmp_input.write(uploaded_file.getvalue())
                            input_path = tmp_input.name
                        
                        # 读取内容用于提取标题
                        with open(input_path, 'r', encoding='utf-8') as f:
                            markdown_content = f.read()
                    
                    # 从内容中提取标题作为文件名
                    if markdown_content:
                        doc_title = extract_title_from_markdown(markdown_content)
                    else:
                        # 如果没有内容，使用原始文件名
                        doc_title = os.path.splitext(uploaded_file.name)[0]
                        doc_title = sanitize_filename(doc_title)
                    
                    download_filename = f"{doc_title}.docx"
                    output_path = input_path.replace('.md', '.docx')
                    
                    # 转换文档
                    success = convert_markdown_to_gov_docx(input_path, output_path)
                    
                    if success:
                        # 读取生成的文件
                        with open(output_path, 'rb') as f:
                            docx_data = f.read()
                        
                        st.success(f"✅ 转换成功！文件名：{download_filename}")
                        
                        # 直接下载
                        st.download_button(
                            label="📥 下载Word文档",
                            data=docx_data,
                            file_name=download_filename,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True
                        )
                        
                        # 清理临时文件
                        try:
                            os.remove(input_path)
                            os.remove(output_path)
                        except:
                            pass
                    else:
                        st.error("❌ 转换失败，请检查Markdown格式是否正确")
    
    
    # 简洁页脚
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0 1rem 0; color: #a0aec0; font-size: 0.85rem;">
        <p style="margin: 0.5rem 0;">✨ 自动添加标题序号：## 标题 → 一、标题 | ### 标题 → （一）标题 | #### 标题 → 1. 标题</p>
        <p style="margin: 0.5rem 0;">支持标题、表格、列表、加粗、斜体 | 符合 GB/T 9704-2012 标准</p>
        <p style="margin: 0.5rem 0;">
            <a href="https://github.com/liusai0820/md2govdoc" target="_blank" style="color: #3182ce; text-decoration: none;">Github</a>
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
