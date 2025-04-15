'''
此工具用于将所有因子数据和收益数据合并成一个数据集，并保存为h5文件
用下一期收益数据作为标签，因子数据作为特征

对于每个股票：
获取该股票的所有因子日期并排序
遍历因子日期（除了最后一个日期）
对于每个当前日期，直接取因子日期序列中的下一个日期
用这个下一个日期去收益率数据中查找对应的收益率
如果这个日期在收益率数据中不存在，则填充为NaN
最后将结果保存为一个具有多级索引的DataFrame，第一级为股票代码，第二级为因子日期
'''
import pandas as pd
import numpy as np
import os

def merge_factor_return_data(factors_file, returns_file, output_file, drop_missing=True):
    """
    合并因子数据和收益数据，将下一期收益作为标签

    参数:
    factors_file (str): 因子数据文件路径
    returns_file (str): 收益率数据文件路径
    output_file (str): 输出数据文件路径
    drop_missing (bool): 是否删除包含缺失值的行，默认为True

    返回:
    pd.DataFrame: 合并后的数据
    """
    # 检查文件是否存在
    if not os.path.exists(factors_file) or not os.path.exists(returns_file):
        print(f"文件不存在，请确认{factors_file}和{returns_file}文件路径正确")
        return None

    # 读取h5文件
    factors_data = pd.read_hdf(factors_file)
    returns_data = pd.read_hdf(returns_file)

    # 显示数据基本信息
    print(f"\n因子数据形状(原始): {factors_data.shape}")
    print(f"收益数据形状: {returns_data.shape}")

    # 获取唯一的股票代码，set去重，sorted排序
    instruments = sorted(set(idx[0] for idx in factors_data.index))
    print(f"共有 {len(instruments)} 个唯一股票代码")

    # 创建列表收集所有数据行
    rows_list = []
    multi_index_list = []

    # 对每个股票分别处理
    for instrument in instruments:
        
        # 获取该股票的因子数据和收益数据
        try:
            instrument_factors = factors_data.loc[instrument]
            instrument_returns = returns_data.loc[instrument]
        except KeyError:
            # 如果股票在收益数据中不存在，跳过
            continue

        # 获取该股票的所有因子日期并排序
        factor_dates = sorted(instrument_factors.index)
        
        # 对每个因子日期处理（除了最后一个日期）
        for i in range(len(factor_dates) - 1):
            current_date = factor_dates[i]
            next_date = factor_dates[i + 1]  # 取因子数据中的下一个日期当成对收益数据的索引
            
            # 获取当期因子数据
            if isinstance(instrument_factors, pd.DataFrame):
                factor_row = instrument_factors.loc[current_date].values
            else:  # Series
                factor_row = [instrument_factors.loc[current_date]]
            
            # 获取下一期收益数据（如果存在）
            try:
                if isinstance(instrument_returns, pd.DataFrame):
                    return_row = instrument_returns.loc[next_date].values
                else:  # Series
                    return_row = [instrument_returns.loc[next_date]]
            except KeyError:
                # 如果下一期日期在收益数据中不存在，使用NaN
                return_row = [np.nan] * (len(returns_data.columns) if isinstance(returns_data, pd.DataFrame) else 1)
            
            # 合并数据行
            combined_row = list(factor_row) + list(return_row)
            rows_list.append(combined_row)
            multi_index_list.append((instrument, current_date))
            
            if len(rows_list) % 10000 == 0:
                print(f"已处理 {len(rows_list)} 行数据...")

    # 获取列名
    factor_columns = factors_data.columns.tolist()
    return_columns = returns_data.columns.tolist()
    all_columns = factor_columns + return_columns

    # 创建多级索引
    multi_index = pd.MultiIndex.from_tuples(multi_index_list, names=['instrument', 'datetime'])

    # 创建最终DataFrame
    total_data = pd.DataFrame(rows_list, index=multi_index, columns=all_columns)

    # 显示合并后的数据信息
    print(f"\n合并后数据形状: {total_data.shape}")
    print(f"合并后的列: {total_data.columns.tolist()}")

    # 检查并处理缺失值
    missing_values_count = total_data.isnull().sum().sum()
    rows_with_missing = total_data.isnull().any(axis=1).sum()
    print(f"\n数据中共有 {missing_values_count} 个缺失值")
    print(f"包含缺失值的行数: {rows_with_missing}")

    # 根据参数决定是否删除缺失值行
    if drop_missing and rows_with_missing > 0:
        # 丢弃包含缺失值的行
        original_shape = total_data.shape
        total_data = total_data.dropna()
        print(f"已丢弃缺失值行，数据形状从 {original_shape} 变为 {total_data.shape}")

    # 保存到新的h5文件
    print(f"\n正在保存到{output_file}...")
    total_data.to_hdf(output_file, key='data', mode='w')

    print(f"数据已成功保存到{output_file}")

    # 输出示例数据以供验证
    print("\n数据样例（前5行）:")
    print(total_data.head())
    
    return total_data

if __name__ == "__main__":
    # 默认文件路径
    factors_file = 'combined_factors.h5'
    returns_file = 'returns.h5'
    output_file = 'new_total_data.h5'
    
    # 是否删除缺失值，默认为True
    drop_missing = True
    
    # 运行数据合并
    result_data = merge_factor_return_data(
        factors_file=factors_file,
        returns_file=returns_file,
        output_file=output_file,
        drop_missing=drop_missing
    )
    
    print("处理完成!")
