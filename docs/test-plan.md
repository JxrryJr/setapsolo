# Supervisor Finder test plan

## Objective and approach

This plan verifies each implemented functional requirement and applies equivalence partition testing. Each input field is divided into representative valid, invalid and boundary partitions so that tests do not repeat the same type of input unnecessarily.

Automated tests are in [`tests/test_app.py`](../tests/test_app.py). Manual checks should be completed against the running application before submission, with screenshots captured as evidence.

## Requirements coverage

| Requirement ID | Requirement | Automated tests | Manual checks |
|---|---|---|---|
| FR-01 | Students can browse staff profiles. | TC-01 | M-01 |
| FR-02 | Students can search and filter staff. | TC-01, TC-02 | M-02 |
| FR-03 | Students can view and save project ideas. | TC-10 | M-03 |
| FR-04 | Staff authenticate before accessing management features. | TC-03–TC-05 | M-04 |
| FR-05 | Staff can add/delete their own interests. | TC-06–TC-07 | M-05 |
| FR-06 | Staff can create/edit/delete their own project ideas. | TC-08–TC-09 | M-06 |
| FR-07 | Staff cannot modify another staff member's content. | TC-09 | M-07 |
| NFR-01 | Interface is responsive and readable. | — | M-08 |
| NFR-02 | Validation gives useful feedback. | TC-06, TC-09, TC-11 | M-09 |

## Automated test cases

| ID | Unit / requirement | Partition and test data | Expected result | Result |
|---|---|---|---|---|
| TC-01 | Directory filtering (FR-01, FR-02) | Valid partition: no filter; valid known interest `Graph theory` | All staff appear without a filter; only the matching supervisor appears with the filter. | Pass |
| TC-02 | Directory search (FR-02) | Invalid/no-match partition: `unfindable-subject` | Clear empty state appears. | Pass |
| TC-03 | Authentication (FR-04) | Valid partition: `ada@university.ac.uk` / `demo123` | Dashboard is displayed. | Pass |
| TC-04 | Authentication (FR-04) | Invalid partition: correct email with wrong password | Error shown; staff session is not created. | Pass |
| TC-05 | Authorisation (FR-04) | Unauthenticated partition: direct request for `/dashboard` | Sign-in page is shown with an explanation. | Pass |
| TC-06 | Interest validation (FR-05, NFR-02) | Boundary values: 1, 2 and 61 characters | 1 and 61 characters rejected; 2 characters accepted. | Pass |
| TC-07 | Interest persistence (FR-05) | Valid new interest; duplicate differing only by case | New interest is stored; duplicate is rejected. | Pass |
| TC-08 | Create project (FR-06) | Valid partition: complete form with accepted select values | Project is saved and shown on dashboard. | Pass |
| TC-09 | Project creation / ownership (FR-06, FR-07) | Invalid: blank title; unauthorised: Ada requests James's project edit URL | Blank title rejected without saving; request returns 403. | Pass |
| TC-10 | Saved project session feature (FR-03) | Valid existing project ID; repeat same request | First request saves project; second removes it. | Pass |
| TC-11 | Profile validation (NFR-02) | Boundaries: department 1/2/101 chars, biography 29/30/1001 chars | Only 2-char department and 30-char biography accepted at lower boundary; over-limit values rejected. | Pass |

## Manual test cases to complete before submission

| ID | Steps | Expected result | Evidence to capture |
|---|---|---|---|
| M-01 | Open the directory; open each staff profile. | All sample profiles and their projects load correctly. | Directory and profile screenshots. |
| M-02 | Search by a staff name, keyword and interest; clear filters. | Results update accurately; no-results state is useful. | Search results screenshot. |
| M-03 | Open a project, save it, then remove it. | Button and confirmation message change correctly. | Project-detail screenshot. |
| M-04 | Sign in using the demo account; sign out; try dashboard URL again. | Access is granted then removed on sign-out. | Dashboard and sign-in screenshot. |
| M-05 | Add an interest, remove it using confirmation dialogue. | Public profile changes appropriately. | Dashboard screenshot. |
| M-06 | Create, edit and delete a project with valid data. | Changes appear in dashboard and public staff profile. | Before/after screenshots. |
| M-07 | Sign in as Ada and attempt to edit project ID 3 directly. | A 403 access-denied page appears and no data changes. | 403 screenshot. |
| M-08 | Check Home, Directory, Profile, Project and Dashboard at 1440px, 768px and 375px widths. | Text remains readable, navigation fits, forms are usable and there is no horizontal scroll. | One desktop and one mobile screenshot. |
| M-09 | Submit every form with a required field blank and with too-short/too-long text. | Field-specific message explains why data cannot be saved. | Validation screenshot. |

## Test environment

- Python 3.13
- Flask 3.1.2
- SQLite (bundled with Python)
- Modern desktop browser; responsive browser emulation for viewport checks

## Exit criteria

All automated tests must pass. All manual cases must be completed, with any failures recorded, fixed where feasible, and re-tested.
