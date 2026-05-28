# 4×4 Magic Square — User 엔티티 구현 보고서

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare (`DEV/MagicSquare`) |
| **범위** | ECB `entity` 레이어 — `User` 도메인 엔티티 |
| **작성일** | 2026-05-28 |
| **상태** | 구현·단위 테스트 완료 (7 passed) |
| **선행** | `.cursorrules`, `Report/MagicSquare-TDD-Design-Report.md` |

---

## 1. Executive Summary

`.cursorrules`의 **ECB entity 레이어** 규칙에 따라 `User` 불변 엔티티를 추가했다. 마방진 **격자 검증(RED-01~08)** 과는 별도 트랙이며, QA·학습자 **신원·역할**을 도메인에 표현한다. **pytest 7건** 통과, `src/`·`tests/`·`pyproject.toml` 초기 스캐폴딩이 함께 생성되었다.

---

## 2. 아키텍처 (ECB)

| 레이어 | 본 구현 | 의존 |
|--------|---------|------|
| **entity** | `User`, `UserRole`, `UserValidationError` | stdlib만 |
| control | *(미구현)* | — |
| boundary | *(미구현)* | — |

**의존 방향:** entity는 control·boundary·pytest를 import하지 않음 (`.cursorrules` 준수).

---

## 3. 도메인 모델

### 3.1 `UserRole`

| 값 | 의미 |
|----|------|
| `QA` | QA 운영·검증 담당 |
| `LEARNER` | 학습·TDD 실습 (기본값) |

### 3.2 `User` (frozen dataclass)

| 필드 | 타입 | 불변 조건 |
|------|------|-----------|
| `user_id` | `str` | strip 후 비어 있지 않음 |
| `display_name` | `str` | strip 후 비어 있지 않음 |
| `role` | `UserRole` | 기본 `LEARNER` |
| `email` | `str \| None` | 있으면 비어 있지 않고 기본 이메일 형식 |

### 3.3 공개 API

| 메서드 | 설명 |
|--------|------|
| `User.create(...)` | 검증 후 인스턴스 생성 |
| `with_role(role)` | 역할만 바꾼 새 `User` (불변) |

---

## 4. 파일 목록

| 경로 | 역할 |
|------|------|
| `src/magicsquare/entity/user.py` | 엔티티 구현 |
| `src/magicsquare/entity/__init__.py` | export |
| `tests/unit/entity/test_user.py` | 단위 테스트 (AAA) |
| `tests/conftest.py` | `sample_user` fixture |
| `pyproject.toml` | `pythonpath=src`, pytest 설정 |

---

## 5. 테스트 요약

| # | 테스트 | 검증 |
|---|--------|------|
| 1 | 유효 필드 생성 | strip·필드 값 |
| 2 | 이메일 생략 | `email is None` |
| 3 | 빈 `user_id` | `UserValidationError` |
| 4 | 빈 `display_name` | `UserValidationError` |
| 5 | 잘못된 이메일 | `UserValidationError` |
| 6 | `with_role` | 새 인스턴스·원본 불변 |
| 7 | frozen | `AttributeError` on setattr |

**실행:** `python -m pytest tests/unit/entity/test_user.py -v` → **7 passed**

---

## 6. `.cursorrules` 준수 체크

| 규칙 | 준수 |
|------|------|
| Python 3.10+ · type hints · Google docstring | ✅ |
| ECB entity only | ✅ |
| pytest · AAA · `test_` 접두사 | ✅ |
| `print()` / bare `except` 없음 | ✅ |
| RED-01~08 선행 구현 없음 (User는 별도 요청) | ✅ (범위 외 명시) |

---

## 7. 미구현·다음 단계

- [ ] RED-01: `boundary/grid_input` — 3×4 거부 (TDD 설계 문서 우선)
- [ ] `control/magic_square_validator`
- [ ] `entity/rule_catalog`, `validation_result`
- [ ] User ↔ Validator 연동 (필요 시 control에서)

---

## 8. 참조 문서

| 문서 | 용도 |
|------|------|
| `Report/MagicSquare-TDD-Design-Report.md` | RED 백로그·IN/OUT |
| `Report/MagicSquare-Implementation-Preparation-Report.md` | 디렉터리·RED-01 경로 |
| `Prompt/MagicSquare-Implementation-Session-Prompt.md` | 본 구현 세션 transcript |

---

## 문서 이력

| 버전 | 날짜 | 설명 |
|------|------|------|
| 1.0 | 2026-05-28 | User 엔티티·테스트·스캐폴딩 보고 |

---

*본 보고서는 마방진 판정 알고리즘을 포함하지 않습니다.*
