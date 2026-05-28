# MagicSquare — TDD 설계 대화형 프롬프트 Transcript Export

| 항목 | 내용 |
|------|------|
| **Export 일시** | 2026-05-28 (v2 — Turn 10~11 반영) |
| **프로젝트** | DEV/MagicSquare |
| **선행** | `Report/MagicSquare-Problem-Definition-Report.md` (STEP 1~5 완료) |
| **산출 Report** | `MagicSquare-TDD-Design-Report.md`, `MagicSquare-Implementation-Preparation-Report.md` |
| **용도** | TDD 설계·구현 착수 준비 워크플로 재실행 |

---

## 사용 방법

1. 아래 **시스템 역할** 블록을 새 대화 맨 앞에 붙여 넣습니다.
2. **선행 입력**(STEP 0) 후 **STEP 1 ~ STEP 8** User 블록을 순서대로 실행합니다.
3. **STEP 9**로 Report·본 Prompt Export를 요청합니다.
4. **STEP 9** Export 후 **Turn 10**(구현 준비) 실행.
5. 마지막 **「다음 턴: RED-01」** 으로 실패 테스트·최소 Green을 이어갑니다.

---

## 시스템 역할 (권장)

```text
당신은 TDD·테스트 설계 전문가이며, QA 관점에서 요구를 검증 가능한 설계로 바꿉니다.

나는 4×4 Magic Square 프로그램을 TDD로 구현할 예정입니다.
지금 단계는 「TDD 설계 문서」 작성입니다.

절대 하지 말 것:
- 프로덕션 코드·테스트 코드·의사코드 작성
- 알고리즘·자료구조·성능 최적화 상세 설명
- 특정 언어·프레임워크에 종속된 구현(단, 테스트 도구는 「후보」로만 언급 가능)
- 문제 정의(STEP 1~5)를 뒤집거나 재논의

반드시 할 것:
- 저장소의 문제 정의 보고서를 전제로 진행
- 불변 조건(S·V·M·P, I1~I7)을 테스트·계약·책임 분리로 연결
- Red → Green → Refactor 관점에서 「첫 실패 테스트」부터 설계
- 산출물은 구조화된 Markdown

한 STEP 요청에는 그 STEP의 질문·표·목록만 답합니다.
```

---

## Turn 0 — User (선행 입력 + STEP 0)

```text
다음 파일을 읽고 내용을 전제로만 사용하십시오. 요약 후 STEP 0 질문에 답하십시오.
- Report/MagicSquare-Problem-Definition-Report.md
- README.md (프로젝트 상태·미결정 사항)

--------------------------------------------
STEP 0 — 전제 확인
--------------------------------------------
Report/MagicSquare-Problem-Definition-Report.md를 읽은 뒤, 다음만 작성하십시오.

1. 이해한 「진짜 문제 정의」 한 문장
2. 채택할 Invariant 계층 요약 (S·V·M·P — 각 1줄)
3. 보고서의 「미결정 사항」 목록을 그대로 인용한 뒤, TDD 설계에서 반드시 결정해야 할 항목에 ★ 표시
4. 본 TDD 설계 문서의 범위(In scope / Out of scope) 초안 — 각 3~5개 bullet

구현·코드·알고리즘은 금지합니다.
```

### Turn 0 — Assistant (요약)

- 진짜 문제: 판정 핵심 + 선택 산출 + 자동 검증.
- S·V·M·P 각 1줄 확정.
- 미결정 5항 전부 ★ (TDD에서 결정).
- In scope: 계약·Red·AC·DoD / Out: 코드·생성(1차)·n×n·UI.

---

## Turn 1 — User (STEP 1)

```text
--------------------------------------------
STEP 1 — 범위 고정
--------------------------------------------
문제 정의 보고서의 미결정 「1순위 기능: 검증 vs 생성」을 결정하십시오.

다음 형식으로만 답하십시오.

| 항목 | 결정 | 근거 (QA·TDD 관점, 2~3문장) |
|------|------|---------------------------|
| 1순위 기능 | 검증 우선 / 생성 포함 / 생성 우선 | |
| 2순위 기능 | (있다면) | |
| 이번 TDD 사이클에서 제외 | | |

추가:
- 「검증 우선」일 때: 생성 기능을 언제·어떤 테스트로 도입할지 「게이트 조건」 3개
- 「생성 포함」일 때: 생성물이 반드시 통과해야 하는 판정 계약 3개

코드·알고리즘 금지.
```

### Turn 1 — Assistant (요약)

- 1순위: **검증 우선**; 2순위: 생성(2차); 제외: 생성 알고리즘·n×n·UI·골든 단독 오라클.
- 게이트 G1~G3: P0 Green, IN/OUT+P1, 생성 AC+Red.

---

## Turn 2 — User (STEP 2)

```text
--------------------------------------------
STEP 2 — 입출력 계약
--------------------------------------------
4×4 격자에 대한 시스템 경계 계약을 정의하십시오.
(구현 방식·파싱 라이브러리·UI는 다루지 마십시오.)

### 2.1 입력 계약
| 계약 ID | 입력 형태 | 허용 | 거부·미완성 처리 |
|---------|-----------|------|------------------|
| IN-… | (예: 완전 4×4 정수 격자) | | |

최소 4행: 완전 격자 / 빈 칸·null / 범위 밖 값 / 형식 오류

### 2.2 출력 계약
| 계약 ID | 상황 | 출력(관측 가능) | 실패 시 필수 정보 |
|---------|------|-----------------|-------------------|
| OUT-… | 통과 | | |
| OUT-… | 실패 | | |
| OUT-… | 미완성·판정 불가 | | |

위반 규칙 ID(S/V/M/P 또는 I1~I7 매핑) 포함 여부를 명시하십시오.

### 2.3 결정성
- 동일 입력 → 동일 판정 결과가 보장되어야 하는가? (예/아니오 + 이유 1문단)

코드 금지. Given/When/Then 예시는 STEP 5에서만 작성합니다.
```

### Turn 2 — Assistant (요약)

- IN-01~06, OUT-01~04; FAIL/NA/REJECTED 구분; 위반 ID 필수.
- 결정성: **예**.

---

## Turn 3 — User (STEP 3)

```text
--------------------------------------------
STEP 3 — Invariant → 테스트 매핑
--------------------------------------------
문제 정의의 S·V·M·P(및 I1~I7)를 테스트 관점으로 매핑하십시오.

| Invariant ID | 의미(1줄) | 테스트 유형 (단위/속성/통합/골든/부정) | 실패 시 관측 기대 | 우선순위 P0/P1/P2 |
|--------------|-----------|----------------------------------------|-------------------|-------------------|

- 모든 S·V·M 항목 포함
- P1~P3(판정·산출 신뢰)는 STEP 1 범위 결정과 일치하게
- 「특정 16개 배치 한 장」은 비불변임을 테스트 설계에 어떻게 반영하는지 1문단

알고리즘·코드 금지.
```

### Turn 3 — Assistant (요약)

- S1~M4, P1~P2 P0; P3 P2(2차).
- 비불변: 규칙 오라클, 유효 격자 ≥2종, 골든은 회귀 샘플만.

---

## Turn 4 — User (STEP 4)

```text
--------------------------------------------
STEP 4 — 테스트 전략
--------------------------------------------

### 4.1 테스트 피라미드
| 레벨 | 목적 | Magic Square에서 다룰 내용 | 비율(대략) |
|------|------|------------------------------|----------|

### 4.2 책임 분리 (설계 수준)
다음 관점으로 **모듈/컴포넌트 이름만** 제안하십시오 (메서드·클래스 시그니처·코드 없음):
- 판정(Validator)
- (선택) 생성(Generator)
- (선택) 표시/입출력 어댑터
- 도메인 규칙 표현

각 컴포넌트: 책임 1문장 / 하지 않을 일 1문장 / 테스트가 주입할 관측 지점 1개

### 4.3 회귀·CI
- 회귀에 넣을 P0 테스트 범주 5개
- CI에서 실패하면 merge 차단해야 하는 조건 3개

구현·알고리즘 금지.
```

### Turn 4 — Assistant (요약)

- 피라미드 50/35/10/5; GridInput·Validator·RuleCatalog·Reporter.
- P0 회귀 5범주; CI P0 실패·P1·시나리오 매핑.

---

## Turn 5 — User (STEP 5)

```text
--------------------------------------------
STEP 5 — 첫 실패 테스트 (Red 백로그)
--------------------------------------------
TDD Red 단계용 시나리오를 **정확히 8개** 작성하십시오.
(구현 전에 실패해야 하는 순서가 드러나도록 번호 매기기)

각 시나리오 형식:
| # | ID | Given | When | Then (관측 가능) | 검증 Invariant | P0/P1 |
|---|-----|-------|------|------------------|----------------|-------|

구성 규칙:
- 최소 3개: S·V 계층 (형태·값·중복)
- 최소 3개: M 계층 (행·열·대각 합 — 실패 케이스 포함)
- 최소 1개: 부정/경계 (범위 밖·미완성 등)
- 최소 1개: P 계층 (결정성·위반 시 통과 금지 등)
- STEP 1에서 「제외」한 기능은 시나리오에 넣지 말 것

테스트 이름(한글 또는 영문)만 제안 가능. **테스트 코드 본문은 금지.**

권장 구현 순서(1→8)와 각 단계에서 Green을 만족시키는 「최소 행위」(문장, 코드 아님)를 마지막에 표로 추가하십시오.
```

### Turn 5 — Assistant (요약)

- RED-01~08: S1→S2→V1→V2→M1→M2→M3→유효2종+P1.
- Green 최소 행위 표 1→8.

---

## Turn 6 — User (STEP 6)

```text
--------------------------------------------
STEP 6 — Green & Refactor 원칙
--------------------------------------------

### 6.1 Green (최소 구현) 원칙
| 원칙 ID | 내용 | Magic Square 적용 예 |
|---------|------|----------------------|
| G-… | | |

5개 이상. 「한 번에 모든 규칙 구현」 금지를 명시할 것.

### 6.2 Refactor 트리거
다음 중 Magic Square에 해당하는 항목을 체크리스트로 6개 이상:
- [ ] 중복 제거 시점
- [ ] 규칙 ID와 메시지 일원화
- [ ] 판정 순서(S→V→M) 고정
- (기타 TDD·QA 관점)

### 6.3 기술 부채 허용 범위
- Red/Green 단계에서 허용할 임시 단순화 3개
- Refactor 전까지 금지할 것 3개

코드·알고리즘 금지.
```

### Turn 6 — Assistant (요약)

- G-01~G-07; G-02 전 규칙 일괄 구현 금지.
- Refactor 8항; 부채 허용 3 / 금지 3.

---

## Turn 7 — User (STEP 7)

```text
--------------------------------------------
STEP 7 — 수용 기준 & Definition of Done
--------------------------------------------

### 7.1 수용 기준 (AC)
| AC ID | 조건(측정 가능) | 검증 방법(테스트 레벨) | STEP 5 시나리오 링크 |
|-------|-----------------|------------------------|----------------------|

8개 이상. 모호어(「잘 동작」 등) 금지.

### 7.2 Definition of Done (TDD 설계 문서 기준)
- [ ] … (체크리스트 10개 이상)

### 7.3 비기능 (이번 범위)
| 속성 | 이번 In/Out | 메모 |
|------|-------------|------|
| 성능 | | |
| n×n 일반화 | | |
| UI/CLI | | |

코드 금지.
```

### Turn 7 — Assistant (요약)

- AC-01~AC-12; DoD 15항; 성능·n×n·UI Out.

---

## Turn 8 — User (STEP 8)

```text
--------------------------------------------
STEP 8 — TDD 설계 문서 통합
--------------------------------------------
STEP 0~7 산출물만을 통합하여, 아래 목차의 **완성본 Markdown**을 한 번에 작성하십시오.

# 4×4 Magic Square — TDD 설계 문서

## 1. Executive Summary
## 2. 전제 (문제 정의 요약·참조 문서)
## 3. 범위 결정 (STEP 1)
## 4. 입출력 계약 (STEP 2)
## 5. Invariant ↔ 테스트 매핑 (STEP 3)
## 6. 테스트 전략·책임 분리 (STEP 4)
## 7. Red: 첫 실패 테스트 백로그 (STEP 5)
## 8. Green·Refactor 원칙 (STEP 6)
## 9. 수용 기준·DoD (STEP 7)
## 10. 구현 착수 전 체크리스트
## 11. 미결정·리스크
## 12. 문서 이력

제약:
- 프로덕션/테스트 코드·알고리즘 상세 없음
- Report/MagicSquare-Problem-Definition-Report.md와 모순 없음
- 표·체크리스트 위주, 복붙 가능한 수준의 명확성

STEP 8 이전 단계 내용을 새로 논의하지 마십시오.
```

### Turn 8 — Assistant (요약)

- `Report/MagicSquare-TDD-Design-Report.md` — 12절 통합본 작성.

---

## Turn 9 — User (STEP 9 Export)

```text
--------------------------------------------
STEP 9 — Export
--------------------------------------------
다음 순서로만 실행하십시오.

1. Report/MagicSquare-TDD-Design-Report.md 에 STEP 8 통합본 저장
2. Prompt/MagicSquare-TDD-Design-Prompt.md 에
   - 시스템 역할
   - STEP 0~9 User 프롬프트 전문
   - 「다음 턴: 구현 착수」 1개 제안
   을 대화형 transcript 형식으로 저장

구현·테스트 코드 작성은 하지 마십시오.
```

### Turn 9 — Assistant (요약)

- Report 확정(v1.1); 본 Prompt Export 완료.

---

## Turn 10 — User (구현 착수 준비)

```text
MagicSquare-TDD-Design-Report.md를 전제로, 다음만 진행하십시오.
- 테스트 프레임워크 후보 2개 비교 (선택 기준만, 코드 없음)
- STEP 5의 #1 시나리오에 대한 「실패하는 테스트 파일」 스켈레톤 경로·이름만 정의
- 프로젝트 디렉터리 구조 초안 (src/test 폴더만, 파일 내용 없음)
설계 문서 수정·구현 로직은 하지 마십시오.
```

### Turn 10 — Assistant (요약)

- pytest vs JUnit 5 선택 기준표; RED-01 → `tests/unit/grid_input/test_RED01_S1_non_4x4_dimensions.py`.
- `src/magicsquare/...`, `tests/fixtures/grids/red01_input_3x4.json` 디렉터리 초안.

---

## Turn 11 — User (Export — 구현 준비)

```text
다음의 순서로 실행해줘
1. Report 폴더에 보고서 생성해줘
2. 현재까지의 프롬프트 전체를 대화형 프롬프트로 Prompt 폴더에 Export transcript 해줘
```

### Turn 11 — Assistant (요약)

- `Report/MagicSquare-Implementation-Preparation-Report.md` 생성.
- 본 Prompt v2 갱신(Turn 10~11·참조·다음 턴).

---

## Turn A — User (시스템 역할 단독 붙여넣기, 선택)

```text
당신은 TDD·테스트 설계 전문가이며, QA 관점에서 요구를 검증 가능한 설계로 바꿉니다.

나는 4×4 Magic Square 프로그램을 TDD로 구현할 예정입니다.
지금 단계는 「TDD 설계 문서」 작성입니다.

절대 하지 말 것:
- 프로덕션 코드·테스트 코드·의사코드 작성
- 알고리즘·자료구조·성능 최적화 상세 설명
- 특정 언어·프레임워크에 종속된 구현(단, 테스트 도구는 「후보」로만 언급 가능)
- 문제 정의(STEP 1~5)를 뒤집거나 재논의

반드시 할 것:
- 저장소의 문제 정의 보고서를 전제로 진행
- 불변 조건(S·V·M·P, I1~I7)을 테스트·계약·책임 분리로 연결
- Red → Green → Refactor 관점에서 「첫 실패 테스트」부터 설계
- 산출물은 구조화된 Markdown

한 STEP 요청에는 그 STEP의 질문·표·목록만 답합니다.
```

---

## 전체 User 프롬프트 일괄 복사 (Sequential)

<details>
<summary>클릭하여 펼치기 — Full User Prompt Chain (시스템 역할 + STEP 0~9 + Turn 10~11)</summary>

**재현 순서:** Turn A(시스템 역할) → Prompt 0 ~ Prompt 11.  
**전문:** STEP 0~9는 위 **Turn 0 ~ Turn 9** 코드 블록과 동일. Prompt 10·11은 **Turn 10 ~ Turn 11** 과 동일.

| 순서 | User 프롬프트 | 위치 |
|------|---------------|------|
| A | 시스템 역할 | Turn A |
| 0 | 선행 입력 + STEP 0 | Turn 0 |
| 1 | STEP 1 범위 고정 | Turn 1 |
| 2 | STEP 2 입출력 계약 | Turn 2 |
| 3 | STEP 3 Invariant 매핑 | Turn 3 |
| 4 | STEP 4 테스트 전략 | Turn 4 |
| 5 | STEP 5 Red 백로그 8건 | Turn 5 |
| 6 | STEP 6 Green·Refactor | Turn 6 |
| 7 | STEP 7 AC·DoD | Turn 7 |
| 8 | STEP 8 통합 문서 | Turn 8 |
| 9 | STEP 9 Export | Turn 9 |
| 10 | 구현 착수 준비 | Turn 10 |
| 11 | Report + Prompt Export | Turn 11 |

</details>

---

## 다음 턴 제안 (RED-01 TDD)

```text
Report/MagicSquare-TDD-Design-Report.md,
Report/MagicSquare-Implementation-Preparation-Report.md 를 전제로 다음만 진행하십시오.

1. 테스트 프레임워크를 하나 확정하십시오(pytest 또는 JUnit 5 — 이유 1문단, 코드 없음).
2. Implementation-Preparation-Report §3 디렉터리대로 빈 폴더·`__init__.py` 만 생성하십시오.
3. RED-01만: tests/unit/grid_input/test_RED01_S1_non_4x4_dimensions.py 에
   **실패하는 테스트 1개**와 GridInput **최소 스텁**만 작성하여 Green 가능하게 하십시오.
4. RED-02 이상은 작성하지 마십시오 (G-02).

생성(Generator)·n×n·UI·Validator 전체 구현은 하지 마십시오.
```

---

## 참조 파일

| 파일 | 설명 |
|------|------|
| `Report/MagicSquare-TDD-Design-Report.md` | STEP 8 통합 TDD 설계 문서 |
| `Report/MagicSquare-Implementation-Preparation-Report.md` | 프레임워크·RED-01·디렉터리 |
| `Report/MagicSquare-Problem-Definition-Report.md` | 선행 문제 정의 |
| `Prompt/MagicSquare-Problem-Definition-Prompt.md` | 문제 정의 transcript |

---

*End of TDD Design Interactive Prompt Transcript (v2)*
