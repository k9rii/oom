import json

def filter_common_categories(train_file_path, test_file_path, output_file_path):
    """
    test 데이터와 train 데이터의 공통된 소분류 카테고리만 남겨 새로운 train 파일을 생성합니다.
    """
    # 1. test 파일에서 고유한 소분류 카테고리 목록을 추출합니다.
    test_categories = set()
    with open(test_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                if 'CATEGORYDEPTH_3' in data:
                    test_categories.add(data['CATEGORYDEPTH_3'])
            except json.JSONDecodeError:
                # JSON 형식이 아닌 라인은 건너뜁니다.
                continue

    print(f"✅ {len(test_categories)}개의 고유한 소분류 카테고리를 찾았습니다.")

    # 2. train 파일에서 공통된 카테고리에 해당하는 데이터만 필터링하고 저장합니다.
    filtered_count = 0
    with open(train_file_path, 'r', encoding='utf-8') as train_f, \
         open(output_file_path, 'w', encoding='utf-8') as output_f:
        
        for line in train_f:
            try:
                data = json.loads(line)
                if 'CATEGORYDEPTH_3' in data and data['CATEGORYDEPTH_3'] in test_categories:
                    output_f.write(json.dumps(data, ensure_ascii=False) + '\n')
                    filtered_count += 1
            except json.JSONDecodeError:
                continue

    print(f"🎉 성공적으로 {filtered_count}개의 데이터를 {output_file_path} 파일에 저장했습니다.")


# 파일 경로를 지정해 주세요
TRAIN_FILE = "train.coll.json"
TEST_FILE = "test.coll.json"
OUTPUT_FILE = "new_train.json"

# 함수 실행
filter_common_categories(TRAIN_FILE, TEST_FILE, OUTPUT_FILE)