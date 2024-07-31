# BloodViscometer
Development of Blood Viscometer

# Data Description

![image](https://file.notion.so/f/f/dcf0fb52-1450-4279-bd48-b86e803ce6b3/2231a19c-3921-4c82-bf64-2f964bf24c6f/Untitled.png?id=a5fe24b6-543f-4b3a-a09a-5119dd87c86c&table=block&spaceId=dcf0fb52-1450-4279-bd48-b86e803ce6b3&expirationTimestamp=1722506400000&signature=dSNVQvjkuFzV32J5kp3vqxHih06nLoyW5-h_7zKoF-U&downloadName=Untitled.png)

혈액점도계로부터 혈액 샘플 또는 유사 물질로 측정하여 얻어진 시계열 센서 데이터와
얻어진 시계열 센서 데이터를 유체역학 계산식을 통하여 계산되어진 9개의 결과값 및 그래프 데이터

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
