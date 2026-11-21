# Write tests that can catch mistakes

## Start with the required behaviour

Read the project's test commands, conventions, fixtures and relevant requirements.
Use its existing test framework and the narrowest layer that exercises the
responsible code. Honour required project gates; choose additional work by risk.
A mechanical edit may need only a direct check. Do not invent coverage targets,
mutation quotas or a separate test-plan document.

Before writing an assertion, identify the expected result, its source and a
plausible mistake the check should detect. Use requirements, independently worked
examples, established contracts or a suitable independent reference. Inspect the
implementation to understand inputs and effects, but do not obtain the expected
answer by calling the same function again or copying its algorithm into the test.

Tests that preserve observed legacy behaviour are useful characterization tests.
Label that purpose when it matters. They establish what currently happens;
requirement-backed checks establish whether that behaviour is wanted. If a
material requirement is unresolved, expose the uncertainty instead of inventing
an expectation.

## Exercise the responsible code

Assert through a public interface or observable state so harmless refactors can
keep passing. Run the real logic responsible for the behaviour. Replace external
dependencies at suitable boundaries when needed for control, speed or isolation.
A mock assertion can check a required interaction, but it cannot establish that
the real dependency accepts the request or performs the effect. Use a contract or
integration check when that boundary is part of the risk.

Select relevant boundaries, invalid inputs, failures, retries and state
transitions. Check important effects that must happen and effects that must not,
including duplicate records or messages. Do not add every category to every test.

For example, if repeating an operation ID must preserve one record, call the real
operation twice and inspect the records. Mocking the operation itself and
asserting its preset return value says nothing about duplicate prevention.

Control time, randomness and shared resources where they affect the outcome.
Keep fixtures isolated, await asynchronous work and clean up owned resources.
Prefer an observable completion condition to arbitrary sleeps. Retain seeds and
useful timing details when investigating intermittent failures.

## Establish that the check works

For a repair, show the original defect makes the regression check fail when
practical, then run it against the repair. Confirm the failure concerns the
intended behaviour; an import, setup or service error is different evidence.
Rerun the original scenario as well as a smaller reproduction when relevant.

For a consequential new check, try a representative bad case or isolated fault
and a valid case. The check should reject the former and accept the latter.
Use temporary fixtures or an isolated copy, preserve the intended implementation,
and report when this sensitivity check was unavailable. This need not become a
mutation-testing exercise for every assertion.

Inspect runner discovery, selection, skips and completion. Confirm the relevant
action and assertions were reached. A zero exit code with no relevant tests, only
skipped cases or unfinished asynchronous assertions is not passing evidence.
Legitimate skips remain explicit limits on the result.

## Keep the meaning of success intact

Review changes to assertions, snapshots, fixtures, mocks, generated inputs,
filters and gates against the requirements. Update an expectation when the
requirement or a demonstrated test error justifies it. Preserve useful coverage;
do not relax checks to accommodate a defect or exclude inconvenient cases.

Finish by checking the material acceptance and preservation conditions. Give
relevant evidence for each, or state what remains untested. Keep this in the
existing task record when one is useful.
