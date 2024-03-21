# Library Import
import pandas as pd
import numpy as np
import os
import argparse

from tqdm.auto import tqdm
from glob import glob

from sklearn.preprocessing import LabelEncoder

import onnx
import onnxruntime as ort


# Get DAT Files
# Extract Radius, Start Index, CIS Information from DAT Files
def get_X(dat_path, r_mode):
    start_index = 0
    radius = 0.0
    radius_data = None
    data = []

    with open(dat_path, 'r', encoding='euc-kr') as file:
        lines = file.readlines()
        
    # Radius Information
    radius = float(lines[24].replace(" ","").replace("\n","").split(",")[-2])
    radius = round(radius / 0.9447 * 1000 * 2, 2)
    
    radius_label = [3.10,3.11,3.12,3.13,3.14,3.15,3.16,3.17,
                    3.18,3.19,3.20,3.21,3.22,3.23,3.24,3.25,
                    3.26,3.27,3.28]
    
    radius = [radius_label.index(radius)]
    data.extend(radius)
    
    # CIS Information
    start_index = int(lines[10].replace(" ","").replace("\n","").split(",")[-2]) # 관측 시작 지점
    
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
    
    data.extend(cis_1_data)
    data.extend(cis_2_data)
    
    cis_data = np.array([data]).astype(np.float32)

    return cis_data

# Load ONNX Model
def get_model(onnx_path):
    # ONNX 모델을 로드합니다.
    model = onnx.load(onnx_path)

    # ONNX 런타임 세션을 생성합니다.
    model = ort.InferenceSession(onnx_path)
    return model

# Predict, UnScaling and Save result
def get_result(dat_path, r_mode, model, output_path):
    # 7. Predic
    cis_data = get_X(dat_path, r_mode)
    try:
        inputs = {
            model.get_inputs()[0].name: cis_data
        }
        outputs = model.run(None, inputs)
        
        scale_list = [10,10,10,10,10,10,10,15,20]
        
        output_cnt = len(outputs[0][0])
        output_list = []
        for i in range(output_cnt):
            output = outputs[0][0][i]
            output_list.append(output)
        output_list = sorted(output_list)
        
        shear_list = [round(o_i * s_i,2) for o_i, s_i in zip(output_list, scale_list)]
        shear_df = pd.DataFrame(columns=["1000","300", "150", "100", "50", "10", "5", "2", "1"],
                                data=[shear_list])
        
        shear_df.to_csv(output_path, index=False)
    except Exception as ex:
        print("Fail to Get Result!\nERROR : Input Type Error\nCheck ONNX Model Type!")
        print(ex)
    return

# Main Function
def main(dat_path, onnx_path, output_path):
    # Get Path Parameter
    dat_path = dat_path.replace("\\", "/")
    onnx_path = onnx_path.replace("\\", "/")
    output_path = output_path.replace("\\", "/")
    
    # Check ONNX Model
    onnx_chk = onnx_path.split(".")[-1]
    if onnx_chk == "onnx":
        # Get ONNX Model
        onnx_model = get_model(onnx_path)
        
        # Get DAT Files
        dat_list = list(glob(os.path.join(dat_path, "*.dat")))
        r_mode = onnx_path.split("/")[-1].split("_")[2] # radius pre-processing mode check
        if len(dat_list) > 0:
            for dat_idx in range(len(dat_list)):
                # Get Dat File
                dat_file = dat_list[dat_idx].replace("\\", "/")
                
                # Set Ouput File Path
                if os.path.isdir(output_path) == False:
                    os.makedirs(output_path)
                dat_nm = dat_file.split("/")[-1]
                dat_name = dat_nm.split(".")[0]
                output_paths = os.path.join(output_path, ".".join((dat_name, "csv"))).replace("\\", "/")
                
                # Get Shear Rate Result
                get_result(dat_file, r_mode, onnx_model, output_paths)
        else:
            print("No Exist DAT File!\nCheck DAT Files Path!")
    else:
        print("No Exist ONNX Model!\nCheck ONNX Model Path!")

if __name__ == "__main__":
    # argparse.ArgumentParser 객체를 생성합니다.
    parser = argparse.ArgumentParser(description="Ubiosis 혈액점도계 계산")
    
    # dat_path, onnx_path, output_path를 추가합니다.
    parser.add_argument("dat_path", type=str, help="dat 파일 경로", default="./")
    parser.add_argument("onnx_path", type=str, help="ONNX 파일 경로", default="./")
    parser.add_argument("output_path", type=str, help="결과 파일 경로", default="./result")
    
    # 명령줄 인수를 파싱합니다.
    args = parser.parse_args()
    
    # main 함수를 호출하여 작업을 수행합니다.
    main(args.dat_path, args.onnx_path, args.output_path)