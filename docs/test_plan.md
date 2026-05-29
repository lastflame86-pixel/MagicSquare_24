# MagicSquare — Test Plan (FR-01 Input Verification)

| 항목 | 내용 |
|------|------|
| **문서 ID** | TP-MS-FR01-001 |
| **앵커 AC** | AC-FR01-01 (`matrix == null` → E003, Domain 0회) |
| **PRD 참조** | FR-01, §12.1, §12.3, §13.1, §15, §16.2 ES-03, NFR-01~03 |
| **대상 스택** | Python 3.11+, pytest, pydantic, unittest.mock |
| **Track** | Track A — Boundary / UI Contract |
| **상태** | 구현 전 RED 기준 |

---

## 1. 목적 및 범위

본 계획서는 **FR-01 Input Verification (Boundary)** 의 선행 AC인 **AC-FR01-01**을 앵커로, 입력 유효성 검사(null·size) 및 **Domain 진입점(`SolvePartialMagicSquare.execute`) 호출 격리**를 pytest 단위 테스트로 검증하는 범위·우선순위·측정 전략을 정의한다.

### 1.1 In-Scope

| 구분 | 대상 |
|------|------|
| **컴포넌트** | `InputValidator`, `UIBoundary`, `ErrorMapper`, pydantic Failure schema |
| **AC** | AC-FR01-01 (null), AC-FR01-02 (행 수 불일치), AC-FR01-03 (열 수 불일치), AC-FR01-08 (null 선행·Domain 0회) |
| **Error Code** | E003 (null), E001 (size ≠ 4×4) |
| **Test ID** | U-IN-01, U-IN-02, U-IN-03, U-FLOW-02 |

### 1.2 Out-of-Scope (본 계획서)

| 항목 | 사유 |
|------|------|
| **4×4 정상 입력 (G1 등)** | AC-FR01-07 영역; U-FLOW-01·IT-01에서 별도 검증 |
| E002~E005 (빈칸·값·중복) | AC-FR01-04~06; 후속 테스트 계획 |
| Track B Domain 로직 | D-VAL-*, D-LOC-*, D-SOL-* 별도 계획 |
| Integration (IT-E01 등) | Boundary 단위 GREEN 후 확장 |

### 1.3 용어 정리 (PRD SSOT)

| 프롬프트/레거시 표현 | PRD Error Code | PRD Message |
|---------------------|----------------|-------------|
| `grid=None` | **E003** | `INVALID_MATRIX_NULL: matrix must not be null` |
| `INVALID_SIZE` (크기 위반) | **E001** | `INVALID_MATRIX_SIZE: expected 4x4` |

> AC-FR01-01 앵커는 **null → E003**이다. 크기 불일치(3×4, 4×3, 5×5, `[]`, `[[]]*4`)는 **E001**이다.

---

## 2. pytest 단위 테스트 범위 및 우선순위

### 2.1 테스트 레이아웃

```
tests/
├── boundary/
│   ├── test_input_validator.py    # U-IN-01~03
│   ├── test_ui_boundary.py          # U-FLOW-02
│   └── test_error_schema.py         # pydantic Failure envelope
└── conftest.py                      # 공통 fixture, G1/G2 제외 (본 계획)
```

### 2.2 우선순위 매트릭스

| 우선순위 | Test ID | 파일 | 검증 대상 | AC | RED 순서 |
|----------|---------|------|-----------|-----|----------|
| **P0** | U-IN-01 | `test_input_validator.py` | `matrix=None` → E003, message exact | AC-FR01-01 | 1 |
| **P0** | U-FLOW-02 | `test_ui_boundary.py` | invalid 입력 → `execute` **0회** | AC-FR01-01, AC-FR01-08, BR-05 | 2 |
| **P1** | U-IN-02 | `test_input_validator.py` | 3×4, 5×5 → E001 | AC-FR01-02 | 3 |
| **P1** | U-IN-03 | `test_input_validator.py` | 4×3, `[[]]*4`, `[]` → E001 | AC-FR01-03 | 4 |
| **P2** | schema | `test_error_schema.py` | Failure envelope pydantic 직렬화 | BR-20, UX-05 | 5 |

### 2.3 RED → GREEN → REFACTOR 흐름

```
1. U-IN-01  (null → E003)           ← AC-FR01-01 앵커 RED
2. U-FLOW-02 (execute 0회)          ← Domain 격리 RED
3. U-IN-02~03 (size → E001)         ← 경계값 확장 RED
4. GREEN: InputValidator 최소 구현
5. GREEN: UIBoundary early-return
6. REFACTOR: 검증 순서 일원화 (계약·message 불변)
```

### 2.4 AAA 패턴 (pytest)

각 테스트 함수는 **Arrange → Act → Assert** 3구역으로 분리한다.

- **Arrange:** 입력 `matrix`, mock `execute` 주입
- **Act:** `InputValidator.validate(matrix)` 또는 `UIBoundary.solve(matrix)` 호출
- **Assert:** `result.type`, `result.error.code`, `result.error.message`, `mock_execute.call_count`

---

## 3. 경계값 케이스 목록

검증 순서: **null → size → empty count → value range → duplicate** (FR-01 Rule 6)

| ID | 입력 (`matrix`) | 기대 Code | 기대 Message | Domain 호출 | AC | Test ID |
|----|-----------------|-----------|--------------|-------------|-----|---------|
| **BV-01** | `None` (명시적 None) | E003 | `INVALID_MATRIX_NULL: matrix must not be null` | **0회** | AC-FR01-01 | U-IN-01 |
| **BV-02** | `[]` (빈 리스트, 행 0개) | E001 | `INVALID_MATRIX_SIZE: expected 4x4` | **0회** | AC-FR01-02 | U-IN-02 |
| **BV-03** | `[[]] * 4` (행 4개, 열 0개) | E001 | `INVALID_MATRIX_SIZE: expected 4x4` | **0회** | AC-FR01-03 | U-IN-03 |
| **BV-04** | 3×4 (행 3, 열 4) | E001 | `INVALID_MATRIX_SIZE: expected 4x4` | **0회** | AC-FR01-02 | U-IN-02 |
| **BV-05** | 4×3 (행 4, 1행 length=3) | E001 | `INVALID_MATRIX_SIZE: expected 4x4` | **0회** | AC-FR01-03 | U-IN-03 |
| **BV-06** | 5×5 (행 5, 열 5) | E001 | `INVALID_MATRIX_SIZE: expected 4x4` | **0회** | AC-FR01-02 | U-IN-02 |
| ~~BV-07~~ | ~~4×4 정상 (G1)~~ | — | **본 계획 범위 외** | — | AC-FR01-07 | U-FLOW-01 |

### 3.1 BV-03 `[[]] * 4` 주의사항

Python에서 `[[]] * 4`는 4개 행이 **동일 inner list 객체**를 공유한다. size 검증 단계에서는 `len(row) != 4`이므로 E001이 반환되어야 하며, Domain 진입 전에 차단된다. 본 AC 범위에서는 mutation 부수효과 검증은 **Out-of-Scope** (NFR-05는 Solver/Validator 원본 불변; size 실패 경로는 copy 미발생).

### 3.2 null vs size 선행 검증 (AC-FR01-08)

| ID | 입력 | 기대 | 검증 포인트 |
|----|------|------|-------------|
| BV-08 | `None` | E003 (**E001 아님**) | null 분기에서 size 검사 **미진입** |
| BV-09 | `[]` | E001 (**E003 아님**) | null 통과 후 size 검사 **진입** |

---

## 4. 예외 / 특이 케이스 목록

| ID | 시나리오 | 입력 / 조건 | 기대 동작 | Test ID |
|----|----------|-------------|-----------|---------|
| **EX-01** | 명시적 `None` | `UIBoundary.solve(None)` | E003, `execute` 0회 | U-IN-01, U-FLOW-02 |
| **EX-02** | 암시적 falsy 혼동 방지 | `None` only (not `[]`) | `[]`는 E001; `None`만 E003 | U-IN-01, U-IN-02 |
| **EX-03** | 부분 행만 존재 | `[[1,2,3,4], [1,2,3]]` (2행, 2행째 length=3) | E001 at row index 1 | U-IN-03 |
| **EX-04** | 행 수만 초과 | `[[0]*4]*5` | E001 (len(matrix)=5) | U-IN-02 |
| **EX-05** | pydantic 직렬화 | E003/E001 `ErrorResponse` | `type=="ERROR"`, `error` 필드만; `data` **부재** | schema test |
| **EX-06** | Success/Failure 혼재 금지 | E003 응답 | `data` 키 **없음** (UX-05) | U-IN-01 |
| **EX-07** | message 불변 | E001, E003 | 대소문자·구두점 **완전 일치** (RG-01, §13.3) | U-IN-* |
| **EX-08** | Domain 예외 미발생 | 모든 BV-01~06 | `UnsolvableDomainError` 등 Domain 예외 **raise 금지** | U-FLOW-02 |
| **EX-09** | Control Mock 주입 | `UIBoundary(solver=mock)` | invalid 시 mock **0회**; valid 시 1회 (본 계획은 0회만) | U-FLOW-02 |
| **EX-10** | 이중 호출 결정성 | `validate(None)` 2회 | 동일 E003 응답 (BR-17) | U-IN-01 |

---

## 5. Domain 해결 진입점 호출 횟수 검증 전략

### 5.1 진입점 정의

| 항목 | 값 |
|------|-----|
| **Domain resolver** | `SolvePartialMagicSquare.execute(grid: Grid)` |
| **호출 주체** | `UIBoundary.solve(matrix)` → validate 통과 시 Control 경유 1회 |
| **BR-05** | Boundary 입력 검증 실패 시 **0회** |

### 5.2 Mock / Spy 전략

Track A에서는 Control/Entity **Mock 허용** (PRD §15.1).

#### 패턴 A — `unittest.mock.Mock` (권장)

```python
from unittest.mock import Mock

# Arrange
mock_execute = Mock(return_value=...)
boundary = UIBoundary(solver=Mock(execute=mock_execute))

# Act
result = boundary.solve(None)

# Assert
mock_execute.assert_not_called()
assert result.type == "ERROR"
assert result.error.code == "E003"
```

#### 패턴 B — `Mock(spec=SolvePartialMagicSquare)`

spec을 지정하여 실제 resolver API 이외 호출을 차단한다. REFACTOR 단계에서 인터페이스 drift를 조기 탐지한다.

#### 패턴 C — `wraps` Spy (Integration 전환용)

단위 테스트(P0)에서는 **Mock**을 사용한다. Integration(IT-E01)에서는 spy(`wraps=real_execute`)로 E2E 경로에서 0/1회를 재확인한다.

### 5.3 검증 매트릭스

| 입력 유형 | `execute.call_count` | 검증 Test ID |
|-----------|---------------------|--------------|
| BV-01~06 (null·size 위반) | **0** | U-FLOW-02 |
| 4×4 valid G1 (범위 외) | **1** | U-FLOW-01 (별도 계획) |

### 5.4 실패 시나리오 (Defect Pattern)

| Defect | 증상 | 기대 수정 |
|--------|------|-----------|
| Domain 조기 호출 | `None` 입력인데 `execute` 1회 | validate 실패 시 **즉시 return** |
| None 분기 누락 | `AttributeError` on None | `if matrix is None:` 선행 분기 |
| size 검사 전 Domain 호출 | 3×4에서 execute 1회 | 검증 순서 null → size 준수 |

---

## 6. 커버리지 목표

PRD §14 NFR 기준.

| 계층 | 목표 | 측정 대상 | 본 계획 기여 |
|------|------|-----------|--------------|
| **Domain Logic** | **≥ 95%** line | `src/magicsquare/entity/`, Control solver | **0%** (본 계획 Track A only) |
| **Boundary Validation** | **≥ 85%** line | `src/magicsquare/boundary/` | AC-FR01-01~03만으로 **부분 달성**; AC-FR01-04~06 추가 필요 |
| **전역** | **≥ 80%** | `src/` 전체 | REFACTOR gate |

> AC-FR01-01~03만으로 Boundary 85% 전체 달성은 불가능하다. 후속 AC-FR01-04~06 (U-IN-04~08) 및 U-OUT-*로 보완한다.

### 6.1 본 계획 최소 커버리지 파일

| 파일 (예상) | 커버 대상 분기 |
|-------------|----------------|
| `boundary/input_validator.py` | null, row count, col count |
| `boundary/ui_boundary.py` | early return, solver 미호출 |
| `boundary/error_schema.py` | E001, E003 Failure model |
| `boundary/error_mapper.py` | (본 AC 범위: 미사용, 0%) |

---

## 7. pytest-cov 측정 전략

### 7.1 설치

```bash
pip install pytest-cov
```

### 7.2 실행 명령 (전역)

```bash
pytest --cov=src --cov-report=term-missing
```

### 7.3 Track A 분리 측정 (Boundary only)

```bash
pytest tests/boundary/ \
  --cov=src/magicsquare/boundary \
  --cov-report=term-missing \
  --cov-fail-under=85
```

> 초기 RED 단계(구현 전)에는 `--cov-fail-under` 생략. GREEN 완료 후 gate 적용.

### 7.4 Track B 분리 측정 (Domain only — 참고)

```bash
pytest tests/unit/entity/ \
  --cov=src/magicsquare/entity \
  --cov-report=term-missing \
  --cov-fail-under=95
```

### 7.5 측정 주기

| 단계 | 명령 | Gate |
|------|------|------|
| RED 확인 | `pytest tests/boundary/test_input_validator.py -v` | 실패 확인 (미구현) |
| GREEN (U-IN-01) | `pytest tests/boundary/ --cov=src/magicsquare/boundary --cov-report=term-missing` | E003 pass |
| GREEN (전체 FR-01 null·size) | 동일 + `--cov-fail-under=85` | BV-01~06 pass |
| REFACTOR | 전체 `pytest --cov=src --cov-report=term-missing` | global ≥ 80% |

### 7.6 term-missing 해석

`term-missing` 출력에서 **Miss** 컬럼으로 미커버 라인을 확인한다. FR-01 null·size RED 완료 후에도 Miss에 `empty count`, `value range`, `duplicate` 분기가 남는 것은 **정상** (AC-FR01-04~06 미구현).

---

## 8. 추적성 (Traceability)

| AC ID | Business Rule | 경계값 ID | Test ID |
|-------|---------------|-----------|---------|
| AC-FR01-01 | BR-05 | BV-01 | U-IN-01, U-FLOW-02 |
| AC-FR01-02 | BR-01 | BV-02, BV-04, BV-06 | U-IN-02 |
| AC-FR01-03 | BR-01 | BV-03, BV-05 | U-IN-03 |
| AC-FR01-08 | BR-05 | BV-08, BV-09 | U-FLOW-02 |

---

## 9. Canonical Failure 응답 (Assert 기준)

### E003 — null (AC-FR01-01)

```json
{
  "type": "ERROR",
  "error": {
    "code": "E003",
    "message": "INVALID_MATRIX_NULL: matrix must not be null"
  }
}
```

### E001 — size 위반 (AC-FR01-02, AC-FR01-03)

```json
{
  "type": "ERROR",
  "error": {
    "code": "E001",
    "message": "INVALID_MATRIX_SIZE: expected 4x4"
  }
}
```

---

## 10. 리스크 및 완화

| Risk | Impact | Mitigation |
|------|--------|------------|
| `INVALID_SIZE` vs E003 혼동 | 잘못된 assert | §1.3 용어표, BV-08/09 선행 검증 |
| Mock 남용으로 Domain 미검증 | Track B 공백 | Track B D-* 병행 (P-04) |
| message drift | RG-01 위반 | §13.3 완전 일치 assert |
| `[[]]*4` reference 공유 | 테스트 오해 | §3.1 주석; size AC만 검증 |

---

*본 문서는 AC-FR01-01 앵커 기준 FR-01 null·size 입력 검증 테스트 계획이다. 4×4 정상 입력(AC-FR01-07) 및 후속 FR-01 AC(빈칸·값·중복)는 별도 계획으로 확장한다.*
