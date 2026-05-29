# MagicSquare Level 1-5 Planning and Verification Report

## Metadata

- Project: Magic Square 4x4 TDD Practice
- Date: 2026-05-28
- Scope: Level 1 (Epic) to Level 5 (Scenario Verification)
- Authoring mode: Planning and verification only (no implementation code, no test code)

---

## 1) Level 1 Epic Summary

- Epic Title: 불변식 기반 사고 훈련 시스템 구축
- Business Goal:
  - 4x4 마방진 문제를 규칙 기반 오라클로 다루고, 계약 중심 검증 체계를 수립한다.
- Learning Goal:
  - Concept -> Invariant -> Contract -> Test 추적성을 기반으로 TDD 사고를 훈련한다.
- Success Criteria (핵심):
  - Domain Logic 고커버리지 목표
  - Boundary 계약 검증 완전성
  - 매직 넘버/정답 하드코딩 금지
  - 리팩토링 후 계약 불변

---

## 2) Level 2 User Journey Summary

Journey는 다음 5단계로 정리되었다.

1. Problem Recognition
2. Contract Definition
3. Domain Separation
4. Dual-Track TDD Progress
5. Regression Protection

핵심 관찰:

- 학습자가 "정답 맞추기"가 아닌 "불변식 기반 설계/검증"으로 문제를 재정의한다.
- 입력/출력/오류 계약을 구현 전에 명시하는 흐름이 고정되었다.
- Boundary와 Domain 책임 분리를 전제로 Story와 시나리오가 연결되었다.

---

## 3) Level 3 User Stories Summary

정의된 주요 Story:

- Story 1: 입력 검증 (Boundary)
- Story 2: 빈칸 좌표 탐색 (Domain)
- Story 3: 누락 숫자 탐색 (Domain)
- Story 4: 마방진 검증 (Domain)
- Story 5: 두 가지 조합 시도 (Domain/Solver + Output Contract)

공통 특징:

- 모든 Story가 보호 대상 Contract/Invariant를 명시
- Acceptance Criteria가 테스트 가능한 문장 중심으로 작성
- Boundary Story와 Domain Story 분리 유지

---

## 4) Level 4 Technical Scenario Summary

정의된 시나리오:

- SC-DOM-SOL-001: small-first 실패 후 reverse 조합 성공
- SC-BND-VAL-001: 빈칸 개수 오류
- SC-BND-VAL-002: 0 제외 중복 오류
- SC-BND-VAL-003: 값 범위 오류

분해 연결:

- Future RED Test ID 후보와 Future Implementation Task 후보가 각 시나리오에 매핑됨

---

## 5) Level 5 Verification Summary

종합 판단:

- 현재 상태: 일부 수정 필요
- 강점:
  - Epic -> Journey -> Story 연결 일관성 높음
  - Boundary/Domain 분리 명확
  - 핵심 Solver 시나리오(SC-DOM-SOL-001) 구조화 완료
- 보완 필요:
  - 4x4 형식 오류 시나리오 보강
  - small-first 즉시 성공 시나리오 보강
  - BlankFinder/MissingNumberFinder 전용 시나리오 보강

---

## 6) Invariant and Contract Traceability Snapshot

- 입력은 4x4여야 한다
- 빈칸은 정확히 2개여야 한다
- 값은 0 또는 1..16이어야 한다
- 0 제외 중복 금지
- 누락 숫자는 정확히 2개
- 누락 숫자 오름차순 반환
- 행/열/대각선 합은 34
- 결과는 int[6], 좌표는 1-index

본 항목은 이후 RED 시나리오 분해의 기준선으로 유지한다.

---

## 7) Next-Step Recommendation (Planning Only)

- Level 5 보완 항목을 우선 반영해 Scenario 집합을 완결한다.
- 이후 RED 테스트 ID 단위로 1건씩 Green 처리 가능한 순서를 확정한다.
- 본 문서는 기획/검증 산출물이며 코드/테스트 구현은 포함하지 않는다.
