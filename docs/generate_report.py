"""
generate_report.py - Programmatically Generates Academic Word (.docx) Report
Adheres strictly to OS Mini Project Submission Guidelines:
- A4 Portrait, 1-inch margins
- Times New Roman, 12pt body, 1.5 line spacing, justified alignment
- 14pt bold chapter headings, 12pt bold section headings
- IEEE citations, tables, and test matrices
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn


def set_cell_background(cell, hex_color):
    """Sets background color of a table cell."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets cell internal padding."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def create_report():
    doc = Document()

    # Configure Margins: 1 inch on all sides
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)  # A4 width
        section.page_height = Inches(11.69)  # A4 height

    # Configure Default Font: Times New Roman, 12pt
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(6)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # ---------------------------------------------------------
    # COVER PAGE
    # ---------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING\nACADEMIC YEAR 2024–2025")
    r_inst.bold = True
    r_inst.font.size = Pt(13)

    doc.add_paragraph().paragraph_format.space_after = Pt(24)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("OPERATING SYSTEMS MINI PROJECT REPORT\n\nBANKER'S ALGORITHM FOR DEADLOCK AVOIDANCE AND RESOURCE-ALLOCATION VERIFICATION")
    r_title.bold = True
    r_title.font.size = Pt(16)
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph().paragraph_format.space_after = Pt(36)

    # Submission Table
    table_meta = doc.add_table(rows=5, cols=2)
    table_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Course Name:", "Operating Systems (CSE-301)"),
        ("Project Topic Number:", "Topic 11: Banker's Algorithm for Deadlock Avoidance"),
        ("Student Name(s):", "Avignya Hjakku (and Team)"),
        ("PRN / Roll Number(s):", "[Student PRN / Roll Number]"),
        ("Faculty Guide:", "[Faculty Guide Name, Designation]"),
    ]
    for idx, (label, val) in enumerate(meta_data):
        row = table_meta.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.paragraphs[0].add_run(label).bold = True
        cell_val.paragraphs[0].add_run(val)
        cell_lbl.width = Inches(2.5)
        cell_val.width = Inches(3.8)

    doc.add_page_break()

    # ---------------------------------------------------------
    # CERTIFICATE & DECLARATION
    # ---------------------------------------------------------
    h_cert = doc.add_paragraph()
    h_cert.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cert = h_cert.add_run("CERTIFICATE OF APPROVAL")
    r_cert.bold = True
    r_cert.font.size = Pt(14)

    p_cert_body = doc.add_paragraph(
        "This is to certify that the mini project entitled \"Banker's Algorithm for Deadlock Avoidance and "
        "Resource-Allocation Verification\" is a bona fide record of work carried out by Avignya Hjakku "
        "in partial fulfillment of the requirements for the award of the Degree of Bachelor of Technology "
        "in Computer Science and Engineering during the academic session 2024–2025."
    )
    p_cert_body.paragraph_format.space_after = Pt(36)

    # Signature blocks
    sig_table = doc.add_table(rows=2, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_table.rows[0].cells[0].paragraphs[0].add_run("_____________________\nFaculty Guide\nDepartment of CSE").bold = True
    sig_table.rows[0].cells[1].paragraphs[0].add_run("_____________________\nHead of Department\nDepartment of CSE").bold = True
    sig_table.rows[0].cells[0].width = Inches(3.2)
    sig_table.rows[0].cells[1].width = Inches(3.2)

    doc.add_paragraph().paragraph_format.space_after = Pt(24)

    h_decl = doc.add_paragraph()
    h_decl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_decl = h_decl.add_run("STUDENT DECLARATION")
    r_decl.bold = True
    r_decl.font.size = Pt(14)

    doc.add_paragraph(
        "We hereby declare that the project work presented in this mini-project report is an authentic record "
        "of our original work completed under the guidance of our faculty guide. All citations, literature sources, "
        "and algorithmic formulations have been properly referenced in accordance with standard academic integrity guidelines."
    )

    doc.add_page_break()

    # ---------------------------------------------------------
    # ACKNOWLEDGEMENT & ABSTRACT
    # ---------------------------------------------------------
    h_ack = doc.add_paragraph()
    h_ack.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ack = h_ack.add_run("ACKNOWLEDGEMENT")
    r_ack.bold = True
    r_ack.font.size = Pt(14)

    doc.add_paragraph(
        "We express our profound gratitude to our faculty guide and the Department of Computer Science & Engineering "
        "for providing essential facilities, valuable mentorship, and academic encouragement throughout the course of "
        "this Operating Systems mini project. We also thank our peers for their collaborative technical discussions."
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(18)

    h_abs = doc.add_paragraph()
    h_abs.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_abs = h_abs.add_run("ABSTRACT")
    r_abs.bold = True
    r_abs.font.size = Pt(14)

    doc.add_paragraph(
        "In multiprogrammed operating systems, deadlocks present a critical concurrency hazard where a set of processes "
        "remain indefinitely blocked because each process holds resources while awaiting others held by peers in a circular "
        "dependency. While deadlock prevention imposes rigid, throughput-degrading restrictions and deadlock detection is "
        "inherently reactive, deadlock avoidance provides a dynamic, mathematically sound middle ground. Dijkstra's Banker's "
        "Algorithm simulates resource allocations provisionally to ensure that the system never enters an unsafe state.\n\n"
        "This project presents a comprehensive, modular implementation of the Banker's Algorithm supporting multiple resource "
        "types and processes. The system incorporates: (1) a rigorous Safety Algorithm verifying whether safe execution sequences "
        "exist; (2) a complete Resource-Request Algorithm executing automated provisional allocation and state rollback upon unsafe "
        "conditions; (3) an all-sequence backtracking depth-first search engine; and (4) dual interfaces including an interactive, "
        "color-coded command-line interface (CLI) and a modern responsive Web Dashboard GUI. Rigorous empirical validation on standard "
        "textbook benchmarks, stress cases, and edge tests confirms algorithmic correctness and polynomial time complexity O(m · n²)."
    )

    doc.add_page_break()

    # ---------------------------------------------------------
    # TABLE OF CONTENTS
    # ---------------------------------------------------------
    h_toc = doc.add_paragraph()
    h_toc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_toc = h_toc.add_run("TABLE OF CONTENTS")
    r_toc.bold = True
    r_toc.font.size = Pt(14)

    toc_items = [
        ("1. Introduction", "1"),
        ("    1.1 Concurrency and Deadlock Overview", "1"),
        ("    1.2 The Four Coffman Deadlock Conditions", "1"),
        ("    1.3 Deadlock Handling Strategies Comparison", "2"),
        ("    1.4 Banker's Algorithm Principles", "2"),
        ("2. Problem Statement and Objectives", "3"),
        ("    2.1 Problem Statement", "3"),
        ("    2.2 Specific Objectives", "3"),
        ("3. Literature Survey and Existing Systems", "4"),
        ("4. Requirements and Tool Specifications", "5"),
        ("    4.1 Hardware Requirements", "5"),
        ("    4.2 Software and Development Tools", "5"),
        ("5. System Design and Methodology", "6"),
        ("    5.1 System Architecture", "6"),
        ("    5.2 Mathematical Formalism and Data Structures", "6"),
        ("    5.3 Safety Algorithm Flow and Pseudocode", "7"),
        ("    5.4 Resource-Request Algorithm and Rollback", "8"),
        ("6. Implementation Details", "9"),
        ("    6.1 Core Algorithmic Engine (Python)", "9"),
        ("    6.2 Interactive CLI Architecture", "10"),
        ("    6.3 Modern Web Dashboard Interface", "11"),
        ("    6.4 Systems-Level C++ / ANSI C Implementation", "11"),
        ("7. Testing, Verification, and Experimental Results", "12"),
        ("    7.1 Test Case 1: Silberschatz Textbook Baseline", "12"),
        ("    7.2 Test Case 2: Unsafe Deadlock Danger State", "13"),
        ("    7.3 Test Case 3: Resource Request Verification & Grant", "14"),
        ("    7.4 Test Case 4: Invalid Request Rejection & Rollback", "14"),
        ("    7.5 Test Case 5: Boundary and Stress Testing", "15"),
        ("8. Discussion and Complexity Analysis", "16"),
        ("    8.1 Time and Space Complexity Formal Analysis", "16"),
        ("    8.2 Resource Utilization Metrics", "16"),
        ("    8.3 Practical Operating Systems Limitations", "17"),
        ("9. Conclusion and Future Scope", "18"),
        ("References", "19"),
        ("Appendix: Project Source Code Listings", "20"),
    ]

    toc_table = doc.add_table(rows=len(toc_items), cols=2)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (title, page) in enumerate(toc_items):
        r = toc_table.rows[idx]
        c0, c1 = r.cells[0], r.cells[1]
        c0.paragraphs[0].add_run(title)
        c1.paragraphs[0].add_run(page)
        c0.width = Inches(5.2)
        c1.width = Inches(1.1)
        c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    doc.add_page_break()

    # ---------------------------------------------------------
    # CHAPTER 1: INTRODUCTION
    # ---------------------------------------------------------
    def add_chapter_title(title_text):
        p = doc.add_paragraph()
        r = p.add_run(title_text)
        r.bold = True
        r.font.size = Pt(14)
        r.font.color.rgb = RGBColor(15, 23, 42)
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(8)
        return p

    def add_section_title(title_text):
        p = doc.add_paragraph()
        r = p.add_run(title_text)
        r.bold = True
        r.font.size = Pt(12)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
        return p

    add_chapter_title("CHAPTER 1: INTRODUCTION")
    add_section_title("1.1 Concurrency and Deadlock Overview")
    doc.add_paragraph(
        "In modern multiprogrammed operating systems, multiple processes execute concurrently and compete for a finite set "
        "of physical and logical resources, such as CPU cores, main memory segments, I/O devices, files, and mutex locks. "
        "When two or more processes request exclusive access to overlapping sets of resources, an undesirable condition known as "
        "a deadlock can arise. A deadlock is defined as a system state in which every process in a set is blocked, waiting for "
        "an event (typically resource acquisition) that can only be triggered by another blocked process in the same set."
    )

    add_section_title("1.2 The Four Coffman Deadlock Conditions")
    doc.add_paragraph(
        "As established by E. G. Coffman et al. (1971), a deadlock can occur if and only if the following four conditions "
        "hold simultaneously within the operating system:\n"
        "1. Mutual Exclusion: At least one resource must be held in a non-shareable mode; only one process may use it at a time.\n"
        "2. Hold and Wait: A process must currently hold at least one resource while simultaneously requesting additional resources "
        "held by other processes.\n"
        "3. No Preemption: Resources cannot be forcibly preempted from a process holding them; they can only be released voluntarily "
        "after the process finishes its task.\n"
        "4. Circular Wait: A closed chain of processes {P0, P1, ..., Pn} must exist such that P0 is waiting for a resource held by P1, "
        "P1 is waiting for P2, and Pn is waiting for a resource held by P0."
    )

    add_section_title("1.3 Deadlock Handling Strategies Comparison")
    doc.add_paragraph(
        "Operating systems handle deadlocks using one of four foundational strategies:\n"
        "• Deadlock Ignorance (Ostrich Algorithm): Assume deadlocks never occur; reboot if frozen (used by general-purpose OS like Linux and Windows due to low frequency).\n"
        "• Deadlock Prevention: Invalidate at least one of the four Coffman conditions statically. While safe, it causes low resource utilization and reduced system throughput.\n"
        "• Deadlock Detection and Recovery: Allow deadlocks to occur, periodically execute a detection graph algorithm, and recover by killing processes or preempting resources.\n"
        "• Deadlock Avoidance: Make dynamic allocation decisions based on advance knowledge of maximum resource demands, ensuring the system never enters an unsafe state."
    )

    add_section_title("1.4 Banker's Algorithm Principles")
    doc.add_paragraph(
        "Formulated by Edsger W. Dijkstra in 1965, the Banker's Algorithm is the quintessential deadlock avoidance algorithm. "
        "The algorithm takes its name from a banking metaphor: a small-town banker manages cash credit lines for multiple clients. "
        "The banker will never allocate cash in a way that leaves the bank unable to satisfy the maximum remaining credit demand of at "
        "least one client, who can then finish their business and return all borrowed funds to the bank's reserves."
    )

    # ---------------------------------------------------------
    # CHAPTER 2: PROBLEM STATEMENT AND OBJECTIVES
    # ---------------------------------------------------------
    add_chapter_title("CHAPTER 2: PROBLEM STATEMENT AND OBJECTIVES")
    add_section_title("2.1 Problem Statement")
    doc.add_paragraph(
        "Operating system resource managers face the challenge of scheduling dynamic multi-resource requests from concurrent "
        "processes without inducing deadlock states or starving active tasks. Given a system with n processes and m distinct "
        "resource types, the problem is to design and implement a software simulation engine that continuously validates system "
        "safety, inspects pending resource allocation requests, provisionally simulates grant outcomes, and autonomously decides "
        "whether to grant the allocation or force the requesting process to wait while rolling back provisional state changes."
    )

    add_section_title("2.2 Specific Project Objectives")
    doc.add_paragraph(
        "The specific technical objectives of this mini project are:\n"
        "1. Algorithmic Rigor: Implement Dijkstra's Banker's Safety Algorithm to verify system state safety and generate safe sequences.\n"
        "2. Resource Request Handling: Implement the complete Resource-Request Algorithm with automatic state rollback on unsafe predictions.\n"
        "3. Multi-Path Traversal: Implement a backtracking depth-first search engine to discover all valid safe execution permutations.\n"
        "4. Dual User Interfaces: Build both a high-productivity terminal Command Line Interface (CLI) and an interactive web-based graphical dashboard.\n"
        "5. Cross-Language Implementation: Provide production-quality implementations in Python 3, modern C++17, and ANSI C.\n"
        "6. Empirical Validation: Validate system behavior across textbook cases, circular deadlocks, boundary tests, and polynomial complexity benchmarks."
    )

    # ---------------------------------------------------------
    # CHAPTER 3: LITERATURE SURVEY
    # ---------------------------------------------------------
    add_chapter_title("CHAPTER 3: LITERATURE SURVEY AND EXISTING SYSTEMS")
    doc.add_paragraph(
        "The study of deadlock avoidance originated with Dijkstra's pioneering paper (1965), which introduced the concept of safe states "
        "using single resource types. Habermann (1969) generalized the model to accommodate multiple resource instances. Silberschatz, "
        "Galvin, and Gagne (2018) formalized the standard modern representation of the algorithm using Available, Max, Allocation, "
        "and Need matrices, defining the O(m · n²) time complexity bounds.\n\n"
        "Existing commercial operating systems such as Linux, Windows NT/11, and macOS do not employ Banker's Algorithm for kernel thread "
        "synchronization because acquiring accurate, static declarations of maximum memory and file handle requirements in advance from "
        "arbitrary user-space applications is unfeasible in practice. However, Banker's Algorithm remains essential in specialized mission-critical "
        "environments, including hard real-time systems, aerospace embedded avionics, high-performance database transaction managers, "
        "and distributed cloud resource orchestrators where task profiles and peak resource demands are strictly bounded and contractually declared."
    )

    # ---------------------------------------------------------
    # CHAPTER 4: REQUIREMENTS AND TOOLS
    # ---------------------------------------------------------
    add_chapter_title("CHAPTER 4: REQUIREMENTS AND TOOL SPECIFICATIONS")
    add_section_title("4.1 Hardware Requirements")
    doc.add_paragraph(
        "• Processor: Modern x86-64 / ARM64 dual-core processor (Intel Core i3/i5/i7, AMD Ryzen, or Apple Silicon).\n"
        "• Memory (RAM): Minimum 2.0 GB (4.0 GB recommended for browser GUI).\n"
        "• Storage: Minimum 100 MB available disk storage space.\n"
        "• Display: Standard 1080p (1920x1080) resolution for optimal web dashboard rendering."
    )

    add_section_title("4.2 Software and Development Tools")
    doc.add_paragraph(
        "• Operating System: Windows 10/11, Linux (Ubuntu/Debian/Fedora), or macOS.\n"
        "• Primary Programming Language: Python 3.10+ (tested on Python 3.13).\n"
        "• Web Framework: Flask 3.1.1 (lightweight WSGI web server).\n"
        "• Frontend Architecture: HTML5, CSS3 (Modern Flexbox & CSS Grid), ES6+ Vanilla JavaScript.\n"
        "• Systems Implementation: Modern C++17 (g++ / Clang / MSVC) and ANSI C99.\n"
        "• Document Generation Tools: python-docx (v1.2.0) and python-pptx (v1.0.2).\n"
        "• Testing Suite: Python unittest framework."
    )

    # ---------------------------------------------------------
    # CHAPTER 5: SYSTEM DESIGN AND METHODOLOGY
    # ---------------------------------------------------------
    add_chapter_title("CHAPTER 5: SYSTEM DESIGN AND METHODOLOGY")
    add_section_title("5.1 System Architecture")
    doc.add_paragraph(
        "The project follows a modular, decoupled architecture consisting of three primary layers:\n"
        "1. Core Domain Engine (`src/models.py`, `src/banker.py`): Houses data structures, matrix validation logic, the safety evaluation algorithm, "
        "the resource request handler, and the state rollback manager.\n"
        "2. Presentation Layer (`src/cli.py`, `web/app.py`): Delivers dual interaction mediums—a formatted command-line interface with colorized "
        "ASCII state tables and a modern Flask-powered web UI.\n"
        "3. Verification & Benchmark Layer (`tests/`, `test_cases/`): Automated regression test suites verifying boundary correctness and empirical "
        "time complexity scaling."
    )

    add_section_title("5.2 Mathematical Formalism and Data Structures")
    doc.add_paragraph(
        "Let n be the number of processes and m be the number of resource types:\n"
        "• Available: Vector of length m. If Available[j] = k, there are k instances of resource type Rj available.\n"
        "• Max: An n × m matrix. If Max[i][j] = k, process Pi may request at most k instances of resource type Rj.\n"
        "• Allocation: An n × m matrix. If Allocation[i][j] = k, process Pi is currently allocated k instances of resource type Rj.\n"
        "• Need: An n × m matrix. Need[i][j] = Max[i][j] - Allocation[i][j]. Represents remaining resources Pi may need to finish."
    )

    add_section_title("5.3 Safety Algorithm Pseudocode")
    doc.add_paragraph(
        "Algorithm 1: Banker's Safety Algorithm\n"
        "Input: Available vector, Allocation matrix, Need matrix\n"
        "Output: is_safe (Boolean), safe_sequence (List of processes)\n\n"
        "1. Let Work be a vector of length m, initialized to Available.\n"
        "   Let Finish be a boolean array of length n, initialized to [False, ..., False].\n"
        "2. Search for an index i such that:\n"
        "      a. Finish[i] == False, and\n"
        "      b. Need[i][j] <= Work[j] for all j ∈ {0, ..., m-1}.\n"
        "3. If such an i is found:\n"
        "      Work = Work + Allocation[i]\n"
        "      Finish[i] = True\n"
        "      Append Pi to safe_sequence\n"
        "      Repeat Step 2.\n"
        "4. If Finish[i] == True for all i ∈ {0, ..., n-1}, the system is SAFE.\n"
        "   Otherwise, the system is UNSAFE (potential deadlock)."
    )

    add_section_title("5.4 Resource-Request Algorithm and Rollback")
    doc.add_paragraph(
        "Algorithm 2: Resource-Request Algorithm\n"
        "Let Request[i] be the vector of requested resources by process Pi.\n\n"
        "Step 1: If Request[i][j] > Need[i][j] for any j, raise ERROR (process exceeded maximum claim).\n"
        "Step 2: If Request[i][j] > Available[j] for any j, process Pi MUST WAIT (resources insufficient).\n"
        "Step 3: Simulate provisional allocation:\n"
        "        Available = Available - Request[i]\n"
        "        Allocation[i] = Allocation[i] + Request[i]\n"
        "        Need[i] = Need[i] - Request[i]\n"
        "Step 4: Execute Safety Algorithm on the provisional state:\n"
        "        • If SAFE: Commit allocation permanently. Process Pi continues.\n"
        "        • If UNSAFE: Rollback to previous state:\n"
        "          Available = Available + Request[i]\n"
        "          Allocation[i] = Allocation[i] - Request[i]\n"
        "          Need[i] = Need[i] + Request[i]\n"
        "          Process Pi must wait."
    )

    # ---------------------------------------------------------
    # CHAPTER 6: IMPLEMENTATION
    # ---------------------------------------------------------
    add_chapter_title("CHAPTER 6: IMPLEMENTATION DETAILS")
    doc.add_paragraph(
        "The project implementation is structured cleanly across modular directories:\n"
        "• `src/models.py`: Defines BankerState with comprehensive validation (non-negativity, dimension matching, Allocation <= Max), "
        "and dataclasses for SimulationStep, SafetyResult, and RequestResult.\n"
        "• `src/banker.py`: Implements BankerEngine housing `check_safety()`, `request_resources()`, `release_resources()`, "
        "`find_all_safe_sequences()`, and comparative `detect_deadlock()`.\n"
        "• `src/cli.py`: Interactive console interface featuring styled ASCII matrix tables, live request simulation, preset loading, and benchmark runner.\n"
        "• `web/app.py`: Flask WSGI backend serving RESTful endpoints for real-time state manipulation and algorithm triggering.\n"
        "• `web/static/`: Vanilla JS and modern CSS3 dashboard providing responsive matrix tables, animated step traces, and resource utilization bars.\n"
        "• `cpp/bankers_algorithm.cpp`: High-performance C++17 implementation using vectors and stream formatting for university lab environments."
    )

    # ---------------------------------------------------------
    # CHAPTER 7: TESTING AND RESULTS
    # ---------------------------------------------------------
    add_chapter_title("CHAPTER 7: TESTING, VERIFICATION, AND EXPERIMENTAL RESULTS")
    add_section_title("7.1 Test Case 1: Silberschatz Textbook Baseline")
    doc.add_paragraph(
        "The system was evaluated against the canonical 5-process, 3-resource benchmark from Silberschatz Operating System Concepts (Chapter 8):\n"
        "Available = [3, 3, 2]; Allocation = [P0: [0,1,0], P1: [2,0,0], P2: [3,0,2], P3: [2,1,1], P4: [0,0,2]]; "
        "Max = [P0: [7,5,3], P1: [3,2,2], P2: [9,0,2], P3: [2,2,2], P4: [4,3,3]]."
    )

    # Table of Safety Trace
    table_test = doc.add_table(rows=6, cols=6)
    table_test.alignment = WD_TABLE_ALIGNMENT.CENTER
    test_headers = ["Step", "Process", "Work (Before)", "Need", "Allocation", "Work (After)"]
    for j, h in enumerate(test_headers):
        cell = table_test.rows[0].cells[j]
        cell.paragraphs[0].add_run(h).bold = True
        set_cell_background(cell, "E2E8F0")

    trace_data = [
        ("1", "P1", "[3, 3, 2]", "[1, 2, 2]", "[2, 0, 0]", "[5, 3, 2]"),
        ("2", "P3", "[5, 3, 2]", "[0, 1, 1]", "[2, 1, 1]", "[7, 4, 3]"),
        ("3", "P0", "[7, 4, 3]", "[7, 4, 3]", "[0, 1, 0]", "[7, 5, 3]"),
        ("4", "P2", "[7, 5, 3]", "[6, 0, 0]", "[3, 0, 2]", "[10, 5, 5]"),
        ("5", "P4", "[10, 5, 5]", "[4, 3, 1]", "[0, 0, 2]", "[10, 5, 7]"),
    ]
    for row_idx, data_row in enumerate(trace_data, start=1):
        for col_idx, val in enumerate(data_row):
            table_test.rows[row_idx].cells[col_idx].paragraphs[0].add_run(val)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    doc.add_paragraph("Primary Safe Sequence: P1 → P3 → P0 → P2 → P4. Total Alternative Safe Sequences: 16.")

    add_section_title("7.2 Test Case 2: Unsafe Deadlock Danger State")
    doc.add_paragraph(
        "A system state with Available = [0, 0, 0] where all processes hold resources and each requires at least 1 unit to complete. "
        "The safety algorithm halts with zero candidate processes satisfying Need <= Work. "
        "Result: System identified as UNSAFE STATE; deadlock danger flagged; allocation denied."
    )

    add_section_title("7.3 Test Case 3: Valid Resource Request Simulation")
    doc.add_paragraph(
        "In the baseline state, process P1 requests Request = [1, 0, 2].\n"
        "• Check 1: [1, 0, 2] <= Need [1, 2, 2] → Valid.\n"
        "• Check 2: [1, 0, 2] <= Available [3, 3, 2] → Valid.\n"
        "• Provisional state evaluated: Available becomes [2, 3, 0].\n"
        "• Safety algorithm executes: Finds valid safe sequence P1 → P3 → P0 → P2 → P4.\n"
        "• Outcome: REQUEST GRANTED; state changes committed."
    )

    add_section_title("7.4 Test Case 4: Invalid Request Rejection and Rollback")
    doc.add_paragraph(
        "1. Request Exceeding Max Need: Process P0 requests [0, 6, 0]. System halts at Step 1 with status DENIED_EXCEEDS_MAX.\n"
        "2. Request Exceeding Available: Process P4 requests [4, 3, 1] when Available is [3, 3, 2]. Halts at Step 2 with status DENIED_INSUFFICIENT_AVAILABLE.\n"
        "3. Request Leading to Unsafe State: Process P0 requests [3, 3, 0]. Provisional available becomes [0, 0, 2]. No process can finish. "
        "Status: DENIED_UNSAFE_STATE; provisional changes immediately rolled back."
    )

    # ---------------------------------------------------------
    # CHAPTER 8: DISCUSSION
    # ---------------------------------------------------------
    add_chapter_title("CHAPTER 8: DISCUSSION AND COMPLEXITY ANALYSIS")
    add_section_title("8.1 Algorithmic Time and Space Complexity")
    doc.add_paragraph(
        "• Time Complexity: In the worst case, the safety algorithm scans up to n unfinished processes in each pass. "
        "In each pass, verifying Need[i][j] <= Work[j] takes m operations. If one process completes per pass, the total operations "
        "are bounded by: T(n, m) = m · n + m · (n - 1) + ... + m · 1 = m · n(n + 1)/2 = O(m · n²).\n"
        "• Space Complexity: Storing Available, Work, and Finish vectors requires O(m + n) auxiliary space, which is optimal."
    )

    add_section_title("8.2 Resource Utilization Metrics")
    doc.add_paragraph(
        "The system dynamically computes the resource utilization percentage for each resource type: "
        "U(Rj) = (Total Allocated Instances of Rj / Total System Capacity of Rj) × 100%. "
        "In the baseline state, resource utilization stands at A: 70.0%, B: 40.0%, and C: 71.43%. Following P1's granted request, "
        "utilization climbs to A: 80.0%, B: 40.0%, and C: 100.0%, demonstrating the engine's ability to maintain high throughput safely."
    )

    add_section_title("8.3 Comparison of Deadlock Strategies")
    
    comp_table = doc.add_table(rows=5, cols=4)
    comp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    comp_headers = ["Strategy", "Resource Utilization", "Runtime Overhead", "Feasibility in General OS"]
    for j, h in enumerate(comp_headers):
        cell = comp_table.rows[0].cells[j]
        cell.paragraphs[0].add_run(h).bold = True
        set_cell_background(cell, "E2E8F0")

    comp_rows = [
        ("Prevention", "Low (rigid limits)", "Low (static)", "Medium (poor concurrency)"),
        ("Avoidance (Banker's)", "High (optimal)", "Medium (O(m·n²) per request)", "High in Real-Time / Low in General OS"),
        ("Detection & Recovery", "High", "High during graph scan & kill", "Medium (used in DBMS)"),
        ("Ignorance (Ostrich)", "Maximum", "Zero", "High (default in Linux/Windows)"),
    ]
    for r_idx, r_data in enumerate(comp_rows, start=1):
        for c_idx, val in enumerate(r_data):
            comp_table.rows[r_idx].cells[c_idx].paragraphs[0].add_run(val)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # ---------------------------------------------------------
    # CHAPTER 9: CONCLUSION
    # ---------------------------------------------------------
    add_chapter_title("CHAPTER 9: CONCLUSION AND FUTURE SCOPE")
    doc.add_paragraph(
        "This project successfully developed an end-to-end, mathematically verified simulation and verification platform for "
        "Dijkstra's Banker's Algorithm for deadlock avoidance. The software accurately detects system safety, computes all possible "
        "safe process ordering permutations, simulates dynamic resource requests, enforces maximum claim constraints, and executes "
        "flawless state rollbacks whenever an allocation would compromise system integrity.\n\n"
        "Future Scope:\n"
        "1. Dynamic Process Registration: Allowing processes to dynamically join and depart without re-initializing matrix dimensions.\n"
        "2. Distributed Banker's Algorithm: Extending the engine to manage resources across distributed cloud nodes using consensus protocols (e.g., Raft/Paxos).\n"
        "3. Live Kernel Integration: Creating an experimental Linux loadable kernel module (LKM) applying Banker's checks to POSIX semaphore allocation."
    )

    # ---------------------------------------------------------
    # REFERENCES
    # ---------------------------------------------------------
    add_chapter_title("REFERENCES")
    refs = [
        "[1] A. Silberschatz, P. B. Galvin, and G. Gagne, Operating System Concepts, 10th ed. Hoboken, NJ: John Wiley & Sons, 2018.",
        "[2] E. W. Dijkstra, \"Cooperatieve bank-overeenkomsten,\" Tech. Rep. EWD-108, Technische Hogeschool Eindhoven, Eindhoven, Netherlands, 1965.",
        "[3] E. G. Coffman, M. J. Elphick, and A. Shoshani, \"System Deadlocks,\" ACM Computing Surveys, vol. 3, no. 2, pp. 67–78, Jun. 1971.",
        "[4] A. N. Habermann, \"Prevention of system deadlocks,\" Communications of the ACM, vol. 12, no. 7, pp. 373–377, Jul. 1969.",
        "[5] A. S. Tanenbaum and H. Bos, Modern Operating Systems, 4th ed. Boston, MA: Pearson, 2015.",
        "[6] W. Stallings, Operating Systems: Internals and Design Principles, 9th ed. Boston, MA: Pearson, 2018.",
    ]
    for r in refs:
        p_ref = doc.add_paragraph(r)
        p_ref.paragraph_format.space_after = Pt(4)

    # Output directory
    output_path = os.path.join(os.path.dirname(__file__), "OS_MiniProject_Report.docx")
    doc.save(output_path)
    print(f"Report successfully generated at: {output_path}")


if __name__ == "__main__":
    create_report()
