# Data Annotation for Relation Extraction - Olympic :trophy:

## [Wrap-UP Report](https://leeyeryeong.notion.site/Wrap-up-report-NLP-04-635d19f786ea4449a72808fa47e385fd)
## 팀 구성 및 역할
- 공통 : Entity 및 Relation 정의, 파일럿 태깅 및 메인 어노테이션
- **김해원** : 가이드라인 작성
- **김혜빈** : 모델 튜닝
- **박준형** : 가이드라인 작성
- **양봉석** : Relation map 작성
- **이예령** : IAA 계산

---

## 1. 프로젝트 개요

### 1.1. 관계 추출(Relation Extraction)

- **관계 추출** : 하나의 문장에서 나타나는 개체(Entity) 쌍 사이의 의미적 관계를 분류하는 태스크이다. 문장에서 나타나는 개체 쌍은 주체(Subject entity)와 대상(Object entity)로 이루어진다. 이 개체 쌍 간의 관계를 분류하는 것이 관계 추출의 목표이다.

### 1.2. 데이터셋

- 도메인: **올림픽**
- 소스 문장 출처: 한국어 위키피디아 (https://ko.wikipedia.org/ CC BY-SA 3.0)
- 규모: 개체 분석이 불가능한 문장을 제외한, 총 1,091 개의 문장
- Train set, Dev set, Test set: 클래스 분포가 유사하도록 층화추출을 활용해 분리하였다.
- 데이터셋의 평가:
    - 작업자 간 일치도(Inter-annotator agreement, IAA): Fleiss’ Kappa = **0.911**
    - 모델 튜닝 결과: klue/roberta-large 로 학습 시 F1 score = **95.035**, AUPRC = **92.903**

**<p align = "center"><img src="https://user-images.githubusercontent.com/99173116/208086310-eba75496-8d9f-4691-a43a-4e7135f133bc.png" width="800" height="300"/>  
Train set, Dev set, Test set의 관계 클래스별 분포</p>** 
</br> 

## 2. 태깅 작업

### 2.1. 작업 과정

**<p align = "center"><img src="https://user-images.githubusercontent.com/99173116/208086914-71705fd2-f256-4791-a5f3-d2a22873f146.png" width="800" height="250"/></p>** 

1. 원시 코퍼스 문장 분리
    - KSS 라이브러리를 이용해 원시 코퍼스를 문장 단위로 분리한 후, 빈 괄호 및 소제목 등을 제거하였다.
    - 개체를 찾을 수 없는 경우에는 작업자가 직접 앞문장이나 뒷문장과 병합하였다.  
2. 개체 유형 및 관계 설정
    - 올림픽 도메인에서 자주 등장하는 개체 유형과 관계를 선정하였다.  
3. 개체 태깅 및 관계 태깅 (파일럿)
    - 2에서 선정한 개체와 관계를 바탕으로 파일럿 태깅을 진행하였다.  
4. IAA 및 관계 분포 확인 및 개체 유형 및 관계 수정
    - 파일럿 결과 IAA는 **0.838**로 높게 나왔으나, 관계 클래스 간 명확한 구분을 위해 개체 유형 및 관계를 다시 수정하였다.  
5. 본 태깅
    - 4에서 선정한 개체와 관계를 바탕으로 1명당 200개 문장에 대한 개체 및 관계를 태깅한 뒤, 다른 작업자가 태깅한 작업물에 대해서도 관계를 태깅하였다.  
6. 최종 IAA 측정
    - 5명의 작업자 간 IAA: **0.911**  
7. 완성된 데이터셋으로 fine-tuning
    - 모델 학습 성능 (RbertWithLSTM)  
    
      |  | test micro-f1 | test auprc | epoch | batch |
      | --- | --- | --- | --- | --- |
      | 1. klue/bert-base | 90.226 | 95.930 | 10 | 16 |
      | **2. klue/roberta-large** | **95.035** | 92.903 | 10 | 16 |
      | 3. klue/bert-base | 93.525 | 96.756 | 10 | 32 |
      | 4. klue/roberta-large | 92.308 | 93.804 | 10 | 32 |
    
**<p align = "center"><img src="https://user-images.githubusercontent.com/99173116/208087071-f0ad62c5-9841-4204-82b9-310835db7024.png" width="600" height="500"/>  
가장 좋게 나온 2. klue/roberta-large 모델의 Confusion matrix</p>** 

### 2.2. 작업 도구
- **Tagtog**
  - 개체 태깅을 위해 사용하였다.
  - Subject, Object의 범위를 지정한 후, 타입을 태깅하였다.
      - 이를 csv파일로 변환 후 관계 태깅을 위해 스프레드 시트로 옮겨서 작업을 진행하였다.

- **스프레드시트**
  - 관계 태깅을 위해 사용하였다.
  - Tagtog의 작업 결과물에 대해 Subject Entity와 Object Entity 사이의 관계 태깅을 진행하였다.  
</br>      
    
## 3. Relation map
- [Relation map 파일](https://github.com/boostcampaitech4lv23nlp1/level2_dataannotation_nlp-level2-nlp-04/files/10245408/04_relation.xlsx)

<p align = "center"><img src="https://user-images.githubusercontent.com/99173116/208088670-2661a566-9e52-42ad-80f7-ad3d57fd1619.png" width="800" height="400"/></p> 
</br>

## 4. Guideline
- [Guideline 파일](https://github.com/boostcampaitech4lv23nlp1/level2_dataannotation_nlp-level2-nlp-04/files/10245443/04_guideline.pdf)
</br>

## 5. 자체 평가 의견

- 직접 작업자가 되어서 태깅을 할 때 애매했던 부분이나 이슈가 되는 부분에 대해서 토론을 통해 규칙을 정하고, 그것을 가이드라인에 반영해서 명확한 가이드라인을 세웠다. 명확한 가이드라인을 통해 IAA지수가 높은 데이터셋을 만들 수 있었다.
- 교차 검수를 통해 팀원 모두가 한번씩 전체 데이터셋을 어노테이션 할 수 있도록 하였고 검수 시 발생한 이슈들을 토론을 거쳐서 해결하였다.
- 클래스 간의 불균형을 최대한 고려하여 관계를 지정하기 위해서 파일럿 태깅 후 토론을 거쳤지만 불균형 문제를 완전히 해결하지 못하였던 것이 아쉬웠다.
- 설정한 개체와 관계 간의 구분이 명확했던 덕분에 IAA가 높게 나올 수 있었다.
