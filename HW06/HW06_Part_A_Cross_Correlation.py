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
    cross_correlation_table = round(sss_df.corr(method='pearson'), 3)
    cross_correlation_table.to_csv('cross_correlation_table.csv', index=False)
    return cross_correlation_table


def strongest_correlation(cct_df):
    max_correlation_col = 0
    max_correlation_row = 0
    max_correlation = 0
    for col_index in range(0, len(cct_df)):
        for row_index in range(0, len(cct_df)):
            if row_index != col_index:
                correlation_coefficient = abs(cct_df.iloc[row_index, col_index])
                if correlation_coefficient > max_correlation:
                    max_correlation_col = col_index
                    max_correlation_row = row_index
    fields = list(cct_df.columns.values)
    print("The two attributes with the strongest correlation are " + fields[max_correlation_col] + " and "
          + fields[max_correlation_row] + ".")


def get_strongest_correlated_with(cct_df):
    attr = input('Enter valid attribute (Beans,Bread,Cerel,ChdBby,Chips,Corn,Eggs,Fish,Fruit,Meat,Milk,Pepper,' +
                  'Rice,Salza,Sauce,Soda,Tomato,Tortya,Vegges,YogChs): ')
    max_correlation = 0
    best_attr = 0
    count = 0
    fields = list(cct_df.columns.values)
    for coefficient in cct_df.loc[attr]:
        if (abs(coefficient) > max_correlation) and (coefficient != 1):
            max_correlation = abs(coefficient)
            best_attr = count
        count = count + 1
    print(attr + " is strongly correlated with " + fields[best_attr] + ".")


def get_least_correlated_with(cct_df):
    fields = list(cct_df.columns.values)
    cct = {}
    for attr in fields:
        average_coefficient = 0
        for coefficient in cct_df.loc[attr]:
            average_coefficient = average_coefficient + abs(coefficient)
        average_coefficient = average_coefficient / len(fields)
        cct[attr] = round(average_coefficient, 3)
    cct = {k: v for k, v in sorted(cct.items(), key=lambda item: item[1])}
    print(cct)


def part_a_driver():
    cross_correlation_table = calculate_cross_correlation("HW_PCA_SHOPPING_CART_v896.csv")
    #strongest_correlation(cross_correlation_table)
    #get_strongest_correlated_with(cross_correlation_table)
    get_least_correlated_with(cross_correlation_table)


if __name__ == '__main__':
    """
    
    """
    part_a_driver()

