"""
Assignment: HW06
Description:
Author: Reed Cogliano, Neel Raj
"""

import pandas

def calculate_cross_correlation(csv_file):
    """

    """
    sss_df_full = pandas.read_csv(csv_file)
    sss_df = sss_df_full.drop(['ID'], axis=1)
    correlation_table = sss_df.corr(method='pearson')\

    correlation_table.to_csv('correlation_table.csv', index=False)

    print(correlation_table)


if __name__ == '__main__':
    """
    
    """
    calculate_cross_correlation("test.csv")
