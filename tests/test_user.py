from src.core.models import User
from src.core.errors import UnableToMapRecordError

import pytest


class TestUser:

    def test_successfull_dict_from_tuple_with_user_attributes(self):
        user_record = ("123", "baby shark", "2020-05-22")
        user_attributes = User.dict_from_tuple(user_record)
        assert isinstance(user_attributes, dict)

    def test_fails_dict_from_tuple_with_null_user_attribute(self):
        user_record = ("123", None, "2020-05-22")
        with pytest.raises(UnableToMapRecordError):
            User.dict_from_tuple(user_record)

    def test_fails_dict_from_tuple_with_extra_user_attribute(self):
        user_record = ("123", None, "2020-05-22", "foo")
        with pytest.raises(UnableToMapRecordError):
            User.dict_from_tuple(user_record)

    def test_fail_dict_from_tuple_with_user_attributes_when_missing_element(self):
        user_record = ("123", "baby shark")
        with pytest.raises(UnableToMapRecordError):
            User.dict_from_tuple(user_record)

    def test_fail_dict_from_tuple_with_user_attribute_with_wrong_type(self):
        user_record = ("123", "2020-01-21", "pepepe", "foo")
        with pytest.raises(UnableToMapRecordError):
            User.dict_from_tuple(user_record)
