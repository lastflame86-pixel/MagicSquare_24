# MagicSquare (4×4)

QA 관점에서 **4×4 마방진** 과제의 **문제 인식·정의**를 수행한 프로젝트입니다.  
현재 단계는 **STEP 1 ~ STEP 5 완료**, **구현·설계는 아직 시작하지 않았습니다.**

---

## 프로젝트 목적

| 구분 | 내용 |
|------|------|
| **표면 목표 (지양)** | “4×4 마방진을 만드는 프로그램” |
| **진짜 목표** | 고정 규칙에 대한 **일관된 판정**, (선택) 규칙 충족 **산출**, **반복·자동 검증** 가능한 품질·학습 과제 |
| **훈련 초점** | 규칙 분해, 오라클·수용 기준, 계약(입출력), 회귀, 문제 정의 비판 |

4×4는 계산이 어려워서가 아니라, **검증 규칙이 명확하고 테스트·TDD로 고정하기 좋은 규모**라서 다룹니다.

---

## 도메인 규칙 (요약)

- 격자: **4×4**, 16칸 모두 채움
- 값: **1 ~ 16** 각각 **한 번씩** (중복 없음)
- 합: 모든 **행·열·주대각·부대각**의 합이 같음 → 4×4일 때 **마방 상수 34**

**오라클:** 특정 숫자 배치 한 장이 아니라, 위 **규칙 집합**을 만족하는지로 “맞다”를 판단합니다. (유효한 배치는 여러 개 존재할 수 있음)

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

상세 정의와 STEP별 분석은 [Report](Report/MagicSquare-Problem-Definition-Report.md)를 참고하세요.

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

## 저장소 구조

```
MagicSquare/
├── README.md                                      ← 이 문서
├── Report/
│   └── MagicSquare-Problem-Definition-Report.md  ← STEP 1~5 통합 보고서
└── Prompt/
    ├── MagicSquare-Problem-Definition-Prompt.md    ← 대화형 프롬프트·턴 요약
    └── MagicSquare-Problem-Definition-Row.jsonl    ← 세션 원본 transcript
```

| 경로 | 설명 |
|------|------|
| [Report/MagicSquare-Problem-Definition-Report.md](Report/MagicSquare-Problem-Definition-Report.md) | Executive Summary, Why 분석, Invariant, 미결정 체크리스트 |
| [Prompt/MagicSquare-Problem-Definition-Prompt.md](Prompt/MagicSquare-Problem-Definition-Prompt.md) | 턴별 User 프롬프트, Assistant 요약, 재현·이어가기 가이드 |
| [Prompt/MagicSquare-Problem-Definition-Row.jsonl](Prompt/MagicSquare-Problem-Definition-Row.jsonl) | Cursor 에이전트 세션 JSONL 원본 |

---

## Prompt 재사용 방법

1. [Prompt/MagicSquare-Problem-Definition-Prompt.md](Prompt/MagicSquare-Problem-Definition-Prompt.md)의 **시스템 역할**을 새 대화에 붙입니다.
2. **Turn 1 ~ 6** User 블록을 순서대로 실행합니다.
3. 문서 하단 **「다음 턴 제안」**으로 수용 기준·Given/When/Then 등 후속 STEP을 이어갑니다.

각 STEP에서는 **구현 설계·코드·알고리즘 설명 없이** 문제 정의만 진행하는 것을 전제로 합니다.

---

## 현재 상태

| 항목 | 상태 |
|------|------|
| 문제 인식·정의 (STEP 1~5) | ✅ 완료 |
| 수용 기준·첫 실패 테스트 시나리오 | ⬜ 미착수 |
| 설계·구현·테스트 코드 | ⬜ 미착수 |

### 미결정 사항 (다음 단계)

- [ ] 1순위 기능: **검증** vs **생성**
- [ ] 입력 계약: 완전 격자 / 미완성 / 잘못된 값
- [ ] 출력 계약: 통과·실패·미완성, 위반 규칙 ID 포함 여부
- [ ] 첫 실패 테스트 시나리오 (Given / When / Then)
- [ ] 수용 기준·DoD 문서화

---

## RED 단계 To-Do 리스트

> 이 체크리스트는 test_plan.md 기반으로 생성되었습니다.
> 각 항목은 RED(실패 테스트 작성) 완료 시 체크합니다.

### Track A — UI / Boundary 테스트
- [ ] TC-A-01: grid=None 입력 → 실패 결과 반환 (Happy Path of Failure)
- [ ] TC-A-02: code가 정확히 "INVALID_SIZE" 문자열인지 검증
- [ ] TC-A-03: message가 "Grid must be 4x4." 와 문자 단위 동일한지 검증
- [ ] TC-A-04: grid=None 시 Domain 진입점 0회 호출 (mock/spy 검증)
- [ ] TC-A-05: grid=[] 빈 리스트 → 실패 결과 반환
- [ ] TC-A-06: grid=3×4 크기 불일치 → 실패 결과 반환
- [ ] TC-A-07: 반환 객체 타입이 지정 실패 결과 구조체인지 검증

### Track B — Domain / Logic 테스트
- [ ] TC-B-01: resolve()가 None grid를 직접 받지 않음을 격리 검증
- [ ] TC-B-02: Boundary가 None 분기를 처리 후 resolve() 미호출 확인
- [ ] TC-B-03: resolve() mock이 호출됐을 경우 테스트 실패 처리
- [ ] TC-B-04: AC-FR-01-02~05 범위의 케이스는 이 커밋에 포함하지 않음 확인

### 커버리지 목표
- [ ] Domain Logic: 95%+ (pip install pytest-cov)
- [ ] Boundary Layer: 85%+
- [ ] 전체 TOTAL: 90%+

### 결함 목록 연결
- [x] defect_list.md 생성 및 발견 결함 기록
- [x] 모든 결함 수정 후 회귀 테스트 통과 확인

---

## 권장 진행 순서

```
관찰·정의 (현재) → 수용 기준·테스트 시나리오 → 설계 → TDD 구현 → 회귀·문서 갱신
```

---

## 문서 이력

| 버전 | 날짜 | 설명 |
|------|------|------|
| 1.0 | 2026-05-28 | README 초안 (STEP 1~5 반영) |

---

*본 저장소의 Report·Prompt 문서는 구현·알고리즘 설계를 포함하지 않습니다.*
