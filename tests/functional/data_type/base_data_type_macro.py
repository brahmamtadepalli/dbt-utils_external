import os
import pytest
from dbt.tests.util import run_dbt, check_relations_equal, get_relation_columns

class BaseDataTypeMacro:
    @pytest.fixture(scope="class")
    def packages(self):
        return {"packages": [{"local": os.getcwd()}]}

    def is_legacy(self):
        return False

    def test_check_types_assert_match(self, project):
        run_dbt(['deps'])
        run_dbt(['build'])
        
        # check contents equal
        check_relations_equal(project.adapter, ["expected", "actual"])
        
        # check types equal
        expected_cols = get_relation_columns(project.adapter, "expected")
        actual_cols = get_relation_columns(project.adapter, "actual")
        print(f"Expected: {expected_cols}")
        print(f"Actual: {actual_cols}")
        
        
        if not self.is_legacy():
            assert expected_cols == actual_cols, f"Type difference detected: {expected_cols} vs. {actual_cols}"
        # we need to be a little more lenient when mapping between 'legacy' and 'new' types that are equivalent
        # e.g. 'character varying' and 'text'
        elif expected_cols == actual_cols:
            # cool, no need for jank
            pass
        else:
            # this is pretty janky
            for i in range(0, len(expected_cols)):
                expected = project.adapter.Column(*expected_cols[i])
                actual = project.adapter.Column(*actual_cols[i])
                print(f"Subtle type difference detected: {expected.data_type} vs. {actual.data_type}")
                if any((
                    expected.is_string() and actual.is_string(),
                    expected.is_float() and actual.is_float(),
                    expected.is_integer() and actual.is_integer(),
                    expected.is_numeric() and actual.is_numeric(),
                )):
                    pytest.xfail()
                else:
                    pytest.fail()
