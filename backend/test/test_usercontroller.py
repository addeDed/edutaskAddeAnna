import pytest
from src.controllers.usercontroller import UserController

class TestUserController:
    def test_invalid_email_format(self, mocker):
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

