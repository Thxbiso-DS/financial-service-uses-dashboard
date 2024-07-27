import pandas as pd

def load_and_clean_data(filepath):
    financial_service_df = pd.read_csv(filepath, sep=",")
    
    def validate_column_keys(dataframe, column_names, range_of_keys):
        invalid_rows = {}

        if isinstance(column_names, str):
            column_names = [column_names]

        for column in column_names:
            invalid_rows[column] = []
            for index, value in dataframe[column].items():
                if value not in range_of_keys:
                    invalid_rows[column].append(index)

        for column, rows in invalid_rows.items():
            if rows:
                mode_value = dataframe[column].mode()[0]
                dataframe.loc[rows, column] = mode_value

        return dataframe
    
    def validate_if_answer_yes(dataframe, column_to_validate, yes_no_column, range_of_answer):
        invalid_rows_indices = []
        removed_ids = []
        
        for index, value in dataframe[yes_no_column].items():
            dependent_value = dataframe.loc[index, column_to_validate]
            if (value == 1 and dependent_value not in range_of_answer[1:]) or (value == 0 and dependent_value != -1):
                invalid_rows_indices.append(index)
                removed_ids.append(dataframe.loc[index, 'ID'])
        
        if invalid_rows_indices:        
            print("The following responses are invalid")
            invalid_data = dataframe.loc[invalid_rows_indices]
            print(invalid_data)
        else:
            validate_column_keys(dataframe, column_to_validate, range_of_answer)
    
    columns_with_1_and_0_keys = ["Q8_1", "Q8_2", "Q8_3", "Q8_4", "Q8_5", "Q8_6", "Q8_7", "Q8_8", "Q8_9", "Q8_10", "Q8_11", "mobile_money", "savings", "borrowing", "insurance"]
    columns_with_1_and_2_keys = ["Q6", "Q7", "Q12", "Q14"]
    money_range = list(range(-1, 0)) + list(range(0, 7))
    mobile_money_range = list(range(-1, 0)) + list(range(0, 6))

    validate_column_keys(financial_service_df, "Q3", range(1, 5))
    validate_column_keys(financial_service_df, columns_with_1_and_0_keys, range(0, 2))
    validate_column_keys(financial_service_df, columns_with_1_and_2_keys, range(1, 3))
    validate_column_keys(financial_service_df, "Q4", range(1, 8))
    validate_column_keys(financial_service_df, "Q5", range(1, 7))
    validate_column_keys(financial_service_df, "Q13", money_range)
    validate_column_keys(financial_service_df, "Q15", money_range)
    validate_column_keys(financial_service_df, "Q16", mobile_money_range)
    validate_column_keys(financial_service_df, "Q17", mobile_money_range)
    validate_column_keys(financial_service_df, "Q18", range(0, 6))
    validate_column_keys(financial_service_df, "Q19", range(0, 6))

    employment_type_range = list(range(-1, 0)) + list(range(1, 8))
    selling_things_range = list(range(-1, 0)) + list(range(1, 11))
    providing_service_range = list(range(-1, 0)) + list(range(1, 13))

    validate_if_answer_yes(financial_service_df, "Q9", "Q8_1", employment_type_range)
    validate_column_keys(financial_service_df, "Q10", selling_things_range)
    validate_column_keys(financial_service_df, "Q11", providing_service_range)
    validate_column_keys(financial_service_df, "mobile_money_classification", range(0, 4))

    column_name_mapping = {
        'ID': 'User ID',
        'Q1': 'Age',
        'Q2': 'Gender',
        'Q3': 'Marital status',
        'Q4': 'Highest level of education completed?',
        'Q5': 'Ownership of land/plot',
        'Q6': 'Ownership of land with certificates',
        'Q7': 'Ownership of mobile phone',
        'Q8_1': 'Salaries/wages',
        'Q8_2': 'Trading/selling produce',
        'Q8_3': 'Service providing income',
        'Q8_4': 'Piece work/Casual labor',
        'Q8_5': 'Rental income',
        'Q8_6': 'Interest from savings/investments',
        'Q8_7': 'Pension',
        'Q8_8': 'Social welfare grant',
        'Q8_9': 'Receive money from others',
        'Q8_10': 'Expenses covered by others',
        'Q8_11': 'Other income',
        'Q9': 'Employment type',
        'Q10': 'Main items sold',
        'Q11': 'Main services provided',
        'Q12': 'Sent money in last 12 months?',
        'Q13': 'Last time sent money',
        'Q14': 'Received money in last 12 months?',
        'Q15': 'Last time received money',
        'Q16': 'Frequency of mobile money usage for purchases',
        'Q17': 'Frequency of mobile money usage for bill payment',
        'Q18': 'Literacy in Kiswahili',
        'Q19': 'Literacy in English',
        'mobile_money': 'Use of mobile money',
        'savings': 'Savings behavior',
        'borrowing': 'Borrowing behavior',
        'insurance': 'Insurance ownership',
        'mobile_money_classification': 'Mobile money classification'
    }

    financial_service_df = financial_service_df.rename(columns=column_name_mapping)

    replacement_dict = {
        'Gender': {
            1: 'Male',
            2: 'Female'
        },
        'Marital status': {
            1: 'Married',
            2: 'Divorced',
            3: 'Widowed',
            4: 'Single/never married'
        },
        'Highest level of education completed?': {
            1: 'No formal education',
            2: 'Some primary',
            3: 'Primary completed',
            4: 'Post primary technical training',
            5: 'Some secondary',
            6: 'University or other higher education',
            7: 'Do not know'
        },
        'Ownership of land/plot': {
            1: 'You personally own the land/plot where you live',
            2: 'You own the land/plot together with someone else',
            3: 'A household member owns the land/plot',
            4: 'The land/plot is rented',
            5: 'You do not own or rent the land',
            6: 'Do not know'
        },
        'Ownership of land with certificates': {
            1: 'Yes',
            2: 'No'
        },
        'Ownership of mobile phone': {
            1: 'Yes',
            2: 'No'
        },
        'Salaries/wages': {
            1: 'Yes',
            0: 'No'
        },
        'Trading/selling produce': {
            1: 'Yes',
            0: 'No'
        },
        'Service providing income': {
            1: 'Yes',
            0: 'No'
        },
        'Piece work/Casual labor': {
            1: 'Yes',
            0: 'No'
        },
        'Rental income': {
            1: 'Yes',
            0: 'No'
        },
        'Interest from savings/investments': {
            1: 'Yes',
            0: 'No'
        },
        'Pension': {
            1: 'Yes',
            0: 'No'
        },
        'Social welfare grant': {
            1: 'Yes',
            0: 'No'
        },
        'Receive money from others': {
            1: 'Yes',
            0: 'No'
        },
        'Expenses covered by others': {
            1: 'Yes',
            0: 'No'
        },
        'Other income': {
            1: 'Yes',
            0: 'No'
        },
        'Employment type': {
            -1: 'Not applicable',
            1: 'Government',
            2: 'Private company/business',
            3: 'Individual who owns his own business',
            4: 'Small scale farmer',
            5: 'Commercial farmer',
            6: 'Work for individual/household e.g. security guard, maid etc.',
            7: 'Other'
        },
        'Main items sold': {
            -1: 'Not applicable',
            1: 'Crops/produce I grow',
            2: 'Products I get from livestock',
            3: 'Livestock',
            4: 'Fish you catch yourself/aquaculture',
            5: 'Things you buy from others - agricultural products',
            6: 'Things you buy from others - non-agricultural products',
            7: 'Things you make (clothes, art, crafts)',
            8: 'Things you collect from nature (stones, sand, thatch, herbs)',
            9: 'Things you process (honey, dairy products, flour)',
            10: 'Other'
        },
        'Main services provided': {
            -1: 'Not applicable',
            1: 'Personal services (hairdressers, massage, etc.)',
            2: 'Telecommunications/IT',
            3: 'Financial services',
            4: 'Transport',
            5: 'Hospitality /Accommodation, restaurants, etc.',
            6: 'Information/research',
            7: 'Technical - mechanic, etc.',
            8: 'Educational/child care',
            9: 'Health services - traditional healer etc.',
            10: 'Legal services',
            11: 'Security',
            12: 'Other, specify'
        },
        'Sent money in last 12 months?': {
            1: 'Yes',
            2: 'No'
        },
        'Last time sent money': {
            -1: 'Not applicable',
            1: 'Yesterday/today',
            2: 'In the past 7 days',
            3: 'In the past 30 days',
            4: 'In the past 90 days',
            5: 'More than 90 days ago but less than 6 months ago',
            6: '6 months or longer ago'
        },
        'Received money in last 12 months?': {
            1: 'Yes',
            2: 'No'
        },
        'Last time received money': {
            -1: 'Not applicable',
            1: 'Yesterday/today',
            2: 'In the past 7 days',
            3: 'In the past 30 days',
            4: 'In the past 90 days',
            5: 'More than 90 days ago but less than 6 months ago',
            6: '6 months or longer ago'
        },
        'Frequency of mobile money usage for purchases': {
            -1: 'Not applicable',
            1: 'Never',
            2: 'Daily',
            3: 'Weekly',
            4: 'Monthly',
            5: 'Less often than monthly'
        },
        'Frequency of mobile money usage for bill payment': {
            -1: 'Not applicable',
            1: 'Never',
            2: 'Daily',
            3: 'Weekly',
            4: 'Monthly',
            5: 'Less often than monthly'
        },
        'Literacy in Kiswahili': {
            1: 'Can read and write',
            2: 'Can read only',
            3: 'Can write only',
            4: 'Can neither read nor write',
            5: 'Refused to read'
        },
        'Literacy in English': {
            1: 'Can read and write',
            2: 'Can read only',
            3: 'Can write only',
            4: 'Can neither read nor write',
            5: 'Refused to read'
        },
        'Use of mobile money': {
            1: 'Yes',
            0: 'No'
        },
        'Savings behavior': {
            1: 'Yes',
            0: 'No'
        },
        'Borrowing behavior': {
            1: 'Yes',
            0: 'No'
        },
        'Insurance ownership': {
            1: 'Yes',
            0: 'No'
        },
        'Mobile money classification': {
            0: 'Does not use any financial service',
            1: 'Does not use mobile money',
            2: 'Uses mobile money only',
            3: 'Uses both'
        }
    }

    for column, replacements in replacement_dict.items():
        financial_service_df[column] = financial_service_df[column].replace(replacements)

    return financial_service_df

def save_cleaned_data(dataframe, output_path):
    dataframe.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")



