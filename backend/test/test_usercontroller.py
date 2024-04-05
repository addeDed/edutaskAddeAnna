import pytest
from src.controllers.usercontroller import UserController

class TestUserController:
    def test_query_database_for_user(self, mocker):
        # Mock the DAO object
        dao_mock = mocker.MagicMock()
        
        # Create UserController instance with the mocked DAO
        controller = UserController(dao=dao_mock)
        
        # Mock the find method to raise an error
        dao_mock.find.side_effect = Exception('Database operation failed')
        
        # Call the method with a valid email address
        try:
            controller.get_user_by_email('test@example.com')
        except Exception:
            pass  # Ignore any exceptions raised

        print("Mocked DAO calls:")
        print(dao_mock.method_calls)
        
        # Assert that the DAO's find method was called once
        dao_mock.find.assert_called_once()