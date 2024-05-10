'''
testingfile
'''
import pytest

def get_user_by_email(email: str):
    '''
    docstring here later
    '''
    db = ['duplicate@example.com','duplicate@example.com','user1@example.com']

    
    if email not in db:
        raise ValueError('Error: invalid email address')
    
    try:
        filtered_list = [selector for selector in db if selector == email]

        if len(filtered_list) == 1:
            return filtered_list[0]
        else:
            print(f'Error: more than one user found with mail {email}')
            return filtered_list[0]
    except Exception as e:
        raise Exception()

def test_get_user_by_email_duplicate(capsys):
    '''
    test for duplicate
    '''
    get_user_by_email('duplicate@example.com')
    captured = capsys.readouterr()
    assert "Error: more than one user found with mail" in captured.out

def test_get_user_by_email_user_not_found():
    '''
    test for user not found
    '''
    with pytest.raises(ValueError) as exc_info:
        get_user_by_email('user_do_not_exists@example.com')

def test_get_user_by_email_exists():
    '''
    test for user exists
    '''
    assert('user1@example.com') == get_user_by_email('user1@example.com')
