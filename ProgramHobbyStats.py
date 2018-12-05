import numpy as np
import pandas as pd

# To reduce the number of characters in Professional.
professional_map = {
    "None of these": "None of these",
    "Professional developer": "Developer",
    "Professional non-developer who sometimes writes code": "Non-developer",
    "Student": "Student",
    "Used to be a professional developer": "Used to be"
}


def gen_hobby_ratios_df(pro_vals, pro_hobby_df):
    '''Generate A new dataframe containing some new columns about ratios of hobby.
    
    INPUT:
    pro_vals - The counts corresponding to the indexes about Professional.
    pro_hobby_df - The dataframe containing some columns about hobby.
    
    OUTPUT:
    ratios_df - The dataframe containing columns hobby, contrib and both.
    '''
    ratios_df = pd.DataFrame([],
                             columns=['hobby', 'contrib', 'both'],
                             index=pro_vals.index)
    for col in ['hobby', 'contrib', 'both']:
        # Create a dataframe with a value equal to 1 for a column.
        curr_df = pro_hobby_df[pro_hobby_df[col] == 1]
        # Get the count of value about Professional, sorted by index.
        curr_pro_vals = curr_df['Professional'].value_counts().sort_index()
        ratios_df[col] = [
            get_ratio(pro_index, curr_pro_vals, pro_hobby_df)
            for pro_index in pro_vals.index.values
        ]
    return ratios_df


def get_ratio(pro_index, pro_vals, df):
    '''Get the ratio of the count to the number of rows.

    INPUT:
    pro_index - An index about a major.
    pro_vals - The counts corresponding to the indexes about Professional.
    df - The dataframe containing column Professional.
    
    OUTPUT:
    ratio - The ratio of the count to the number of rows in the dataframe.    
    '''
    # Find the count of value based on the index about Professional.
    pro_val = pro_vals.loc[[pro_index]][0]
    # Create a dataframe for a specialized value of Professional.
    df_temp = df[df['Professional'] == pro_index]
    ratio = pro_val / df_temp.shape[0]
    return ratio


def gen_pro_hobby_df(df):
    '''Generate A new dataframe containing some new columns from column ProgramHobby.
    
    INPUT:
    df - The dataframe containing columns Professional and ProgramHobby.
    
    OUTPUT:
    pro_hobby_df - The dataframe containing columns Professional, hobby, contrib and both.
    '''
    pro_hobby_df = df[['Professional', 'ProgramHobby']]
    # Append some columns derive from column ProgramHobby.
    pro_hobby_df = add_hobby_columns(pro_hobby_df)
    # Delete column ProgramHobby.
    pro_hobby_df = pro_hobby_df.drop(['ProgramHobby'], axis=1)
    return pro_hobby_df


def add_hobby_columns(hobby_df):
    '''Append some columns derive from column ProgramHobby to the copy of dataframe, 
    and return the copy.
    
    INPUT:
    hobby_df - The dataframe containing column ProgramHobby.
    
    OUTPUT:
    df_copy - The copy of dataframe hobby_df containing columns hobby, contrib and both.
    '''
    df_copy = hobby_df.copy()
    # Add a column about programming hobby.
    df_copy['hobby'] = df_copy.apply(
        lambda x: hobby(x['ProgramHobby']), axis=1)
    # Add a column about open source project contribution.
    df_copy['contrib'] = df_copy.apply(
        lambda x: contrib(x['ProgramHobby']), axis=1)
    # Add a column about the hobby and the contribution.
    df_copy['both'] = df_copy.apply(
        lambda x: hobby_and_contrib(x['ProgramHobby']), axis=1)
    return df_copy


def hobby(value):
    '''Get the hobby tag.
    '''
    if value in ['Yes, I program as a hobby', 'Yes, both']:
        return 1
    else:
        return 0


def contrib(value):
    '''Get the contrib tag.
    '''
    if value in ['Yes, I contribute to open source projects', 'Yes, both']:
        return 1
    else:
        return 0


def hobby_and_contrib(value):
    '''Get the tag for hobby and contribution.
    '''
    if value == 'Yes, both':
        return 1
    else:
        return 0


if __name__ == "__main__":
    df = pd.read_csv('./survey_results_public.csv')
    program_hobby_df = df[df['ProgramHobby'].isnull() == False]
    pro_hobby_df = gen_pro_hobby_df(program_hobby_df)
    print(pro_hobby_df.shape)

    pro_vals = pro_hobby_df['Professional'].value_counts().sort_index()
    ratios_df = gen_hobby_ratios_df(pro_vals, pro_hobby_df)
    print(ratios_df.head())