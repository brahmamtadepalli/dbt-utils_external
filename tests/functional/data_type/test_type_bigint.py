import os
import pytest
from tests.functional.data_type.base_data_type_macro import BaseDataTypeMacro

models__expected_sql = """
select 9223372036854775800 as bigint_col
""".lstrip()

models__actual_sql = """
select cast('9223372036854775800' as {{ dbt_utils.type_bigint() }}) as bigint_col
"""

# previous dbt_utils code, replaced in this PR
macros__legacy_sql = """
{% macro default__type_bigint() %}
    bigint
{% endmacro %}

{% macro bigquery__type_bigint() %}
    int64
{% endmacro %}
"""


class BaseTypeBigInt(BaseDataTypeMacro):
    @pytest.fixture(scope="class")
    def models(self):
        return {
            "expected.sql": models__expected_sql,
            "actual.sql": models__actual_sql
        }


class TestTypeBigInt(BaseTypeBigInt):
    pass


class BaseTypeBigIntLegacy(TestTypeBigInt):
    @pytest.fixture(scope="class")
    def macros(self):
        return {
            "legacy.sql": macros__legacy_sql
        }

    # perform a slightly more lenient comparison, xfail if subtly different
    def is_legacy(self):
        return True


class TestTypeBigIntLegacy(BaseTypeBigIntLegacy):
    pass
