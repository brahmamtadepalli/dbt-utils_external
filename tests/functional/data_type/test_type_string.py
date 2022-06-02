import os
import pytest
from tests.functional.data_type.base_data_type_macro import BaseDataTypeMacro

seeds__expected_csv = """string_col
"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
""".lstrip()

models__actual_sql = """
select cast('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.' as {{ dbt_utils.type_string() }}) as string_col
"""

# previous dbt_utils code, replaced in this PR
macros__legacy_sql = """
{% macro default__type_string() %}
    string
{% endmacro %}

{%- macro redshift__type_string() -%}
    varchar
{%- endmacro -%}

{% macro postgres__type_string() %}
    varchar
{% endmacro %}

{% macro snowflake__type_string() %}
    varchar
{% endmacro %}
"""


class BaseTypeString(BaseDataTypeMacro):
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


class TestTypeString(BaseTypeString):
    pass


class BaseTypeStringLegacy(TestTypeString):
    @pytest.fixture(scope="class")
    def macros(self):
        return {
            "legacy.sql": macros__legacy_sql
        }

    # perform a slightly more lenient comparison, xfail if subtly different
    def is_legacy(self):
        return True


class TestTypeStringLegacy(BaseTypeStringLegacy):
    pass
