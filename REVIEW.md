# Engineering Workflows 2.2.0 — revised review candidate

The original candidate was prepared on 21 November 2026 from
[`f5b5c09d66697d64c56658d71624a4973d90760e`](https://github.com/Vidcar/EngineeringWorkflows/tree/f5b5c09d66697d64c56658d71624a4973d90760e).
These notes describe the revised ZIP reviewed before promotion.

## Start here

| File | What to review |
| --- | --- |
| [Workflows](engineering-workflows/SKILL.md) | The main route through a task and the testing read trigger. |
| [Shared rules](engineering-workflows/references/contract.md) | Scope, review depth, actual test execution and evidence at completion. |
| [Testing](engineering-verify/references/testing.md) | Practical guidance for meaningful assertions, mocks, failure cases and test maintenance. |
| [Check](engineering-check/SKILL.md) | Review of changed tests, snapshots, fixtures, selected checks and gates. |
| [Evaluation kit](evals/README.md) | Seven repeatable tasks and evaluator controls. |

## What changed

- Rewrote all seven entrypoints and their prose references with direct verbs,
  short paragraphs and clearer steps. Kept the same skill names and roles.
- Kept shared rules in one place. Added explicit reading triggers so an agent
  writing tests loads the testing guidance even when it does not delegate.
- Added a focused testing reference covering independent expectations, useful
  characterization tests, real code behind mocks, relevant failure paths,
  forbidden effects, deterministic fixtures and meaningful regression checks.
- Required evidence that selected checks actually ran and completed. Empty,
  skipped or unfinished checks cannot support a passing claim.
- Made changes to test expectations and check settings an explicit review target.
  Legitimate requirement changes and demonstrated test errors can still justify
  updating expectations.
- Clarified lead continuity when the user changes the requested result, and kept
  repairs within the assignment's allowed writes. Review packages leave active
  installations unchanged.
- Kept [Bend guidance](engineering-verify/references/bend.md) short and conditional.
  It adds no mandatory proof step, language migration or unverified tool syntax.
- Fixed the snapshot helper's handling of repository paths ending in whitespace.
  Added regressions for a missing trimmed path and a neighbouring repository.
- Added the evaluation kit outside the skill folders, so its fixtures and
  evaluator answers do not enter ordinary agent context. Preserved licenses,
  icons and invocation policies; simplified the UI descriptions and prompts.

## Size

Counts below include frontmatter and use whitespace-separated words.

| Main skill | Before | Candidate |
| --- | ---: | ---: |
| Workflows | 351 | 354 |
| Verify | 271 | 278 |
| Check | 261 | 282 |
| Measure | 257 | 256 |
| Arena | 322 | 308 |
| Campaign | 329 | 314 |
| Configure | 310 | 305 |
| **Total** | **2,101** | **2,097** |

The main files are 33–49 lines. The new testing reference is 586 words and the
conditional Bend reference is 229 words. Neither needs loading for every task.

## Follow-up fixes

- Verify's testing guide is a required pack file. The validator rejects a 2.2.0
  pack containing the 2.1.0 Verify folder.
- The snapshot suite checks a trailing nonbreaking space with real Git and covers
  both a missing trimmed path and a neighbouring repository. It exercises a
  trailing ASCII space on filesystems that distinguish it from the trimmed path.
  The suite also checks the executable mode in the Git index on Windows.
- The evaluation helper records relative paths with forward slashes on all
  platforms. Each check keeps its report, probe results and logs together in
  its own directory. The command output includes the report location.

## Windows verification

Tested on native Windows with Python 3.12.10 and Git 2.56.0.windows.4.

- All seven skills passed the skill-format and pack validators. The mixed-version
  pack with 2.1.0 Verify was rejected because the required guide was missing.
- The pack suite ran 55 cases. **53 passed** and two were skipped because the
  filesystem aliases trailing ASCII spaces and lacks a working-tree executable
  bit. The nonbreaking-space and Git-index executable-mode checks passed.
- All **eight** evaluation-helper controls passed, including the check that
  repeated scoring preserves a failed report and its probe files.
- These checks cover the packaged files and helpers.

With Python and PyYAML available, rerun from the extracted pack root:

```powershell
python -B engineering-workflows/scripts/validate_pack.py --root .
python -B -m unittest discover -s engineering-workflows/scripts -p 'test_*.py' -v
python -B -m unittest discover -s evals -p 'test_*.py' -v
```

## Installation verification

After installation on Windows, Codex listed all seven 2.2.0 skills as enabled
user skills in the repository and in a separate working directory. Each resolved
to its installed folder with no duplicate entries or load errors. The installed
pack passed validation and matched the 49 skill files from the revised ZIP.

## Agent trials from the original review

The original review reported two fresh-context scenarios that used supplied
candidate files and isolated task workspaces.

| Scenario | Observed result |
| --- | --- |
| A passing test mocks the defective function | The agent replaced it with real assertions and left production code unchanged. Eight tests ran: seven exposed the defect and one checked input preservation. All eight passed against a temporary reference repair. |
| A command exits successfully after selecting no tests | The agent reported that zero tests establish no passing behaviour. It separately ran the documented test, reported its limited coverage and left source files unchanged. |

An initial empty-selection trial exposed a Python-version difference: the standard
unittest CLI returned exit 5. The fixture now supplies a small runner that returns
zero for an empty selection. Its control executes that exact runner for zero and
one selected tests, and the corrected task was tried in a fresh context.

These are focused examples, not a measured improvement rate. The trials supplied
the candidate files directly; they do not establish automatic discovery in another
host. Five other scenarios are provided for later trials. Evaluation reports keep
manual judgment separate from objective checks and retain failed attempts.

## Try the candidate

Use [README.md](README.md) for validation and installation options. Keep the seven
skill folders together. Keep `evals/` with the source for evaluation; it does not
need to be installed with the skills. Review and install through your host's
supported process when you are ready.
