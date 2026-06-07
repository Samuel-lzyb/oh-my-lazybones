# Test Specification

> **Required before any feature PR.** Define "done" before writing code.

---

## Feature

<!-- Link to design.md -->

## Success Criteria

<!-- When is this feature "done"? Bullet points. -->

- [ ] 
- [ ] 
- [ ] 

## Test Scenarios

### Unit Tests

<!-- One row per test case -->

| # | Scenario | Input | Expected Output |
|---|----------|-------|-----------------|
| 1 | | | |
| 2 | | | |

### Integration Tests

<!-- API-level tests, DB interaction -->

| # | Scenario | Setup | Action | Expected |
|---|----------|-------|--------|----------|
| 1 | | | | |
| 2 | | | | |

### Edge Cases

<!-- Empty input, null, max length, concurrent, timeout, auth failure -->

| # | Edge Case | Expected Behavior |
|---|-----------|-------------------|
| 1 | | |
| 2 | | |

### Regression Tests

<!-- Existing features that must still work -->

| # | Existing Feature | Verification |
|---|-----------------|-------------|
| 1 | | |
| 2 | | |

---

## Test Data

<!-- Any fixtures, seed data, or mock setup needed -->

## Acceptance Gate

<!-- All must be green before the PR can merge -->

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Edge cases covered
- [ ] Regression suite passes
- [ ] CI green (lint + test + security)

---

## AI Self-Assessment

<!-- AI fills this after running all tests -->

| Check | Result |
|-------|--------|
| All scenarios pass? | |
| Edge cases handled? | |
| Regression clean? | |
| Any flaky tests? | |
