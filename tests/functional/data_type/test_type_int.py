import os
import pytest
from tests.functional.data_type.base_data_type_macro import BaseDataTypeMacro

seeds__expected_csv = """int_col
12345678
""".lstrip()

models__actual_sql = """
select cast('12345678' as {{ dbt_utils.type_int() }}) as int_col
"""

# previous dbt_utils code, replaced in this PR
macros__legacy_sql = """
{% macro default__type_int() %}
    int
{% endmacro %}

{% macro bigquery__type_int() %}
    int64
{% endmacro %}
"""


class TestTypeFloat(BaseDataTypeMacro):
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


class TestTypeFloatLegacy(TestTypeFloat):
    @pytest.fixture(scope="class")
    def macros(self):
        return {
            "legacy.sql": macros__legacy_sql
        }

    def is_legacy(self):
        return True
