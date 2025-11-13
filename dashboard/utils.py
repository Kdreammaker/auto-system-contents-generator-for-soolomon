import os
import json

# 프로젝트 루트 디렉토리를 기준으로 content-output 경로를 설정합니다.
# Flask 앱의 root_path를 사용하거나, 환경 변수 등으로 설정할 수 있습니다.
# 여기서는 임시로 상대 경로를 사용하며, 실제 배포 시에는 더 견고한 경로 설정이 필요합니다.
# 예: APP_ROOT = os.path.dirname(os.path.abspath(__file__))
#     CONTENT_OUTPUT_DIR = os.path.join(APP_ROOT, '..', 'content-output')

def get_content_output_path():
    """
    content-output 디렉토리의 절대 경로를 반환합니다.
    이 함수는 Flask 앱 컨텍스트 외부에서도 작동하도록 설계되었습니다.
    """
    # 현재 파일(utils.py)의 경로를 기준으로 프로젝트 루트를 찾습니다.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
    return os.path.join(project_root, 'content-output')

def get_manifest_path(cycle_id: str) -> str:
    """
    주어진 cycle_id에 해당하는 manifest.json 파일의 전체 경로를 반환합니다.
    """
    cycle_dir = os.path.join(get_content_output_path(), cycle_id)
    return os.path.join(cycle_dir, 'manifest.json')

def read_manifest(cycle_id: str) -> dict | None:
    """
    특정 사이클의 manifest.json 파일을 읽어 Python 딕셔너리로 반환합니다.
    파일이 없으면 None을 반환합니다.
    """
    manifest_path = get_manifest_path(cycle_id)
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: manifest.json for cycle {cycle_id} is malformed.")
            return None
    return None

def write_manifest(cycle_id: str, manifest_data: dict):
    """
    주어진 manifest_data를 특정 사이클의 manifest.json 파일에 씁니다.
    필요한 경우 디렉토리를 생성합니다.
    """
    cycle_dir = os.path.join(get_content_output_path(), cycle_id)
    os.makedirs(cycle_dir, exist_ok=True) # 디렉토리가 없으면 생성

    manifest_path = get_manifest_path(cycle_id)
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest_data, f, indent=2, ensure_ascii=False)
