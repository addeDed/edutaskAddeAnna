import pytest
from src.util.dao import DAO
from pymongo.errors import WriteError, ServerSelectionTimeoutError
from unittest.mock import patch, MagicMock

# Fixture for setting up the DAO object and mocking the database interactions
@pytest.fixture
def mock_dao():
    with patch('pymongo.MongoClient') as mock_client:
        # Setup mock database and collection
        mock_db = mock_client.return_value.edutask
        mock_collection = mock_db.test_collection

        # Instantiate DAO with mocked collection
        dao = DAO('test_collection')
        dao.collection = mock_collection
        yield dao, mock_collection

# Test for successful insertion of valid data
def test_create_valid_data(mock_dao):
    dao, mock_collection = mock_dao
    valid_data = {"name": "John Doe", "email": "john@example.com"}
    fake_id = "fake_id"
    mock_collection.insert_one.return_value = MagicMock(inserted_id=fake_id)
    mock_collection.find_one.return_value = valid_data.copy()
    mock_collection.find_one.return_value["_id"] = fake_id

    result = dao.create(valid_data)

    assert "_id" in result, "Result should contain the '_id' key"
    assert result["_id"] == fake_id, "The '_id' key should have the value 'fake_id'"
    mock_collection.insert_one.assert_called_once_with(valid_data)
    mock_collection.find_one.assert_called_once_with({'_id': fake_id})

# Test for insertion with invalid data
def test_create_invalid_data(mock_dao):
    dao, mock_collection = mock_dao
    invalid_data = {"email": "john@example.com"}  # Missing 'name'
    mock_collection.insert_one.side_effect = WriteError("Invalid data")
    
    with pytest.raises(WriteError):
        dao.create(invalid_data)

# Test for insertion with database unavailable
def test_create_database_unavailable(mock_dao):
    dao, mock_collection = mock_dao
    mock_collection.insert_one.side_effect = ServerSelectionTimeoutError("Database unavailable")
    
    with pytest.raises(ServerSelectionTimeoutError):
        dao.create({"name": "Jane Doe", "email": "jane@example.com"})

# Test for insertion with unique constraint violation
def test_create_unique_constraint_violation(mock_dao):
    dao, mock_collection = mock_dao
    duplicate_data = {"name": "John Doe", "email": "john@example.com"}  # Duplicate email
    mock_collection.insert_one.side_effect = WriteError("Duplicate key error")

    with pytest.raises(WriteError):
        dao.create(duplicate_data)