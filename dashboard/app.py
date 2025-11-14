# -*- coding: utf-8 -*-
"""
메인 Flask 애플리케이션 및 Celery 설정 파일입니다.
이 파일은 Flask 앱을 초기화하고 비동기 작업을 위한 Celery를 설정합니다.
"""
import os
import json
import datetime
from flask import Flask, jsonify, request, render_template, redirect, url_for
from celery import Celery
from .utils import read_manifest, write_manifest # manifest 유틸리티 함수 임포트

def make_celery(app):
    """
    Flask 앱 컨텍스트를 사용하여 Celery를 설정합니다.

    Args:
        app (Flask): Flask 애플리케이션 인스턴스.

    Returns:
        Celery: 설정된 Celery 인스턴스.
    """
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

# 1. Flask 앱 초기화
# template_folder를 dashboard/templates로 명시적으로 설정합니다.
app = Flask(__name__, template_folder='templates')

# 2. 환경 변수(.env)로부터 Celery 설정 로드
app.config.update(
    CELERY_BROKER_URL=os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0'),
    CELERY_RESULT_BACKEND=os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
)

# 3. Celery 인스턴스 생성
celery = make_celery(app)

# --- Celery Tasks ---
@celery.task
def debug_task(cycle_id, step_id):
    """
    Celery 워커가 실행할 간단한 디버그 태스크입니다.
    실제 파이프라인 로직은 run_pipeline.py에서 처리됩니다.
    """
    print(f"Celery Debug Task: Cycle {cycle_id}, Step {step_id} received by worker.")
    # 여기에 실제 파이프라인 실행 로직을 호출할 수 있습니다.
    # 예: subprocess.run(["python", "run_pipeline.py", cycle_id, step_id])
    return {"status": "completed", "cycle_id": cycle_id, "step_id": step_id}

# --- Frontend Routes ---
@app.route('/')
def index():
    """메인 페이지 (View 1)를 렌더링합니다."""
    return render_template('index.html')

@app.route('/cycle/<cycle_id>')
def cycle_dashboard(cycle_id):
    """특정 사이클의 대쉬보드 (View 2)를 렌더링합니다."""
    # manifest = read_manifest(cycle_id)
    # return render_template('cycle_dashboard.html', cycle_id=cycle_id, manifest=manifest)
    return render_template('cycle_dashboard.html', cycle_id=cycle_id)


# --- API Endpoints ---

@app.route('/api/cycles', methods=['GET'])
def get_cycles():
    """(모의) 과거 사이클 목록을 조회합니다."""
    mock_cycles = [
        {"cycle_id": "251112", "createdAt": "2025-11-12T10:30:01Z", "status": {"text": "Step 14: 최종 배포 (PM)"}},
        {"cycle_id": "251111", "createdAt": "2025-11-11T09:00:00Z", "status": {"text": "완료"}}
    ]
    return jsonify(mock_cycles)

@app.route('/api/cycle/start', methods=['POST'])
def start_cycle():
    """
    새 사이클을 시작합니다.
    - cycle_id 생성
    - content-output/{cycle_id} 폴더 생성
    - manifest.json 파일 초기화
    - 성공 시 새 사이클 대쉬보드 URL 반환
    """
    try:
        data = request.get_json()
        mode = data.get('mode', 'standard')
        template = data.get('template', 'blog-post-default.html')

        # cycle_id를 현재 시간 기반으로 생성 (e.g., 251114105501)
        cycle_id = datetime.datetime.now().strftime('%y%m%d%H%M%S')
        
        # manifest.json 초기 구조 (PRD 참조)
        manifest = {
            "cycle_id": cycle_id,
            "createdAt": datetime.datetime.now().isoformat(),
            "status": {
                "step": 1,
                "code": "STEP_1_PENDING",
                "text": "Step 1: 자료 조사 대기중"
            },
            "config": {
                "mode": mode,
                "template": template
            },
            "selection": {},
            "files": {},
            "logs": f"content-output/{cycle_id}/pipeline.log"
        }
        
        # manifest.json 파일 쓰기 (utils.py 함수 사용)
        write_manifest(cycle_id, manifest)

        # TODO: Step 1 (자료 조사) Celery 작업 즉시 트리거
        # run_step.delay(cycle_id, 1) 

        return jsonify({"redirect_url": url_for('cycle_dashboard', cycle_id=cycle_id)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/cycle/<cycle_id>/status', methods=['GET'])
def get_cycle_status(cycle_id):
    """(모의) 특정 사이클의 상태를 조회합니다."""
    manifest = read_manifest(cycle_id)
    if manifest:
        return jsonify(manifest)
    else:
        return jsonify({
            "cycle_id": cycle_id,
            "status": { "step": 0, "code": "NOT_FOUND", "text": f"Cycle {cycle_id} not found or malformed." },
            "logs": f"Manifest for cycle {cycle_id} not found or malformed."
        }), 404

@app.route('/api/cycle/<cycle_id>/run/<int:step_id>', methods=['POST'])
def run_step(cycle_id, step_id):
    """
    (모의) 특정 단계를 비동기적으로 실행합니다.
    Design Document의 멱등성(S-1) 로직을 구현하여 중복 작업을 방지합니다.
    """
    manifest = read_manifest(cycle_id)

    if manifest:
        current_status_code = manifest.get('status', {}).get('code')
        # 예시: STEP_X_RUNNING, STEP_X_PENDING과 같은 상태 코드를 확인
        # 실제 구현에서는 step_id에 해당하는 정확한 상태 코드를 확인해야 합니다.
        if current_status_code and (f"STEP_{step_id}_RUNNING" in current_status_code or f"STEP_{step_id}_PENDING" in current_status_code):
            return jsonify({
                "message": f"Step {step_id} for cycle {cycle_id} is already running or pending.",
                "current_status": current_status_code
            }), 409 # Conflict

    # Celery 작업을 트리거합니다.
    debug_task.delay(cycle_id, step_id) # Celery 태스크 호출
    return jsonify({"message": f"Step {step_id} for cycle {cycle_id} has been triggered and sent to worker."}), 202

@app.route('/api/cycle/<cycle_id>/approve/<int:step_id>', methods=['POST'])
def approve_step(cycle_id, step_id):
    """(모의) PM이 특정 단계를 승인합니다."""
    return jsonify({"message": f"Step {step_id} for cycle {cycle_id} has been approved."})

@app.route('/api/cycle/<cycle_id>/content', methods=['GET', 'POST'])
def handle_content(cycle_id):
    """(모의) 에디터용 콘텐츠를 조회하거나 저장합니다."""
    if request.method == 'GET':
        file_path = request.args.get('file', 'step2-outline.md')
        return jsonify({
            "cycle_id": cycle_id,
            "file_path": file_path,
            "content": f"## Mock Content for {file_path}\n\nThis is mock content from the backend."
        })
    elif request.method == 'POST':
        # content = request.json.get('content')
        return jsonify({"message": f"Content for cycle {cycle_id} saved successfully."})

@app.route('/api/schedules', methods=['GET'])
def get_schedules():
    """(모의) 예약된 작업 목록을 조회합니다."""
    return jsonify([{"schedule_id": "sched_1", "cron": "0 0 * * 1", "next_run": "2025-11-17T00:00:00Z"}])

@app.route('/api/schedules/add', methods=['POST'])
def add_schedule():
    """(모의) 새 예약 작업을 추가합니다."""
    return jsonify({"message": "Schedule added successfully."}), 201

@app.route('/api/components', methods=['GET'])
def get_components():
    """(모의) 사용 가능한 Shortcode 컴포넌트 목록을 조회합니다."""
    return jsonify([
        {"name": "PremiumBanner", "snippet": "[PremiumBanner]"},
        {"name": "WineCard", "snippet": '[WineCard: {"name": "...", "price": "..."}]'}
    ])
