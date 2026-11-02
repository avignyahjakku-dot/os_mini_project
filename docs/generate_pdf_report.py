"""
generate_pdf_report.py - Generates the complete academic PDF matching the SIT Symbiosis format
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(DOCS_DIR, "images")
OUTPUT_PDF = os.path.join(DOCS_DIR, "OS_MiniProject_Report.pdf")

def create_pdf():
    # 1.0 inch margins on A4 (595.27 x 841.89 pt)
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=inch,
        rightMargin=inch,
        topMargin=inch,
        bottomMargin=inch
    )

    styles = getSampleStyleSheet()

    # Custom styles matching Times New Roman standard
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=11,
        leading=14.5,
        spaceAfter=6,
        textColor=colors.HexColor('#111827')
    )

    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=body_style,
        leftIndent=18,
        spaceAfter=4,
    )

    chapter_style = ParagraphStyle(
        'CustomChapter',
        parent=styles['Heading1'],
        fontName='Times-Bold',
        fontSize=13,
        leading=17,
        spaceBefore=14,
        spaceAfter=6,
        textColor=colors.HexColor('#0f172a')
    )

    section_style = ParagraphStyle(
        'CustomSection',
        parent=styles['Heading2'],
        fontName='Times-Bold',
        fontSize=11.5,
        leading=15,
        spaceBefore=8,
        spaceAfter=4,
        textColor=colors.HexColor('#1e293b')
    )

    table_header_style = ParagraphStyle(
        'CustomTH',
        parent=body_style,
        fontName='Times-Bold',
        fontSize=10,
        leading=12,
        alignment=1, # Center
        textColor=colors.HexColor('#0f172a')
    )

    table_cell_style = ParagraphStyle(
        'CustomTD',
        parent=body_style,
        fontSize=10,
        leading=12,
        textColor=colors.HexColor('#1e293b')
    )

    table_cell_center = ParagraphStyle(
        'CustomTDCenter',
        parent=table_cell_style,
        alignment=1 # Center
    )

    caption_style = ParagraphStyle(
        'CustomCaption',
        parent=body_style,
        fontName='Times-Bold',
        fontSize=10,
        leading=13,
        spaceAfter=6,
        textColor=colors.HexColor('#1e293b')
    )

    story = []

    # =========================================================
    # PAGE 1: TITLE PAGE
    # =========================================================
    p_inst = Paragraph(
        "<font size='13' color='#A00000'><b>SYMBIOSIS INSTITUTE OF TECHNOLOGY, HYDERABAD</b></font><br/>"
        "<font size='11'><b>Symbiosis International (Deemed University), Pune</b></font><br/>"
        "<font size='9.5' color='#4B5563'><i>Established under section 3 of the UGC Act, 1956<br/>"
        "Re-Accredited by NAAC with ‘A++’ Grade | Awarded Category – I by UGC</i></font>",
        ParagraphStyle('CoverHeader', parent=body_style, alignment=1, leading=15)
    )
    story.append(p_inst)
    story.append(Spacer(1, 45))

    p_op = Paragraph(
        "<font size='22' color='#A00000'><b>OPERATING SYSTEMS</b></font>",
        ParagraphStyle('CoverOS', parent=body_style, alignment=1)
    )
    story.append(p_op)
    story.append(Spacer(1, 15))

    p_mpr = Paragraph(
        "<font size='14' color='#1A5276'><b>MINI PROJECT REPORT</b></font>",
        ParagraphStyle('CoverMPR', parent=body_style, alignment=1)
    )
    story.append(p_mpr)
    story.append(Spacer(1, 40))

    # Details Table
    meta_table_data = [
        [Paragraph("<b>Course Name</b>", table_cell_style), Paragraph("Operating Systems", table_cell_center)],
        [Paragraph("<b>Mini Project Title</b>", table_cell_style), Paragraph("Banker's Algorithm for Deadlock Avoidance Simulator", table_cell_center)],
        [Paragraph("<b>Student Name(s)</b>", table_cell_style), Paragraph("Avignya Reddy Jakku<br/>Aapti Erragunta<br/>Ahila Meghana<br/>Krithika Reddy", table_cell_center)],
        [Paragraph("<b>PRN / Roll Number(s)</b>", table_cell_style), Paragraph("25070721024<br/>25070721018<br/>25070721002<br/>25070721062", table_cell_center)],
        [Paragraph("<b>Faculty Guide</b>", table_cell_style), Paragraph("Dr. Bibhuprasad Sahu", table_cell_center)],
    ]
    t_meta = Table(meta_table_data, colWidths=[2.2*inch, 4.0*inch])
    t_meta.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('INNERGRID', (0,0), (-1,-1), 1, colors.HexColor('#000000')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 45))

    p_foot = Paragraph(
        "Academic Year  :  2026<br/>Semester  :  3<sup>rd</sup><br/>Section  :  Batch-1",
        ParagraphStyle('CoverFoot', parent=body_style, alignment=1, leading=16)
    )
    story.append(p_foot)
    story.append(PageBreak())

    # =========================================================
    # PAGE 2: ACKNOWLEDGEMENT & ABSTRACT
    # =========================================================
    story.append(Paragraph("ACKNOWLEDGEMENT", chapter_style))
    story.append(Paragraph(
        "We would like to express our sincere gratitude to our Operating Systems faculty guide "
        "<b>Dr. Bibhuprasad Sahu</b> for providing valuable guidance, continuous support and encouragement throughout the "
        "development of this mini project. His suggestions and feedback helped us understand the "
        "concepts of deadlock avoidance, resource-allocation graphs, and Dijkstra's Banker's Algorithm and improve our implementation.",
        body_style
    ))
    story.append(Paragraph(
        "We extend our heartfelt thanks to the Head of the Department <b>Dr. Suryanarayana</b> and the Department of Computer "
        "Science and Engineering for providing us with the opportunity, resources and facilities required "
        "to complete this project successfully.",
        body_style
    ))
    story.append(Paragraph(
        "We are also grateful to our institute, <b>Symbiosis Institute of Technology (SIT), Hyderabad</b>, for providing a supportive learning environment and access "
        "to the necessary software tools and laboratory facilities.",
        body_style
    ))
    story.append(Paragraph(
        "This project helped us strengthen our knowledge of operating system concepts, C "
        "programming, process management, dynamic resource allocation and deadlock avoidance algorithms. We would also "
        "like to thank our classmates and friends for their valuable suggestions, discussions and support "
        "during the development and testing phases.",
        body_style
    ))
    story.append(Spacer(1, 15))

    story.append(Paragraph("ABSTRACT", chapter_style))
    story.append(Paragraph(
        "Deadlock is a critical state in multi-programming operating systems where concurrent processes are permanently "
        "blocked from execution because each process holds resources while waiting for resources currently held by others in a "
        "circular dependency. Deadlock avoidance is an active strategy that ensures the operating system never transitions from a "
        "safe state to an unsafe state where deadlock could occur.",
        body_style
    ))
    story.append(Paragraph(
        "This mini project develops a menu-driven <b>Banker's Algorithm Simulator for Deadlock Avoidance</b> using "
        "the C programming language. The simulator models a multi-process, multi-resource system featuring n = 5 processes "
        "(P0 to P4) and m = 3 resource types (R0, R1, R2). It implements the complete Banker's safety verification algorithm and "
        "dynamic resource-request evaluation logic.",
        body_style
    ))
    story.append(Paragraph(
        "The user interacts with a clean console interface allowing them to display allocation matrices, execute the safety "
        "algorithm to determine if a safe execution sequence exists, and dynamically request resources for any process. The system "
        "computes the Need matrix (Need[i][j] = Maximum[i][j] - Allocation[i][j]) and validates incoming requests against maximum claims "
        "and available capacities. A provisional allocation is performed, followed by safety verification using a Work vector. If the "
        "resulting state remains safe, the request is permanently granted; if unsafe, the system executes an immediate state rollback "
        "and orders the process to wait.",
        body_style
    ))
    story.append(Paragraph(
        "The project uses arrays, functions, loops, conditional statements and temporary state vectors to simulate resource "
        "distribution and ensure robust error handling against negative inputs and invalid process indices. "
        "The simulator is an educational model that provides students with practical insight into how conservative resource-allocation "
        "policies prevent deadlock in operating systems without incurring runtime process termination.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================
    # PAGE 3: TABLE OF CONTENTS
    # =========================================================
    story.append(Paragraph("TABLE OF CONTENTS", chapter_style))
    story.append(Spacer(1, 6))

    toc_entries = [
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
    for item in toc_entries:
        story.append(Paragraph(item, ParagraphStyle('TOCItem', parent=body_style, spaceAfter=5)))

    story.append(PageBreak())

    # =========================================================
    # SECTION 1 & 2
    # =========================================================
    story.append(Paragraph("1. INTRODUCTION", chapter_style))
    story.append(Paragraph("1.1 Background", section_style))
    story.append(Paragraph(
        "An operating system manages computer hardware and system resources, providing an environment in which "
        "application programs execute efficiently. A process is a program in execution. In a multi-programming or "
        "multi-tasking system, multiple processes compete for a finite set of shared system resources such as CPU cycles, "
        "memory partitions, I/O devices, files, and database locks. If resource allocation is uncoordinated, circular wait conditions "
        "can emerge where processes become permanently halted, resulting in deadlock.",
        body_style
    ))

    story.append(Paragraph("1.2 Deadlock Avoidance and Banker's Algorithm", section_style))
    story.append(Paragraph(
        "Deadlock avoidance is an active dynamic strategy where the operating system evaluates every resource request before granting it. "
        "If allocating the requested resources leaves the system in a safe state—meaning there exists at least one order of process execution "
        "that allows every process to satisfy its maximum claim and terminate—the request is granted. Otherwise, the process must wait. "
        "Dijkstra's Banker's Algorithm is the classic and mathematically proven deadlock avoidance algorithm for systems with multiple instances "
        "of each resource type.",
        body_style
    ))

    story.append(Paragraph("1.3 Relevance to Operating Systems", section_style))
    story.append(Paragraph(
        "The project is directly related to process management, concurrency control, and deadlock handling in the Operating "
        "Systems syllabus (CSE-301). It bridges the gap between theoretical classroom definitions and real-world implementation, "
        "showing how matrix data structures and vector arithmetic are used by operating system kernels to maintain system integrity.",
        body_style
    ))

    story.append(Paragraph("1.4 Scope", section_style))
    story.append(Paragraph(
        "The simulator is a menu-driven educational console application implemented in C. It models 5 processes (P0 to P4) "
        "and 3 resource types (A, B, C). It supports initial safety state verification, dynamic process resource requests, "
        "provisional allocation testing, automatic rollback upon detecting unsafe states, and full matrix visualization. "
        "The simulator assumes cooperative processes that eventually release held resources upon completion.",
        body_style
    ))

    story.append(Paragraph("2. PROBLEM STATEMENT AND OBJECTIVES", chapter_style))
    story.append(Paragraph("2.1 Problem Statement", section_style))
    story.append(Paragraph(
        "Students often learn the Banker's Algorithm through theoretical textbook examples but find it difficult to visualize "
        "how dynamic resource requests alter system vectors, how the Work vector reclaims resources during execution traces, "
        "and how state rollbacks prevent catastrophic deadlocks. The problem is to develop a C-based simulator that accepts "
        "process requests interactively, computes the Need matrix, evaluates safety, displays step-by-step results, and demonstrates "
        "instant state rollbacks.",
        body_style
    ))

    story.append(Paragraph("2.2 Objectives", section_style))
    objectives = [
        "To understand the fundamental role of deadlock avoidance in operating systems.",
        "To implement Dijkstra's Banker's Safety Algorithm and Resource-Request Algorithm in C.",
        "To dynamically compute the Need matrix from the Maximum and Allocation matrices.",
        "To validate process requests against maximum claims and system available limits.",
        "To perform provisional resource allocations and verify resultant system safety.",
        "To execute immediate state rollbacks when an allocation leads to an unsafe state.",
        "To determine and display the topological safe execution sequence (e.g., P1 -> P3 -> P4 -> P0 -> P2).",
        "To provide an interactive menu for matrix inspection, safety checks, and simulation.",
    ]
    for obj in objectives:
        story.append(Paragraph(f"•  {obj}", bullet_style))

    story.append(Paragraph("2.3 Expected Outcome", section_style))
    story.append(Paragraph(
        "The expected outcome is a working menu-driven C program that allows a user to inspect resource matrices, "
        "execute safety verification, submit real-time resource requests, observe whether requests are granted or denied, "
        "and understand the practical mechanics of deadlock avoidance.",
        body_style
    ))

    # =========================================================
    # SECTION 3 & 4
    # =========================================================
    story.append(Paragraph("3. LITERATURE / EXISTING SYSTEM", chapter_style))
    story.append(Paragraph("3.1 Existing Approach", section_style))
    story.append(Paragraph(
        "CPU resource allocation and deadlock problems are conventionally taught using static textbook examples and manually "
        "solved tabular matrices. Students manually calculate Need matrices and iteratively update Available vectors on paper. "
        "While useful for basic conceptual understanding, manual calculation becomes tedious, slow, and prone to arithmetic mistakes "
        "when multiple sequential requests must be evaluated.",
        body_style
    ))

    story.append(Paragraph("3.2 Proposed System", section_style))
    story.append(Paragraph(
        "The proposed system automates all matrix arithmetic and algorithmic safety checks. The simulator maintains state vectors "
        "in memory, computes the Need matrix automatically, and evaluates the safety algorithm in polynomial time O(m * n^2). "
        "It supports non-destructive provisional allocations, meaning the system state is only permanently updated if safety is guaranteed.",
        body_style
    ))

    story.append(Paragraph("3.3 Limitations of the Existing Manual Method", section_style))
    story.append(Paragraph("•  Manual calculation is slow and impractical for multi-step requests.", bullet_style))
    story.append(Paragraph("•  Human error in vector addition or subtraction can lead to incorrect safety conclusions.", bullet_style))
    story.append(Paragraph("•  Manual methods cannot easily demonstrate instant rollbacks or boundary violations.", bullet_style))
    story.append(Paragraph("•  Visualizing alternative topological safe sequences requires recalculating all permutations.", bullet_style))

    story.append(Paragraph("4. REQUIREMENTS AND TOOLS", chapter_style))
    story.append(Paragraph("4.1 Hardware Requirements", section_style))
    story.append(Paragraph("<b>Table 4.1: Hardware Requirements</b>", caption_style))

    t_hw_data = [
        [Paragraph("<b>Component</b>", table_header_style), Paragraph("<b>Minimum Requirement</b>", table_header_style)],
        [Paragraph("Processor", table_cell_style), Paragraph("Modern desktop or laptop processor (Intel / AMD / Apple Silicon)", table_cell_style)],
        [Paragraph("RAM", table_cell_style), Paragraph("2 GB or higher", table_cell_style)],
        [Paragraph("Storage", table_cell_style), Paragraph("A few MB for project source code and executable binaries", table_cell_style)],
        [Paragraph("Input", table_cell_style), Paragraph("Keyboard", table_cell_style)],
        [Paragraph("Output", table_cell_style), Paragraph("Monitor or display console", table_cell_style)],
    ]
    t_hw = Table(t_hw_data, colWidths=[2.2*inch, 4.0*inch])
    t_hw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_hw)
    story.append(Spacer(1, 10))

    story.append(Paragraph("4.2 Software Requirements", section_style))
    story.append(Paragraph("<b>Table 4.2: Software Requirements</b>", caption_style))

    t_sw_data = [
        [Paragraph("<b>Software / Tool</b>", table_header_style), Paragraph("<b>Purpose</b>", table_header_style)],
        [Paragraph("C Language (C99 / C11)", table_cell_style), Paragraph("Core algorithmic implementation", table_cell_style)],
        [Paragraph("GCC Compiler", table_cell_style), Paragraph("Compiling and optimizing source code", table_cell_style)],
        [Paragraph("Visual Studio Code / Terminal", table_cell_style), Paragraph("Source code editing and interactive execution", table_cell_style)],
        [Paragraph("Windows / Linux / macOS", table_cell_style), Paragraph("Cross-platform operating system environments", table_cell_style)],
        [Paragraph("Microsoft Word / PDF Viewer", table_cell_style), Paragraph("Preparing and viewing the academic project report", table_cell_style)],
    ]
    t_sw = Table(t_sw_data, colWidths=[2.2*inch, 4.0*inch])
    t_sw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sw)
    story.append(Spacer(1, 10))

    story.append(Paragraph("4.3 Programming Concepts Used", section_style))
    story.append(Paragraph("•  Two-dimensional arrays to represent Allocation, Maximum, and Need matrices.", bullet_style))
    story.append(Paragraph("•  One-dimensional integer vectors to store Available, Work, and Request arrays.", bullet_style))
    story.append(Paragraph("•  Boolean/integer tracking arrays (Finish) to record satisfied process execution status.", bullet_style))
    story.append(Paragraph("•  Modular functions (calculateNeed, displayMatrices, safetyAlgorithm, requestResources).", bullet_style))
    story.append(Paragraph("•  Loops (while, for) and conditional decision branching to implement algorithmic search.", bullet_style))
    story.append(Paragraph("•  Provisional allocation logic with non-destructive state restoration (rollback).", bullet_style))

    story.append(Paragraph("4.4 Implementation Code Provided by Team", section_style))
    story.append(Paragraph(
        "As part of the project specification and laboratory implementation, the team designed and implemented a concise, "
        "self-contained C program implementing the Banker's Algorithm simulator. The code defines P = 5 processes, R = 3 resource types, "
        "and encapsulates matrix calculations, safety searches, and resource request evaluations into clean procedural functions. "
        "The full complete code listing is presented in Appendix B.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================
    # SECTION 5: SYSTEM DESIGN / METHODOLOGY
    # =========================================================
    story.append(Paragraph("5. SYSTEM DESIGN / METHODOLOGY", chapter_style))
    story.append(Paragraph("5.1 System Architecture", section_style))
    story.append(Paragraph(
        "The simulator follows an input–processing–output architecture. The user selects operations through the interactive menu, "
        "the core engine performs vector operations and safety analysis, and the output module displays formatted matrices and status messages.",
        body_style
    ))
    story.append(Paragraph("<b>Table 5.1: System Architecture</b>", caption_style))

    t_arch_data = [
        [Paragraph("<b>Stage</b>", table_header_style), Paragraph("<b>Description</b>", table_header_style)],
        [Paragraph("Input Module", table_cell_style), Paragraph("Reads user choices, process IDs, and requested resource vectors", table_cell_style)],
        [Paragraph("State Storage Module", table_cell_style), Paragraph("Stores Allocation, Maximum, Need, and Available matrices", table_cell_style)],
        [Paragraph("Safety Engine", table_cell_style), Paragraph("Executes Dijkstra's safety algorithm using Work and Finish vectors", table_cell_style)],
        [Paragraph("Request & Rollback Module", table_cell_style), Paragraph("Validates constraints, performs provisional allocation, and rolls back if unsafe", table_cell_style)],
        [Paragraph("Display Module", table_cell_style), Paragraph("Prints formatted matrix tables, safe sequences, and status banners", table_cell_style)],
    ]
    t_arch = Table(t_arch_data, colWidths=[2.2*inch, 4.0*inch])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 10))

    img_arch = os.path.join(IMG_DIR, "fig_5_1_architecture.png")
    if os.path.exists(img_arch):
        story.append(Image(img_arch, width=5.8*inch, height=1.6*inch))
        story.append(Paragraph("<b>Figure 5.1: System Architecture of Banker's Algorithm Simulator</b>", caption_style))

    story.append(Paragraph("5.2 Process Data Structure and Matrices", section_style))
    story.append(Paragraph(
        "The system state is defined by four core data structures:<br/>"
        "1. <b>Available[R]</b>: Vector of length R. If Available[j] = k, there are k instances of resource type Rj available.<br/>"
        "2. <b>Max[P][R]</b>: P x R matrix. Max[i][j] defines the maximum claim of process Pi for resource Rj.<br/>"
        "3. <b>Allocation[P][R]</b>: P x R matrix. Allocation[i][j] defines instances of Rj currently allocated to Pi.<br/>"
        "4. <b>Need[P][R]</b>: P x R matrix. Need[i][j] = Max[i][j] - Allocation[i][j] defines remaining resources needed.",
        body_style
    ))
    story.append(Paragraph("<b>Table 5.2: Process and Matrix Attributes</b>", caption_style))

    t_attr_data = [
        [Paragraph("<b>Attribute</b>", table_header_style), Paragraph("<b>Description</b>", table_header_style)],
        [Paragraph("Allocation[P][R]", table_cell_style), Paragraph("Resources currently held by each process", table_cell_style)],
        [Paragraph("Maximum[P][R]", table_cell_style), Paragraph("Maximum claim declared by each process before execution", table_cell_style)],
        [Paragraph("Need[P][R]", table_cell_style), Paragraph("Remaining resources required by process: Need = Maximum - Allocation", table_cell_style)],
        [Paragraph("Available[R]", table_cell_style), Paragraph("Currently unallocated resources available in the system pool", table_cell_style)],
        [Paragraph("Work[R] & Finish[P]", table_cell_style), Paragraph("Auxiliary tracking vectors used during safety verification", table_cell_style)],
    ]
    t_attr = Table(t_attr_data, colWidths=[2.2*inch, 4.0*inch])
    t_attr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_attr)
    story.append(Spacer(1, 10))

    story.append(Paragraph("5.3 Algorithmic Formulation", section_style))
    story.append(Paragraph("<b>5.3.1 Safety Algorithm</b>", body_style))
    story.append(Paragraph(
        "Let Work be an integer vector of length R and Finish be a boolean vector of length P.<br/>"
        "1. Initialize: Work = Available; Finish[i] = 0 for all i = 0, 1, ..., P-1.<br/>"
        "2. Find an index i such that: Finish[i] == 0 and Need[i][j] &le; Work[j] for all j = 0, ..., R-1. If no such i exists, go to Step 4.<br/>"
        "3. Work = Work + Allocation[i]; Finish[i] = 1; append Pi to SafeSequence; go to Step 2.<br/>"
        "4. If Finish[i] == 1 for all i, the system is in a <b>SAFE STATE</b>. Otherwise, the system is in an <b>UNSAFE STATE</b>.",
        body_style
    ))

    story.append(Paragraph("<b>5.3.2 Resource-Request Algorithm</b>", body_style))
    story.append(Paragraph(
        "When process Pi issues a request vector Request[R]:<br/>"
        "1. If Request[j] &le; Need[i][j] for all j, proceed to Step 2. Else raise error (request exceeds maximum claim).<br/>"
        "2. If Request[j] &le; Available[j] for all j, proceed to Step 3. Else process Pi must wait (insufficient resources).<br/>"
        "3. Provisionally alter state:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Available[j] = Available[j] - Request[j]<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Allocation[i][j] = Allocation[i][j] + Request[j]<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Need[i][j] = Need[i][j] - Request[j]<br/>"
        "4. Run Safety Algorithm. If safe &rarr; <b>GRANT</b> request permanently. If unsafe &rarr; <b>ROLLBACK</b> state:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Available[j] = Available[j] + Request[j]<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Allocation[i][j] = Allocation[i][j] - Request[j]<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Need[i][j] = Need[i][j] + Request[j], and process Pi must wait.",
        body_style
    ))

    img_class = os.path.join(IMG_DIR, "fig_5_2_classification.png")
    if os.path.exists(img_class):
        story.append(Image(img_class, width=5.8*inch, height=1.9*inch))
        story.append(Paragraph("<b>Figure 5.2: Classification of Deadlock Handling Strategies</b>", caption_style))

    story.append(Paragraph("5.4 Mathematical Formulation and Invariants", section_style))
    story.append(Paragraph("<b>Table 5.3: Core Mathematical Formulas and Invariants</b>", caption_style))

    t_form_data = [
        [Paragraph("<b>Metric / Invariant</b>", table_header_style), Paragraph("<b>Formula / Rule</b>", table_header_style)],
        [Paragraph("Need Matrix Computation", table_cell_style), Paragraph("Need[i][j] = Maximum[i][j] - Allocation[i][j]", table_cell_style)],
        [Paragraph("Total System Resource Conservation", table_cell_style), Paragraph("Total[j] = Available[j] + &sum; Allocation[i][j] (for i=0 to P-1)", table_cell_style)],
        [Paragraph("Claim Boundary Invariant", table_cell_style), Paragraph("0 &le; Allocation[i][j] &le; Maximum[i][j] &forall; i, j", table_cell_style)],
        [Paragraph("Safe Sequence Condition", table_cell_style), Paragraph("Need[s<sub>k</sub>][j] &le; Work<sub>k-1</sub>[j] &forall; j=0 to R-1", table_cell_style)],
    ]
    t_form = Table(t_form_data, colWidths=[2.2*inch, 4.0*inch])
    t_form.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_form)
    story.append(Spacer(1, 10))

    story.append(Paragraph("5.5 Overall Execution Flow", section_style))
    exec_steps = [
        "Start the program.",
        "Initialize static process matrices: Allocation, Maximum, and Available.",
        "Compute initial Need matrix using calculateNeed().",
        "Display the main menu to the user.",
        "Read and validate menu choice (1 to 5).",
        "Option 1: Display current Allocation, Maximum, Need, and Available matrices.",
        "Option 2: Execute safetyAlgorithm() and display the topological safe sequence.",
        "Option 3: Prompt process ID and request vector; execute requestResources() with provisional allocation and safety check; grant or rollback.",
        "Option 4: Clear console screen; Option 5: Terminate program cleanly.",
    ]
    for idx, s in enumerate(exec_steps, 1):
        story.append(Paragraph(f"{idx}.  {s}", bullet_style))

    img_flow = os.path.join(IMG_DIR, "fig_5_3_flowchart.png")
    if os.path.exists(img_flow):
        story.append(Spacer(1, 4))
        story.append(Image(img_flow, width=4.5*inch, height=3.9*inch))
        story.append(Paragraph("<b>Figure 5.3: Flowchart of Banker's Algorithm Simulator</b>", caption_style))

    story.append(Paragraph("5.6 Methodology", section_style))
    story.append(Paragraph(
        "The simulator preserves system stability through deterministic verification. Whenever a process requests resources, "
        "the simulator does not permanently commit changes until the safety algorithm confirms that all P processes can complete. "
        "If even one process remains unsatisfied, the provisional changes are immediately reverted. This prevents race conditions "
        "and circular deadlock.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================
    # SECTION 6: IMPLEMENTATION
    # =========================================================
    story.append(Paragraph("6. IMPLEMENTATION", chapter_style))
    story.append(Paragraph("6.1 Program Modules", section_style))
    story.append(Paragraph("<b>Table 6.1: Program Functions and Responsibilities</b>", caption_style))

    t_mod_data = [
        [Paragraph("<b>Function</b>", table_header_style), Paragraph("<b>Responsibility</b>", table_header_style)],
        [Paragraph("calculateNeed(int need[P][R])", table_cell_style), Paragraph("Computes Need matrix: Need[i][j] = Maximum[i][j] - Allocation[i][j]", table_cell_style)],
        [Paragraph("displayMatrices()", table_cell_style), Paragraph("Displays formatted Allocation, Maximum, Need, and Available matrices", table_cell_style)],
        [Paragraph("safetyAlgorithm()", table_cell_style), Paragraph("Executes Banker's safety search; returns 1 if safe, 0 if unsafe", table_cell_style)],
        [Paragraph("requestResources()", table_cell_style), Paragraph("Accepts requests, performs provisional allocation, verifies safety, and executes rollback if unsafe", table_cell_style)],
        [Paragraph("clearScreen()", table_cell_style), Paragraph("Clears the console screen across Windows and UNIX environments", table_cell_style)],
        [Paragraph("main()", table_cell_style), Paragraph("Controls the interactive menu loop, user input handling, and exit", table_cell_style)],
    ]
    t_mod = Table(t_mod_data, colWidths=[2.2*inch, 4.0*inch])
    t_mod.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_mod)
    story.append(Spacer(1, 10))

    story.append(Paragraph("6.2 Important Design Decisions", section_style))
    story.append(Paragraph("•  Predictable fixed matrix sizes: #define P 5 and #define R 3 optimize memory layout.", bullet_style))
    story.append(Paragraph("•  In-place state rollback: Temporary subtraction and addition cleanly restore state without memory overhead.", bullet_style))
    story.append(Paragraph("•  Strict input sanitization: Process number checked (0 to 4); negative resource quantities explicitly rejected.", bullet_style))
    story.append(Paragraph("•  Safe sequence recording: An integer array tracks the execution sequence as processes finish.", bullet_style))

    story.append(Paragraph("6.3 Compilation and Execution", section_style))
    story.append(Paragraph(
        "The project is developed using standard ANSI C (C99 compliant) and compiles cleanly using the GNU Compiler Collection (GCC).<br/><br/>"
        "<b>Compilation command:</b><br/>"
        "<font face='Courier'>gcc -std=c99 -Wall -Wextra -O2 bankers_algorithm.c -o bankers_c</font><br/><br/>"
        "<b>Execution command on Linux / macOS:</b><br/>"
        "<font face='Courier'>./bankers_c</font><br/><br/>"
        "<b>Execution command on Windows:</b><br/>"
        "<font face='Courier'>bankers_c.exe</font>",
        body_style
    ))

    img_code = os.path.join(IMG_DIR, "fig_6_1_source_code.png")
    if os.path.exists(img_code):
        story.append(Image(img_code, width=5.8*inch, height=2.7*inch))
        story.append(Paragraph("<b>Figure 6.1: Source Code in Visual Studio Code</b>", caption_style))

    img_comp = os.path.join(IMG_DIR, "fig_6_2_compilation.png")
    if os.path.exists(img_comp):
        story.append(Image(img_comp, width=5.8*inch, height=1.9*inch))
        story.append(Paragraph("<b>Figure 6.2: Successful Compilation and Program Execution</b>", caption_style))

    story.append(PageBreak())

    # =========================================================
    # SECTION 7: TESTING AND RESULTS
    # =========================================================
    story.append(Paragraph("7. TESTING AND RESULTS", chapter_style))
    story.append(Paragraph("7.1 Test Environment", section_style))
    story.append(Paragraph(
        "Testing was performed on macOS (Darwin arm64) and Linux using GCC 14. The canonical Silberschatz textbook scenario "
        "featuring 5 processes and 3 resource types (A:10, B:5, C:7 total instances) was tested across all menu options.",
        body_style
    ))

    story.append(Paragraph("7.2 Sample Input State", section_style))
    story.append(Paragraph("<b>Table 7.1: Canonical Resource Allocation State (Silberschatz Example)</b>", caption_style))

    t_state_data = [
        [Paragraph("<b>Process</b>", table_header_style), Paragraph("<b>Allocation (A B C)</b>", table_header_style), Paragraph("<b>Maximum (A B C)</b>", table_header_style), Paragraph("<b>Need (A B C)</b>", table_header_style), Paragraph("<b>Available (A B C)</b>", table_header_style)],
        [Paragraph("P0", table_cell_style), Paragraph("0 &nbsp; 1 &nbsp; 0", table_cell_center), Paragraph("7 &nbsp; 5 &nbsp; 3", table_cell_center), Paragraph("7 &nbsp; 4 &nbsp; 3", table_cell_center), Paragraph("3 &nbsp; 3 &nbsp; 2", table_cell_center)],
        [Paragraph("P1", table_cell_style), Paragraph("2 &nbsp; 0 &nbsp; 0", table_cell_center), Paragraph("3 &nbsp; 2 &nbsp; 2", table_cell_center), Paragraph("1 &nbsp; 2 &nbsp; 2", table_cell_center), Paragraph("", table_cell_center)],
        [Paragraph("P2", table_cell_style), Paragraph("3 &nbsp; 0 &nbsp; 2", table_cell_center), Paragraph("9 &nbsp; 0 &nbsp; 2", table_cell_center), Paragraph("6 &nbsp; 0 &nbsp; 0", table_cell_center), Paragraph("", table_cell_center)],
        [Paragraph("P3", table_cell_style), Paragraph("2 &nbsp; 1 &nbsp; 1", table_cell_center), Paragraph("2 &nbsp; 2 &nbsp; 2", table_cell_center), Paragraph("0 &nbsp; 1 &nbsp; 1", table_cell_center), Paragraph("", table_cell_center)],
        [Paragraph("P4", table_cell_style), Paragraph("0 &nbsp; 0 &nbsp; 2", table_cell_center), Paragraph("4 &nbsp; 3 &nbsp; 3", table_cell_center), Paragraph("4 &nbsp; 3 &nbsp; 1", table_cell_center), Paragraph("", table_cell_center)],
        [Paragraph("<b>Total System</b>", table_header_style), Paragraph("<b>[ 10, &nbsp; 5, &nbsp; 7 ]</b>", table_header_style), Paragraph("", table_cell_center), Paragraph("", table_cell_center), Paragraph("", table_cell_center)],
    ]
    t_state = Table(t_state_data, colWidths=[1.1*inch, 1.3*inch, 1.3*inch, 1.3*inch, 1.2*inch])
    t_state.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_state)
    story.append(Spacer(1, 10))

    story.append(Paragraph("7.3 Actual Output Screenshots", section_style))

    # EMBEDDING USER'S PROVIDED SCREENSHOT!
    img_user = os.path.join(IMG_DIR, "actual_output_simulation.png")
    if os.path.exists(img_user):
        story.append(Image(img_user, width=5.5*inch, height=3.5*inch))
        story.append(Paragraph("<b>Figure 7.1: Main Menu & Resource Request Simulation (User Test Execution)</b>", caption_style))

    story.append(Paragraph(
        "As seen in Figure 7.1, the user chose Option 3 (Request Resources), selected process P1, and requested resources "
        "[R0: 1, R1: 0, R2: 2]. The simulator verified constraints, provisionally allocated resources, executed the safety algorithm, "
        "found the safe sequence P1 &rarr; P3 &rarr; P4 &rarr; P0 &rarr; P2, and successfully <b>GRANTED</b> the request.",
        body_style
    ))
    story.append(Spacer(1, 6))

    img_mat = os.path.join(IMG_DIR, "fig_7_2_matrices.png")
    if os.path.exists(img_mat):
        story.append(Image(img_mat, width=5.8*inch, height=2.6*inch))
        story.append(Paragraph("<b>Figure 7.2: Resource Matrices Display Output (Option 1)</b>", caption_style))

    img_trace = os.path.join(IMG_DIR, "fig_7_3_safety_trace.png")
    if os.path.exists(img_trace):
        story.append(Image(img_trace, width=5.8*inch, height=2.0*inch))
        story.append(Paragraph("<b>Figure 7.3: Safety State Verification Output (Option 2)</b>", caption_style))

    story.append(Paragraph("7.4 Scenario Verification and Outcome Summary", section_style))
    story.append(Paragraph("<b>Table 7.2: Verification Scenarios and Algorithmic Outcomes</b>", caption_style))

    t_res_data = [
        [Paragraph("<b>Scenario / Action</b>", table_header_style), Paragraph("<b>Parameters</b>", table_header_style), Paragraph("<b>Observed Outcome</b>", table_header_style), Paragraph("<b>Safety Status</b>", table_header_style)],
        [Paragraph("Initial System State", table_cell_style), Paragraph("P = 5, R = 3", table_cell_style), Paragraph("Safe Sequence: P1 &rarr; P3 &rarr; P4 &rarr; P0 &rarr; P2", table_cell_style), Paragraph("<font color='#059669'><b>SAFE</b></font>", table_cell_center)],
        [Paragraph("Valid Request by P1", table_cell_style), Paragraph("Request: [1, 0, 2]", table_cell_style), Paragraph("Granted safely; Available becomes [2, 3, 0]", table_cell_style), Paragraph("<font color='#059669'><b>SAFE</b></font>", table_cell_center)],
        [Paragraph("Exceed Maximum Need", table_cell_style), Paragraph("P0 requests [0, 5, 0]", table_cell_style), Paragraph("Denied: Request exceeds process Need", table_cell_style), Paragraph("<font color='#DC2626'><b>REJECTED</b></font>", table_cell_center)],
        [Paragraph("Exceed Available Pool", table_cell_style), Paragraph("P4 requests [4, 3, 1]", table_cell_style), Paragraph("Wait: Request exceeds Available [3, 3, 2]", table_cell_style), Paragraph("<font color='#D97706'><b>WAIT</b></font>", table_cell_center)],
        [Paragraph("Unsafe Request Hazard", table_cell_style), Paragraph("P0 requests [0, 2, 0]", table_cell_style), Paragraph("Denied & Rolled Back: leads to unsafe state", table_cell_style), Paragraph("<font color='#DC2626'><b>ROLLED BACK</b></font>", table_cell_center)],
    ]
    t_res = Table(t_res_data, colWidths=[1.5*inch, 1.4*inch, 2.3*inch, 1.0*inch])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_res)
    story.append(PageBreak())

    # =========================================================
    # SECTION 8 & 9
    # =========================================================
    story.append(Paragraph("8. DISCUSSION", chapter_style))
    story.append(Paragraph("8.1 Comparison of Deadlock Handling Strategies", section_style))
    story.append(Paragraph(
        "Deadlock handling in operating systems is approached through four primary paradigms:<br/>"
        "• <b>Deadlock Prevention</b>: Imposes strict structural constraints to invalidate one of the four necessary Coffman conditions "
        "(Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait). However, this severely curtails device utilization.<br/>"
        "• <b>Deadlock Avoidance (Banker's Algorithm)</b>: Allows all four conditions to exist but dynamically inspects every request. "
        "It achieves higher concurrency than prevention by granting requests whenever system safety is preserved.<br/>"
        "• <b>Deadlock Detection and Recovery</b>: Optimistically grants all requests and periodically checks for deadlock using a wait-for graph. "
        "If deadlock is detected, processes must be aborted or resources preempted, causing data loss.<br/>"
        "• <b>Deadlock Ignorance (Ostrich Algorithm)</b>: Ignores the problem under the assumption that deadlocks occur infrequently. Used by "
        "general-purpose operating systems like Linux and Windows, which rely on user intervention when an application hangs.",
        body_style
    ))

    story.append(Paragraph("8.2 Interpretation of Matrices and Safety Sequences", section_style))
    story.append(Paragraph(
        "The safety algorithm operates on the principle of conservative worst-case analysis: it assumes that whenever a process runs, "
        "it will request its entire remaining Need before terminating and releasing all held resources. In our textbook state, "
        "P1 is satisfied first (Need [1, 2, 2] &le; Work [3, 3, 2]), releasing [2, 0, 0] and boosting Work to [5, 3, 2]. This creates a "
        "cascade effect allowing P3, P4, P0, and P2 to finish in succession. Multiple topological sequences may exist, but any valid sequence "
        "proves safety.",
        body_style
    ))

    story.append(Paragraph("8.3 Limitations", section_style))
    story.append(Paragraph("•  Requires prior knowledge of maximum claims, which is difficult for general-purpose user applications.", bullet_style))
    story.append(Paragraph("•  Assumes a fixed number of processes and resource types, whereas modern operating systems spawn processes dynamically.", bullet_style))
    story.append(Paragraph("•  Conservative policy: may delay requests that would not have actually resulted in deadlock in practice.", bullet_style))

    story.append(Paragraph("9. CONCLUSION AND FUTURE SCOPE", chapter_style))
    story.append(Paragraph("9.1 Conclusion", section_style))
    story.append(Paragraph(
        "The Banker's Algorithm for Deadlock Avoidance Simulator successfully demonstrates the principles of safe state verification "
        "and dynamic resource allocation using the C programming language. The simulator computes Need matrices, enforces maximum claim "
        "boundaries, simulates provisional allocations, and guarantees that circular deadlock cannot occur through automated rollback. "
        "Testing validated the canonical Silberschatz scenario and confirmed that valid requests (P1 requesting [1, 0, 2]) are safely granted "
        "while unsafe requests are promptly prevented.",
        body_style
    ))

    story.append(Paragraph("9.2 Future Scope", section_style))
    story.append(Paragraph("•  Extending the engine to support dynamic runtime process creation and resource registration.", bullet_style))
    story.append(Paragraph("•  Integrating multi-threading using POSIX pthreads and mutex locks to simulate concurrent thread resource claims.", bullet_style))
    story.append(Paragraph("•  Developing a web-based graphical dashboard (Flask / JavaScript) featuring animated resource gauges and matrix visualizers.", bullet_style))
    story.append(Paragraph("•  Exporting execution trace logs and state tables to CSV and PDF formats for automated lab evaluation.", bullet_style))
    story.append(PageBreak())

    # =========================================================
    # SECTION 10: REFERENCES & APPENDICES
    # =========================================================
    story.append(Paragraph("10. REFERENCES", chapter_style))
    references = [
        "[1] A. Silberschatz, P. B. Galvin, and G. Gagne, <i>Operating System Concepts</i>, 10th ed. Hoboken, NJ, USA: Wiley, 2018.",
        "[2] W. Stallings, <i>Operating Systems: Internals and Design Principles</i>, 9th ed. Harlow, England: Pearson, 2018.",
        "[3] A. S. Tanenbaum and H. Bos, <i>Modern Operating Systems</i>, 4th ed. Boston, MA, USA: Pearson, 2015.",
        "[4] E. W. Dijkstra, “Cooperating sequential processes,” Technological University, Eindhoven, The Netherlands, Tech. Rep. EWD-123, 1965.",
        "[5] B. W. Kernighan and D. M. Ritchie, <i>The C Programming Language</i>, 2nd ed. Englewood Cliffs, NJ, USA: Prentice Hall, 1988.",
        "[6] Free Software Foundation, “Using the GNU Compiler Collection (GCC),” [Online]. Available: https://gcc.gnu.org/onlinedocs/. [Accessed: Nov. 2026].",
        "[7] Visual Studio Code, “Documentation and C/C++ Extensions,” [Online]. Available: https://code.visualstudio.com/docs. [Accessed: Nov. 2026].",
    ]
    for r in references:
        story.append(Paragraph(r, ParagraphStyle('Ref', parent=body_style, spaceAfter=4)))

    story.append(Spacer(1, 10))
    story.append(Paragraph("APPENDIX A – SAMPLE INPUT & SYSTEM ALLOCATION STATE", chapter_style))
    story.append(Paragraph("<b>Table A.1: Sample Input State Vectors and Matrices</b>", caption_style))

    t_app_data = [
        [Paragraph("<b>Process ID</b>", table_header_style), Paragraph("<b>Allocation [A B C]</b>", table_header_style), Paragraph("<b>Maximum Claim [A B C]</b>", table_header_style), Paragraph("<b>Need Vector [A B C]</b>", table_header_style)],
        [Paragraph("P0", table_cell_style), Paragraph("0 &nbsp; 1 &nbsp; 0", table_cell_center), Paragraph("7 &nbsp; 5 &nbsp; 3", table_cell_center), Paragraph("7 &nbsp; 4 &nbsp; 3", table_cell_center)],
        [Paragraph("P1", table_cell_style), Paragraph("2 &nbsp; 0 &nbsp; 0", table_cell_center), Paragraph("3 &nbsp; 2 &nbsp; 2", table_cell_center), Paragraph("1 &nbsp; 2 &nbsp; 2", table_cell_center)],
        [Paragraph("P2", table_cell_style), Paragraph("3 &nbsp; 0 &nbsp; 2", table_cell_center), Paragraph("9 &nbsp; 0 &nbsp; 2", table_cell_center), Paragraph("6 &nbsp; 0 &nbsp; 0", table_cell_center)],
        [Paragraph("P3", table_cell_style), Paragraph("2 &nbsp; 1 &nbsp; 1", table_cell_center), Paragraph("2 &nbsp; 2 &nbsp; 2", table_cell_center), Paragraph("0 &nbsp; 1 &nbsp; 1", table_cell_center)],
        [Paragraph("P4", table_cell_style), Paragraph("0 &nbsp; 0 &nbsp; 2", table_cell_center), Paragraph("4 &nbsp; 3 &nbsp; 3", table_cell_center), Paragraph("4 &nbsp; 3 &nbsp; 1", table_cell_center)],
    ]
    t_app = Table(t_app_data, colWidths=[1.5*inch, 1.5*inch, 1.6*inch, 1.6*inch])
    t_app.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_app)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>System Resource Vector:</b> Available = [ 3, 3, 2 ]<br/>"
        "<b>Total System Capacity:</b> [ 10, 5, 7 ]<br/>"
        "Select menu option 2 to check safety or option 3 to simulate process requests.",
        body_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("APPENDIX B – SOURCE CODE SUBMISSION", chapter_style))
    story.append(Paragraph(
        "The complete C source code of the Banker's Algorithm Simulator is provided below. "
        "The code implements calculateNeed(), displayMatrices(), safetyAlgorithm(), requestResources(), clearScreen(), and main().",
        body_style
    ))

    code_block = """#include <stdio.h>
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

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8.5,
        leading=10.5,
        textColor=colors.HexColor('#1e293b')
    )
    story.append(Preformatted(code_block, code_style))

    doc.build(story)
    print(f"PDF successfully generated at: {OUTPUT_PDF}")

if __name__ == "__main__":
    create_pdf()
