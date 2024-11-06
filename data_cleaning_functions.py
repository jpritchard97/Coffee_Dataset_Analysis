'''
Define Functions for Data Cleaning
---------------------------------

1. Combine Columns into Single Column
Function: `combine_columns(df, columns_to_combine, new_column_name, separator='; ')`
    Input Parameters:
       - `df`: DataFrame to modify.
       - `columns_to_combine`: List of column names to combine.
       - `new_column_name`: Name of the new combined column.
       - `separator`: String to separate combined values.
    Process:
       - Define an inner function to collect meaningful values from each row:
         - If the value is `True`, use column names with modifications (e.g., strip parentheses).
         - If the value is a non-empty string, keep it.
       - Use `.apply()` to create the combined column by applying the inner function to the given columns.
       - Drop original columns.
    Return: Modified DataFrame with new combined column.
''' 

# data_cleaning_functions.py

def combine_columns(df, columns_to_combine, new_column_name, separator='; '):
    """
    Combines multiple columns into a single column and drops the original columns.
    
    Returns:
    pd.DataFrame: Modified DataFrame with combined column.
    """
    def get_positive_responses(row):
        # Collect only meaningful values: column names if `True`, or non-empty strings directly
        return [
            col.split('(')[-1].replace(')', '').strip() if value == True else str(value).strip() 
            for col, value in zip(columns_to_combine, row) 
            if value == True or (isinstance(value, str) and value.strip())
        ]

    # Apply the function to create the combined column
    df[new_column_name] = df[columns_to_combine].apply(lambda row: separator.join(get_positive_responses(row)), axis=1)
    
    # Drop the original columns
    df = df.drop(columns=columns_to_combine, errors='ignore')
    
    return df


''' 
2. Remove Columns with High Missing Values
Function: `remove_high_missing_columns(df, threshold=0.9)`
    Input Parameters:
       - `df`: DataFrame to clean.
       - `threshold`: Proportion of missing values above which columns will be dropped (0.0 to 1.0).
    Process:
       - Calculate the proportion of missing values for each column.
       - Identify columns where the missing proportion exceeds the given threshold.
       - Drop these columns from the DataFrame.
       - Print names of dropped columns.
    Return: Cleaned DataFrame with columns removed based on the missing value threshold.
'''

def remove_high_missing_columns(df, threshold=0.9):
    """
    Removes columns with missing values above a certain threshold.
    
    Returns:
    pd.DataFrame: DataFrame with columns removed based on the threshold.
    """
    # Calculate the proportion of missing values for each column
    missing_proportion = df.isnull().mean()

    # Identify columns where the proportion of missing values exceeds the threshold
    columns_to_drop = missing_proportion[missing_proportion > threshold].index

    # Drop the identified columns from the DataFrame
    df = df.drop(columns=columns_to_drop, errors='ignore')

    # Print the list of columns that were dropped
    print(f"Columns dropped: {list(columns_to_drop)}")

    # Return the DataFrame with the columns removed
    return df






