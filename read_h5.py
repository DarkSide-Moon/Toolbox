import pandas as pd
import os
import glob
from pathlib import Path

def read_h5_file(file_path, rows=5):
    """读取H5文件并显示指定行数的数据
    
    参数:
        file_path: H5文件的路径
        rows: 要显示的数据行数，默认为5
    
    返回:
        DataFrame对象或在出错时返回None
    """
    try:
        # 使用pandas读取H5文件
        df = pd.read_hdf(file_path)
        print(f"\n文件名: {os.path.basename(file_path)}")
        print(f"数据形状: {df.shape}")
        print(f"列名: {list(df.columns)}")
        print(f"\n前{rows}行数据:")
        print(df.head(rows))
        print('='*100)
        return df
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
        return None

def list_h5_files(directory):
    """列出指定目录中的所有H5文件
    
    参数:
        directory: 要搜索的目录路径
    
    返回:
        H5文件路径列表
    """
    h5_files = glob.glob(os.path.join(directory, "*.h5"))
    return h5_files

def process_directory(directory, rows=5):
    """处理目录中的H5文件，允许用户选择读取全部或单个文件
    
    参数:
        directory: 包含H5文件的目录路径
        rows: 要显示的数据行数，默认为5
    """
    
    h5_files = list_h5_files(directory)
    
    if not h5_files:
        print(f"在目录 {directory} 中没有找到H5文件")
        return
    
    print(f"找到以下H5文件:")
    for i, file_path in enumerate(h5_files):
        print(f"{i+1}. {os.path.basename(file_path)}")
    
    file_choice = input("\n请输入要查看的文件编号，或输入'all'查看所有文件: ")
    
    if file_choice.lower() == 'all':
        for file_path in h5_files:
            read_h5_file(file_path, rows)
    else:
        try:
            idx = int(file_choice) - 1
            if 0 <= idx < len(h5_files):
                read_h5_file(h5_files[idx], rows)
            else:
                print("无效的文件编号")
        except ValueError:
            print("请输入有效的数字或'all'")

# 示例用法
if __name__ == "__main__":
    # 使用方法1：指定目录和行数
    # process_directory("C:/Users/adi/Desktop/factor_data/FactorData_df_ljh", rows=10)
    
    # 使用方法2：只指定目录，使用默认行数(5)
    # process_directory("C:/Users/adi/Desktop/factor_data/FactorData_df_ljh")
    
    # 示例
    base_dir = r"C:\Users\adi\Desktop\factor_data\FactorData_df_ljh"
    process_directory(base_dir) 
