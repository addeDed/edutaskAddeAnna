import pytest
from pymongo.errors import WriteError
from unittest.mock import patch, MagicMock
import datetime
# Corrected import path for the DAO class
from src.util.dao import DAO

# Setup for all tests, ensuring each collection and its validator is correctly mocked
@pytest.fixture(scope="module")
def setup_dao():
    with patch('src.util.dao.pymongo.MongoClient') as mock_client:
        mock_db = mock_client.return_value.edutask
        collections = {
            'task': mock_db.task_collection,
            'todo': mock_db.todo_collection,
            'video': mock_db.video_collection
        }

        daos = {}
        for name, collection in collections.items():
            dao = DAO(name)
            dao.collection = collection
            daos[name] = (dao, collection)
        
        yield daos

# Task Collection Tests
def test_task_valid_data(setup_dao):
    dao, mock_collection = setup_dao['task']
    valid_data = {"title": "Task 1", "description": "Complete this task", "startdate": "2023-01-01", "duedate": "2023-01-15"}
    fake_id = "fake_id"
    mock_collection.insert_one.return_value = MagicMock(inserted_id=fake_id)
    mock_collection.find_one.return_value = valid_data.copy()
    mock_collection.find_one.return_value["_id"] = fake_id

    result = dao.create(valid_data)

    assert "_id" in result
    assert result["_id"] == fake_id
    mock_collection.insert_one.assert_called_once_with(valid_data)
    mock_collection.find_one.assert_called_once_with({'_id': fake_id})

def test_task_missing_required_fields(setup_dao):
    dao, mock_collection = setup_dao['task']
    incomplete_data = {"description": "Incomplete task"}
    mock_collection.insert_one.side_effect = WriteError("Missing required field: title")

    with pytest.raises(WriteError):
        dao.create(incomplete_data)

# Todo Collection Tests - Focused on schema-defined constraints
def test_todo_valid_data(setup_dao):
    dao, mock_collection = setup_dao['todo']
    valid_data = {"description": "Finish assignment", "done": True}
    fake_id = "fake_id"
    mock_collection.insert_one.return_value = MagicMock(inserted_id=fake_id)
    mock_collection.find_one.return_value = valid_data.copy()
    mock_collection.find_one.return_value["_id"] = fake_id

    result = dao.create(valid_data)

    assert "_id" in result
    assert result["_id"] == fake_id
    mock_collection.insert_one.assert_called_once_with(valid_data)

def test_todo_incorrect_data_type(setup_dao):
    dao, mock_collection = setup_dao['todo']
    invalid_data = {"description": 123, "done": "Yes"}
    mock_collection.insert_one.side_effect = WriteError("Data type mismatch for 'done'")

    with pytest.raises(WriteError):
        dao.create(invalid_data)

# Video Collection Tests - Corrected for schema compliance
def test_video_valid_data(setup_dao):
    dao, mock_collection = setup_dao['video']
    valid_data = {"url": "http://example.com/video.mp4"}
    fake_id = "fake_id"
    mock_collection.insert_one.return_value = MagicMock(inserted_id=fake_id)
    mock_collection.find_one.return_value = valid_data.copy()
    mock_collection.find_one.return_value["_id"] = fake_id

    result = dao.create(valid_data)

    assert "_id" in result
    assert result["_id"] == fake_id
    mock_collection.insert_one.assert_called_once_with(valid_data)

def test_video_empty_url(setup_dao):
    dao, mock_collection = setup_dao['video']
    empty_url_data = {"url": ""}
    mock_collection.insert_one.side_effect = WriteError("URL cannot be empty")
    
    with pytest.raises(WriteError):
        dao.create(empty_url_data)



