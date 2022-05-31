import os
import pytest
from tests.functional.data_type.base_data_type_macro import BaseDataTypeMacro

seeds__expected_csv = """timestamp_col
2021-01-01 01:01:01
""".lstrip()

models__actual_sql = """
select cast('2021-01-01 01:01:01' as {{ dbt_utils.type_timestamp() }}) as timestamp_col
"""

# previous dbt_utils code, replaced in this PR
macros__legacy_sql = """
{% macro default__type_timestamp() %}
    timestamp
{% endmacro %}

{% macro postgres__type_timestamp() %}
    timestamp without time zone
{% endmacro %}

{% macro snowflake__type_timestamp() %}
    timestamp_ntz
{% endmacro %}
"""


class TestTypeTimestamp(BaseDataTypeMacro):
    @pytest.fixture(scope="class")
    def seeds(self):
        return {
            "expected.csv": seeds__expected_csv
        }
    
    @pytest.fixture(scope="class")
    def models(self):
        return {
            "actual.sql": models__actual_sql
        }


class TestTypeTimestampLegacy(TestTypeTimestamp):
    @pytest.fixture(scope="class")
    def macros(self):
        return {
            "legacy.sql": macros__legacy_sql
        }

    def is_legacy(self):
        return True

