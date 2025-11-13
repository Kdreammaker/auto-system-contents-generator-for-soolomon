# -*- coding: utf-8 -*-
"""
메인 Flask 애플리케이션 및 Celery 설정 파일입니다.
이 파일은 Flask 앱을 초기화하고 비동기 작업을 위한 Celery를 설정합니다.
"""
import os
import json
from flask import Flask, jsonify, request
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
app = Flask(__name__)

# 2. 환경 변수(.env)로부터 Celery 설정 로드
app.config.update(
    CELERY_BROKER_URL=os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0'),
    CELERY_RESULT_BACKEND=os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
)

# 3. Celery 인스턴스 생성
# 이 'celery' 변수가 docker-compose.yml의 'celery -A dashboard.app.celery' 명령어에서 찾던 대상입니다.
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

# --- Mock API Endpoints ---

@app.route('/')
def index():
    """
    앱이 실행 중인지 확인하기 위한 간단한 테스트 라우트입니다.
    """
    return "Flask server is running with mock API endpoints!"

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
    """(모의) 새 사이클을 시작합니다."""
    return jsonify({"message": "New cycle started successfully", "cycle_id": "251113"}), 202 # 비동기 처리를 암시하는 202 응답

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
