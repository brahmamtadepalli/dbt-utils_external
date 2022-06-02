import os
import pytest
from tests.functional.data_type.base_data_type_macro import BaseDataTypeMacro

seeds__expected_csv = """timestamp_col
2021-01-01 01:01:01
""".lstrip()

# need to explicitly cast this to avoid it being a DATETIME on BigQuery
# (but - should it actually be a DATETIME, for consistency with other dbs?)
seeds__expected_yml = """
version: 2
seeds:
  - name: expected
    config:
      column_types:
        timestamp_col: timestamp
"""

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
            "expected.csv": seeds__expected_csv,
            "expected.yml": seeds__expected_yml,
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

    # perform a slightly more lenient comparison, xfail if subtly different
    def is_legacy(self):
        return True

