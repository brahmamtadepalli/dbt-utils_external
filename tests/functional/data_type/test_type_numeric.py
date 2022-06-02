import os
import pytest
from tests.functional.data_type.base_data_type_macro import BaseDataTypeMacro

seeds__expected_csv = """numeric_col
1.2345
""".lstrip()

# need to explicitly cast this to avoid it being a double/float
seeds__expected_yml = """
version: 2
seeds:
  - name: expected
    config:
      column_types:
        numeric_col: {}
"""

models__actual_sql = """
select cast('1.2345' as {{ dbt_utils.type_numeric() }}) as numeric_col
"""

# previous dbt_utils code, replaced in this PR
macros__legacy_sql = """
{% macro default__type_numeric() %}
    numeric(28, 6)
{% endmacro %}

{% macro bigquery__type_numeric() %}
    numeric
{% endmacro %}
"""


class BaseTypeNumeric(BaseDataTypeMacro):
    def numeric_fixture_type(self):
        return "numeric(5,4)"
    
    @pytest.fixture(scope="class")
    def seeds(self):
        return {
            "expected.csv": seeds__expected_csv,
            "expected.yml": seeds__expected_yml.format(self.numeric_fixture_type())
        }
    
    @pytest.fixture(scope="class")
    def models(self):
        return {
            "actual.sql": models__actual_sql
        }


@pytest.mark.skip_profile('bigquery')
class TestTypeNumeric(BaseTypeNumeric):
    pass


class BaseTypeNumericLegacy(TestTypeNumeric):
    @pytest.fixture(scope="class")
    def macros(self):
        return {
            "legacy.sql": macros__legacy_sql
        }

    # perform a slightly more lenient comparison, xfail if subtly different
    def is_legacy(self):
        return True


@pytest.mark.skip_profile('bigquery')
class TestTypeNumericLegacy(BaseTypeNumericLegacy):
    pass


@pytest.mark.only_profile('bigquery')
class TestBigQueryTypeNumeric(BaseTypeNumeric):
    def numeric_fixture_type(self):
        return "numeric"


@pytest.mark.only_profile('bigquery')
class TestBigQueryTypeNumericLegacy(BaseTypeNumericLegacy):
    def numeric_fixture_type(self):
        return "numeric"
