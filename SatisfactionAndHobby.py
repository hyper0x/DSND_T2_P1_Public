import numpy as np
import pandas as pd
import ProgramHobbyStats as phs


def gen_hobby_ratios_df_by_satis(satis_col, satis_df):
    '''Generate a new data framework that contains some new columns 
    about the hobby ratios for different satisfactions. Only for professional developer.
    
    INPUT:
    satis_col - The name of column about satisfactions.
    years_df - The dataframe containing the column about satisfactions (JobSatisfaction or CareerSatisfaction).
    
    OUTPUT:
    ratios_df - The dataframe containing columns satis, hobby_ratio and contrib_ratio.
    '''
    sub_df = satis_df[satis_df['Professional'] == 'Professional developer']
    sub_df = sub_df[['ProgramHobby', 'Professional', satis_col]]
    # Append some columns derive from column ProgramHobby.
    hobby_df = phs.add_hobby_columns(sub_df)
    # Delete column ProgramHobby.
    hobby_df = hobby_df.drop(['ProgramHobby'], axis=1)

    satis_vals = hobby_df[satis_col].drop_duplicates().values
    ratios_df = pd.DataFrame([],
                             columns=['hobby_ratio', 'contrib_ratio'],
                             index=satis_vals)

    def get_ratio(hobby_col, satis):
        '''Get the ratio for hobby.
        '''
        df_temp = hobby_df[hobby_df[satis_col] == satis]
        total = df_temp.shape[0]
        hobby_count = sum(df_temp[hobby_col])
        return hobby_count / total

    ratios_df['hobby_ratio'] = [
        get_ratio('hobby', satis) for satis in satis_vals
    ]
    ratios_df['contrib_ratio'] = [
        get_ratio('contrib', satis) for satis in satis_vals
    ]
    ratios_df['satis'] = [satis for satis in satis_vals]
    ratios_df = ratios_df[['satis', 'hobby_ratio', 'contrib_ratio']]
    ratios_df.sort_values(by=['satis'], inplace=True)

    return ratios_df


if __name__ == "__main__":
    df = pd.read_csv('./survey_results_public.csv')

    job_satis_df = df[df['JobSatisfaction'].isnull() == False]
    hobby_ratios_df = gen_hobby_ratios_df_by_satis('JobSatisfaction',
                                                   job_satis_df)
    print(hobby_ratios_df)

    career_satis_df = df[df['CareerSatisfaction'].isnull() == False]
    hobby_ratios_df2 = gen_hobby_ratios_df_by_satis('CareerSatisfaction',
                                                    career_satis_df)
    print(hobby_ratios_df2)
