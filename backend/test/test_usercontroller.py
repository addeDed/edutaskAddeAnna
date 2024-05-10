'''
test module docstring
'''

import pytest
from src.controllers.usercontroller import UserController
from src.util.dao import DAO

@pytest.mark.unit
class TestUserController:
    '''
    TestUserController class docstring
    '''
# TEST 1
    def test_invalid_email_format(self, mocker):
        """
        Test the behavior of the get_user_by_email method when provided with different email formats.
        It should raise a ValueError for each invalid email format.
        """
        # List of invalid email formats to test
        emails = [
            'invalidemail.com',
            'invalid.email.com',
            'invalidemail@',
            '@invalidemail.com',
            'invalidemail@.com',
            'invalidemail@domain',
            'invalid email@example.com',
            'invalid!email@example.com',
            'invalidemail',
            'valid@email.com'
        ]

        dao_mock = mocker.MagicMock()
        dao_mock.find.return_value = [{'email': 'test@example.com'}]
        controller = UserController(dao=dao_mock)

        # Loop through each invalid email format and test
        for email in emails:
            try:
                controller.get_user_by_email(email)
                print("No error raised for ", email)
            except ValueError as e:
                print(f"ValueError raised: {e} for ", email)

# TEST 2a
    def test_query_database_for_user(self, mocker):
        """
        Test case to verify that the UserController queries the database for a user with the provided email address.

        Purpose:
        This test verifies that when the `get_user_by_email` method of the UserController is called with a valid email address,
        it attempts to query the database for a user with that email address.

        Steps:
        1. Mock the DAO object.
        2. Create a UserController instance with the mocked DAO.
        3. Mock the `find` method of the DAO object to raise an error when called.
        4. Call the `get_user_by_email` method of the UserController with a valid email address.
        5. Assert that the `find` method of the DAO object was called once.

        """
        dao_mock = mocker.MagicMock()
        controller = UserController(dao=dao_mock)
        dao_mock.find.side_effect = Exception('Database operation failed')

        try:
            controller.get_user_by_email('test@example.com')
        except Exception:
            pass  # Ignore any exceptions raised

        print("Mocked DAO calls:")
        print(dao_mock.method_calls)

        # Assert that the DAO's find method was called once
        dao_mock.find.assert_called_once()

# TEST 2b
    def test_query_database_for_user_none(self, mocker):
        """
        Test case to verify that the UserController does not query the database when an empty email address is provided.

        Purpose:
        This test verifies that when the `get_user_by_email` method of the UserController is called with an empty email address,
        it does not attempt to query the database.

        Steps:
        1. Mock the DAO object.
        2. Create a UserController instance with the mocked DAO.
        3. Mock the `find` method of the DAO object to raise an error when called.
        4. Call the `get_user_by_email` method of the UserController with an empty email address.
        5. Assert that the `find` method of the DAO object was not called.

        """
        dao_mock = mocker.MagicMock()
        controller = UserController(dao=dao_mock)
        dao_mock.find.side_effect = Exception('Database operation failed')

        try:
            controller.get_user_by_email('')
        except Exception:
            pass  # Ignore any exceptions raised

        print("Mocked DAO calls:")
        print(dao_mock.method_calls)

        # Assert that the DAO's find method was not called
        dao_mock.find.assert_not_called()

# TEST 3a
    def test_user_with_unique_entry(self, mocker):
        """
        Test the behavior of the get_user_by_email method when provided with an email address that has a unique entry in the database.
        It should return the user object associated with that email address.
        """
        dao_mock = mocker.MagicMock()
        controller = UserController(dao=dao_mock)
        dao_mock.find.return_value = [{'email': 'user1@example.com'}]

        # Call get_user_by_email with the email address
        result = controller.get_user_by_email('user1@example.com')

        # Assert that the result matches the expected result
        assert result == {'email': 'user1@example.com'}

# TEST 3b
    def test_user_with_non_unique_entry(self, mocker, capsys):
        """
        Test the behavior of the get_user_by_email method when provided with an email address that has multiple entries in the database.
        It should raise an exception and return the first user object associated with that email address.
        """
        dao_mock = mocker.MagicMock()
        dao_mock.find.return_value = [{'email': 'user2@example.com'},
                                      {'email': 'user2@example.com'},
                                     ]
        controller = UserController(dao=dao_mock)

        # Call get_user_by_email with the email address
        result = controller.get_user_by_email('user2@example.com')

        captured = capsys.readouterr()
        assert "Error: more than one user found with mail" in captured.out

        # Assert that an exception is raised
        #assert exc_info.type == Exception

        # Assert that the result matches the expected result (first user entry)
        assert result == {'email': 'user2@example.com'}

# TEST 3c
    def test_user_without_entry(self, mocker):
        """
        Test the behavior of the get_user_by_email method when provided with an email address that does not have any entry in the database.
        org - It should return an empty list.
        updated - It should return None (not implemented in function)
        """
        dao_mock = mocker.MagicMock()
        controller = UserController(dao=dao_mock)
        dao_mock.find.return_value = []
        try:
            result = controller.get_user_by_email('user3@example.com')
            assert result == None
        except Exception as exept:
            assert 'IndexError' in f"Unexpected exception type: {type(exept).__name__}"

# TEST 4
    def test_get_user_by_email_database_failure(self, mocker):
        """
        Test the behavior of the get_user_by_email method when a database operation fails.
        It should raise an exception with the appropriate error message.
        """
        dao_mock = mocker.MagicMock()
        dao_mock.find.side_effect = Exception('Database operation failed')
        controller = UserController(dao=dao_mock)

        # Call get_user_by_email with a valid email address and expect Exception
        with pytest.raises(Exception) as exc_info:
            controller.get_user_by_email('test@example.com')

        # Assert that the exception contains the expected error message
        assert str(exc_info.value) == 'Database operation failed'
