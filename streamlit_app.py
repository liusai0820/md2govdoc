#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GovDoc - 政府公文格式转换工具
专业的Markdown到公文格式转换服务
"""

import streamlit as st
import tempfile
import os
from pathlib import Path
from md2gov_docx import convert_markdown_to_gov_docx

# 页面配置
st.set_page_config(
    page_title="GovDoc - 公文格式转换工具",
    page_icon="📋",
    layout="centered",
    initial_sidebar_state="collapsed",  # 隐藏侧边栏
    menu_items={
        'About': "GovDoc - 专业的政府公文格式转换工具 v1.0"
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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.25);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.35);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* 下载按钮特殊样式 */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        width: 100%;
        box-shadow: 0 4px 6px rgba(72, 187, 120, 0.25);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(72, 187, 120, 0.35);
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
        border-color: #667eea;
        background: #edf2f7;
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


def main():
    # 简洁的头部
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 0.5rem 0;">
        <h1 style="color: #1a365d; font-size: 2rem; margin-bottom: 0.3rem; font-weight: 700;">GovDoc</h1>
        <p style="color: #718096; font-size: 0.9rem; margin-bottom: 0;">Markdown 转政府公文格式 | 符合 GB/T 9704-2012 标准</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 创建标签页（默认显示粘贴文本）
    tab1, tab2 = st.tabs(["📝 粘贴文本", "📁 上传文件"])
    
    # 标签页1: 粘贴文本（默认）
    with tab1:
        st.markdown("")
        st.info("💡 提示：可直接在下方文本框中粘贴或输入Markdown内容")
        
        markdown_text = st.text_area(
            "Markdown内容",
            height=450,
            placeholder="# 关于加强公文格式管理的通知\n\n## 一、总体要求\n\n各单位要高度重视公文格式规范化工作，严格按照标准执行。\n\n## 二、具体措施\n\n### 1. 字体要求\n\n正文采用**仿宋_GB2312字体**，字号为三号（16磅）。\n\n### 2. 页面设置\n\n页边距设置如下：\n- 上边距：37毫米\n- 下边距：35毫米",
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
                            
                            st.success("✅ 转换成功！")
                            
                            # 直接下载，不需要再点击
                            st.download_button(
                                label="📥 下载Word文档",
                                data=docx_data,
                                file_name="公文格式文档.docx",
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
        st.markdown("")
        uploaded_file = st.file_uploader(
            "选择Markdown文件",
            type=['md', 'markdown', 'txt'],
            help="支持 .md、.markdown、.txt 格式，文件大小不超过 200MB"
        )
        
        if uploaded_file is not None:
            st.success(f"✅ 已选择文件：**{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚀 转换并下载", key="convert_file", use_container_width=True):
                with st.spinner("正在转换中..."):
                    # 创建临时文件
                    with tempfile.NamedTemporaryFile(mode='wb', suffix='.md', delete=False) as tmp_input:
                        tmp_input.write(uploaded_file.getvalue())
                        input_path = tmp_input.name
                    
                    output_path = input_path.replace('.md', '.docx')
                    
                    # 转换文档
                    success = convert_markdown_to_gov_docx(input_path, output_path)
                    
                    if success:
                        # 读取生成的文件
                        with open(output_path, 'rb') as f:
                            docx_data = f.read()
                        
                        st.success("✅ 转换成功！")
                        
                        # 直接下载
                        st.download_button(
                            label="📥 下载Word文档",
                            data=docx_data,
                            file_name="公文格式文档.docx",
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
        <p style="margin: 0.5rem 0;">支持标题、表格、列表、加粗、斜体 | 符合 GB/T 9704-2012 标准</p>
        <p style="margin: 0.5rem 0;">
            <a href="https://github.com/liusai0820/md2govdoc" target="_blank" style="color: #667eea; text-decoration: none;">GitHub</a>
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
