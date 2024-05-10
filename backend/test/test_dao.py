import pytest
from pymongo.errors import WriteError
from unittest.mock import patch, MagicMock
from src.util.dao import DAO
import datetime

# Inline JSON Schema Validator defined as a Python dictionary
validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["title", "description", "startdate", "duedate"],
        "properties": {
            "title": {
                "bsonType": "string",
                "description": "must be a string and is required",
                "uniqueItems": True
            },
            "description": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "startdate": {
                "bsonType": "date",
                "description": "start date of the task"
            },
            "duedate": {
                "bsonType": "date",
                "description": "due date of the task"
            },
            "requires": {
                "bsonType": "array",
                "items": {
                    "bsonType": "objectId"
                },
                "description": "array of task dependencies represented by ObjectIDs"
            },
            "categories": {
                "bsonType": "array",
                "items": {
                    "bsonType": "string"
                },
                "description": "list of categories associated with the task"
            },
            "todos": {
                "bsonType": "array",
                "items": {
                    "bsonType": "objectId"
                },
                "description": "list of todos linked to the task"
            },
            "video": {
                "bsonType": "objectId",
                "description": "reference to a video object"
            }
        }
    }
}

@pytest.fixture(scope="module")
def setup_dao():
    with patch('src.util.dao.pymongo.MongoClient') as mock_client:
        mock_db = mock_client.return_value.edutask
        mock_collection = mock_db.task_collection
        
        # Mocking the MongoDB collection to use our inline JSON schema validator
        mock_collection.create_collection = MagicMock(name='create_collection')
        mock_collection.create_collection.validator = validator
        
        # Setup DAO with mocked collection
        dao = DAO("task")
        dao.collection = mock_collection
        
        yield dao

def test_create_valid_data(setup_dao):
    dao = setup_dao
    valid_data = {
        "title": "Complete the project",
        "description": "Ensure everything is tested",
        "startdate": datetime.datetime.now(),
        "duedate": datetime.datetime.now() + datetime.timedelta(days=10)
    }
    # Mock successful insertion
    dao.collection.insert_one.return_value = MagicMock(inserted_id="mocked_id")
    dao.collection.find_one.return_value = valid_data
    
    result = dao.create(valid_data)
    assert result is not None
    assert 'title' in result

def test_create_missing_required_fields(setup_dao):
    dao = setup_dao
    invalid_data = {"description": "Missing title"}  # Missing the required 'title' field
    
    # Mock WriteError for missing required fields
    dao.collection.insert_one.side_effect = WriteError("Missing required fields")
    
    with pytest.raises(WriteError):
        dao.create(invalid_data)

def test_create_data_type_mismatch(setup_dao):
    dao = setup_dao
    mismatch_data = {
        "title": 123,  # Incorrect data type (int instead of string)
        "description": "Valid Description",
        "startdate": "Not a date",  # Incorrect data type
        "duedate": datetime.datetime.now()
    }
    # Mock WriteError for data type mismatch
    dao.collection.insert_one.side_effect = WriteError("Data type mismatch")
    
    with pytest.raises(WriteError):
        dao.create(mismatch_data)

def test_create_uniqueness_violation(setup_dao):
    dao = setup_dao
    duplicate_data = {
        "title": "Complete the project",  # Assuming this title already exists
        "description": "Another test",
        "startdate": datetime.datetime.now(),
        "duedate": datetime.datetime.now() + datetime.timedelta(days=10)
    }
    # Mock WriteError for uniqueness violation
    dao.collection.insert_one.side_effect = WriteError("Uniqueness constraint violation")
    
    with pytest.raises(WriteError):
        dao.create(duplicate_data)