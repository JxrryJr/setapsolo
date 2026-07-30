# Chapter 1: Problem Specification

## 1.1 Introduction

Final-year students must identify an appropriate project and supervisor. The problem definition states that staff members have areas of teaching and research interest, can propose project ideas, and need to keep this information current. Students need an accessible way to explore that information while choosing a supervisor. Supervisor Finder is a web prototype that addresses this by presenting searchable staff profiles and project ideas, with a staff-only area for managing profile content.

## 1.2 Requirements elicitation process

### Method selection

A short semi-structured interview was selected as the single requirements-gathering method. The method used a consistent question guide while allowing participants to explain why a feature or piece of information would be useful. This was appropriate because the problem concerns an early-stage user journey: students may describe difficulties in choosing a supervisor more effectively in their own words than through a fixed rating-scale questionnaire.

The interview guide covered current approaches to finding a supervisor, information required about staff and project ideas, preferred search methods, likely difficulties, and usability expectations. Participants were informed that their names would not be collected and that their anonymised responses would be used in coursework. Both participants confirmed this before their responses were used.

### Participants and data collection

Two students took part and are referred to as `S1` and `S2`. `S1` was about to enter their final year; `S2` was not yet a final-year student. Neither had previous experience of selecting a final-year-project supervisor. This makes them prospective users rather than experienced users, which is useful for identifying first-time expectations but limits the ability to generalise the findings.

The same question guide was used for both participants. The questions asked how they would currently find a supervisor, what profile and project information they would need, how they would search, what barriers they expected, and what would make the system easy or frustrating to use. The original anonymised responses should be retained as Appendix A evidence.

### Analysis process

The responses were analysed manually in four steps:

1. Each response was read and summarised without changing its meaning.
2. Short descriptive codes were attached, including `interest filtering`, `keyword/name search`, `staff expertise`, `clear project explanation`, `contact route`, `comparison difficulty`, and `simple navigation`.
3. Related codes were grouped into themes.
4. Each theme was translated into one or more user requirements, with its source recorded using participant and question identifiers.

The following table shows examples of the coding process.

| Data extract / summary | Initial code | Theme |
|---|---|---|
| S1 preferred filtering by interest area because it gives quick, focused results. | Interest filtering; focused results | Efficient discovery |
| S2 preferred keywords and name search when a particular supervisor is already known. | Keyword search; name search | Efficient discovery |
| S1 wanted to know what staff teach, can help with, whether interests align, and what they are like. | Expertise; biography; compatibility | Informed comparison |
| S2 wanted a brief summary of specialisms and what staff can still help with. | Specialism; support scope | Informed comparison |
| S2 wanted unfamiliar programming languages and terminology explained. | Clear language; project explanation | Understandable project information |
| S1 wanted easy contact, while S2 did not know who to approach or where to begin. | Contact route; starting point | Clear next step |
| S1 described crowded, slow and difficult navigation as frustrating. | Avoid clutter; performance; navigation | Usable interface |

### Patterns identified

Three principal patterns were identified. First, both participants wanted the system to reduce the effort of finding relevant people. S1 emphasised filtering by interest, while S2 described keyword and name search. This supports offering both filter-based and keyword-based discovery rather than forcing users to browse a long unstructured list.

Second, both participants needed enough contextual information to compare supervisors. They did not only want a name: they wanted staff expertise, teaching or support areas, a biography, and project information that explains unfamiliar technologies or terminology. The public profile therefore needs to communicate compatibility as well as factual details.

Third, participants described uncertainty as a main barrier. S1 mentioned difficulty weighing options, and S2 did not know who to approach or where to begin. The interface should provide a clear route from discovery to an individual staff profile and contact details, while avoiding crowded layouts and difficult navigation.

## 1.3 User requirements

The following requirements were produced from the interview analysis and the stated problem definition. `S1` and `S2` identify interview evidence; `PD` identifies a requirement directly stated in the problem definition. This distinction is important because no staff members were available for interview.

| ID | User requirement | Source |
|---|---|---|
| UR-01 | Students shall be able to browse a directory of staff members. | S1 Q2; S2 Q2; PD |
| UR-02 | Students shall be able to search for a staff member by name or keyword. | S2 Q4 |
| UR-03 | Students shall be able to filter staff by area of interest. | S1 Q4 |
| UR-04 | Students shall be able to view a staff profile containing a biography, areas of expertise, teaching or support information, and areas of interest. | S1 Q3, Q7; S2 Q3, Q9; PD |
| UR-05 | Students shall be able to view proposed project ideas with clear summaries and suggested skills or technologies. | S1 Q5; S2 Q5; PD |
| UR-06 | Students shall be able to access a clear route for contacting a staff member from the profile. | S1 Q7; S2 Q6, Q7 |
| UR-07 | Students shall be able to use a simple, uncluttered and easy-to-navigate interface. | S1 Q7, Q8; S2 Q6 |
| UR-08 | Staff shall be able to update their public profile information. | PD |
| UR-09 | Staff shall be able to add and remove their own areas of interest. | PD |
| UR-10 | Staff shall be able to add, update and delete their own proposed project ideas. | PD |
| UR-11 | Staff shall only be able to modify content associated with their own profile. | PD; system security inference |

## 1.4 System requirements

### Functional requirements

| ID | System requirement | Derived from |
|---|---|---|
| FR-01 | The system shall display a staff directory containing the name, department and short biography of each staff member. | UR-01, UR-04 |
| FR-02 | The system shall provide a keyword search that matches staff names, departments and biography content. | UR-02 |
| FR-03 | The system shall provide an interest-area filter and show only staff associated with the selected interest. | UR-03 |
| FR-04 | The system shall display a detailed public staff profile containing biography, department, interest areas, contact email and project ideas. | UR-04, UR-06 |
| FR-05 | The system shall display a project-detail page containing title, summary, suggested skills, project type, availability and supervisor details. | UR-05 |
| FR-06 | The system shall provide a mailto contact link from every public staff profile. | UR-06 |
| FR-07 | The system shall require staff authentication before management pages can be accessed. | UR-08, UR-09, UR-10, UR-11 |
| FR-08 | The system shall allow an authenticated staff member to update their department and biography. | UR-08 |
| FR-09 | The system shall allow an authenticated staff member to add and delete interest areas attached to their profile. | UR-09 |
| FR-10 | The system shall allow an authenticated staff member to create, edit and delete project ideas attached to their profile. | UR-10 |
| FR-11 | The system shall deny access when a staff member attempts to edit or delete another staff member's project or interest. | UR-11 |

### Non-functional requirements

| ID | System requirement | Justification / source |
|---|---|---|
| NFR-01 | The user interface shall use clear page headings, consistent navigation, readable labels and visible feedback messages. | S1 Q7–Q8; S2 Q6 |
| NFR-02 | The public directory shall provide useful no-results feedback instead of a blank page. | S1 Q4; S2 Q4; supports clear navigation |
| NFR-03 | Pages and filter interactions shall complete within two seconds using the prototype data set under normal local conditions. | S1 Q8 identified slow systems as frustrating. |
| NFR-04 | The interface shall remain usable on desktop and mobile-width screens without horizontal scrolling. | Requirement for an accessible web prototype; verified through manual responsive checks. |
| NFR-05 | Forms shall validate required fields and show specific messages without saving invalid data. | Supports understandable, low-error interaction (UR-07). |
| NFR-06 | Management functions shall enforce authentication and ownership checks. | UR-11 |
| NFR-07 | The codebase shall separate presentation templates, application rules and database persistence to support maintenance. | Prototype maintainability requirement. |

### Requirements traceability

Each user requirement has at least one corresponding system requirement: UR-01 maps to FR-01; UR-02 to FR-02; UR-03 to FR-03; UR-04 to FR-01 and FR-04; UR-05 to FR-05; UR-06 to FR-04 and FR-06; UR-07 to NFR-01 to NFR-05; UR-08 to FR-07 and FR-08; UR-09 to FR-07 and FR-09; UR-10 to FR-07 and FR-10; and UR-11 to FR-07 and FR-11.

## 1.5 Limitations

The elicitation used two prospective student participants and no staff participants because of limited time before the deadline. The results should therefore be treated as indicative rather than representative of all students and staff. Staff-management requirements were taken directly from the problem definition and should be validated with staff stakeholders in a future iteration. The small sample nevertheless identified consistent patterns around focused discovery, clear information, contactability and low-complexity navigation, which were incorporated into the prototype.

## Appendix A: Interview guide and evidence

The raw, anonymised `S1` and `S2` responses should be included in the final submission appendix alongside the interview questions. The participant information section should state that no names were recorded and both participants consented to anonymised use in this coursework.
