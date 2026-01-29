import yaml
import os

class YamlLoader:
    @staticmethod
    def load_metadata(filename: str):
        # 실행 위치에 상관없이 metadata 폴더를 찾도록 절대 경로 처리
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base_dir, "metadata", filename)
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            
            # YAML 데이터를 LLM 프롬프트용 텍스트로 변환
            metadata_text = f"인덱스 패턴: {data.get('index_pattern')}\n"
            metadata_text += f"설명: {data.get('description')}\n"
            metadata_text += "사용 가능한 주요 필드 경로:\n"

            # field['path'] 대신 field['name'] 사용
            for field in data.get('fields', []):
                metadata_text += f"- {field['name']} ({field.get('type', 'keyword')}): {field['description']}\n"
            
            metadata_text += "\n쿼리 작성 규칙:\n"
            # data['rules'] 대신 data['query_rules'] 사용
            for rule in data.get('query_rules', []):
                metadata_text += f"- {rule}\n"
                
            return metadata_text
        except FileNotFoundError:
            return "메타데이터 파일을 찾을 수 없습니다."
        except Exception as e:
            return f"오류 발생: {str(e)}"            
