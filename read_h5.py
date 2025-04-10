import pandas as pd
import os
import glob
from pathlib import Path

def read_h5_file(file_path):
    """读取H5文件并显示前10行数据"""
    try:
        # 使用pandas读取H5文件
        df = pd.read_hdf(file_path)
        print(f"\n文件名: {os.path.basename(file_path)}")
        print(f"数据形状: {df.shape}")
        print(f"列名: {list(df.columns)}")
        print("\n前10行数据:")
        print(df.head(10))
        return df
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
        return None

def main():
    # 文件路径
    base_dir = r"C:\Users\adi\Desktop\factor_data\FactorData_df_ljh"
    
    # 获取目录下所有的h5文件
    h5_files = glob.glob(os.path.join(base_dir, "*.h5"))
    
    if not h5_files:
        print(f"在目录 {base_dir} 中没有找到H5文件")
        return
    
    print(f"找到以下H5文件:")
    for i, file_path in enumerate(h5_files):
        print(f"{i+1}. {os.path.basename(file_path)}")
    
    # 读取单个文件
    file_choice = input("\n请输入要查看的文件编号，或输入'all'查看所有文件: ")
    
    if file_choice.lower() == 'all':
        for file_path in h5_files:
            read_h5_file(file_path)
    else:
        try:
            idx = int(file_choice) - 1
            if 0 <= idx < len(h5_files):
                read_h5_file(h5_files[idx])
            else:
                print("无效的文件编号")
        except ValueError:
            print("请输入有效的数字或'all'")

if __name__ == "__main__":
    main() 