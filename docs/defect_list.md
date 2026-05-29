# MagicSquare — Defect List (AC-FR-01-01 RED)

| 항목 | 내용 |
|------|------|
| **문서 ID** | DL-MS-FR01-001 |
| **앵커 AC** | AC-FR-01-01 (null·size → INVALID_SIZE, Domain 0회) |
| **관련 테스트** | `tests/boundary/test_RED_AC_FR01_01_null_and_size.py` (8건) |
| **최종 회귀** | 2026-05-29 — `pytest tests/` **15 passed** |
| **상태 범례** | Fixed = GREEN 통과 확인 / Open = 미수정 |

---

## 결함 목록

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 | 상태 |
|----|----------|-------|-----------|--------|--------|-----------|-----------|------|
| DEF-001 | Critical | AC-FR-01-01 | `pytest tests/boundary/test_RED_AC_FR01_01_null_and_size.py -v` 실행 (구현 전) | 8건 테스트 수집·실행 | `ModuleNotFoundError: No module named 'magicsquare.boundary'` (수집 단계 ERROR, 0건 실행) | `src/magicsquare/boundary/` ECB Boundary 패키지 미생성 | `boundary/__init__.py`, `error_schema.py`, `input_validator.py`, `ui_boundary.py` 최소 스켈레톤 추가 | Fixed |
| DEF-002 | Critical | AC-FR-01-01 | `InputValidator.validate(None)` 호출 (None 분기 없을 때) | `FailureResponse`, `code="INVALID_SIZE"`, `message="Grid must be 4x4."` | `TypeError` (`len(None)`) 또는 `AttributeError` (None에 `.error` 접근) | `matrix is None` 선행 분기 누락 — size 검사(`_is_4x4`)로 None 전달 | `if matrix is None: return _invalid_size_failure()` 추가 (`input_validator.py:31-32`) | Fixed |
| DEF-003 | Major | AC-FR-01-01 | `validate([])`, `validate([[]]*4)`, `validate(3×4 grid)` 호출 (size 분기 없을 때) | `INVALID_SIZE` + `"Grid must be 4x4."` | `NotImplementedError` 또는 Domain 진입 | 4×4 행·열 size 검사 미구현 | `_is_4x4()` 및 `if not _is_4x4(matrix): return _invalid_size_failure()` 추가 (`input_validator.py:19-24, 33-34`) | Fixed |
| DEF-004 | Minor | AC-FR-01-01 | `validate(None)` 후 `isinstance(result, FailureResponse)` assert | `FailureResponse` (pydantic), `type=="ERROR"` | `None` 반환 또는 plain dict — 타입 assert 실패 | `FailureResponse` / `ErrorDetail` pydantic 모델 미정의 | `error_schema.py`에 pydantic envelope 정의 | Fixed |
| DEF-005 | Critical | AC-FR-01-01 | `UIBoundary(solver=mock).solve(None)` — mock `resolve` spy | `resolve()` **0회** | `resolve()` 1회 호출 (검증 실패 무시 시) | `validate()` 실패 반환을 early-return하지 않고 `solver.resolve()` 진입 | `validate()`가 `FailureResponse`를 반환하면 즉시 return; 유효 격자만 `NotImplementedError` → `resolve()` (`ui_boundary.py:21-24`) | Fixed |
| DEF-006 | Minor | AC-FR-01-01 | `validate()` 반환 타입 — 테스트 `result.error.code` 직접 접근 | 실패 경로에서 항상 `FailureResponse` | `FailureResponse \| None` — 실패·성공 구분이 호출자 책임 | `validate()` API가 `None`을 성공 sentinel로 사용 | 실패는 `FailureResponse` 반환, 유효 격자는 `NotImplementedError` raise로 Domain 진입 분리 | Fixed |

---

## RED 단계 pytest 실패 로그 (DEF-001, 수집 전)

```
ERROR collecting tests/boundary/test_RED_AC_FR01_01_null_and_size.py
tests\boundary\test_RED_AC_FR01_01_null_and_size.py:13: in <module>
    from magicsquare.boundary.error_schema import FailureResponse
E   ModuleNotFoundError: No module named 'magicsquare.boundary'
=========================== short test summary info ===========================
ERROR tests/boundary/test_RED_AC_FR01_01_null_and_size.py
collected 0 items / 1 error
```

---

## GREEN 회귀 확인 (2026-05-29)

```bash
python -m pytest tests/boundary/test_RED_AC_FR01_01_null_and_size.py -v   # 8 passed
python -m pytest tests/ -v                                                 # 15 passed
python -m pytest tests/boundary/ --cov=src/magicsquare/boundary --cov-report=term-missing  # 93%
```

| 테스트 ID (README) | 대응 결함 | 회귀 |
|--------------------|-----------|------|
| TC-A-01 ~ TC-A-07 | DEF-001 ~ DEF-004 | PASS |
| TC-B-01 ~ TC-B-03 | DEF-005 | PASS |

---

## 미해결 / 후속 관찰 (Open 아님 — 범위 외)

| 항목 | 설명 |
|------|------|
| AC-FR-01-02~05 | 빈칸·값·중복 검증 — 본 RED 커밋 범위 외 (`NotImplementedError` 의도적) |
| Boundary 커버리지 gate 85% | README 목표 대비 측정값 93% — gate 미적용(RED 단계) |
| test_plan E003 vs README INVALID_SIZE | PRD SSOT(E003/E001)와 README RED 체크리스트(INVALID_SIZE) 용어 불일치 — 문서 정합성 이슈(결함 아님) |

---

*본 목록은 AC-FR-01-01 RED→GREEN 사이클에서 관측·수정된 결함만 포함한다. 후속 AC 추가 시 DEF-007부터 번호를 이어간다.*
