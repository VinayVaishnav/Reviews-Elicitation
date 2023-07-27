question_option_dict = {
    1: {
        'question': "How would you describe this person's communication style?",
        'options': [
            {
                'option_num': 1,
                'option_text': 'Straight to the point'
            },
            {
                'option_num': 2,
                'option_text': 'Listens more, talks less'
            },
            {
                'option_num': 3,
                'option_text': 'Provides constructive feedback'
            },
            {
                'option_num': 4,
                'option_text': 'Always has a positive or encouraging word'
            },
        ]
    },
    
    2: {
        'question': 'How does this person typically spends their lunch break at work?',
        'options': [
            {
                'option_num': 1,
                'option_text': 'Chatting with colleagues'
            },
            {
                'option_num': 2,
                'option_text': 'Catching up on industry news'
            },
            {
                'option_num': 3,
                'option_text': 'Relaxing and unwinding'
            },
            {
                'option_num': 4,
                'option_text': 'Doing a quick workout'
            },
        ]
    },

    3: {
        'question': 'How does this person approach challenging situations?',
        'options': [
            {
                'option_num': 1,
                'option_text': 'Thinks before acting'
            },
            {
                'option_num': 2,
                'option_text': 'Collaborates with others'
            },
            {
                'option_num': 3,
                'option_text': 'Takes immediate action'
            },
            {
                'option_num': 4,
                'option_text': 'Seeks assistance when needed'
            },
        ]
    },
}

poll_dict = {
    f'q{question_num}': [f'o{option_num+1}' for option_num in range(len(question_option_dict[question_num]['options']))]
    for question_num in question_option_dict.keys()
}