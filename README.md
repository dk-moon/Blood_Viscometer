# BloodViscometer
Development of Blood Viscometer

# Data Description

혈액점도계로부터 혈액 샘플 또는 유사 물질로 측정하여 얻어진 시계열 센서 데이터와
얻어진 시계열 센서 데이터를 유체역학 계산식을 통하여 계산되어진 9개의 결과값 및 그래프 데이터

![image](https://github.com/KR-ESWord/BloodViscometer/assets/59715960/c88411dc-2112-49cb-b79c-277c38017624)
- CIS 1 : 왼쪽 관에 액체가 채워진 후 점차 오른쪽 관으로 이동할 때 측정되는 액체의 높이
- CIS 2 : 왼쪽 관으로부터 오른쪽 관으로 차오를때 액체의 높이
- Radius : 양쪽 관으로 부터 액체가 이동되는 관의 내경
- Shear Rate : 측정 종료 후 유체역학 수식에 따른 시간의 변화에 따른 혈액점도 변화

# Deep Learning Method
1. DNN
![image](https://github.com/KR-ESWord/BloodViscometer/assets/59715960/61b7c9b4-26b3-428e-b537-264b6aa785da)

  - X : [Radius, CIS 1, CIS 2]
  - Y : [Shear Rate]
2. DNN
![image](https://github.com/KR-ESWord/BloodViscometer/assets/59715960/55e34090-4e5d-4feb-8ba9-6692505dfc21)

  - X1 : [CIS 1]
  - X2 : [CIS 2]
  - X3 : [Radius]
  - Y : [Shear Rate]
3. CNN
![image](https://github.com/KR-ESWord/BloodViscometer/assets/59715960/8a5af313-9b3b-4f35-a38d-3d1c65e94af6)
![image](https://github.com/KR-ESWord/BloodViscometer/assets/59715960/a2091d98-81a6-48da-b49f-e7f94df40c2e)

  - X1 : [CIS 1]
  - X2 : [CIS 2]
  - X3 : [Radius]
  - Y : [Shear Rate]
4. TabNet
![image](https://github.com/KR-ESWord/BloodViscometer/assets/59715960/30e38081-b119-4fed-bc76-b65c0a61f207)

  - X : [Radius, CIS 1, CIS 2]
  - Y : [Shear Rate]
5. ConvLSTM
![image](https://github.com/KR-ESWord/BloodViscometer/assets/59715960/78f26248-17e5-4b8e-920d-00ecb635876e)

  - X1 : [CIS 2]
  - X2 : [Radius]
  - Y : [Shear Rate]
