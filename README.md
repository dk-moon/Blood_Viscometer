# BloodViscometer
Development of Blood Viscometer

## Data Description

![image](https://file.notion.so/f/f/dcf0fb52-1450-4279-bd48-b86e803ce6b3/2231a19c-3921-4c82-bf64-2f964bf24c6f/Untitled.png?id=a5fe24b6-543f-4b3a-a09a-5119dd87c86c&table=block&spaceId=dcf0fb52-1450-4279-bd48-b86e803ce6b3&expirationTimestamp=1722506400000&signature=dSNVQvjkuFzV32J5kp3vqxHih06nLoyW5-h_7zKoF-U&downloadName=Untitled.png)

혈액점도계로부터 혈액 샘플 또는 유사 물질로 측정하여 얻어진 시계열 센서 데이터와
얻어진 시계열 센서 데이터를 유체역학 계산식을 통하여 계산되어진 9개의 결과값 및 그래프 데이터

# 인공지능을 이용한 혈액점도계 개발

## 프로젝트 개요

- 이 프로젝트의 목적은 인공지능 기술을 활용하여 혈액 점도계를 자동화하고, 기존 장비보다 정확하고 빠르게 혈액 점도를 측정하는 시스템을 개발하는 것입니다. 이를 통해 혈액 점도 측정의 효율성을 높이고, 의료 현장에서의 활용도를 증대시키는 것이 목표입니다.

## 도메인 이해

- 혈액 점도: 혈액의 점성은 다양한 질병의 진단과 치료에 중요한 지표로 사용됩니다. 정확한 혈액 점도 측정은 환자의 건강 상태를 평가하고 적절한 치료를 제공하는 데 필수적입니다.

## 데이터

1. 혈액 점도 시계열 데이터: 기존 스캐닝 모세관법을 이용하여 수집한 혈액 점도 시계열 데이터.
2. 혈액 샘플 데이터: 다양한 환자로부터 수집된 혈액 샘플 데이터.

## 모델

- TabNet 및 CNN 앙상블 모델: 혈액 점도 예측을 위해 TabNet과 CNN을 결합한 앙상블 모델을 사용합니다.
- 참고 모델: DNN, ConvLSTM, CNN-LSTM

## 프로젝트 주요 단계

1. 데이터 수집 및 전처리:
    - 시계열 데이터 수집: 스캐닝 모세관법을 이용하여 혈액 점도 시계열 데이터를 수집합니다.
    - 데이터 정제: 수집된 데이터를 정제하고, 노이즈를 제거하여 모델 훈련에 적합한 형식으로 변환합니다.
2. 모델 개발 및 훈련:
    - TabNet 모델 설정: TabNet 모델을 설정하고, 혈액 점도 시계열 데이터를 사용하여 훈련시킵니다.
    - CNN 모델 설정: CNN 모델을 설정하고, 혈액 샘플 데이터를 사용하여 훈련시킵니다.
    - 앙상블 모델 구축: TabNet과 CNN 모델을 결합하여 앙상블 모델을 구축합니다.
    - 모델 최적화: 모델의 성능을 최적화하기 위해 하이퍼파라미터 튜닝을 수행합니다.
3. 혈액 점도 예측:
    - 모델 적용: 훈련된 앙상블 모델을 사용하여 혈액 점도를 예측합니다.
    - 결과 검증: 예측된 결과를 실제 혈액 점도와 비교하여 모델의 정확성을 평가합니다.
4. 시스템 개발 및 적용:
    - 자동화 시스템 개발: Docker로 예측 모델 파이프라인 구성하여 혈액 점도계를 자동화하는 시스템을 개발합니다.
    - 실시간 분석: 실시간으로 혈액 점도를 분석하고 결과를 제공하는 시스템을 구축합니다.

## 결과 및 성과

- 이 프로젝트를 통해 TabNet 및 CNN 앙상블 모델을 사용하여 기존 혈액 점도계산 소프트웨어 대비 정확도를 80% 향상시키고, 추론 속도를 90% 향상시킬 수 있었습니다. 또한, 혈액 점도계 자동화 신규 장비 개발의 특허 출원에 기여하였으며, 의료 현장에서의 활용도를 높이는 데 성공하였습니다. 이로써 의료진이 더 정확하고 신속하게 환자의 건강 상태를 평가할 수 있게 되었습니다.


- CIS 1 : 왼쪽 관에 액체가 채워진 후 점차 오른쪽 관으로 이동할 때 측정되는 액체의 높이
- CIS 2 : 왼쪽 관으로부터 오른쪽 관으로 차오를때 액체의 높이
- Radius : 양쪽 관으로 부터 액체가 이동되는 관의 내경
- Shear Rate : 측정 종료 후 유체역학 수식에 따른 시간의 변화에 따른 혈액점도 변화

# Deep Learning Method
1. DNN

  - X : [Radius, CIS 1, CIS 2]
  - Y : [Shear Rate]
2. DNN

  - X1 : [CIS 1]
  - X2 : [CIS 2]
  - X3 : [Radius]
  - Y : [Shear Rate]
3. CNN

  - X1 : [CIS 1]
  - X2 : [CIS 2]
  - X3 : [Radius]
  - Y : [Shear Rate]
4. TabNet

  - X : [Radius, CIS 1, CIS 2]
  - Y : [Shear Rate]
5. ConvLSTM

  - X1 : [CIS 2]
  - X2 : [Radius]
  - Y : [Shear Rate]
