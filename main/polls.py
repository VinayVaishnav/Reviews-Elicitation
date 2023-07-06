question_option_dict = {
    1: {
        'question': 'What is your favorite color?',
        'options': [
            {
                'option_num': 1,
                'option_text': 'Red'
            },
            {
                'option_num': 2,
                'option_text': 'Blue'
            },
            {
                'option_num': 3,
                'option_text': 'Green'
            },
        ]
    },
    
    2: {
        'question': 'Question 2',
        'options': [
            {
                'option_num': 1,
                'option_text': 'Option 1'
            },
            {
                'option_num': 2,
                'option_text': 'Option 2'
            },
            {
                'option_num': 3,
                'option_text': 'Option 3'
            },
        ]
    },

    3: {
        'question': 'Question 3',
        'options': [
            {
                'option_num': 1,
                'option_text': 'Option 1'
            },
            {
                'option_num': 2,
                'option_text': 'Option 2'
            },
            {
                'option_num': 3,
                'option_text': 'Option 3'
            },
        ]
    },
}

poll_dict = {
    f'q{question_num}': [f'o{option_num+1}' for option_num in range(len(question_option_dict[question_num]['options']))]
    for question_num in question_option_dict.keys()
}