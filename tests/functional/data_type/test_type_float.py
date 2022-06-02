import os
import pytest
from tests.functional.data_type.base_data_type_macro import BaseDataTypeMacro

seeds__expected_csv = """float_col
1.2345
""".lstrip()

models__actual_sql = """
select cast('1.2345' as {{ dbt_utils.type_float() }}) as float_col
"""

# previous dbt_utils code, replaced in this PR
macros__legacy_sql = """
{% macro default__type_float() %}
    float
{% endmacro %}

{% macro bigquery__type_float() %}
    float64
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

    # perform a slightly more lenient comparison, xfail if subtly different
    def is_legacy(self):
        return True
