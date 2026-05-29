"""GM-2 Golden Master regression — Magic Square Solver (approve pattern).

[TAG][GoldenMaster]

Run: ``pytest -m golden_master -v``
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from magicsquare.boundary.error_mapper import E006_CODE
from magicsquare.boundary.error_schema import FailureResponse, SuccessResponse
from magicsquare.boundary.input_validator import E002_CODE, E005_CODE
from magicsquare.boundary.ui_boundary import UIBoundary
from magicsquare.control.solve_partial_magic_square import SolvePartialMagicSquare
from tests.golden_master.approve import (
    DEFAULT_EXPECTED_PATH,
    approve_golden_master,
    approve_section,
    read_expected_file,
)
from tests.golden_master.capture import (
    ERROR_SEMANTIC_BY_CODE,
    capture_all_sections,
    capture_section,
)
from tests.golden_master.contracts import (
    assert_failure_error_contract,
    assert_int_six_format,
    assert_reverse_fallback_combination,
    assert_row_major_and_one_index,
    assert_small_first_combination,
    assert_step_a_fails_step_b_succeeds,
)
from tests.golden_master.parse import parse_sections
from tests.golden_master.scenarios import (
    GoldenScenario,
    GOLDEN_SCENARIOS,
    SCENARIO_BY_TEST_CASE,
)

pytestmark = pytest.mark.golden_master


def _approve_update_requested() -> bool:
    """True when pytest --update-golden or GOLDEN_MASTER_APPROVE=1."""
    return os.environ.get("GOLDEN_MASTER_APPROVE", "").strip() in {
        "1",
        "true",
        "yes",
    }


@pytest.fixture(scope="module")
def ui_boundary() -> UIBoundary:
    """Shared UIBoundary for API result serialization captures."""
    return UIBoundary(solver=SolvePartialMagicSquare())


@pytest.fixture(scope="module")
def golden_master_expected_path() -> Path:
    """Path to version-controlled baseline file."""
    return DEFAULT_EXPECTED_PATH


@pytest.fixture(scope="module")
def golden_master_update(pytestconfig: pytest.Config) -> bool:
    """Whether to regenerate golden_master_expected.txt."""
    return bool(pytestconfig.getoption("--update-golden")) or _approve_update_requested()


@pytest.fixture(scope="module")
def expected_sections(
    golden_master_expected_path: Path,
    golden_master_update: bool,
) -> dict[str, str]:
    """Parsed baseline sections; auto-create file when missing."""
    if golden_master_update or not golden_master_expected_path.is_file():
        approve_golden_master(
            capture_all_sections(),
            golden_master_expected_path,
            update=True,
        )
    document = read_expected_file(golden_master_expected_path)
    return parse_sections(document)


def _serialize_api_result(
    boundary: UIBoundary,
    scenario: GoldenScenario,
) -> tuple[str, SuccessResponse | FailureResponse]:
    """Capture golden block and raw UIBoundary.solve DTO."""
    block = capture_section(boundary, scenario)
    result = boundary.solve(scenario.grid)
    return block, result


class TestGoldenMasterMagicSquareAggregate:
    """Full-file approve (GM-1 compatibility within GM-2 suite)."""

    def test_gm2_all_sections_file_compare(
        self,
        golden_master_expected_path: Path,
        golden_master_update: bool,
    ) -> None:
        """Given all scenarios — When capture — Then open(expected).read() equals actual."""
        # [TAG][GoldenMaster] aggregate
        # Given
        actual = capture_all_sections()

        # When / Then
        action = approve_golden_master(
            actual,
            golden_master_expected_path,
            update=golden_master_update,
        )
        assert action in {"matched", "created", "updated"}


@pytest.mark.parametrize(
    "test_case_id",
    [scenario.test_case_id for scenario in GOLDEN_SCENARIOS],
    ids=[scenario.test_case_id for scenario in GOLDEN_SCENARIOS],
)
class TestGoldenMasterMagicSquareCases:
    """GM-TC-01..05 — per-scenario approve and contract checks."""

    def test_golden_master_section_matches_expected(
        self,
        test_case_id: str,
        ui_boundary: UIBoundary,
        expected_sections: dict[str, str],
        golden_master_update: bool,
        golden_master_expected_path: Path,
    ) -> None:
        """Given TC grid — When API serialize — Then section block matches expected file."""
        # [TAG][GoldenMaster]
        scenario = SCENARIO_BY_TEST_CASE[test_case_id]

        # Given
        if golden_master_update:
            approve_golden_master(
                capture_all_sections(),
                golden_master_expected_path,
                update=True,
            )
            expected_sections = parse_sections(
                read_expected_file(golden_master_expected_path)
            )

        # When
        actual, _result = _serialize_api_result(ui_boundary, scenario)

        # Then
        expected_block = expected_sections[scenario.section_id]
        approve_section(
            actual,
            expected_block,
            context=f"{test_case_id} [{scenario.section_id}]",
        )

    def test_golden_master_domain_contracts(
        self,
        test_case_id: str,
        ui_boundary: UIBoundary,
    ) -> None:
        """Given TC grid — When solve — Then int[6] / row-major / Step rules / Error contract."""
        # [TAG][GoldenMaster]
        scenario = SCENARIO_BY_TEST_CASE[test_case_id]

        # When
        _block, result = _serialize_api_result(ui_boundary, scenario)

        # Then
        if test_case_id == "GM-TC-01":
            assert isinstance(result, SuccessResponse)
            data = result.data
            assert_int_six_format(data)
            assert_row_major_and_one_index(scenario.grid, data)
            assert_step_a_fails_step_b_succeeds(scenario.grid)
            assert_reverse_fallback_combination(scenario.grid, data)
            return

        if test_case_id == "GM-TC-02":
            assert isinstance(result, SuccessResponse)
            data = result.data
            assert_int_six_format(data)
            assert_row_major_and_one_index(scenario.grid, data)
            assert_step_a_fails_step_b_succeeds(scenario.grid)
            assert_reverse_fallback_combination(scenario.grid, data)
            return

        if test_case_id in {"GM-TC-03", "GM-TC-04", "GM-TC-05"}:
            assert isinstance(result, FailureResponse)
            assert scenario.expected_error is not None
            assert_failure_error_contract(
                result,
                expected_semantic=scenario.expected_error,
            )
            semantic = ERROR_SEMANTIC_BY_CODE.get(result.error.code, result.error.code)
            assert semantic == scenario.expected_error
            if test_case_id == "GM-TC-03":
                assert result.error.code == E002_CODE
            elif test_case_id == "GM-TC-04":
                assert result.error.code == E005_CODE
            else:
                assert result.error.code == E006_CODE
            return

        pytest.fail(f"Unhandled test case: {test_case_id}")


class TestGoldenMasterMagicSquareStepAOracle:
    """GM-TC-01 auxiliary — Step A (small-first) placement oracle on G2."""

    @pytest.mark.golden_master
    def test_gm_tc_01_small_first_combination_rule_on_step_a_grid(
        self,
        ui_boundary: UIBoundary,
    ) -> None:
        """Given G2 — When Step A layout applied — Then small-first numbers at blanks."""
        # GM-TC-01 small-first rule (Step A attempt semantics)
        scenario = SCENARIO_BY_TEST_CASE["GM-TC-01"]

        # Given
        grid = scenario.grid

        # When — derive Step A tuple via domain missing pair + blank coords
        from magicsquare.entity.services.empty_cell_locator import find_blank_coords
        from magicsquare.entity.services.missing_number_finder import find_not_exist_nums

        first, second = find_blank_coords(grid)
        smaller, larger = find_not_exist_nums(grid)
        step_a = [first.row, first.col, smaller, second.row, second.col, larger]

        # Then
        assert_small_first_combination(grid, step_a)
        result = ui_boundary.solve(grid)
        assert isinstance(result, SuccessResponse)
        assert result.data != step_a
