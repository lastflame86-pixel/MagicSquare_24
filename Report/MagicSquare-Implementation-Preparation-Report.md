# 4×4 Magic Square — 구현 착수 준비 보고서

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare (`DEV/MagicSquare`) |
| **역할** | TDD 구현 착수 전 준비 (QA) |
| **선행 문서** | `Report/MagicSquare-TDD-Design-Report.md` |
| **작성일** | 2026-05-28 |
| **상태** | RED-01 스켈레톤·디렉터리 확정 — 코드 미착수 |

---

## Executive Summary

`MagicSquare-TDD-Design-Report.md`를 전제로 **테스트 프레임워크 후보 2종 비교**, **RED-01 실패 테스트 스켈레톤 경로·이름**, **`src`/`tests` 디렉터리 초안**을 확정했다. 1차 TDD 사이클은 **검증 우선·RED-01만** 착수하며, 생성·n×n·UI는 포함하지 않는다.

---

## 1. 테스트 프레임워크 후보 비교 (선택 기준만)

**전제:** 언어 미정 — **pytest**(Python) vs **JUnit 5**(JVM) 비교.

| 선택 기준 | pytest | JUnit 5 |
|-----------|--------|---------|
| TDD Red→Green 루프 | `pytest -k RED01` 등 단순 | IDE/빌드 도구 연동 익숙 시 유리 |
| RED-01·AC-01 표현 | parametrize·assert 가독성 | ParameterizedTest·타입 enum |
| §6 책임 분리 테스트 | unit/integration 폴더 관례 | 패키지 미러링 명확 |
| P0 회귀·CI (AC-11) | Actions 예제 다수 | Surefire 표준 |
| P1 결정성 (AC-09) | 동일 픽스처 2회 호출 용이 | @RepeatedTest |
| AC-12 RuleCatalog | assert·스냅샷 | 컴파일 타임 enum |
| Red ID 매핑 | 함수명·docstring | @DisplayName |
| Out of scope | UI E2E 불필요 — 동일 | 동일 |

**선택 흐름:** ① 언어 확정 → ② Red ID 1:1 매핑 가능 프레임워크 → ③ RED-01을 GridInput 단위 vs 통합 중 선택.

| 상황 | 권장 |
|------|------|
| 빠른 TDD·가벼운 CI·보일러플레이트 최소 | **pytest** |
| 정적 타입·IDE 리팩터·RuleCatalog enum | **JUnit 5** |

---

## 2. RED-01 실패 테스트 스켈레톤

| 항목 | 정의 |
|------|------|
| **Red ID** | RED-01 |
| **AC** | AC-01 |
| **Given** | 3×4 등 4×4가 아닌 정수 배열 |
| **When** | GridInput.parse (또는 동등 진입점) |
| **Then** | `result ∈ {REJECTED, NOT_APPLICABLE}`, `violationIds`에 **S1**, `≠ PASS` |
| **테스트 파일** | `tests/unit/grid_input/test_RED01_S1_non_4x4_dimensions.py` |
| **테스트 이름** | `test_RED01_given_3x4_grid_when_parse_then_rejected_with_S1_not_pass` |
| **한글 이름(대안)** | `test_형식_4x4_아님_거부` |
| **픽스처** | `tests/fixtures/grids/red01_input_3x4.json` |

**권장:** 단위 테스트(GridInput만) — G-02, Green 최소 행위 §7 RED-01.

---

## 3. 프로젝트 디렉터리 구조 초안

```text
MagicSquare/
├── src/
│   └── magicsquare/
│       ├── __init__.py
│       ├── domain/
│       │   ├── rule_catalog.py
│       │   └── validation_result.py
│       ├── input/
│       │   └── grid_input.py
│       ├── validation/
│       │   └── magic_square_validator.py
│       └── output/
│           └── validation_reporter.py
└── tests/
    ├── conftest.py
    ├── fixtures/grids/
    │   ├── red01_input_3x4.json
    │   └── ...
    ├── unit/grid_input/
    │   └── test_RED01_S1_non_4x4_dimensions.py
    └── integration/validator/
        └── ...
```

**JVM 선택 시:** `src/main/java/...`, `src/test/java/.../Red01S1Non4x4DimensionsTest.java` 로 동일 역할 치환.

---

## 4. 참조 문서

| 문서 | 내용 |
|------|------|
| `Report/MagicSquare-TDD-Design-Report.md` | STEP 0~8 TDD 설계 통합 |
| `Report/MagicSquare-Problem-Definition-Report.md` | 문제 정의 |
| `Prompt/MagicSquare-TDD-Design-Prompt.md` | 대화형 프롬프트 transcript |

---

## 5. 다음 단계

- [ ] 테스트 프레임워크·언어 확정
- [ ] RED-01 실패 테스트 파일 생성(스켈레톤)
- [ ] GridInput 최소 구현으로 Green
- [ ] RED-02 순차 진행 (G-02)

---

## 문서 이력

| 버전 | 날짜 | 설명 |
|------|------|------|
| 1.0 | 2026-05-28 | 구현 착수 준비 보고서 초안 |

---

*본 보고서는 코드·알고리즘 구현을 포함하지 않습니다.*
