#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown转政府公文格式 - Streamlit Web应用
适合部署到Streamlit Cloud、Heroku等云平台
"""

import streamlit as st
import tempfile
import os
from pathlib import Path
from md2gov_docx import convert_markdown_to_gov_docx

# 页面配置
st.set_page_config(
    page_title="Markdown转公文格式",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 自定义CSS - 干净的纯色设计
st.markdown("""
<style>
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 主容器样式 */
    .main {
        background-color: #f5f5f5;
    }
    
    /* 标题样式 */
    h1 {
        color: #2c3e50;
        font-weight: 600;
        padding-bottom: 20px;
        border-bottom: 2px solid #3498db;
    }
    
    h2, h3 {
        color: #34495e;
    }
    
    /* 文本框样式 */
    .stTextArea textarea {
        font-family: 'Courier New', monospace;
        font-size: 14px;
        border: 1px solid #ddd;
        border-radius: 4px;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px 24px;
        font-weight: 500;
        width: 100%;
        transition: background-color 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #2980b9;
    }
    
    /* 文件上传器样式 */
    .uploadedFile {
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 10px;
        background-color: white;
    }
    
    /* 信息框样式 */
    .stAlert {
        border-radius: 4px;
    }
    
    /* 标签页样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 4px 4px 0 0;
        padding: 10px 20px;
        border: 1px solid #ddd;
        border-bottom: none;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3498db;
        color: white;
    }
    
    /* 分隔线 */
    hr {
        margin: 30px 0;
        border: none;
        border-top: 1px solid #ddd;
    }
    
    /* 代码块样式 */
    code {
        background-color: #ecf0f1;
        padding: 2px 6px;
        border-radius: 3px;
        color: #2c3e50;
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)


def main():
    # 页面标题
    st.title("Markdown转政府公文格式")
    st.markdown("将Markdown文档转换为符合国家标准的政府公文格式Word文档")
    
    st.markdown("---")
    
    # 创建标签页
    tab1, tab2 = st.tabs(["上传文件", "粘贴文本"])
    
    # 标签页1: 上传文件
    with tab1:
        st.markdown("### 上传Markdown文件")
        uploaded_file = st.file_uploader(
            "选择文件",
            type=['md', 'markdown', 'txt'],
            help="支持 .md、.markdown、.txt 格式"
        )
        
        if uploaded_file is not None:
            st.success(f"已选择文件: {uploaded_file.name}")
            
            if st.button("转换并下载", key="convert_file"):
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
                        
                        # 提供下载
                        st.download_button(
                            label="下载Word文档",
                            data=docx_data,
                            file_name="公文格式文档.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                        st.success("转换成功！点击上方按钮下载")
                        
                        # 清理临时文件
                        try:
                            os.remove(input_path)
                            os.remove(output_path)
                        except:
                            pass
                    else:
                        st.error("转换失败，请检查Markdown格式是否正确")
    
    # 标签页2: 粘贴文本
    with tab2:
        st.markdown("### 输入或粘贴Markdown文本")
        markdown_text = st.text_area(
            "Markdown内容",
            height=400,
            placeholder="在此输入或粘贴Markdown文本...\n\n示例：\n# 文档标题\n\n## 一、主要内容\n\n正文内容...",
            help="支持标准Markdown语法"
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("清空", key="clear_text"):
                st.rerun()
        
        with col2:
            if st.button("转换并下载", key="convert_text"):
                if not markdown_text.strip():
                    st.error("请输入Markdown文本")
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
                            
                            # 提供下载
                            st.download_button(
                                label="下载Word文档",
                                data=docx_data,
                                file_name="公文格式文档.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                            st.success("转换成功！点击上方按钮下载")
                            
                            # 清理临时文件
                            try:
                                os.remove(input_path)
                                os.remove(output_path)
                            except:
                                pass
                        else:
                            st.error("转换失败，请检查Markdown格式是否正确")
    
    # 格式说明
    st.markdown("---")
    st.markdown("### 支持的Markdown语法")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        - `#` 主标题 → 方正小标宋简体 22磅
        - `##` 一级标题 → 黑体 16磅
        - `###` 二级标题 → 楷体_GB2312 16磅
        - `####` 三级标题 → 楷体_GB2312 16磅
        """)
    
    with col2:
        st.markdown("""
        - `-` 列表项 → 仿宋_GB2312 16磅
        - `**文本**` → 加粗
        - `*文本*` → 斜体
        - 正文 → 仿宋_GB2312 16磅
        """)
    
    # 页面设置说明
    with st.expander("页面设置规范"):
        st.markdown("""
        **页边距**:
        - 上边距: 37mm
        - 下边距: 35mm
        - 左边距: 28mm
        - 右边距: 26mm
        
        **段落格式**:
        - 行距: 固定值28.8磅
        - 首行缩进: 2字符
        - 段前段后间距: 0
        """)
    
    # 注意事项
    with st.expander("注意事项"):
        st.markdown("""
        1. 请确保系统已安装所需字体（仿宋_GB2312、楷体_GB2312、黑体、方正小标宋简体）
        2. 序号后不会添加空格（如 `一、标题` 而非 `一、 标题`）
        3. 主标题后会自动空一行
        4. 文档完全符合《党政机关公文格式》GB/T 9704-2012标准
        """)


if __name__ == "__main__":
    main()
