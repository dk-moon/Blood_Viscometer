# Library Import
import pandas as pd
import numpy as np
import os
import argparse

from glob import glob

import onnx
import onnxruntime as ort


# Get DAT Files
# Extract Radius, Start Index, CIS Information from DAT Files
def get_X(dat_path):
    tab_data = []
    start_index = 0
    radius = 0.0
    radius_data = None

    with open(dat_path, 'r', encoding='euc-kr') as file:
        lines = file.readlines()
        
    # Radius Information
    radius_label = [3.10,3.11,3.12,3.13,3.14,3.15,3.16,3.17,
                    3.18,3.19,3.20,3.21,3.22,3.23,3.24,3.25,
                    3.26,3.27,3.28]
    
    radius = float(lines[24].replace(" ","").replace("\n","").split(",")[-2])
    radius = round(radius / 0.9447 * 1000 * 2, 2)
    try:
        radius_idx = [radius_label.index(radius)]
    except:
        radius_idx = [len(radius_label)+1]
    
    tab_data.extend(radius_idx)
    radius_data = np.array([radius]).astype(np.float32).reshape(-1,1)
        
    # CIS Information
    start_index = int(lines[10].replace(" ","").replace("\n","").split(",")[-2]) -32 # 관측 시작 지점
    
    # CIS 관측 정보 인덱싱
    cis_1_data = []
    cis_2_data = []
    for i in range(32, len(lines)-32, 1):
        datas = lines[i].replace(" ","").replace("\n","").split(",")
        if len(datas) > 4:
            cis_1 = float(datas[2])
            cis_2 = float(datas[3])
            
            cis_1_data.append(cis_1)
            cis_2_data.append(cis_2)
    # 관측 시작 지점 인덱싱
    cis_1_data = cis_1_data[start_index:start_index+6000]
    cis_2_data = cis_2_data[start_index:start_index+6000]
    tab_data.extend(cis_1_data)
    tab_data.extend(cis_2_data)
    
    cis_1_data = np.array([cis_1_data]).astype(np.float32)
    cis_2_data = np.array([cis_2_data]).astype(np.float32)
    
    cis_data = np.array([tab_data]).astype(np.float32)

    return cis_data, cis_1_data, cis_2_data, radius_data

# Load ONNX Model
def get_model():
    cnn_path = "./CNN_Model.onnx"
    tab_path = "./TabNet_Model.onnx"
    # ONNX 모델을 로드합니다.
    cnn_model = onnx.load(cnn_path)
    tab_model = onnx.load(tab_path)

    # ONNX 런타임 세션을 생성합니다.
    cnn_model = ort.InferenceSession(cnn_path)
    tab_model = ort.InferenceSession(tab_path)
    return cnn_model, tab_model

# Predict, UnScaling and Save result
def get_result(dat_path, cnn_model, tab_model, output_path):
    # 7. Predict
    scale_list = [10,10,10,10,10,10,10,15,20]
    cis_data, cis_1_data, cis_2_data, radius_data = get_X(dat_path)
    try:
        # CNN
        cnn_inputs = {
            cnn_model.get_inputs()[0].name: cis_1_data,
            cnn_model.get_inputs()[1].name: cis_2_data,
            cnn_model.get_inputs()[2].name: radius_data,
        }
        cnn_outputs = cnn_model.run(None, cnn_inputs)
        # TabNet
        tab_inputs = {
            tab_model.get_inputs()[0].name: cis_data
        }
        tab_outputs = tab_model.run(None, tab_inputs)
        
        cnn_output_cnt = len(cnn_outputs[0][0])
        cnn_output_list = []
        for i in range(cnn_output_cnt):
            cnn_output = cnn_outputs[0][0][i]
            cnn_output_list.append(cnn_output)
        cnn_output_list = sorted(cnn_output_list)
        
        tab_output_cnt = len(tab_outputs[0][0])
        tab_output_list = []
        for i in range(tab_output_cnt):
            tab_output = tab_outputs[0][0][i]
            tab_output_list.append(tab_output)
        tab_output_list = sorted(tab_output_list)
        
        final_output_list = [
            cnn_output_list[0],
            cnn_output_list[1],
            cnn_output_list[2],
            ((cnn_output_list[3]+tab_output_list[3])/2),
            ((cnn_output_list[4]+tab_output_list[4])/2),
            ((cnn_output_list[5]+tab_output_list[5])/2),
            tab_output_list[6],
            tab_output_list[7],
            tab_output_list[8]
            ]
        
        shear_list = [round(o_i * s_i,1) for o_i, s_i in zip(final_output_list, scale_list)]
        shear_df = pd.DataFrame(columns=["1000","300", "150", "100", "50", "10", "5", "2", "1"],
                                data=[shear_list])
        
        shear_df.to_csv(output_path, index=False)
    except Exception as ex:
        print("Fail to Get Result!\nERROR : Input Type Error\nCheck ONNX Model Type!")
        print(ex)
    return

# Main Function
def main(dat_path):
    print("===== Start Blood Viscosity =====")
    # Get Path Parameter
    print("Read DAT Files")
    dat_path = dat_path.replace("\\", "/")
    # Get DAT Files
    dat_list = list(glob(os.path.join(dat_path, "*.dat")))
    
    # Get ONNX Model
    print("Create Models Instence")
    cnn_model, tab_model = get_model()
    
    # Get Result
    print("Calculate Result")
    if len(dat_list) > 0:
        for dat_idx in range(len(dat_list)):
            # Get Dat File
            dat_file = dat_list[dat_idx].replace("\\", "/")
            # Get Shear Rate Result
            dat_nm = dat_file.split("/")[-1]
            dat_name = dat_nm.split(".")[0]
            output_paths = os.path.join(dat_path, ".".join((dat_name, "csv"))).replace("\\", "/")
            get_result(dat_file, cnn_model, tab_model, output_paths)
        print("===== Done!! =====\n")
    else:
        print("No Exist DAT File!\nCheck DAT Files Path!")
    

if __name__ == "__main__":
    # argparse.ArgumentParser 객체를 생성합니다.
    parser = argparse.ArgumentParser(description="Ubiosis 혈액점도계 계산")
    
    # dat_path, onnx_path, output_path를 추가합니다.
    parser.add_argument("dat_path", type=str, help="dat 파일 경로", default="./")
    
    # 명령줄 인수를 파싱합니다.
    args = parser.parse_args()
    
    # main 함수를 호출하여 작업을 수행합니다.
    main(args.dat_path)