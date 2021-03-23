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
    correlation_table = round(sss_df.corr(method='pearson'), 3)
    correlation_table.to_csv('correlation_table.csv', index=False)
    return correlation_table


def strongest_correlation(ct_df):
    max_correlation_col = 0
    max_correlation_row = 0
    max_correlation = 0
    for col_index in range(0, len(ct_df)):
        for row_index in range(0, len(ct_df)):
            if row_index != col_index:
                correlation_coefficient = abs(ct_df.iloc[row_index, col_index])
                if correlation_coefficient > max_correlation:
                    max_correlation_col = col_index
                    max_correlation_row = row_index
    fields = list(ct_df.columns.values)
    print("The two attributes with the strongest correlation are " + fields[max_correlation_col] + " and "
          + fields[max_correlation_row] + ".")


def get_strongest_correlated_with(ct_df):
    label = input('Enter valid attribute (Beans,Bread,Cerel,ChdBby,Chips,Corn,Eggs,Fish,Fruit,Meat,Milk,Pepper,' +
                  'Rice,Salza,Sauce,Soda,Tomato,Tortya,Vegges,YogChs): ')
    max_correlation = 0
    best_attr = 0
    count = 0
    fields = list(ct_df.columns.values)
    for coefficient in ct_df.loc[label]:
        if (abs(coefficient) > max_correlation) and (coefficient != 1):
            max_correlation = abs(coefficient)
            best_attr = count
        count = count + 1
    print(label + " is strongly correlated with " + fields[best_attr] + ".")


def part_a_driver():
    correlation_table = calculate_cross_correlation("HW_PCA_SHOPPING_CART_v896.csv")
    strongest_correlation(correlation_table)
    get_strongest_correlated_with(correlation_table)


if __name__ == '__main__':
    """
    
    """
    part_a_driver()

