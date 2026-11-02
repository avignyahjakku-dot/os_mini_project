"""
generate_academic_report.py
Generates the comprehensive academic Word (.docx) report for the Operating Systems Mini Project:
"Banker's Algorithm for Deadlock Avoidance Simulator"
Matching strictly the format, structure, and aesthetics of the SIT Symbiosis demo PDF.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(DOCS_DIR, "images")
OUTPUT_DOCX = os.path.join(DOCS_DIR, "OS_MiniProject_Report.docx")

def set_cell_background(cell, hex_color):
    """Sets background shading of a table cell."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    """Sets internal padding (dxa) for a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    """Applies clean subtle borders to a table."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_report():
    doc = Document()

    # 1. Page Configuration: A4 Portrait, 1.0-inch margins
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        s.page_width = Inches(8.27)
        s.page_height = Inches(11.69)

    # 2. Typography Styles: Times New Roman, 12pt body
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(20, 20, 20)
    normal_style.paragraph_format.line_spacing = 1.25
    normal_style.paragraph_format.space_after = Pt(4)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    # Helper functions
    def add_p(text, space_after=4, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.LEFT):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.25
        r = p.add_run(text)
        r.bold = bold
        r.italic = italic
        return p

    def add_bullet(text, space_after=3):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.25
        p.add_run("•  " + text)
        return p

    def add_num(num_str, text, space_after=3):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.25
        p.add_run(f"{num_str}.  {text}")
        return p

    def add_chapter(title):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(title)
        r.bold = True
        r.font.size = Pt(13)
        return p

    def add_section(title):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(title)
        r.bold = True
        r.font.size = Pt(12)
        return p

    def add_fig(caption, img_name, width_inches=5.8):
        img_path = os.path.join(IMG_DIR, img_name)
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(4)
            p_img.add_run().add_picture(img_path, width=Inches(width_inches))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_cap.paragraph_format.space_after = Pt(8)
        r = p_cap.add_run(caption)
        r.bold = True
        r.font.size = Pt(11)

    # =========================================================
    # PAGE 1: TITLE PAGE (Exact Symbiosis SIT Template)
    # =========================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(10)
    p_inst.paragraph_format.space_after = Pt(2)
    r1 = p_inst.add_run("SYMBIOSIS INSTITUTE OF TECHNOLOGY, HYDERABAD\n")
    r1.bold = True
    r1.font.size = Pt(13)
    r1.font.color.rgb = RGBColor(160, 0, 0)
    
    r2 = p_inst.add_run("Symbiosis International (Deemed University), Pune\n")
    r2.font.size = Pt(11)
    r2.bold = True
    
    r3 = p_inst.add_run("Established under section 3 of the UGC Act, 1956\nRe-Accredited by NAAC with 'A++' Grade | Awarded Category – I by UGC")
    r3.font.size = Pt(9.5)
    r3.italic = True
    r3.font.color.rgb = RGBColor(80, 80, 80)

    doc.add_paragraph().paragraph_format.space_after = Pt(45)

    p_op = doc.add_paragraph()
    p_op.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_op.paragraph_format.space_after = Pt(16)
    r_op = p_op.add_run("OPERATING SYSTEMS")
    r_op.bold = True
    r_op.font.size = Pt(22)
    r_op.font.color.rgb = RGBColor(180, 20, 20)

    p_mpr = doc.add_paragraph()
    p_mpr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mpr.paragraph_format.space_after = Pt(45)
    r_mpr = p_mpr.add_run("MINI PROJECT REPORT")
    r_mpr.bold = True
    r_mpr.font.size = Pt(15)
    r_mpr.font.color.rgb = RGBColor(26, 82, 118)

    # Details Table
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(meta_table, color="000000", sz="6")
    
    meta_data = [
        ("Course Name", "Operating Systems"),
        ("Mini Project Title", "Banker's Algorithm for Deadlock Avoidance Simulator"),
        ("Student Name(s)", "Avignya Reddy Jakku\nAapti Erragunta\nAhila Meghana\nKrithika Reddy"),
        ("PRN / Roll Number(s)", "25070721024\n25070721018\n25070721002\n25070721062"),
        ("Faculty Guide", "Dr. Bibhuprasad Sahu"),
    ]

    for idx, (lbl, val) in enumerate(meta_data):
        row = meta_table.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.3)
        c1.width = Inches(3.9)
        set_cell_margins(c0, 100, 100, 120, 120)
        set_cell_margins(c1, 100, 100, 120, 120)

        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(lbl)
        r0.bold = True
        r0.font.size = Pt(11)

        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1.paragraph_format.space_after = Pt(0)
        p1.paragraph_format.line_spacing = 1.15
        lines = val.split("\n")
        for l_i, line in enumerate(lines):
            if l_i > 0:
                p1 = c1.add_paragraph()
                p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p1.paragraph_format.space_after = Pt(0)
                p1.paragraph_format.line_spacing = 1.15
            r1 = p1.add_run(line)
            r1.font.size = Pt(11)

    doc.add_paragraph().paragraph_format.space_after = Pt(45)

    # Footer Metadata
    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_foot.paragraph_format.line_spacing = 1.3
    r_ay = p_foot.add_run("Academic Year  :  2026\nSemester  :  3rd\nSection  :  Batch-1")
    r_ay.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================
    # PAGE 2: ACKNOWLEDGEMENT & ABSTRACT
    # =========================================================
    add_chapter("ACKNOWLEDGEMENT")
    add_p(
        "We would like to express our sincere gratitude to our Operating Systems faculty guide "
        "Dr. Bibhuprasad Sahu for providing valuable guidance, continuous support and encouragement throughout the "
        "development of this mini project. His suggestions and feedback helped us understand the "
        "concepts of deadlock avoidance, resource-allocation graphs, and Dijkstra's Banker's Algorithm and improve our implementation.",
        space_after=8
    )
    add_p(
        "We extend our heartfelt thanks to the Head of the Department Dr. Suryanarayana and the Department of Computer "
        "Science and Engineering for providing us with the opportunity, resources and facilities required "
        "to complete this project successfully.",
        space_after=8
    )
    add_p(
        "We are also grateful to our institute, Symbiosis Institute of Technology (SIT), Hyderabad, for providing a supportive learning environment and access "
        "to the necessary software tools and laboratory facilities.",
        space_after=8
    )
    add_p(
        "This project helped us strengthen our knowledge of operating system concepts, C "
        "programming, process management, dynamic resource allocation and deadlock avoidance algorithms. We would also "
        "like to thank our classmates and friends for their valuable suggestions, discussions and support "
        "during the development and testing phases.",
        space_after=20
    )

    add_chapter("ABSTRACT")
    add_p(
        "Deadlock is a critical state in multi-programming operating systems where concurrent processes are permanently "
        "blocked from execution because each process holds resources while waiting for resources currently held by others in a "
        "circular dependency. Deadlock avoidance is an active strategy that ensures the operating system never transitions from a "
        "safe state to an unsafe state where deadlock could occur.",
        space_after=8
    )
    add_p(
        "This mini project develops a menu-driven Banker's Algorithm Simulator for Deadlock Avoidance using "
        "the C programming language. The simulator models a multi-process, multi-resource system featuring n = 5 processes "
        "(P0 to P4) and m = 3 resource types (R0, R1, R2). It implements the complete Banker's safety verification algorithm and "
        "dynamic resource-request evaluation logic.",
        space_after=8
    )
    add_p(
        "The user interacts with a clean console interface allowing them to display allocation matrices, execute the safety "
        "algorithm to determine if a safe execution sequence exists, and dynamically request resources for any process. The system "
        "computes the Need matrix (Need[i][j] = Maximum[i][j] - Allocation[i][j]) and validates incoming requests against maximum claims "
        "and available capacities. A provisional allocation is performed, followed by safety verification using a Work vector. If the "
        "resulting state remains safe, the request is permanently granted; if unsafe, the system executes an immediate state rollback "
        "and orders the process to wait.",
        space_after=8
    )
    add_p(
        "The project uses arrays, functions, loops, conditional statements and temporary state vectors to simulate resource "
        "distribution and ensure robust error handling against negative inputs and invalid process indices. "
        "The simulator is an educational model that provides students with practical insight into how conservative resource-allocation "
        "policies prevent deadlock in operating systems without incurring the overhead of runtime process termination.",
        space_after=14
    )

    doc.add_page_break()

    # =========================================================
    # PAGE 3: TABLE OF CONTENTS
    # =========================================================
    add_chapter("TABLE OF CONTENTS")
    
    toc_items = [
        "1. Introduction",
        "2. Problem Statement and Objectives",
        "3. Literature / Existing System",
        "4. Requirements and Tools",
        "5. System Design / Methodology",
        "6. Implementation",
        "7. Testing and Results",
        "8. Discussion",
        "9. Conclusion and Future Scope",
        "10. References",
        "Appendix A – Sample Input & System Allocation State",
        "Appendix B – Source Code Submission",
    ]
    
    for item in toc_items:
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.space_after = Pt(4)
        p_toc.paragraph_format.line_spacing = 1.25
        r_toc = p_toc.add_run(item)
        r_toc.font.size = Pt(12)

    doc.add_page_break()

    # =========================================================
    # PAGE 4-5: 1. INTRODUCTION & 2. PROBLEM STATEMENT & OBJECTIVES
    # =========================================================
    add_chapter("1. INTRODUCTION")
    add_section("1.1 Background")
    add_p(
        "An operating system manages computer hardware and system resources, providing an environment in which "
        "application programs execute efficiently. A process is a program in execution. In a multi-programming or "
        "multi-tasking system, multiple processes compete for a finite set of shared system resources such as CPU cycles, "
        "memory partitions, I/O devices, files, and database locks. If resource allocation is uncoordinated, circular wait conditions "
        "can emerge where processes become permanently halted, resulting in deadlock."
    )

    add_section("1.2 Deadlock Avoidance and Banker's Algorithm")
    add_p(
        "Deadlock avoidance is an active dynamic strategy where the operating system evaluates every resource request before granting it. "
        "If allocating the requested resources leaves the system in a safe state—meaning there exists at least one order of process execution "
        "that allows every process to satisfy its maximum claim and terminate—the request is granted. Otherwise, the process must wait. "
        "Dijkstra's Banker's Algorithm is the classic and mathematically proven deadlock avoidance algorithm for systems with multiple instances "
        "of each resource type."
    )

    add_section("1.3 Relevance to Operating Systems")
    add_p(
        "The project is directly related to process management, concurrency control, and deadlock handling in the Operating "
        "Systems syllabus (CSE-301). It bridges the gap between theoretical classroom definitions and real-world implementation, "
        "showing how matrix data structures and vector arithmetic are used by operating system kernels to maintain system integrity."
    )

    add_section("1.4 Scope")
    add_p(
        "The simulator is a menu-driven educational console application implemented in C. It models 5 processes (P0 to P4) "
        "and 3 resource types (A, B, C). It supports initial safety state verification, dynamic process resource requests, "
        "provisional allocation testing, automatic rollback upon detecting unsafe states, and full matrix visualization. "
        "The simulator assumes cooperative processes that eventually release held resources upon completion."
    )

    add_chapter("2. PROBLEM STATEMENT AND OBJECTIVES")
    add_section("2.1 Problem Statement")
    add_p(
        "Students often learn the Banker's Algorithm through theoretical textbook examples but find it difficult to visualize "
        "how dynamic resource requests alter system vectors, how the Work vector reclaims resources during execution traces, "
        "and how state rollbacks prevent catastrophic deadlocks. The problem is to develop a C-based simulator that accepts "
        "process requests interactively, computes the Need matrix, evaluates safety, displays step-by-step results, and demonstrates "
        "instant state rollbacks."
    )

    add_section("2.2 Objectives")
    add_bullet("To understand the fundamental role of deadlock avoidance in operating systems.")
    add_bullet("To implement Dijkstra's Banker's Safety Algorithm and Resource-Request Algorithm in C.")
    add_bullet("To dynamically compute the Need matrix from the Maximum and Allocation matrices.")
    add_bullet("To validate process requests against maximum claims and system available limits.")
    add_bullet("To perform provisional resource allocations and verify resultant system safety.")
    add_bullet("To execute immediate state rollbacks when an allocation leads to an unsafe state.")
    add_bullet("To determine and display the topological safe execution sequence (e.g., P1 -> P3 -> P4 -> P0 -> P2).")
    add_bullet("To provide an interactive menu for matrix inspection, safety checks, and simulation.")

    add_section("2.3 Expected Outcome")
    add_p(
        "The expected outcome is a working menu-driven C program that allows a user to inspect resource matrices, "
        "execute safety verification, submit real-time resource requests, observe whether requests are granted or denied, "
        "and understand the practical mechanics of deadlock avoidance."
    )

    add_chapter("3. LITERATURE / EXISTING SYSTEM")
    add_section("3.1 Existing Approach")
    add_p(
        "CPU resource allocation and deadlock problems are conventionally taught using static textbook examples and manually "
        "solved tabular matrices. Students manually calculate Need matrices and iteratively update Available vectors on paper. "
        "While useful for basic conceptual understanding, manual calculation becomes tedious, slow, and prone to arithmetic mistakes "
        "when multiple sequential requests must be evaluated."
    )

    add_section("3.2 Proposed System")
    add_p(
        "The proposed system automates all matrix arithmetic and algorithmic safety checks. The simulator maintains state vectors "
        "in memory, computes the Need matrix automatically, and evaluates the safety algorithm in polynomial time O(m * n^2). "
        "It supports non-destructive provisional allocations, meaning the system state is only permanently updated if safety is guaranteed."
    )

    add_section("3.3 Limitations of the Existing Manual Method")
    add_bullet("Manual calculation is slow and impractical for multi-step requests.")
    add_bullet("Human error in vector addition or subtraction can lead to incorrect safety conclusions.")
    add_bullet("Manual methods cannot easily demonstrate instant rollbacks or boundary violations.")
    add_bullet("Visualizing alternative topological safe sequences requires recalculating all permutations.")

    # =========================================================
    # PAGE 5-6: 4. REQUIREMENTS AND TOOLS
    # =========================================================
    add_chapter("4. REQUIREMENTS AND TOOLS")
    add_section("4.1 Hardware Requirements")
    add_p("Table 4.1: Hardware Requirements", bold=True, space_after=3)

    t_hw = doc.add_table(rows=6, cols=2)
    t_hw.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_hw)
    hw_rows = [
        ("Component", "Minimum Requirement"),
        ("Processor", "Modern desktop or laptop processor (Intel / AMD / Apple Silicon)"),
        ("RAM", "2 GB or higher"),
        ("Storage", "A few MB for project source code and executable binaries"),
        ("Input", "Keyboard"),
        ("Output", "Monitor or display console"),
    ]
    for idx, (c0, c1) in enumerate(hw_rows):
        r = t_hw.rows[idx]
        r.cells[0].width = Inches(2.2)
        r.cells[1].width = Inches(4.0)
        set_cell_margins(r.cells[0], 60, 60, 80, 80)
        set_cell_margins(r.cells[1], 60, 60, 80, 80)
        if idx == 0:
            set_cell_background(r.cells[0], "F1F5F9")
            set_cell_background(r.cells[1], "F1F5F9")
        r.cells[0].paragraphs[0].add_run(c0).bold = (idx == 0)
        r.cells[1].paragraphs[0].add_run(c1).bold = (idx == 0)

    add_section("4.2 Software Requirements")
    add_p("Table 4.2: Software Requirements", bold=True, space_after=3)

    t_sw = doc.add_table(rows=6, cols=2)
    t_sw.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_sw)
    sw_rows = [
        ("Software / Tool", "Purpose"),
        ("C Language (C99 / C11)", "Core algorithmic implementation"),
        ("GCC Compiler", "Compiling and optimizing source code"),
        ("Visual Studio Code / Terminal", "Source code editing and interactive execution"),
        ("Windows / Linux / macOS", "Cross-platform operating system environments"),
        ("Microsoft Word / PDF Viewer", "Preparing and viewing the academic project report"),
    ]
    for idx, (c0, c1) in enumerate(sw_rows):
        r = t_sw.rows[idx]
        r.cells[0].width = Inches(2.2)
        r.cells[1].width = Inches(4.0)
        set_cell_margins(r.cells[0], 60, 60, 80, 80)
        set_cell_margins(r.cells[1], 60, 60, 80, 80)
        if idx == 0:
            set_cell_background(r.cells[0], "F1F5F9")
            set_cell_background(r.cells[1], "F1F5F9")
        r.cells[0].paragraphs[0].add_run(c0).bold = (idx == 0)
        r.cells[1].paragraphs[0].add_run(c1).bold = (idx == 0)

    add_section("4.3 Programming Concepts Used")
    add_bullet("Two-dimensional arrays to represent Allocation, Maximum, and Need matrices.")
    add_bullet("One-dimensional integer vectors to store Available, Work, and Request arrays.")
    add_bullet("Boolean/integer tracking arrays (Finish) to record satisfied process execution status.")
    add_bullet("Modular functions (calculateNeed, displayMatrices, safetyAlgorithm, requestResources).")
    add_bullet("Loops (while, for) and conditional decision branching to implement algorithmic search.")
    add_bullet("Provisional allocation logic with non-destructive state restoration (rollback).")

    add_section("4.4 Implementation Code Provided by Team")
    add_p(
        "As part of the project specification and laboratory implementation, the team designed and implemented a concise, "
        "self-contained C program implementing the Banker's Algorithm simulator. The code defines P = 5 processes, R = 3 resource types, "
        "and encapsulates matrix calculations, safety searches, and resource request evaluations into clean procedural functions. "
        "The full complete code listing is presented in Appendix B."
    )

    # =========================================================
    # PAGE 6-10: 5. SYSTEM DESIGN / METHODOLOGY
    # =========================================================
    add_chapter("5. SYSTEM DESIGN / METHODOLOGY")
    add_section("5.1 System Architecture")
    add_p(
        "The simulator follows an input–processing–output architecture. The user selects operations through the interactive menu, "
        "the core engine performs vector operations and safety analysis, and the output module displays formatted matrices and status messages."
    )
    add_p("Table 5.1: System Architecture", bold=True, space_after=3)

    t_arch = doc.add_table(rows=6, cols=2)
    t_arch.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_arch)
    arch_rows = [
        ("Stage", "Description"),
        ("Input Module", "Reads user choices, process IDs, and requested resource vectors"),
        ("State Storage Module", "Stores Allocation, Maximum, Need, and Available matrices"),
        ("Safety Engine", "Executes Dijkstra's safety algorithm using Work and Finish vectors"),
        ("Request & Rollback Module", "Validates constraints, performs provisional allocation, and rolls back if unsafe"),
        ("Display Module", "Prints formatted matrix tables, safe sequences, and status banners"),
    ]
    for idx, (c0, c1) in enumerate(arch_rows):
        r = t_arch.rows[idx]
        r.cells[0].width = Inches(2.2)
        r.cells[1].width = Inches(4.0)
        set_cell_margins(r.cells[0], 60, 60, 80, 80)
        set_cell_margins(r.cells[1], 60, 60, 80, 80)
        if idx == 0:
            set_cell_background(r.cells[0], "F1F5F9")
            set_cell_background(r.cells[1], "F1F5F9")
        r.cells[0].paragraphs[0].add_run(c0).bold = (idx == 0)
        r.cells[1].paragraphs[0].add_run(c1).bold = (idx == 0)

    add_fig("Figure 5.1: System Architecture of Banker's Algorithm Simulator", "fig_5_1_architecture.png", width_inches=6.0)

    add_section("5.2 Process Data Structure and Matrices")
    add_p(
        "The system state is defined by four core data structures:\n"
        "1. Available[R]: Vector of length R. If Available[j] = k, there are k instances of resource type Rj available.\n"
        "2. Max[P][R]: P x R matrix. Max[i][j] defines the maximum claim of process Pi for resource Rj.\n"
        "3. Allocation[P][R]: P x R matrix. Allocation[i][j] defines instances of Rj currently allocated to Pi.\n"
        "4. Need[P][R]: P x R matrix. Need[i][j] = Max[i][j] - Allocation[i][j] defines remaining resources needed."
    )
    add_p("Table 5.2: Process and Matrix Attributes", bold=True, space_after=3)

    t_attr = doc.add_table(rows=6, cols=2)
    t_attr.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_attr)
    attr_rows = [
        ("Attribute", "Description"),
        ("Allocation[P][R]", "Resources currently held by each process"),
        ("Maximum[P][R]", "Maximum claim declared by each process before execution"),
        ("Need[P][R]", "Remaining resources required by process: Need = Maximum - Allocation"),
        ("Available[R]", "Currently unallocated resources available in the system pool"),
        ("Work[R] & Finish[P]", "Auxiliary tracking vectors used during safety verification"),
    ]
    for idx, (c0, c1) in enumerate(attr_rows):
        r = t_attr.rows[idx]
        r.cells[0].width = Inches(2.2)
        r.cells[1].width = Inches(4.0)
        set_cell_margins(r.cells[0], 60, 60, 80, 80)
        set_cell_margins(r.cells[1], 60, 60, 80, 80)
        if idx == 0:
            set_cell_background(r.cells[0], "F1F5F9")
            set_cell_background(r.cells[1], "F1F5F9")
        r.cells[0].paragraphs[0].add_run(c0).bold = (idx == 0)
        r.cells[1].paragraphs[0].add_run(c1).bold = (idx == 0)

    add_section("5.3 Algorithmic Formulation")
    add_p("5.3.1 Safety Algorithm", bold=True)
    add_p(
        "Let Work be an integer vector of length R and Finish be a boolean vector of length P.\n"
        "1. Initialize: Work = Available; Finish[i] = 0 for all i = 0, 1, ..., P-1.\n"
        "2. Find an index i such that: Finish[i] == 0 and Need[i][j] <= Work[j] for all j = 0, ..., R-1. If no such i exists, go to Step 4.\n"
        "3. Work = Work + Allocation[i]; Finish[i] = 1; append Pi to SafeSequence; go to Step 2.\n"
        "4. If Finish[i] == 1 for all i, the system is in a SAFE STATE. Otherwise, the system is in an UNSAFE STATE."
    )

    add_p("5.3.2 Resource-Request Algorithm", bold=True)
    add_p(
        "When process Pi issues a request vector Request[R]:\n"
        "1. If Request[j] <= Need[i][j] for all j, proceed to Step 2. Else raise error (request exceeds maximum claim).\n"
        "2. If Request[j] <= Available[j] for all j, proceed to Step 3. Else process Pi must wait (insufficient resources).\n"
        "3. Provisionally alter state:\n"
        "   Available[j] = Available[j] - Request[j]\n"
        "   Allocation[i][j] = Allocation[i][j] + Request[j]\n"
        "   Need[i][j] = Need[i][j] - Request[j]\n"
        "4. Run Safety Algorithm. If safe -> GRANT request permanently. If unsafe -> ROLLBACK state:\n"
        "   Available[j] = Available[j] + Request[j]\n"
        "   Allocation[i][j] = Allocation[i][j] - Request[j]\n"
        "   Need[i][j] = Need[i][j] + Request[j], and process Pi must wait."
    )

    add_fig("Figure 5.2: Classification of Deadlock Handling Strategies", "fig_5_2_classification.png", width_inches=6.0)

    add_section("5.4 Mathematical Formulation and Invariants")
    add_p("Table 5.3: Core Mathematical Formulas and Invariants", bold=True, space_after=3)

    t_form = doc.add_table(rows=5, cols=2)
    t_form.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_form)
    form_rows = [
        ("Metric / Invariant", "Formula / Rule"),
        ("Need Matrix Computation", "Need[i][j] = Maximum[i][j] - Allocation[i][j]"),
        ("Total System Resource Conservation", "Total[j] = Available[j] + sum(Allocation[i][j] for i=0 to P-1)"),
        ("Claim Boundary Invariant", "0 <= Allocation[i][j] <= Maximum[i][j] for all i, j"),
        ("Safe Sequence Condition", "Need[s_k][j] <= Work_{k-1}[j] for all j=0 to R-1"),
    ]
    for idx, (c0, c1) in enumerate(form_rows):
        r = t_form.rows[idx]
        r.cells[0].width = Inches(2.2)
        r.cells[1].width = Inches(4.0)
        set_cell_margins(r.cells[0], 60, 60, 80, 80)
        set_cell_margins(r.cells[1], 60, 60, 80, 80)
        if idx == 0:
            set_cell_background(r.cells[0], "F1F5F9")
            set_cell_background(r.cells[1], "F1F5F9")
        r.cells[0].paragraphs[0].add_run(c0).bold = (idx == 0)
        r.cells[1].paragraphs[0].add_run(c1).bold = (idx == 0)

    add_section("5.5 Overall Execution Flow")
    add_num("1", "Start the program.")
    add_num("2", "Initialize static process matrices: Allocation, Maximum, and Available.")
    add_num("3", "Compute initial Need matrix using calculateNeed().")
    add_num("4", "Display the main menu to the user.")
    add_num("5", "Read and validate menu choice (1 to 5).")
    add_num("6", "Option 1: Display current Allocation, Maximum, Need, and Available matrices.")
    add_num("7", "Option 2: Execute safetyAlgorithm() and display the topological safe sequence.")
    add_num("8", "Option 3: Prompt process ID and request vector; execute requestResources() with provisional allocation and safety check; grant or rollback.")
    add_num("9", "Option 4: Clear console screen; Option 5: Terminate program cleanly.")

    add_fig("Figure 5.3: Flowchart of Banker's Algorithm Simulator", "fig_5_3_flowchart.png", width_inches=4.8)

    add_section("5.6 Methodology")
    add_p(
        "The simulator preserves system stability through deterministic verification. Whenever a process requests resources, "
        "the simulator does not permanently commit changes until the safety algorithm confirms that all P processes can complete. "
        "If even one process remains unsatisfied, the provisional changes are immediately reverted. This prevents race conditions "
        "and circular deadlock."
    )

    # =========================================================
    # PAGE 10: 6. IMPLEMENTATION
    # =========================================================
    add_chapter("6. IMPLEMENTATION")
    add_section("6.1 Program Modules")
    add_p("Table 6.1: Program Functions and Responsibilities", bold=True, space_after=3)

    t_mod = doc.add_table(rows=7, cols=2)
    t_mod.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_mod)
    mod_rows = [
        ("Function", "Responsibility"),
        ("calculateNeed(int need[P][R])", "Computes Need matrix: Need[i][j] = Maximum[i][j] - Allocation[i][j]"),
        ("displayMatrices()", "Displays formatted Allocation, Maximum, Need, and Available matrices"),
        ("safetyAlgorithm()", "Executes Banker's safety search; returns 1 if safe, 0 if unsafe"),
        ("requestResources()", "Accepts requests, performs provisional allocation, verifies safety, and executes rollback if unsafe"),
        ("clearScreen()", "Clears the console screen across Windows and UNIX environments"),
        ("main()", "Controls the interactive menu loop, user input handling, and exit"),
    ]
    for idx, (c0, c1) in enumerate(mod_rows):
        r = t_mod.rows[idx]
        r.cells[0].width = Inches(2.2)
        r.cells[1].width = Inches(4.0)
        set_cell_margins(r.cells[0], 60, 60, 80, 80)
        set_cell_margins(r.cells[1], 60, 60, 80, 80)
        if idx == 0:
            set_cell_background(r.cells[0], "F1F5F9")
            set_cell_background(r.cells[1], "F1F5F9")
        r.cells[0].paragraphs[0].add_run(c0).bold = (idx == 0)
        r.cells[1].paragraphs[0].add_run(c1).bold = (idx == 0)

    add_section("6.2 Important Design Decisions")
    add_bullet("Predictable fixed matrix sizes: #define P 5 and #define R 3 optimize memory layout.")
    add_bullet("In-place state rollback: Temporary subtraction and addition cleanly restore state without memory overhead.")
    add_bullet("Strict input sanitization: Process number checked (0 to 4); negative resource quantities explicitly rejected.")
    add_bullet("Safe sequence recording: An integer array tracks the execution sequence as processes finish.")

    add_section("6.3 Compilation and Execution")
    add_p(
        "The project is developed using standard ANSI C (C99 compliant) and compiles cleanly using the GNU Compiler Collection (GCC).\n\n"
        "Compilation command:\n"
        "gcc -std=c99 -Wall -Wextra -O2 bankers_algorithm.c -o bankers_c\n\n"
        "Execution command on Linux / macOS:\n"
        "./bankers_c\n\n"
        "Execution command on Windows:\n"
        "bankers_c.exe"
    )

    add_fig("Figure 6.1: Source Code in Visual Studio Code", "fig_6_1_source_code.png", width_inches=6.0)
    add_fig("Figure 6.2: Successful Compilation and Program Execution", "fig_6_2_compilation.png", width_inches=6.0)

    # =========================================================
    # PAGE 11-15: 7. TESTING AND RESULTS
    # =========================================================
    add_chapter("7. TESTING AND RESULTS")
    add_section("7.1 Test Environment")
    add_p(
        "Testing was performed on macOS (Darwin arm64) and Linux using GCC 14. The canonical Silberschatz textbook scenario "
        "featuring 5 processes and 3 resource types (A:10, B:5, C:7 total instances) was tested across all menu options."
    )

    add_section("7.2 Sample Input State")
    add_p("Table 7.1: Canonical Resource Allocation State (Silberschatz Example)", bold=True, space_after=3)

    t_state = doc.add_table(rows=7, cols=5)
    t_state.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_state)
    state_rows = [
        ("Process", "Allocation (A B C)", "Maximum (A B C)", "Need (A B C)", "Available (A B C)"),
        ("P0", "0  1  0", "7  5  3", "7  4  3", "3  3  2"),
        ("P1", "2  0  0", "3  2  2", "1  2  2", ""),
        ("P2", "3  0  2", "9  0  2", "6  0  0", ""),
        ("P3", "2  1  1", "2  2  2", "0  1  1", ""),
        ("P4", "0  0  2", "4  3  3", "4  3  1", ""),
        ("Total System Resources", "[ 10,  5,  7 ]", "", "", ""),
    ]
    for idx, row_data in enumerate(state_rows):
        r = t_state.rows[idx]
        for c_idx, val in enumerate(row_data):
            cell = r.cells[c_idx]
            set_cell_margins(cell, 60, 60, 80, 80)
            if idx == 0:
                set_cell_background(cell, "F1F5F9")
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            r_run = p.add_run(val)
            r_run.bold = (idx == 0 or idx == 6)

    add_section("7.3 Actual Output Screenshots")
    
    # FIGURE 7.1: USER'S PROVIDED SCREENSHOT!
    add_fig(
        "Figure 7.1: Main Menu & Resource Request Simulation (User Test Execution)",
        "actual_output_simulation.png",
        width_inches=5.8
    )

    add_p(
        "As seen in Figure 7.1, the user chose Option 3 (Request Resources), selected process P1, and requested resources "
        "[R0: 1, R1: 0, R2: 2]. The simulator verified constraints, provisionally allocated resources, executed the safety algorithm, "
        "found the safe sequence P1 -> P3 -> P4 -> P0 -> P2, and successfully GRANTED the request."
    )

    add_fig("Figure 7.2: Resource Matrices Display Output (Option 1)", "fig_7_2_matrices.png", width_inches=6.0)
    add_fig("Figure 7.3: Safety State Verification Output (Option 2)", "fig_7_3_safety_trace.png", width_inches=6.0)

    add_section("7.4 Scenario Verification and Outcome Summary")
    add_p("Table 7.2: Verification Scenarios and Algorithmic Outcomes", bold=True, space_after=3)

    t_res = doc.add_table(rows=6, cols=4)
    t_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_res)
    res_rows = [
        ("Scenario / Action", "Parameters", "Observed Outcome", "Safety Status"),
        ("Initial System State", "P = 5, R = 3", "Safe Sequence: P1 -> P3 -> P4 -> P0 -> P2", "SAFE"),
        ("Valid Request by P1", "Request: [1, 0, 2]", "Granted safely; Available becomes [2, 3, 0]", "SAFE"),
        ("Exceed Maximum Need", "P0 requests [0, 5, 0]", "Denied: Request exceeds process Need", "REJECTED"),
        ("Exceed Available Pool", "P4 requests [4, 3, 1]", "Wait: Request exceeds Available [3, 3, 2]", "WAIT"),
        ("Unsafe Request Hazard", "P0 requests [0, 2, 0]", "Denied & Rolled Back: leads to unsafe state", "ROLLED BACK"),
    ]
    for idx, row_data in enumerate(res_rows):
        r = t_res.rows[idx]
        for c_idx, val in enumerate(row_data):
            cell = r.cells[c_idx]
            set_cell_margins(cell, 60, 60, 80, 80)
            if idx == 0:
                set_cell_background(cell, "F1F5F9")
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx > 1 else WD_ALIGN_PARAGRAPH.LEFT
            r_run = p.add_run(val)
            r_run.bold = (idx == 0)

    # =========================================================
    # PAGE 16: 8. DISCUSSION & 9. CONCLUSION
    # =========================================================
    add_chapter("8. DISCUSSION")
    add_section("8.1 Comparison of Deadlock Handling Strategies")
    add_p(
        "Deadlock handling in operating systems is approached through four primary paradigms:\n"
        "• Deadlock Prevention: Imposes strict structural constraints to invalidate one of the four necessary Coffman conditions "
        "(Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait). However, this severely curtails device utilization.\n"
        "• Deadlock Avoidance (Banker's Algorithm): Allows all four conditions to exist but dynamically inspects every request. "
        "It achieves higher concurrency than prevention by granting requests whenever system safety is preserved.\n"
        "• Deadlock Detection and Recovery: Optimistically grants all requests and periodically checks for deadlock using a wait-for graph. "
        "If deadlock is detected, processes must be aborted or resources preempted, causing data loss.\n"
        "• Deadlock Ignorance (Ostrich Algorithm): Ignores the problem under the assumption that deadlocks occur infrequently. Used by "
        "general-purpose operating systems like Linux and Windows, which rely on user intervention when an application hangs."
    )

    add_section("8.2 Interpretation of Matrices and Safety Sequences")
    add_p(
        "The safety algorithm operates on the principle of conservative worst-case analysis: it assumes that whenever a process runs, "
        "it will request its entire remaining Need before terminating and releasing all held resources. In our textbook state, "
        "P1 is satisfied first (Need [1, 2, 2] <= Work [3, 3, 2]), releasing [2, 0, 0] and boosting Work to [5, 3, 2]. This creates a "
        "cascade effect allowing P3, P4, P0, and P2 to finish in succession. Multiple topological sequences may exist, but any valid sequence "
        "proves safety."
    )

    add_section("8.3 Limitations")
    add_bullet("Requires prior knowledge of maximum claims, which is difficult for general-purpose user applications.")
    add_bullet("Assumes a fixed number of processes and resource types, whereas modern operating systems spawn processes dynamically.")
    add_bullet("Conservative policy: may delay requests that would not have actually resulted in deadlock in practice.")

    add_chapter("9. CONCLUSION AND FUTURE SCOPE")
    add_section("9.1 Conclusion")
    add_p(
        "The Banker's Algorithm for Deadlock Avoidance Simulator successfully demonstrates the principles of safe state verification "
        "and dynamic resource allocation using the C programming language. The simulator computes Need matrices, enforces maximum claim "
        "boundaries, simulates provisional allocations, and guarantees that circular deadlock cannot occur through automated rollback. "
        "Testing validated the canonical Silberschatz scenario and confirmed that valid requests (P1 requesting [1, 0, 2]) are safely granted "
        "while unsafe requests are promptly prevented."
    )

    add_section("9.2 Future Scope")
    add_bullet("Extending the engine to support dynamic runtime process creation and resource registration.")
    add_bullet("Integrating multi-threading using POSIX pthreads and mutex locks to simulate concurrent thread resource claims.")
    add_bullet("Developing a web-based graphical dashboard (Flask / JavaScript) featuring animated resource gauges and matrix visualizers.")
    add_bullet("Exporting execution trace logs and state tables to CSV and PDF formats for automated lab evaluation.")

    # =========================================================
    # PAGE 17: 10. REFERENCES & APPENDICES
    # =========================================================
    add_chapter("10. REFERENCES")
    refs = [
        "[1] A. Silberschatz, P. B. Galvin, and G. Gagne, Operating System Concepts, 10th ed. Hoboken, NJ, USA: Wiley, 2018.",
        "[2] W. Stallings, Operating Systems: Internals and Design Principles, 9th ed. Harlow, England: Pearson, 2018.",
        "[3] A. S. Tanenbaum and H. Bos, Modern Operating Systems, 4th ed. Boston, MA, USA: Pearson, 2015.",
        "[4] E. W. Dijkstra, \"Cooperating sequential processes,\" Technological University, Eindhoven, The Netherlands, Tech. Rep. EWD-123, 1965.",
        "[5] B. W. Kernighan and D. M. Ritchie, The C Programming Language, 2nd ed. Englewood Cliffs, NJ, USA: Prentice Hall, 1988.",
        "[6] Free Software Foundation, \"Using the GNU Compiler Collection (GCC),\" [Online]. Available: https://gcc.gnu.org/onlinedocs/. [Accessed: Nov. 2026].",
        "[7] Visual Studio Code, \"Documentation and C/C++ Extensions,\" [Online]. Available: https://code.visualstudio.com/docs. [Accessed: Nov. 2026].",
    ]
    for r in refs:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.space_after = Pt(4)
        p_r.paragraph_format.line_spacing = 1.2
        p_r.add_run(r).font.size = Pt(11)

    add_chapter("APPENDIX A – SAMPLE INPUT & SYSTEM ALLOCATION STATE")
    add_p("Table A.1: Sample Input State Vectors and Matrices", bold=True, space_after=3)

    t_app = doc.add_table(rows=6, cols=4)
    t_app.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_app)
    app_rows = [
        ("Process ID", "Allocation [A B C]", "Maximum Claim [A B C]", "Need Vector [A B C]"),
        ("P0", "0  1  0", "7  5  3", "7  4  3"),
        ("P1", "2  0  0", "3  2  2", "1  2  2"),
        ("P2", "3  0  2", "9  0  2", "6  0  0"),
        ("P3", "2  1  1", "2  2  2", "0  1  1"),
        ("P4", "0  0  2", "4  3  3", "4  3  1"),
    ]
    for idx, row_data in enumerate(app_rows):
        r = t_app.rows[idx]
        for c_idx, val in enumerate(row_data):
            cell = r.cells[c_idx]
            set_cell_margins(cell, 60, 60, 80, 80)
            if idx == 0:
                set_cell_background(cell, "F1F5F9")
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            r_run = p.add_run(val)
            r_run.bold = (idx == 0)

    add_p(
        "\nSystem Resource Vector: Available = [ 3, 3, 2 ]\n"
        "Total Resources Present in System: [ 10, 5, 7 ]\n"
        "Select menu option 2 to check safety or option 3 to simulate process requests.",
        space_after=12
    )

    add_chapter("APPENDIX B – SOURCE CODE SUBMISSION")
    add_p(
        "The complete C source code of the Banker's Algorithm Simulator is provided below. "
        "The code implements calculateNeed(), displayMatrices(), safetyAlgorithm(), requestResources(), clearScreen(), and main()."
    )

    # Add code block with monospace formatting
    code_text = """#include <stdio.h>
#include <stdlib.h>

#define P 5
#define R 3

int allocation[P][R] = {
    {0, 1, 0},
    {2, 0, 0},
    {3, 0, 2},
    {2, 1, 1},
    {0, 0, 2}
};

int maximum[P][R] = {
    {7, 5, 3},
    {3, 2, 2},
    {9, 0, 2},
    {2, 2, 2},
    {4, 3, 3}
};

int available[R] = {3, 3, 2};

void clearScreen() {
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
}

void calculateNeed(int need[P][R]) {
    int i, j;

    for (i = 0; i < P; i++) {
        for (j = 0; j < R; j++) {
            need[i][j] = maximum[i][j] - allocation[i][j];
        }
    }
}

void displayMatrices() {
    int i, j;
    int need[P][R];

    calculateNeed(need);

    printf("\\nAllocation Matrix:\\n");
    for (i = 0; i < P; i++) {
        printf("P%d: ", i);
        for (j = 0; j < R; j++)
            printf("%d ", allocation[i][j]);
        printf("\\n");
    }

    printf("\\nMaximum Matrix:\\n");
    for (i = 0; i < P; i++) {
        printf("P%d: ", i);
        for (j = 0; j < R; j++)
            printf("%d ", maximum[i][j]);
        printf("\\n");
    }

    printf("\\nNeed Matrix:\\n");
    for (i = 0; i < P; i++) {
        printf("P%d: ", i);
        for (j = 0; j < R; j++)
            printf("%d ", need[i][j]);
        printf("\\n");
    }

    printf("\\nAvailable Resources: ");
    for (j = 0; j < R; j++)
        printf("%d ", available[j]);

    printf("\\n");
}

int safetyAlgorithm() {
    int need[P][R];
    int work[R], finish[P] = {0};
    int safeSequence[P];
    int i, j, count = 0, found;

    calculateNeed(need);

    for (j = 0; j < R; j++)
        work[j] = available[j];

    while (count < P) {
        found = 0;

        for (i = 0; i < P; i++) {
            if (finish[i] == 0) {
                int possible = 1;

                for (j = 0; j < R; j++) {
                    if (need[i][j] > work[j]) {
                        possible = 0;
                        break;
                    }
                }

                if (possible) {
                    for (j = 0; j < R; j++)
                        work[j] += allocation[i][j];

                    safeSequence[count++] = i;
                    finish[i] = 1;
                    found = 1;
                }
            }
        }

        if (!found)
            break;
    }

    if (count == P) {
        printf("\\nSystem is in a SAFE STATE.\\n");
        printf("Safe Sequence: ");

        for (i = 0; i < P; i++)
            printf("P%d ", safeSequence[i]);

        printf("\\n");
        return 1;
    }

    printf("\\nSystem is in an UNSAFE STATE.\\n");
    printf("No safe sequence exists.\\n");

    return 0;
}

void requestResources() {
    int process, request[R];
    int need[P][R];
    int i;

    printf("Enter process number (0-4): ");

    if (scanf("%d", &process) != 1) {
        printf("Invalid input!\\n");
        return;
    }

    if (process < 0 || process >= P) {
        printf("Invalid process number!\\n");
        return;
    }

    for (i = 0; i < R; i++) {
        printf("Enter request for R%d: ", i);

        if (scanf("%d", &request[i]) != 1) {
            printf("Invalid input!\\n");
            return;
        }

        if (request[i] < 0) {
            printf("Request cannot be negative!\\n");
            return;
        }
    }

    calculateNeed(need);

    for (i = 0; i < R; i++) {
        if (request[i] > need[process][i]) {
            printf("Request exceeds process need!\\n");
            return;
        }

        if (request[i] > available[i]) {
            printf("Resources are not currently available!\\n");
            return;
        }
    }

    /* Temporarily allocate resources */
    for (i = 0; i < R; i++) {
        available[i] -= request[i];
        allocation[process][i] += request[i];
    }

    printf("\\nChecking system safety...\\n");

    if (safetyAlgorithm()) {
        printf("Resource request GRANTED.\\n");
    } else {
        /* Restore previous allocation */
        for (i = 0; i < R; i++) {
            available[i] += request[i];
            allocation[process][i] -= request[i];
        }

        printf("Resource request DENIED.\\n");
        printf("Previous allocation restored.\\n");
    }
}

int main() {
    int choice;

    while (1) {
        printf("\\n===== BANKER'S ALGORITHM SIMULATOR =====\\n");
        printf("1. Display Resource Matrices\\n");
        printf("2. Check Safe State\\n");
        printf("3. Request Resources\\n");
        printf("4. Clear Screen\\n");
        printf("5. Exit\\n");

        printf("Enter your choice: ");

        if (scanf("%d", &choice) != 1) {
            printf("Invalid input!\\n");
            break;
        }

        switch (choice) {
            case 1:
                displayMatrices();
                break;

            case 2:
                safetyAlgorithm();
                break;

            case 3:
                requestResources();
                break;

            case 4:
                clearScreen();
                break;

            case 5:
                printf("Exiting Banker's Algorithm Simulator.\\n");
                return 0;

            default:
                printf("Invalid choice! Please try again.\\n");
        }
    }

    return 0;
}"""

    p_code = doc.add_paragraph()
    p_code.paragraph_format.left_indent = Inches(0.2)
    p_code.paragraph_format.line_spacing = 1.05
    p_code.paragraph_format.space_after = Pt(2)
    r_code = p_code.add_run(code_text)
    r_code.font.name = 'Courier New'
    r_code.font.size = Pt(9.5)
    r_code.font.color.rgb = RGBColor(30, 41, 59)

    doc.save(OUTPUT_DOCX)
    print(f"Report successfully generated at: {OUTPUT_DOCX}")

if __name__ == "__main__":
    build_report()
