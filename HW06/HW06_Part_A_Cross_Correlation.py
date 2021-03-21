"""
Assignment: HW06
Description:
Author: Reed Cogliano, Neel Raj
"""

import pandas

def calculate_cross_correlation(csv_file):
    """
    :param: csv_file - csv file containing data
    """
    sss_df = pandas.read_csv(csv_file).drop(['ID'], axis=1)
    return sss_df.corr(method='pearson')


def strongest_correlation(df):
    max_correlation_col = 0
    max_correlation_row = 0
    max_correlation = 0
    for col_index in range(1, len(df)):
        for row_index in range(1, len(df)):
            if row_index != col_index:
                correlation_coefficient = abs(df.iloc[row_index, col_index])
                if correlation_coefficient > max_correlation:
                    max_correlation_col = col_index
                    max_correlation_row = row_index
    fields = list(df.columns.values)
    print("The two attributes with the strongest correlation are " + fields[max_correlation_col] + " and "
          + fields[max_correlation_row] + ".")


if __name__ == '__main__':
    """
    
    """
    correlation_table = calculate_cross_correlation("HW_PCA_SHOPPING_CART_v896.csv")
    strongest_correlation(correlation_table)
