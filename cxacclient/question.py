from __future__ import print_function, unicode_literals
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt, Separator

questions = [
    {
        'type': 'checkbox',
        'qmark': 'Checkmarx User OnBoarding',
        'message': 'Select Teams for User',
        'name': 'CxAC Changes',
        'choices': [ 
            Separator('*-* Scanners *-*'),
            {
                'name': 'Dev Team #1.A'
            },
            {
                'name': 'Dev Team #1.B'
            },
            {
                'name': 'Dev Team #1.C'
            },
            Separator('*-* Reviewers *-*'),
            {
                'name': 'Dev Team #2.A',
                'checked': True
            },
            {
                'name': 'Dev Team #2.B'
            },
            {
                'name': 'Dev Team #2.C'
            },
            Separator('*-* Verify/Update Results *-*'),
            {
                'name': 'Dev Team #3.A'
            },
            {
                'name': 'Dev Team #3.B'
            },
            {
                'name': 'Dev Team #3.C'
            },
            Separator('*-* Team 4 Admins *-*'),
            {
                'name': 'CxAdmin #1',
            },
            {
                'name': 'AC Admin',
            },
            {
                'name': 'Server Administrator Group',
            },
            {
                'name': 'CxAudit Group',
            },
            {
                'name': 'Team Admin Group',
            }
        ],
        'validate': lambda answer: 'You must choose at least one topping.' \
            if len(answer) == 0 else True
    }
]

answers = prompt(questions)
pprint(answers)


questions1 = [
    {
        'type': 'confirm',
        'message': 'Do you want to continue?',
        'name': 'continue',
        'default': True,
    }
]

answers1 = prompt(questions1)
pprint(answers1)