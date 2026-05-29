# MagicSquare — Track A/B Phase 통합 프롬프트

| 항목 | 내용 |
|------|------|
| **목적** | 트랙 A(Validator)와 트랙 B(Solver)를 Phase로 통합·고정한 뒤, PRD·설계·TDD 세션의 **단일 범위 기준(SSOT)** 으로 사용 |
| **상태** | 확정안 v1.0 (2026-05-28) |
| **짝 산출물** | PRD Scope §, `Report/MagicSquare-PRD.md` (작성 시) |
| **선행 문서** | Problem Definition, TDD Design, Level 1~5 Planning, project.mdc |

---

## 0. 시스템 역할 (새 대화에 붙여넣기)

```text
당신은 MagicSquare(4×4) 프로젝트의 제품·QA 기획 보조입니다.

반드시 준수:
1) 본 문서의 「Track A/B Phase 통합 표」가 범위의 SSOT이다.
2) Phase 1(Validator)이 Green·P0 안정 전에는 Phase 2(Solver) 구현·테스트 코드 착수 금지.
3) Phase 3(Generator)은 G1~G3 게이트 충족 전 금지.
4) User 엔티티는 Phase 0 별도 학습 트랙이며 Validator/Solver RED와 혼합 금지.
5) 코드·테스트 본문은 사용자가 명시적으로 요청할 때만 작성한다.
6) 트랙 A의 완전 격자 계약과 트랙 B의 2칸 빈칸(0) 계약을 한 API에 섞지 않는다.
```

---

## 1. 트랙 정의

| 트랙 | 명칭 | 제품 행위 | 대표 문서 | 핵심 산출 |
|------|------|-----------|-----------|-----------|
| **A** | Validator | **완전** 4×4 격자에 대해 S→V→M→P **판정** | `MagicSquare-TDD-Design-Report.md` | `result`, `violationIds`, RED-01~08 |
| **B** | Solver | **빈칸 2개(0)** 4×4 격자를 규칙에 맞게 **완성** | Level 1~5 Planning, Story 1~5 | `int[6]` `[r1,c1,n1,r2,c2,n2]` |
| **—** | User Entity | 학습자·QA **신원** (격자와 무관) | `MagicSquare-User-Entity-Report.md` | `User`, `UserRole` (별도 트랙) |

---

## 2. Track A/B Phase 통합 표 (SSOT)

| Phase | 이름 | 트랙 | In Scope | Out of Scope | 진입 조건 | 완료(Exit) 기준 |
|-------|------|------|----------|--------------|-----------|-----------------|
| **P0** | 기획·계약 정합 | A+B 문서 | Epic/Journey/Story/Scenario, PRD Scope·계약 표, Phase 본 문서 확정 | 구현·pytest | — | PRD §6 Scope·§9 Contract에 Phase 표 반영; A/B 계약 충돌 해소 문서화 |
| **P1** | Validator (검증) | **A** | GridInput, MagicSquareValidator, RuleCatalog, ValidationReporter; IN-01~06, OUT-01~04; RED-01~08 순차 Green | Solver, Generator, UI/CLI 본구현, n×n | P0 Exit | RED-01~08 Green; AC-01~12; P0 CI; 유효 격자 ≥2종 PASS; P1 결정성 |
| **P2** | Solver (2칸 완성) | **B** | Boundary 입력 검증(Story 1); BlankFinder; MissingNumberFinder; MagicSquareValidator(재사용); Solver 조합 시도(Story 5); Level 5 보완 시나리오 | Generator; 미완성→자동완성; 정답 16칸 하드코딩 | **P1 Exit** | Story 1~5 AC 충족; SC-DOM-SOL-001 등 Level 4 시나리오 Green; Boundary 실패 시 Domain 미호출 |
| **P3** | Generator (산출) | **A 확장** | MagicSquareGenerator; 산출 → Validator **PASS** 연쇄(P3) | n×n, 성능 벤치, UI 과잉 | **G1∧G2∧G3** (아래 §4) | 생성 Red Green; generate→validate→PASS 시나리오 |
| **Px** | User Entity (학습) | **별도** | entity `User` 불변·검증 | control/boundary, 격자 RED | — | entity 단위 테스트 Green (이미 7 passed 시 유지) |

### Phase 의존 관계 (다이어그램)

```text
P0 (기획·PRD)
 └─► P1 Validator [Track A] ──► P2 Solver [Track B]
         └──────────────────────────► P3 Generator (G1~G3)
Px User Entity  (병렬, P1/P2와 RED 혼합 금지)
```

---

## 3. Phase별 계약 SSOT (충돌 방지)

### 3.1 Phase 1 — Track A (Validator)

| 구분 | 규칙 |
|------|------|
| 입력 | **완전** 4×4 정수 16칸 (1~16, 중복 없음) — 판정 대상 |
| 미완성 | 빈 칸·null → `NOT_APPLICABLE` + **S2** (Solver로 채우지 않음) |
| 형식 오류 | 비 4×4 → `REJECTED`/`NOT_APPLICABLE` + **S1** |
| 출력 | `result` ∈ {PASS, FAIL, NOT_APPLICABLE, REJECTED}, `violationIds`, `summary` |
| 판정 순서 | **S → V → M**; 위반 시 PASS 금지(P2) |
| 오라클 | 특정 16칸 배열 고정 금지; 유효 격자 ≥2종 |

### 3.2 Phase 2 — Track B (Solver)

| 구분 | 규칙 |
|------|------|
| 입력 | 4×4 `int`; **0 = 빈칸**; 빈칸 **정확히 2개**; 값 ∈ {0} ∪ {1..16}; 0 제외 중복 금지 |
| Boundary | 위반 시 **정의된 검증 실패**; **Domain Solver/Resolver 호출 0회** |
| Domain | BlankFinder → MissingNumberFinder → (완성 후보) MagicSquareValidator → Solver |
| 시도 순서 | (1) 작은 누락 수 → 첫 빈칸, 큰 누락 수 → 둘째 빈칸 (2) 실패 시 반대 |
| 출력 | `int[6]` = `[r1, c1, n1, r2, c2, n2]`; 좌표 **1-index**; 길이 6 |
| 실패 | 두 조합 모두 M(34) 불만족 → **정의된 실패** (Phase 2 PRD에서 예외/코드 통일) |

### 3.3 Phase 1 ↔ Phase 2 관계 (통합 원칙)

| 질문 | 결정 |
|------|------|
| P1 Validator가 P2 입력(0 포함)을 받나? | **아니오.** P2 Boundary는 **별도 IN 계약**; P1 GridInput.parse는 완전 격자·미완성 NA 전용 |
| P2에서 M(34) 검증은? | **예.** Phase 1에서 구현한 `MagicSquareValidator`(또는 동등 로직) **재사용** |
| P1의 NOT_APPLICABLE(S2)와 P2의 0 두 칸은 같은 기능? | **아니오.** S2=판정 불가; P2=의도된 퍼즐 입력. **API·진입점 분리** |
| 출력 모델 통합? | **아니오.** P1=`ValidationResult`; P2=`int[6]` 또는 SolverResult DTO. Facade는 Phase 2 PRD 후 선택 |

---

## 4. Phase 3 게이트 (Generator — Track A 확장)

| 게이트 | 조건 | 증거 |
|--------|------|------|
| **G1** | P1 RED-01~08 전부 Green, P0 CI 안정 | CI 로그 |
| **G2** | IN/OUT·violation ID 매핑 고정; 동일 입력 2회 동일 결과(P1) | 통합 테스트 |
| **G3** | 생성 AC + Red 등록; generate → Validator → PASS | 시나리오 Green |

**금지:** G1 미충족 시 Generator 코드·테스트 착수.

---

## 5. Level 5 갭 → Phase 배치

| 갭 항목 | 배치 Phase | 산출 목표 |
|---------|------------|-----------|
| SC-BND-VAL-004 (4×4 형식 오류) | **P2** Boundary | RED-BND-VAL-004 |
| SC-DOM-SOL-002 (small-first 즉시 성공) | **P2** Solver | RED-DOM-SOL-002 |
| SC-DOM-BLK-001, SC-DOM-MISS-001/002 | **P2** Domain | RED-DOM-BLK-001, RED-DOM-MISS-* |
| RED-01~08, AC-01~12 | **P1** | 기존 TDD Design |

---

## 6. PRD 반영 체크리스트 (Phase 표 → PRD 섹션)

PRD 작성 시 아래를 **그대로** 옮긴다.

| PRD 섹션 | Phase 표에서 가져올 내용 |
|----------|-------------------------|
| §6 Scope | §2 Phase 표 전체 + §3 계약 SSOT |
| §7 Domain Rules | §3.1 (P1), §3.2 (P2) 불변식 |
| §9 Contracts | §3.1 OUT-*, §3.2 int[6] — **subsection 분리** |
| §10 User Stories | P1: RED↔AC; P2: Story 1~5 |
| §14 Release Plan | P0→P1→P2→P3 + Px 병렬 |
| §15 Risks | §3.3 통합 원칙 위반 시 리스크 |

---

## 7. 대화형 프롬프트 (Turn 순서)

### Turn 1 — PRD Scope·Phase 확정 (코드 없음)

```text
MagicSquare-Track-AB-Phase-Integration-Prompt.md §2 Phase 통합 표를 SSOT로 하여,
PRD의 다음 섹션만 작성하십시오 (구현·테스트 코드 없음):

1) Document Control (버전 0.1, 참조 문서 목록)
2) Executive Summary (1단락: P1 Validator → P2 Solver → P3 Generator)
3) §6 Scope — Phase 표(§2) 전체 인용 + In/Out of Scope
4) §15 Risks — 트랙 A/B API 혼합 금지, Phase 순서 위반 금지

다른 PRD 섹션은 작성하지 마십시오.
```

### Turn 2 — PRD Contracts (코드 없음)

```text
동일 SSOT(§3 Phase별 계약)를 기준으로 PRD §9 Contracts만 작성하십시오.

- 9.1 Phase 1 Validator Contracts (IN-01~06, OUT-01~04 요약 표)
- 9.2 Phase 2 Solver Contracts (입력 0/빈칸2/범위/중복, 출력 int[6], 오류 정책)
- 9.3 Contract Separation Rule (§3.3 통합 원칙 4줄)

구현·테스트 코드 없음.
```

### Turn 3 — PRD Functional Requirements + Stories (코드 없음)

```text
SSOT Phase 표를 기준으로:

1) §8 Functional Requirements — FR-V-01~ (P1), FR-S-01~ (P2) ID 부여
2) §10 User Stories — P1: RED-01~08 ↔ AC-01~12 매핑; P2: Story 1~5 + Level 5 갭(§5) AC

코드 없음. Task 수준 분해 금지.
```

### Turn 4 — PRD Quality·Release·Traceability (코드 없음)

```text
SSOT를 기준으로 PRD §13 Quality/DoD, §14 Release Plan, §16 Traceability Appendix를 작성하십시오.

- P1: magicsquare-tdd-testing.mdc (Dual-Track, RED 1건 Green, 80% 커버리지)
- P2: Boundary vs Domain RED 분리, Level 4 Scenario ID 링크
- Epic → Journey → Story → Scenario → Phase 표

코드 없음.
```

### Turn 5 — PRD 통합본 + Report Export 요청

```text
Turn 1~4 산출을 하나의 PRD로 통합하고,
Report/MagicSquare-PRD.md 로 저장하십시오.
Prompt/MagicSquare-PRD-Session-Transcript.md 에 Turn 요약을 Export하십시오.
```

---

## 8. 금지·허용 (모든 Phase 공통)

| 금지 | 허용(Phase 내) |
|------|----------------|
| P1 미완료 시 P2 pytest 착수 | P1 내 RED 1건씩 Green |
| 정답 16칸 배열 전역 하드코딩 | `MAGIC_CONSTANT=34`, `GRID_SIZE=4` 등 명명 상수 |
| assert 완화·skip으로 Red 제거 | Phase 1: 최초 위반 ID 1개(설계 부채 §8.3) |
| Boundary 실패 시 Domain 호출 | P2: Validator 로직 재사용 |
| Phase 3 Generator 선행 | Px: User entity 독립 유지 |

---

## 9. 문서 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| 1.0 | 2026-05-28 | Track A/B Phase 통합 표 및 PRD용 Turn 1~5 최초 확정 |

---

*본 프롬프트는 Phase 범위 SSOT이며, 구현·테스트 본문을 포함하지 않습니다.*
