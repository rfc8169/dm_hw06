"""
Assignment: HW06
Description: Calculates the cross correlation of all the attributes
Author: Reed Cogliano, Neel Raj
"""

import pandas


def calculate_cross_correlation(csv_file):
    """
    Uses the pandas library to determine the cross correlation table of the provided csv file.
    Writes the pandas dataframe containing the cross correlation table to a file.
    :param: csv_file - csv file containing data to process
    :return: cross_correlation_table - pandas dataframe containing the cross correlation values
    """
    sss_df = pandas.read_csv(csv_file).drop(['ID'], axis=1)
    cross_correlation_table = round(sss_df.corr(method='pearson'), 3)
    cross_correlation_table.to_csv('cross_correlation_table.csv', index=False)
    return cross_correlation_table


def strongest_correlation(cct_df):
    """
    Determines the two attributes with the strongest cross correlation coefficient and prints it out.
    :param: cct_df - pandas dataframe containing the cross correlation table
    """
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
    """
    The user inputs a valid attribute, and the attribute's strongest correlated attribute is printed out.
    :param: cct_df - pandas dataframe containing the cross correlation table
    """
    attr = input('Enter valid attribute (Beans,Bread,Cerel,ChdBby,Chips,Corn,Eggs,Fish,Fruit,Meat,Milk,Pepper,' +
                 'Rice,Salza,Sauce,Soda,Tomato,Tortya,Vegges,YogChs,NULL): ')
    if attr != 'NULL':
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
    """
    Creates a sorted dictionary with the attributes as keys and the average absolute value coefficient for each
    attribute in the cross correlation table.
    :param: cct_df - pandas dataframe containing the cross correlation table
    """
    fields = list(cct_df.columns.values)
    cct = {}
    for attr in fields:
        average_coefficient = 0
        for coefficient in cct_df.loc[attr]:
            if coefficient != 1:
                average_coefficient = average_coefficient + abs(coefficient)
        average_coefficient = average_coefficient / len(fields)
        cct[attr] = round(average_coefficient, 3)
    cct = {k: v for k, v in sorted(cct.items(), key=lambda item: item[1])}
    print(cct)


def get_cross_correlation_coefficient(cct_df):
    print('List of attributes: Beans,Bread,Cerel,ChdBby,Chips,Corn,Eggs,Fish,Fruit,Meat,Milk,Pepper,' +
          'Rice,Salza,Sauce,Soda,Tomato,Tortya,Vegges,YogChs,NULL')
    row = input("First attribute: ")
    col = input("Second attribute: ")
    if row != 'NULL' or col != 'NULL':
        fields = list(cct_df.columns.values)
        row_index = fields.index(row)
        col_index = fields.index(col)
        coefficient = cct_df.iloc[row_index, col_index]
        print("The coefficient between " + str(row) + " and " + str(col) + " is: " + str(coefficient))


def part_a_driver():
    """
    Part A Driver creates the cross correlation coefficient table and passes it into the rest of the defined functions.
    """
    cross_correlation_table = calculate_cross_correlation("HW_PCA_SHOPPING_CART_v896.csv")
    strongest_correlation(cross_correlation_table)
    get_strongest_correlated_with(cross_correlation_table)
    get_least_correlated_with(cross_correlation_table)
    get_cross_correlation_coefficient(cross_correlation_table)


if __name__ == '__main__':
    """
    Runs the driver for the methods defined in Part A.
    """
    part_a_driver()
