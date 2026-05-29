# MagicSquare (4×4)

QA 관점에서 **4×4 마방진** 과제의 **문제 인식·정의·Dual-Track TDD 구현**을 수행하는 프로젝트입니다.

**현재 단계:** STEP 1~5 완료 · PRD·테스트 플랜 · **FR-01~05 Dual-Track GREEN** · Golden Master 회귀 · **REFACTOR Wave 1~4 완료**

---

## 프로젝트 목적

| 구분 | 내용 |
|------|------|
| **표면 목표 (지양)** | “4×4 마방진을 만드는 프로그램” |
| **진짜 목표** | 고정 규칙에 대한 **일관된 판정**, (선택) 규칙 충족 **산출**, **반복·자동 검증** 가능한 품질·학습 과제 |
| **훈련 초점** | 규칙 분해, 오라클·수용 기준, 계약(입출력), 회귀, ECB·Dual-Track TDD |

4×4는 계산이 어려워서가 아니라, **검증 규칙이 명확하고 테스트·TDD로 고정하기 좋은 규모**라서 다룹니다.

---

## 도메인 규칙 (요약)

- 격자: **4×4**, 16칸 모두 채움
- 값: **1 ~ 16** 각각 **한 번씩** (중복 없음)
- 합: 모든 **행·열·주대각·부대각**의 합이 같음 → 4×4일 때 **마방 상수 34**

**오라클:** 특정 숫자 배치 한 장이 아니라, 위 **규칙 집합**을 만족하는지로 “맞다”를 판단합니다. (유효한 배치는 여러 개 존재할 수 있음)

**PRD 범위 (FR-01~05):** 2빈칸 부분 격자 입력 → small-first / reverse Step B solver → `int[6]` 1-index 좌표·값 출력.

---

## 핵심 Invariant (S · V · M · P)

```
S1, S2  →  격자 형태 (4×4, 전 칸 채움)
    ↓
V1, V2  →  값·집합 (1~16, 중복 없음)
    ↓
M1~M4   →  합·대각 (공통 합 34)
    ↓
P1~P3   →  판정·산출 신뢰 (결정적 판정, 위반 시 통과 금지, 산출물 규칙 준수)
```

상세 정의와 STEP별 분석은 [Report/MagicSquare-Problem-Definition-Report.md](Report/MagicSquare-Problem-Definition-Report.md)를 참고하세요.

---

## ECB 아키텍처 (구현)

```
Screen (PyQt6)          boundary/screen/app.py
    ↓
Boundary                boundary/ui_boundary.py, input_validator.py, error_schema.py
    ↓
Control                 control/solve_partial_magic_square.py
    ↓
Entity                  entity/services/*.py, value_objects/, constants.py
```

| 레이어 | 경로 | 역할 |
|--------|------|------|
| **Screen** | `src/magicsquare/boundary/screen/app.py` | PyQt6 UI, composition root |
| **Boundary** | `src/magicsquare/boundary/` | 입력 검증, Success/Failure envelope |
| **Control** | `src/magicsquare/control/` | FR-05 오케스트레이션, `SolutionResult` SSOT |
| **Entity** | `src/magicsquare/entity/` | 빈칸 탐색, 누락 수, 마방진 검증, 2-cell solver |

---

## 문제 정의 워크플로 (완료된 단계)

| STEP | 주제 | 핵심 산출 |
|------|------|-----------|
| **1** | Observation (관찰) | 상황·QA 맥락·열린 질문 정리 |
| **2** | Why #1 | “완성” 가정과 구조적 문제 6가지 |
| **3** | Why #2 | 프로그램화 이유 (반복·자동검증·오류방지·규칙 사고) |
| **4** | Why #3 (TDD) | 통제 대상, 불변 I1~I7, 입출력 계약 |
| **5** | 진짜 문제 정의 | 표면 vs 개선 정의, Invariant, 훈련 사고 능력 |

---

## 개발 세션 이력 (01 ~ 13)

| # | 세션 | TDD phase | 핵심 산출 |
|---|------|-----------|-----------|
| 01 | Agent Setup | — | Cursor 에이전트·규칙 구성 |
| 02 | PRD | Track A | [docs/PRD_MagicSquare.md](docs/PRD_MagicSquare.md) v0.2 |
| 03 | README & TDD Start | Track A | To-Do 보드·TDD 시작 계획 |
| 04 | AC-FR01-01 Dual-Track | RED→GREEN | Boundary 8건, `test_plan.md`, `defect_list.md` |
| 05 | FR01-05 RED Design | Track A | Dual-Track 테스트 설계표 |
| 06 | FR01-05 RED Skeleton | RED | Track A/B 스켈레톤 22건 |
| 07 | FR01-05 GREEN & Screen | GREEN | Entity·Control·Boundary GREEN, PyQt6 Screen |
| 08 | Golden Master | 회귀 | GM-01~10, approve 패턴, `stabilize/green` |
| 09 | ECB REFACTOR Planning | Track A | 스멜·SRP·Wave 로드맵 계획서 |
| 10 | REFACTOR Program RF-05 | REFACTOR | `_failure()` SSOT 통합 (C5) |
| 11 | QA Coverage Analysis | Ask | Dual-Track 커버리지 실측, NFR gate |
| 12 | NFR Coverage Gate GREEN | GREEN | G-05 Screen headless, E007, NFR gate 충족 |
| 13 | REFACTOR Wave 1~4 Complete | REFACTOR | G-04, RF-03~08, R-L/R-U, 68 pytest |

세션별 상세: [Report/](Report/) 디렉터리 · 대화 재현: [Prompt/](Prompt/) Transcript Export

---

## 저장소 구조

```
MagicSquare/
├── README.md                          ← 이 문서
├── pyproject.toml                     ← pytest·coverage·PyQt6 optional
├── docs/
│   ├── PRD_MagicSquare.md             ← FR-01~05, G0~G3, Error Contract
│   ├── test_plan.md                   ← Dual-Track 테스트 플랜
│   └── defect_list.md                 ← AC-FR01-01 결함 기록
├── src/magicsquare/
│   ├── boundary/                      ← InputValidator, UIBoundary, error_schema
│   │   └── screen/app.py              ← PyQt6 MagicSquareMainWindow
│   ├── control/                       ← SolvePartialMagicSquare
│   └── entity/                        ← services, value_objects, constants
├── tests/
│   ├── boundary/                      ← Track A (34건, incl. test_main_window)
│   ├── control/                       ← SC-CTL-002~004 (3건, G-04)
│   ├── entity/                        ← Track B (19건 + User 학습용)
│   ├── golden_master/                 ← capture, approve, scenarios
│   ├── test_golden_master_magic_square.py  ← GM 12건
│   └── golden_master_expected.txt     ← approve 기준 파일
├── scripts/
│   └── generate_golden_master_expected.py
├── Report/                            ← 세션 Report 01~11
└── Prompt/                            ← 세션 Transcript·Prompt Export
```

---

## 빠른 시작

```bash
# 가상환경·설치
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -e ".[gui]"         # PyQt6 Screen 포함

# 전체 테스트 (68건)
python -m pytest -q

# Golden Master만 (12건)
python -m pytest -m golden_master -v

# PyQt6 Screen (수동 검증)
python -m magicsquare.boundary.screen.app
python -m magicsquare.boundary.screen.app --verify   # G1 fixture 자동 입력
```

---

## 현재 상태

| 항목 | 상태 |
|------|------|
| 문제 인식·정의 (STEP 1~5) | ✅ 완료 |
| PRD·테스트 플랜 | ✅ 완료 |
| AC-FR01-01 Boundary RED→GREEN | ✅ 완료 (8건) |
| FR-01~05 Dual-Track GREEN | ✅ 완료 (68 pytest PASS) |
| Golden Master 회귀 (GM-01~10) | ✅ 완료 (12 GM PASS) |
| PyQt6 Screen (수동 검증) | ✅ 완료 |
| REFACTOR RF-03~05 (SolutionResult, Entity→Control, `_failure`) | ✅ 완료 |
| REFACTOR RF-06~08 (Screen composition·SSOT·CLI) | ✅ 완료 |
| REFACTOR R-L1~L4 (Grid SSOT, demo_grids, entity cleanup) | ✅ 완료 |
| REFACTOR R-U2~U3 (ui_boundary Extract Method, grid narrowing) | ✅ 완료 |
| G-04 Control 단위 테스트 (SC-CTL-002~004) | ✅ 완료 |
| G-05 Screen headless (`test_main_window.py`) | ✅ 완료 |
| NFR 커버리지 gate (Boundary·전역) | ✅ 충족 (Boundary 98%, 전역 96%) |

### pytest 기준선 (G-05 Screen 테스트 반영)

| Track | 경로 | 건수 | 결과 |
|-------|------|------|------|
| Boundary | `tests/boundary/` | 34 | PASS |
| Control | `tests/control/` | 3 | PASS |
| Entity | `tests/entity/` | 19 | PASS |
| Golden Master | `tests/test_golden_master_magic_square.py` | 12 | PASS |
| **합계** | | **68** | **PASS** |

RED 스켈레톤(`pytest.fail("RED: …")`): **0건** — REFACTOR gate 충족

### NFR 커버리지 gate

| Gate | 목표 | 실측 | 판정 | 주요 원인 |
|------|------|------|------|-----------|
| NFR-01 Domain | ≥ 95% | 95% (entity + GM) | ✅ PASS | — |
| NFR-02 Boundary | ≥ 85% | 98% | ✅ PASS | — |
| NFR-03 전역 | ≥ 80% | 96% | ✅ PASS | — |

```bash
# Domain Track
python -m pytest tests/entity/ tests/test_golden_master_magic_square.py \
  --cov=src/magicsquare/entity --cov=src/magicsquare/control --cov-report=term-missing

# Boundary Track
python -m pytest tests/boundary/ \
  --cov=src/magicsquare/boundary --cov-report=term-missing
```

---

## RED 단계 To-Do 리스트

> `docs/test_plan.md` 기반. AC-FR01-01 앵커 + FR-01~05 Dual-Track 진행 상황.

### Track A — UI / Boundary 테스트
- [x] TC-A-01: grid=None 입력 → 실패 결과 반환 (Happy Path of Failure)
- [x] TC-A-02: code가 정확히 "INVALID_SIZE" 문자열인지 검증
- [x] TC-A-03: message가 "Grid must be 4x4." 와 문자 단위 동일한지 검증
- [x] TC-A-04: grid=None 시 Domain 진입점 0회 호출 (mock/spy 검증)
- [x] TC-A-05: grid=[] 빈 리스트 → 실패 결과 반환
- [x] TC-A-06: grid=3×4 크기 불일치 → 실패 결과 반환
- [x] TC-A-07: 반환 객체 타입이 지정 실패 결과 구조체인지 검증
- [x] U-IN-04~08: 빈칸 수·값 범위·중복 → E002/E004/E005
- [x] U-OUT-01~03: Success `int[6]`, 1-index, E006 unsolvable
- [x] U-FLOW-02: 검증 실패 시 `resolve()` 0회 (3건 — 설계 6건 대비 부분)

### Track B — Domain / Logic 테스트
- [x] TC-B-01: resolve()가 None grid를 직접 받지 않음을 격리 검증
- [x] TC-B-02: Boundary가 None 분기를 처리 후 resolve() 미호출 확인
- [x] TC-B-03: resolve() mock이 호출됐을 경우 테스트 실패 처리
- [x] TC-B-04: AC-FR-01-02~05 범위의 케이스는 이 커밋에 포함하지 않음 확인
- [x] D-LOC-01: G1 row-major 빈칸 좌표 (1-index)
- [x] D-MIS-01: G1 누락 수 정렬 쌍
- [x] D-VAL-01~06: G0 마방진 검증 (행·열·대각·중복·0)
- [x] D-SOL-01~04: G1/G2/G3 solver (Step B, reverse, unsolvable)

### 커버리지 목표
- [x] Domain Logic: 95%+ (entity + GM 경계 PASS)
- [x] Boundary Layer: 85%+ (G-05 Screen headless — 99%)
- [x] 전체 TOTAL: 80%+ (96%)

### 결함 목록 연결
- [x] defect_list.md 생성 및 발견 결함 기록
- [x] 모든 결함 수정 후 회귀 테스트 통과 확인

---

## Golden Master 회귀 안전장치

> Refactoring 시작 전 구축. GREEN 완료 후 즉시 적용.

### 기준 파일 생성

- [x] **GM-01:** `tests/golden_master_expected.txt` 생성
- [x] **GM-02:** 정상/역순/오류 시나리오 추가 (`normal_success`, `reverse_success`, `invalid_blank_count`, `duplicate_number`, `no_valid_magic_square`)
- [x] **GM-03:** `git add tests/golden_master_expected.txt` (버전 관리 포함)

### 테스트 코드

- [x] **GM-04:** `tests/test_golden_master_magic_square.py` 작성
- [x] **GM-05:** approve 패턴 적용 (기준 없으면 생성 · 있으면 `expected` vs `actual` 비교 · 불일치 시 unified diff)
- [x] **GM-06:** Golden Master 테스트 PASS 확인 (`pytest -m golden_master -v`)

### 회귀 보호

- [x] **GM-07:** row-major 규칙 보호 (빈칸 좌표 = row-major 첫·둘째 `0`)
- [x] **GM-08:** 1-index 출력 보호 (`int[6]` 좌표 `1..4`)
- [x] **GM-09:** reverse 조합 fallback 보호 (Step A 실패 → Step B 성공, G1/G2)
- [x] **GM-10:** Error Contract 보호 (`INVALID_BLANK_COUNT`, `DUPLICATE_NUMBER`, `NO_VALID_MAGIC_SQUARE`)

**실행**

```bash
pytest -m golden_master -v
python scripts/generate_golden_master_expected.py   # 기준 갱신
pytest -m golden_master --update-golden -v          # approve 갱신 후 회귀
```

**참고:** approve 패턴·섹션 형식 — [tests/docs/Golden-Master-Approve-Pattern.md](tests/docs/Golden-Master-Approve-Pattern.md)

---

## REFACTOR 로드맵 (Wave 1~4 요약)

| 커밋 | ID | Track | 상태 |
|------|-----|-------|------|
| C1 | RF-01 | Boundary | ✅ 완료 |
| C2 | RF-02 | Boundary | ✅ 완료 |
| C3 | RF-03 | Control | ✅ SolutionResult SSOT |
| C4 | RF-04 | Control+Entity | ✅ orchestration Entity→Control |
| C5 | RF-05 | Boundary | ✅ `_failure()` extract |
| C6~C8 | RF-06~08 | Screen | ✅ composition·SSOT·CLI |
| C9~C12 | R-L1~L4 | Entity | ✅ Grid SSOT·demo_grids·helpers |
| C13~C14 | R-U2~U3 | Boundary | ✅ ui_boundary Extract Method |

**Phase 0 게이트:** G-01 pytest GREEN ✅ · G-02 GM matched ✅ · G-03 U-FLOW 부분 ✅ · G-04 SC-CTL ✅ · G-05 Screen ✅

상세: [Report/09.MagicSquare-ECB-REFACTOR-Planning-Session_Report.md](Report/09.MagicSquare-ECB-REFACTOR-Planning-Session_Report.md), [Report/10.MagicSquare-REFACTOR-Program-RF05-Session_Report.md](Report/10.MagicSquare-REFACTOR-Program-RF05-Session_Report.md), [Report/13.MagicSquare-REFACTOR-Wave-1-4-Complete-Session_Report.md](Report/13.MagicSquare-REFACTOR-Wave-1-4-Complete-Session_Report.md)

---

## 주요 참고 문서

| 문서 | 경로 | 설명 |
|------|------|------|
| 문제 정의 | [Report/MagicSquare-Problem-Definition-Report.md](Report/MagicSquare-Problem-Definition-Report.md) | STEP 1~5, Invariant |
| TDD 설계 | [Report/MagicSquare-TDD-Design-Report.md](Report/MagicSquare-TDD-Design-Report.md) | RED-01~08, RuleCatalog |
| PRD | [docs/PRD_MagicSquare.md](docs/PRD_MagicSquare.md) | FR-01~05, Error Contract |
| 테스트 플랜 | [docs/test_plan.md](docs/test_plan.md) | Dual-Track 시나리오·AC |
| QA 커버리지 | [Report/11.MagicSquare-QA-Coverage-Analysis-Session_Report.md](Report/11.MagicSquare-QA-Coverage-Analysis-Session_Report.md) | NFR gate 실측 |
| NFR gate GREEN | [Report/12.MagicSquare-NFR-Coverage-Gate-GREEN-Session_Report.md](Report/12.MagicSquare-NFR-Coverage-Gate-GREEN-Session_Report.md) | G-05·E007 GREEN |
| REFACTOR Wave 1~4 | [Report/13.MagicSquare-REFACTOR-Wave-1-4-Complete-Session_Report.md](Report/13.MagicSquare-REFACTOR-Wave-1-4-Complete-Session_Report.md) | G-04·RF-03~08·R-L/R-U |
| Cursor Rules | [.cursor/rules/](.cursor/rules/) | TDD·ECB·금지 패턴 |

---

## 권장 진행 순서

```
문제 정의 ✅ → PRD·테스트 플랜 ✅ → Dual-Track GREEN ✅ → Golden Master ✅
    → REFACTOR Wave 1~4 ✅ → NFR gate ✅
```

**다음 우선 작업 (REFACTOR 완료 후):**

1. U-FLOW-02 설계 6건 대비 3건 잔여 시나리오 보강 (선택)
2. RuleCatalog 일원화 (P2 — 별도 REFACTOR)
3. 문서·Report 세션 13 Export (REFACTOR 완료 기록)

---

## 문서 이력

| 버전 | 날짜 | 설명 |
|------|------|------|
| 1.0 | 2026-05-28 | README 초안 (STEP 1~5 반영) |
| 2.2 | 2026-05-29 | REFACTOR Wave 1~4 완료 — G-04, RF-03~08, R-L/R-U, 68 pytest |
| 2.1 | 2026-05-29 | 세션 12 — NFR gate GREEN, G-05·E007, Report/12 |
| 2.0 | 2026-05-29 | 세션 01~11 진행 현황 반영 — GREEN·GM·REFACTOR·커버리지 |

---

*Report·Prompt Track A 문서는 구현 설계·코드 없이 시나리오·AC 중심으로 작성됩니다. `src/`·`tests/`는 Track B TDD 산출물입니다.*
