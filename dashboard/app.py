# -*- coding: utf-8 -*-
"""
메인 Flask 애플리케이션입니다.
이 파일은 Flask 앱을 초기화하고, 콘텐츠 생성기 대시보드를 위한 라우트를 정의합니다.
"""
import os
from flask import Flask, render_template

# 1. Flask 앱 초기화
# template_folder와 static_folder를 dashboard 폴더 기준으로 명시적으로 설정합니다.
app = Flask(__name__, template_folder='templates', static_folder='static')

# --- Frontend Routes ---
@app.route('/')
def index():
    """메인 대시보드 페이지를 렌더링합니다."""
    return render_template('index.html')

@app.route('/preview')
def preview():
    """미리보기 IFrame에 사용될 페이지를 렌더링합니다."""
    return render_template('preview.html')

