import numpy as np
import pandas as pd
import ProgramHobbyStats as phs


def gen_counts_df_by_years(years_col, years_df):
    '''Generate A new data frame containing some new columns about years.
    
    INPUT:
    years_col - The name of column about years.
    years_df - The dataframe containing the column about years (YearsProgram or YearsCodedJob).
    
    OUTPUT:
    counts_df - The dataframe containing columns years, count, ratio, 
                dev_count, dev_ratio, not_dev_count and not_dev_ratio.
    '''
    years_df = years_df[years_df['Professional'] != 'None of these']

    # Create a new dataframe for counts and ratios.
    years_vals = years_df[years_col].value_counts().sort_index()
    counts_df = pd.DataFrame(
        years_vals.values, columns=['count'], index=years_vals.index)

    # Add a new column to store the overall ratios.
    count_total = sum(counts_df['count'])
    counts_df['ratio'] = [count / count_total for count in counts_df['count']]

    # Add a new column to store the counts of professional developers.
    dev_years_vals = \
        years_df[years_df['Professional']=='Professional developer'][
        years_col].value_counts().sort_index()
    counts_df['dev_count'] = dev_years_vals.values
    # Add a new column to store the ratios of professional developers.
    dev_count_total = sum(counts_df['dev_count'])
    counts_df['dev_ratio'] = [
        count / dev_count_total for count in counts_df['dev_count']
    ]

    # Add a new column to store the counts of professional non-developers.
    not_dev_years_vals = \
        years_df[years_df['Professional']!='Professional developer'][
        years_col].value_counts().sort_index()
    counts_df['not_dev_count'] = not_dev_years_vals.values
    # Add a new column to store the ratios of professional non-developers.
    not_dev_count_total = sum(counts_df['not_dev_count'])
    counts_df['not_dev_ratio'] = [
        count / not_dev_count_total for count in counts_df['not_dev_count']
    ]

    # Adjust and rebuild the column about years to facilitate sorting and drawing.
    if 'years' not in counts_df.columns:
        counts_df['years'] = [
            get_years_num(years) for years in counts_df.index
        ]

    cols = [
        'years', 'count', 'ratio', 'dev_count', 'dev_ratio', 'not_dev_count',
        'not_dev_ratio'
    ]
    counts_df = counts_df[cols]
    counts_df.sort_values(by=['years'], inplace=True)

    return counts_df


def get_years_num(years):
    '''Convert a string argument to a floating point number.
    '''
    if years == "":
        return 0
    first_word = years.split(' ')[0]
    if first_word == 'Less':
        return 0.5
    else:
        return float(first_word) + 0.5


def get_median_of_years(years_str_list):
    '''Find the median of YearsProgram from list.
    '''
    years_list = []
    years_map = {}
    for years_str in years_str_list:
        years = get_years_num(years_str)
        years_list.append(years)
        years_map[years] = years_str

    years_median = years_map[np.median(years_list)]
    return years_median


def gen_hobby_ratios_df_by_years(years_col, years_df, only_dev=True):
    '''Generate a new data framework that contains some new columns 
    about the hobby ratios for different years.
    
    INPUT:
    years_col - The name of column about years.
    years_df - The dataframe containing the column about years (YearsProgram or YearsCodedJob).
    only_dev - Is it only for professional developers.
    
    OUTPUT:
    ratios_df - The dataframe containing columns years, hobby_ratio and contrib_ratio.
    '''
    sub_df = years_df[['ProgramHobby', 'Professional', years_col]]

    if only_dev:
        sub_df = sub_df[sub_df['Professional'] == 'Professional developer']
        sub_df = sub_df.drop(['Professional'], axis=1)
    else:
        sub_df = sub_df[sub_df['Professional'] != 'None of these']

    # Append some columns derive from column ProgramHobby.
    hobby_df = phs.add_hobby_columns(sub_df)
    # Delete column ProgramHobby.
    hobby_df = hobby_df.drop(['ProgramHobby'], axis=1)

    years_vals = hobby_df[years_col].drop_duplicates().values
    ratios_df = pd.DataFrame([],
                             columns=['hobby_ratio', 'contrib_ratio'],
                             index=years_vals)

    def get_ratio(hobby_col, years):
        '''Get the ratio for hobby.
        '''
        df_temp = hobby_df[hobby_df[years_col] == years]
        total = df_temp.shape[0]
        hobby_count = sum(df_temp[hobby_col])
        return hobby_count / total

    ratios_df['hobby_ratio'] = [
        get_ratio('hobby', years) for years in years_vals
    ]
    ratios_df['contrib_ratio'] = [
        get_ratio('contrib', years) for years in years_vals
    ]

    if 'years' not in ratios_df.columns:
        ratios_df['years'] = [get_years_num(years) for years in years_vals]

    ratios_df = ratios_df[['years', 'hobby_ratio', 'contrib_ratio']]
    ratios_df.sort_values(by=['years'], inplace=True)

    return ratios_df


if __name__ == "__main__":
    df = pd.read_csv('./survey_results_public.csv')

    years_program_df = df[df['YearsProgram'].isnull() == False]
    counts_df = gen_counts_df_by_years('YearsProgram', years_program_df)
    counts = [
        sum(counts_df['count']),
        sum(counts_df['dev_count']),
        sum(counts_df['not_dev_count'])
    ]
    sums = [
        sum(counts_df['ratio']),
        sum(counts_df['dev_ratio']),
        sum(counts_df['not_dev_ratio'])
    ]
    print([counts, sums])
    print(counts_df.head())

    dev_hobby_ratios_df = gen_hobby_ratios_df_by_years(
        'YearsProgram', years_program_df, only_dev=True)
    print(dev_hobby_ratios_df)

    years_coded_job_df = df[df['YearsCodedJob'].isnull() == False]
    counts_df = gen_counts_df_by_years('YearsCodedJob', years_coded_job_df)
    counts = [
        sum(counts_df['count']),
        sum(counts_df['dev_count']),
        sum(counts_df['not_dev_count'])
    ]
    sums = [
        sum(counts_df['ratio']),
        sum(counts_df['dev_ratio']),
        sum(counts_df['not_dev_ratio'])
    ]
    print([counts, sums])
    print(counts_df.head())

    dev_hobby_ratios_df2 = gen_hobby_ratios_df_by_years(
        'YearsCodedJob', years_coded_job_df, only_dev=True)
    print(dev_hobby_ratios_df2)
