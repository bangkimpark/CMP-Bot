# test_main.py
from services.controller import ChatController

def main():
    controller = ChatController()
    print("=== ES 자연어 검색 테스트 (종료: 'exit') ===")
    
    while True:
        user_input = input("\n질문을 입력하세요: ")
        if user_input.lower() == 'exit': break

        try:
            print("🔍 쿼리 생성 중...")
            query, res = controller.execute_workflow(user_input)
            
            # print(f"\n[생성된 쿼리]\n{query}")
            import json
            print("\n[생성된 쿼리]")
            print(json.dumps(query, indent=2, ensure_ascii=False))

            
            hits = res.get('hits', {}).get('hits', [])
            aggs = res.get('aggregations', {})

            if hits:
                print(f"\n[검색 결과: {len(hits)}건]")
                for hit in hits: print(f"- {hit['_source']}")

            if aggs:
                print(f"\n[집계 결과]")
                for agg_name, agg_data in aggs.items():
                    buckets = agg_data.get('buckets', [])
                    for bucket in buckets:
                        print(f"- ID: {bucket['key']} (doc_count: {bucket['doc_count']})")

            if not hits and not aggs:
                print("\n검색 결과가 없습니다.")

            # if aggs:
            #     print(f"\n[집계 결과]")
            #     for agg_name, agg_data in aggs.items():
            #         for bucket in agg_data.get('buckets', []):
            #             print(f"- ID: {bucket['key']} (count: {bucket['doc_count']})")


        except Exception as e:
            print(f"❌ 오류 상세 정보:")
            # 에러의 원인과 메시지를 구체적으로 출력
            if hasattr(e, 'response'):
                print(f"Status Code: {e.status_code}")
                print(f"Response Body: {e.response.json()}")
            else:
                print(f"Message: {str(e)}")

if __name__ == "__main__":
    main()