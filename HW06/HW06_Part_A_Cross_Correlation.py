"""
Assignment: HW06
Description:
Author: Reed Cogliano, Neel Raj
"""

import pandas

def calculate_cross_correlation(csv_file):
    """

    """
    student_df = pandas.read_csv(csv_file)
    print(student_df)


if __name__ == '__main__':
    """
    
    """
    calculate_cross_correlation("test.csv")
