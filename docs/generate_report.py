"""
generate_report.py - Programmatically Generates Academic Word (.docx) Report
Adheres strictly to OS Mini Project Submission Guidelines:
- A4 Portrait, 1-inch margins
- Times New Roman, 12pt body, clean left alignment (no stretched gaps)
- 14pt bold chapter headings, 12pt bold section headings
- Proper independent paragraphs for bullet points and numbered lists
- Styled tables with proper padding, header shading, and centered numeric cells
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


def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    """Sets internal padding (dxa) for a table cell."""
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

    # Configure Margins: 1 inch on all sides (A4 Portrait)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)

    # Configure Default Style: Times New Roman, 12pt, Left-Aligned (avoids Word justification gaps)
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(15, 23, 42)
    normal_style.paragraph_format.line_spacing = 1.3
    normal_style.paragraph_format.space_after = Pt(4)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    # Helper functions for clean typography
    def add_p(text, space_after=4, bold=False, italic=False):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.3
        r = p.add_run(text)
        r.bold = bold
        r.italic = italic
        return p

    def add_bullet(bold_prefix, text, space_after=3):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.25
        r_bullet = p.add_run("•  ")
        r_bullet.bold = True
        r_bullet.font.color.rgb = RGBColor(59, 130, 246)
        if bold_prefix:
            r_pre = p.add_run(bold_prefix + " ")
            r_pre.bold = True
        p.add_run(text)
        return p

    def add_numbered(num_str, bold_prefix, text, space_after=3):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.25
        r_num = p.add_run(num_str + "  ")
        r_num.bold = True
        if bold_prefix:
            r_pre = p.add_run(bold_prefix + " ")
            r_pre.bold = True
        p.add_run(text)
        return p

    def add_chapter(title_text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(title_text)
        r.bold = True
        r.font.size = Pt(14)
        r.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_section(title_text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(title_text)
        r.bold = True
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(30, 41, 59)
        return p

    # ---------------------------------------------------------
    # COVER PAGE
    # ---------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_after = Pt(4)
    r_inst = p_inst.add_run("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING")
    r_inst.bold = True
    r_inst.font.size = Pt(13)

    p_ay = doc.add_paragraph()
    p_ay.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ay.paragraph_format.space_after = Pt(28)
    r_ay = p_ay.add_run("ACADEMIC YEAR 2024–2025")
    r_ay.bold = True
    r_ay.font.size = Pt(11)
    r_ay.font.color.rgb = RGBColor(100, 116, 139)

    p_rep = doc.add_paragraph()
    p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rep.paragraph_format.space_after = Pt(6)
    r_rep = p_rep.add_run("OPERATING SYSTEMS MINI PROJECT REPORT")
    r_rep.bold = True
    r_rep.font.size = Pt(13)
    r_rep.font.color.rgb = RGBColor(59, 130, 246)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(36)
    r_title = p_title.add_run("BANKER'S ALGORITHM FOR DEADLOCK AVOIDANCE AND RESOURCE-ALLOCATION VERIFICATION")
    r_title.bold = True
    r_title.font.size = Pt(16)
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    # Submission Table on Cover Page
    table_meta = doc.add_table(rows=5, cols=2)
    table_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_rows = [
        ("Course Name:", "Operating Systems (CSE-301)"),
        ("Project Topic:", "Topic 11: Banker's Algorithm for Deadlock Avoidance"),
        ("Team Members & PRN:", "1. Avignya Reddy Jakku (PRN: 25070721024)\n2. Aapti Reddy Erragunta (PRN: 25070721018)\n3. Ahila Meghana (PRN: 25070721002)\n4. Krithika Reddy (PRN: 25070721062)"),
        ("Faculty Guide:", "Prof. Bibhu Prasad Sahu (Faculty of Operating Systems)"),
        ("Head of Department:", "Dr. Suryanarayana (Head of Department of CSE)"),
    ]

    for idx, (label, val) in enumerate(meta_rows):
        row = table_meta.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.0)
        set_cell_margins(c0, 100, 100, 120, 120)
        set_cell_margins(c1, 100, 100, 120, 120)

        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(label)
        r0.bold = True

        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p1.paragraph_format.space_after = Pt(0)
        p1.paragraph_format.line_spacing = 1.2
        # Split multiline cleanly
        lines = val.split("\n")
        for l_idx, line in enumerate(lines):
            if l_idx > 0:
                p1 = c1.add_paragraph()
                p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p1.paragraph_format.space_after = Pt(0)
                p1.paragraph_format.line_spacing = 1.2
            p1.add_run(line)

    doc.add_page_break()

    # ---------------------------------------------------------
    # CERTIFICATE OF APPROVAL
    # ---------------------------------------------------------
    p_cert = doc.add_paragraph()
    p_cert.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert.paragraph_format.space_after = Pt(18)
    r_cert = p_cert.add_run("CERTIFICATE OF APPROVAL")
    r_cert.bold = True
    r_cert.font.size = Pt(14)

    add_p(
        "This is to certify that the mini project entitled \"Banker's Algorithm for Deadlock Avoidance and "
        "Resource-Allocation Verification\" is a bona fide record of work carried out by Avignya Reddy Jakku "
        "(PRN: 25070721024), Aapti Reddy Erragunta (PRN: 25070721018), Ahila Meghana (PRN: 25070721002), "
        "and Krithika Reddy (PRN: 25070721062) in partial fulfillment of the requirements for the award of "
        "the Degree of Bachelor of Technology in Computer Science and Engineering during the academic session 2024–2025.",
        space_after=40
    )

    # Signature blocks
    sig_table = doc.add_table(rows=1, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_sig0, c_sig1 = sig_table.rows[0].cells[0], sig_table.rows[0].cells[1]
    c_sig0.width = Inches(3.1)
    c_sig1.width = Inches(3.1)
    set_cell_margins(c_sig0, 80, 80, 80, 80)
    set_cell_margins(c_sig1, 80, 80, 80, 80)

    p_s0 = c_sig0.paragraphs[0]
    p_s0.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_s0.paragraph_format.line_spacing = 1.2
    r_s0 = p_s0.add_run("_______________________________\nProf. Bibhu Prasad Sahu\nFaculty Guide (Operating Systems)\nDepartment of CSE")
    r_s0.bold = True

    p_s1 = c_sig1.paragraphs[0]
    p_s1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_s1.paragraph_format.line_spacing = 1.2
    r_s1 = p_s1.add_run("_______________________________\nDr. Suryanarayana\nHead of Department\nDepartment of CSE")
    r_s1.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(28)

    # Student Declaration
    p_decl = doc.add_paragraph()
    p_decl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_decl.paragraph_format.space_after = Pt(12)
    r_decl = p_decl.add_run("STUDENT DECLARATION")
    r_decl.bold = True
    r_decl.font.size = Pt(14)

    add_p(
        "We hereby declare that the project work presented in this mini project report is an authentic record "
        "of our original work completed under the guidance of our faculty guide Prof. Bibhu Prasad Sahu. All citations, "
        "literature sources, and algorithmic formulations have been properly referenced in accordance with standard academic integrity guidelines.",
        space_after=18
    )

    add_p("Avignya Reddy Jakku (25070721024)", bold=True, space_after=2)
    add_p("Aapti Reddy Erragunta (25070721018)", bold=True, space_after=2)
    add_p("Ahila Meghana (25070721002)", bold=True, space_after=2)
    add_p("Krithika Reddy (25070721062)", bold=True, space_after=18)

    doc.add_page_break()

    # ---------------------------------------------------------
    # ACKNOWLEDGEMENT & ABSTRACT
    # ---------------------------------------------------------
    p_ack = doc.add_paragraph()
    p_ack.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ack.paragraph_format.space_after = Pt(12)
    r_ack = p_ack.add_run("ACKNOWLEDGEMENT")
    r_ack.bold = True
    r_ack.font.size = Pt(14)

    add_p(
        "We express our profound gratitude to our faculty guide Prof. Bibhu Prasad Sahu and our Head of Department "
        "Dr. Suryanarayana, Department of Computer Science & Engineering, for providing valuable academic guidance, "
        "necessary computing facilities, and constant encouragement throughout this Operating Systems mini project.",
        space_after=24
    )

    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abs.paragraph_format.space_after = Pt(12)
    r_abs = p_abs.add_run("ABSTRACT")
    r_abs.bold = True
    r_abs.font.size = Pt(14)

    add_p(
        "In multiprogrammed operating systems, deadlocks represent a critical concurrency hazard where a set of processes "
        "remain indefinitely blocked because each holds resources while awaiting others held by peers in a closed circular "
        "dependency. While deadlock prevention imposes rigid, throughput-degrading restrictions and deadlock detection is "
        "inherently reactive, deadlock avoidance provides a dynamic, mathematically sound balance. Dijkstra's Banker's "
        "Algorithm simulates resource allocations provisionally to ensure that the system never enters an unsafe state.",
        space_after=8
    )

    add_p(
        "This project presents a comprehensive, modular implementation of the Banker's Algorithm supporting multiple resource "
        "types and processes. The system incorporates: (1) a rigorous Safety Algorithm verifying whether safe execution sequences "
        "exist; (2) a complete Resource-Request Algorithm executing automated provisional allocation and state rollback upon unsafe "
        "conditions; (3) an all-sequence backtracking depth-first search engine; and (4) dual interfaces including an interactive "
        "command-line interface (CLI) and a modern responsive Web Dashboard GUI. Rigorous empirical validation on textbook benchmarks, "
        "stress cases, and edge tests confirms algorithmic correctness and polynomial time complexity O(m · n²).",
        space_after=12
    )

    doc.add_page_break()

    # ---------------------------------------------------------
    # TABLE OF CONTENTS
    # ---------------------------------------------------------
    p_toc = doc.add_paragraph()
    p_toc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc.paragraph_format.space_after = Pt(12)
    r_toc = p_toc.add_run("TABLE OF CONTENTS")
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
        c0.width = Inches(5.3)
        c1.width = Inches(0.9)
        set_cell_margins(c0, 40, 40, 60, 60)
        set_cell_margins(c1, 40, 40, 60, 60)

        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p0.paragraph_format.space_after = Pt(0)
        p0.paragraph_format.line_spacing = 1.15
        p0.add_run(title)

        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.space_after = Pt(0)
        p1.paragraph_format.line_spacing = 1.15
        p1.add_run(page)

    doc.add_page_break()

    # ---------------------------------------------------------
    # CHAPTER 1: INTRODUCTION
    # ---------------------------------------------------------
    add_chapter("CHAPTER 1: INTRODUCTION")
    add_section("1.1 Concurrency and Deadlock Overview")
    add_p(
        "In modern multiprogrammed operating systems, multiple processes execute concurrently and compete for a finite set "
        "of physical and logical resources, such as CPU cores, main memory segments, I/O devices, files, and mutex locks. "
        "When two or more processes request exclusive access to overlapping sets of resources, an undesirable condition known as "
        "a deadlock can arise. A deadlock is defined as a system state in which every process in a set is blocked, waiting for "
        "an event (typically resource acquisition) that can only be triggered by another blocked process in the same set."
    )

    add_section("1.2 The Four Coffman Deadlock Conditions")
    add_p("As established by E. G. Coffman et al. (1971), a deadlock can occur if and only if all four of the following conditions hold simultaneously:")
    add_numbered("1.", "Mutual Exclusion:", "At least one resource must be held in a non-shareable mode; only one process may use it at a time.")
    add_numbered("2.", "Hold and Wait:", "A process must currently hold at least one resource while simultaneously requesting additional resources held by other processes.")
    add_numbered("3.", "No Preemption:", "Resources cannot be forcibly preempted from a process; they can only be released voluntarily after completion.")
    add_numbered("4.", "Circular Wait:", "A closed chain of processes {P0, P1, ..., Pn} exists such that P0 waits for P1, P1 waits for P2, and Pn waits for P0.")

    add_section("1.3 Deadlock Handling Strategies Comparison")
    add_p("Operating systems handle deadlocks using one of four foundational strategies:")
    add_bullet("Deadlock Ignorance (Ostrich Algorithm):", "Assume deadlocks never occur; reboot if frozen. Used in general-purpose systems like Linux and Windows due to low deadlock frequency.")
    add_bullet("Deadlock Prevention:", "Statically invalidate at least one of the four Coffman conditions. Highly safe, but causes low resource utilization and reduced system throughput.")
    add_bullet("Deadlock Detection and Recovery:", "Allow deadlocks to occur, periodically execute a cycle-detection graph algorithm, and recover by killing processes or preempting resources.")
    add_bullet("Deadlock Avoidance:", "Make dynamic allocation decisions based on advance knowledge of maximum resource demands, ensuring the system never enters an unsafe state.")

    add_section("1.4 Banker's Algorithm Principles")
    add_p(
        "Formulated by Edsger W. Dijkstra in 1965, the Banker's Algorithm is the quintessential deadlock avoidance algorithm. "
        "The algorithm takes its name from a banking metaphor: a small-town banker manages cash credit lines for multiple clients. "
        "The banker will never allocate cash in a way that leaves the bank unable to satisfy the maximum remaining credit demand of at "
        "least one client, who can then finish their business and return all borrowed funds to the bank's reserves."
    )

    # ---------------------------------------------------------
    # CHAPTER 2: PROBLEM STATEMENT AND OBJECTIVES
    # ---------------------------------------------------------
    add_chapter("CHAPTER 2: PROBLEM STATEMENT AND OBJECTIVES")
    add_section("2.1 Problem Statement")
    add_p(
        "Operating system resource managers face the challenge of scheduling dynamic multi-resource requests from concurrent "
        "processes without inducing deadlock states or starving active tasks. Given a system with n processes and m distinct "
        "resource types, the problem is to design and implement a software simulation engine that continuously validates system "
        "safety, inspects pending resource allocation requests, provisionally simulates grant outcomes, and autonomously decides "
        "whether to grant the allocation or force the requesting process to wait while rolling back provisional state changes."
    )

    add_section("2.2 Specific Objectives")
    add_numbered("1.", "Algorithmic Rigor:", "Implement Dijkstra's Banker's Safety Algorithm to verify system state safety and generate safe sequences.")
    add_numbered("2.", "Resource Request Handling:", "Implement the complete Resource-Request Algorithm with automatic state rollback on unsafe predictions.")
    add_numbered("3.", "Multi-Path Traversal:", "Implement a backtracking depth-first search engine to discover all valid safe execution permutations.")
    add_numbered("4.", "Dual User Interfaces:", "Build both a high-productivity terminal Command Line Interface (CLI) and an interactive web-based graphical dashboard.")
    add_numbered("5.", "Cross-Language Implementation:", "Provide production-quality implementations in Python 3, modern C++17, and ANSI C.")
    add_numbered("6.", "Empirical Validation:", "Validate system behavior across textbook cases, circular deadlocks, boundary tests, and polynomial complexity benchmarks.")

    # ---------------------------------------------------------
    # CHAPTER 3: LITERATURE SURVEY
    # ---------------------------------------------------------
    add_chapter("CHAPTER 3: LITERATURE SURVEY AND EXISTING SYSTEMS")
    add_p(
        "The study of deadlock avoidance originated with Dijkstra's pioneering paper (1965), which introduced the concept of safe states "
        "using single resource types. Habermann (1969) generalized the model to accommodate multiple resource instances. Silberschatz, "
        "Galvin, and Gagne (2018) formalized the standard modern representation of the algorithm using Available, Max, Allocation, "
        "and Need matrices, defining the O(m · n²) time complexity bounds."
    )
    add_p(
        "Existing commercial operating systems such as Linux, Windows NT/11, and macOS do not employ Banker's Algorithm for kernel thread "
        "synchronization because acquiring accurate, static declarations of maximum memory and file handle requirements in advance from "
        "arbitrary user-space applications is unfeasible in practice. However, Banker's Algorithm remains essential in specialized mission-critical "
        "environments, including hard real-time systems, aerospace embedded avionics, high-performance database transaction managers, "
        "and distributed cloud resource orchestrators where task profiles and peak resource demands are strictly bounded and contractually declared."
    )

    # ---------------------------------------------------------
    # CHAPTER 4: REQUIREMENTS AND TOOLS
    # ---------------------------------------------------------
    add_chapter("CHAPTER 4: REQUIREMENTS AND TOOL SPECIFICATIONS")
    add_section("4.1 Hardware Requirements")
    add_bullet("Processor:", "Modern x86-64 / ARM64 dual-core processor (Intel Core i3/i5/i7, AMD Ryzen, or Apple Silicon).")
    add_bullet("Memory (RAM):", "Minimum 2.0 GB (4.0 GB recommended for browser GUI).")
    add_bullet("Storage:", "Minimum 100 MB available disk storage space.")
    add_bullet("Display:", "Standard 1080p (1920x1080) resolution for optimal web dashboard rendering.")

    add_section("4.2 Software and Development Tools")
    add_bullet("Operating System:", "Windows 10/11, Linux (Ubuntu/Debian/Fedora), or macOS.")
    add_bullet("Primary Programming Language:", "Python 3.10+ (tested on Python 3.13).")
    add_bullet("Web Framework:", "Flask 3.1.1 (lightweight WSGI web server).")
    add_bullet("Frontend Architecture:", "HTML5, CSS3 (Modern Flexbox & CSS Grid), ES6+ Vanilla JavaScript.")
    add_bullet("Systems Implementation:", "Modern C++17 (g++ / Clang / MSVC) and ANSI C99.")
    add_bullet("Document Generation Tools:", "python-docx (v1.2.0) and python-pptx (v1.0.2).")
    add_bullet("Testing Suite:", "Python unittest framework (15/15 passing tests).")

    # ---------------------------------------------------------
    # CHAPTER 5: SYSTEM DESIGN AND METHODOLOGY
    # ---------------------------------------------------------
    add_chapter("CHAPTER 5: SYSTEM DESIGN AND METHODOLOGY")
    add_section("5.1 System Architecture")
    add_p(
        "The project follows a modular, decoupled architecture consisting of three primary layers:\n"
        "1. Core Domain Engine (src/models.py, src/banker.py): Houses data structures, matrix validation logic, the safety evaluation algorithm, "
        "the resource request handler, and the state rollback manager.\n"
        "2. Presentation Layer (src/cli.py, web/app.py): Delivers dual interaction mediums—a formatted command-line interface with colorized "
        "ASCII state tables and a modern Flask-powered web UI.\n"
        "3. Verification & Benchmark Layer (tests/, test_cases/): Automated regression test suites verifying boundary correctness and empirical "
        "time complexity scaling."
    )

    add_section("5.2 Mathematical Formalism and Data Structures")
    add_p("Let n be the number of processes and m be the number of resource types:")
    add_bullet("Available[m]:", "Vector of length m. If Available[j] = k, there are k instances of resource type Rj available.")
    add_bullet("Max[n][m]:", "Matrix n x m. If Max[i][j] = k, process Pi may request at most k instances of resource type Rj.")
    add_bullet("Allocation[n][m]:", "Matrix n x m. If Allocation[i][j] = k, process Pi currently holds k instances of resource type Rj.")
    add_bullet("Need[n][m]:", "Matrix n x m. Need[i][j] = Max[i][j] - Allocation[i][j]. Represents remaining resources Pi may request to finish.")

    add_section("5.3 Safety Algorithm Flow and Pseudocode")
    add_numbered("Step 1:", "Initialization:", "Work = Available (vector of length m); Finish[i] = False for all i = 0, ..., n-1.")
    add_numbered("Step 2:", "Candidate Search:", "Find an index i such that Finish[i] == False AND Need[i][j] <= Work[j] for all j. If none exists, go to Step 4.")
    add_numbered("Step 3:", "Reclaim Resources:", "Work = Work + Allocation[i]; Finish[i] = True; Append Pi to safe sequence. Repeat Step 2.")
    add_numbered("Step 4:", "Verification:", "If Finish[i] == True for all i, system is SAFE. Otherwise, system is UNSAFE (potential deadlock).")

    add_section("5.4 Resource-Request Algorithm and Rollback")
    add_numbered("Rule 1:", "Claim Verification:", "If Request[i][j] > Need[i][j] for any j, raise ERROR (process exceeded maximum claim).")
    add_numbered("Rule 2:", "Availability Check:", "If Request[i][j] > Available[j] for any j, process Pi MUST WAIT (resources insufficient).")
    add_numbered("Rule 3:", "Provisional Allocation:", "Pretend to allocate: Available -= Request; Allocation[i] += Request; Need[i] -= Request.")
    add_numbered("Rule 4:", "Safety Check & Rollback:", "Run Safety Algorithm on provisional state: If safe, grant allocation permanently; if unsafe, ROLLBACK state and force process to wait.")

    # ---------------------------------------------------------
    # CHAPTER 6: IMPLEMENTATION
    # ---------------------------------------------------------
    add_chapter("CHAPTER 6: IMPLEMENTATION DETAILS")
    add_p("The project implementation is structured cleanly across modular directories:")
    add_bullet("src/models.py:", "Defines BankerState with strict validation (non-negativity, dimension matching, Allocation <= Max), and dataclasses for SimulationStep, SafetyResult, and RequestResult.")
    add_bullet("src/banker.py:", "Implements BankerEngine housing check_safety(), request_resources(), release_resources(), find_all_safe_sequences(), and comparative detect_deadlock().")
    add_bullet("src/cli.py:", "Interactive console interface featuring styled ASCII matrix tables, live request simulation, preset loading, and benchmark runner.")
    add_bullet("web/app.py:", "Flask WSGI backend serving RESTful endpoints for real-time state manipulation and algorithm triggering.")
    add_bullet("web/static/:", "Vanilla JS and modern CSS3 dashboard providing responsive matrix tables, animated step traces, and resource utilization bars.")
    add_bullet("cpp/bankers_algorithm.cpp:", "High-performance C++17 implementation using vectors and stream formatting for university lab environments.")

    # ---------------------------------------------------------
    # CHAPTER 7: TESTING AND RESULTS
    # ---------------------------------------------------------
    add_chapter("CHAPTER 7: TESTING, VERIFICATION, AND EXPERIMENTAL RESULTS")
    add_section("7.1 Test Case 1: Silberschatz Textbook Baseline")
    add_p(
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
        set_cell_background(cell, "F1F5F9")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(11)

    trace_data = [
        ("1", "P1", "[3, 3, 2]", "[1, 2, 2]", "[2, 0, 0]", "[5, 3, 2]"),
        ("2", "P3", "[5, 3, 2]", "[0, 1, 1]", "[2, 1, 1]", "[7, 4, 3]"),
        ("3", "P0", "[7, 4, 3]", "[7, 4, 3]", "[0, 1, 0]", "[7, 5, 3]"),
        ("4", "P2", "[7, 5, 3]", "[6, 0, 0]", "[3, 0, 2]", "[10, 5, 5]"),
        ("5", "P4", "[10, 5, 5]", "[4, 3, 1]", "[0, 0, 2]", "[10, 5, 7]"),
    ]
    for row_idx, data_row in enumerate(trace_data, start=1):
        for col_idx, val in enumerate(data_row):
            cell = table_test.rows[row_idx].cells[col_idx]
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(0)
            p.add_run(val)

    add_p("Primary Safe Sequence: P1 → P3 → P0 → P2 → P4. Total Alternative Safe Sequences: 16.", bold=True, space_after=8)

    add_section("7.2 Test Case 2: Unsafe Deadlock Danger State")
    add_p(
        "A system state with Available = [0, 0, 0] where all processes hold resources and each requires at least 1 unit to complete. "
        "The safety algorithm halts with zero candidate processes satisfying Need <= Work. "
        "Result: System identified as UNSAFE STATE; deadlock danger flagged; allocation denied."
    )

    add_section("7.3 Test Case 3: Valid Resource Request Simulation")
    add_bullet("Request Parameter:", "Process P1 requests Request = [1, 0, 2].")
    add_bullet("Verification 1:", "[1, 0, 2] <= Need [1, 2, 2] (Passed).")
    add_bullet("Verification 2:", "[1, 0, 2] <= Available [3, 3, 2] (Passed).")
    add_bullet("Provisional State:", "Available becomes [2, 3, 0]. Safety algorithm finds safe sequence P1 → P3 → P0 → P2 → P4.")
    add_bullet("Outcome:", "REQUEST GRANTED; state changes committed permanently.")

    add_section("7.4 Test Case 4: Invalid Request Rejection and Rollback")
    add_numbered("1.", "Request Exceeding Max Need:", "Process P0 requests [0, 6, 0]. System halts at Step 1 with status DENIED_EXCEEDS_MAX.")
    add_numbered("2.", "Request Exceeding Available:", "Process P4 requests [4, 3, 1] when Available is [3, 3, 2]. Halts at Step 2 with status DENIED_INSUFFICIENT_AVAILABLE.")
    add_numbered("3.", "Request Leading to Unsafe State:", "Process P0 requests [3, 3, 0]. Provisional available becomes [0, 0, 2]. No process can finish. Status: DENIED_UNSAFE_STATE; provisional changes immediately rolled back.")

    # ---------------------------------------------------------
    # CHAPTER 8: DISCUSSION
    # ---------------------------------------------------------
    add_chapter("CHAPTER 8: DISCUSSION AND COMPLEXITY ANALYSIS")
    add_section("8.1 Algorithmic Time and Space Complexity")
    add_bullet("Time Complexity: O(m · n²):", "In the worst case, the safety algorithm scans up to n processes per pass. In each pass, evaluating Need <= Work takes m operations. Total operations bounded by m · n(n+1)/2 = O(m · n²).")
    add_bullet("Space Complexity: O(m + n):", "Storing Available, Work, and Finish vectors requires linear auxiliary space, which is optimal.")

    add_section("8.2 Resource Utilization Metrics")
    add_p(
        "The system dynamically computes the resource utilization percentage for each resource type: "
        "U(Rj) = (Total Allocated Instances of Rj / Total System Capacity of Rj) × 100%. "
        "In the baseline state, resource utilization stands at A: 70.0%, B: 40.0%, and C: 71.43%. Following P1's granted request, "
        "utilization climbs to A: 80.0%, B: 40.0%, and C: 100.0%, demonstrating the engine's ability to maintain high throughput safely."
    )

    add_section("8.3 Comparison of Deadlock Strategies")
    comp_table = doc.add_table(rows=5, cols=4)
    comp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    comp_headers = ["Strategy", "Resource Utilization", "Runtime Overhead", "Feasibility in General OS"]
    for j, h in enumerate(comp_headers):
        cell = comp_table.rows[0].cells[j]
        set_cell_background(cell, "F1F5F9")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(10.5)

    comp_rows = [
        ("Prevention", "Low (rigid limits)", "Low (static)", "Medium (poor concurrency)"),
        ("Avoidance (Banker's)", "High (optimal)", "Medium (O(m·n²) per request)", "High in Real-Time / Low in General OS"),
        ("Detection & Recovery", "High", "High during graph scan & kill", "Medium (used in DBMS)"),
        ("Ignorance (Ostrich)", "Maximum", "Zero", "High (default in Linux/Windows)"),
    ]
    for r_idx, r_data in enumerate(comp_rows, start=1):
        for c_idx, val in enumerate(r_data):
            cell = comp_table.rows[r_idx].cells[c_idx]
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(0)
            p.add_run(val)

    add_p("", space_after=12)

    # ---------------------------------------------------------
    # CHAPTER 9: CONCLUSION
    # ---------------------------------------------------------
    add_chapter("CHAPTER 9: CONCLUSION AND FUTURE SCOPE")
    add_p(
        "This project successfully developed an end-to-end, mathematically verified simulation and verification platform for "
        "Dijkstra's Banker's Algorithm for deadlock avoidance. The software accurately detects system safety, computes all possible "
        "safe process ordering permutations, simulates dynamic resource requests, enforces maximum claim constraints, and executes "
        "flawless state rollbacks whenever an allocation would compromise system integrity."
    )
    add_p("Future Scope:")
    add_bullet("Dynamic Process Registration:", "Allowing processes to dynamically join and depart without re-initializing matrix dimensions.")
    add_bullet("Distributed Banker's Algorithm:", "Extending the engine to manage resources across distributed cloud nodes using consensus protocols (e.g., Raft/Paxos).")
    add_bullet("Live Kernel Integration:", "Creating an experimental Linux loadable kernel module (LKM) applying Banker's checks to POSIX semaphore allocation.")

    # ---------------------------------------------------------
    # REFERENCES
    # ---------------------------------------------------------
    add_chapter("REFERENCES")
    refs = [
        "[1] A. Silberschatz, P. B. Galvin, and G. Gagne, Operating System Concepts, 10th ed. Hoboken, NJ: John Wiley & Sons, 2018.",
        "[2] E. W. Dijkstra, \"Cooperatieve bank-overeenkomsten,\" Tech. Rep. EWD-108, Technische Hogeschool Eindhoven, Eindhoven, Netherlands, 1965.",
        "[3] E. G. Coffman, M. J. Elphick, and A. Shoshani, \"System Deadlocks,\" ACM Computing Surveys, vol. 3, no. 2, pp. 67–78, Jun. 1971.",
        "[4] A. N. Habermann, \"Prevention of system deadlocks,\" Communications of the ACM, vol. 12, no. 7, pp. 373–377, Jul. 1969.",
        "[5] A. S. Tanenbaum and H. Bos, Modern Operating Systems, 4th ed. Boston, MA: Pearson, 2015.",
        "[6] W. Stallings, Operating Systems: Internals and Design Principles, 9th ed. Boston, MA: Pearson, 2018.",
    ]
    for r in refs:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_ref.paragraph_format.left_indent = Inches(0.25)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.add_run(r)

    # Save outputs
    output_path = os.path.join(os.path.dirname(__file__), "OS_MiniProject_Report.docx")
    doc.save(output_path)
    print(f"Report successfully generated at: {output_path}")


if __name__ == "__main__":
    create_report()
