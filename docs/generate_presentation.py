"""
generate_presentation.py - Generates an 8-10 Minute Presentation Deck (.pptx)
Operating Systems Mini Project
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor


def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    PRIMARY_COLOR = RGBColor(15, 23, 42)
    ACCENT_BLUE = RGBColor(59, 130, 246)
    TEXT_DARK = RGBColor(30, 41, 59)
    TEXT_MUTED = RGBColor(100, 116, 139)

    def add_header(slide, title, category="OPERATING SYSTEMS MINI PROJECT"):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_BLUE

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = PRIMARY_COLOR

    def add_bullet_list(slide, items):
        box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
        tf = box.text_frame
        tf.word_wrap = True
        for idx, (title, desc) in enumerate(items):
            p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
            r1 = p.add_run()
            r1.text = f"•  {title} "
            r1.font.bold = True
            r1.font.size = Pt(15)
            r1.font.color.rgb = PRIMARY_COLOR

            r2 = p.add_run()
            r2.text = desc
            r2.font.size = Pt(15)
            r2.font.color.rgb = TEXT_DARK
            p.space_after = Pt(12)

    # Slide 1: Title
    s1 = prs.slides.add_slide(blank_layout)
    tbox = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.33), Inches(3.8))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "OPERATING SYSTEMS MINI PROJECT • TOPIC 11"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_BLUE
    p0.space_after = Pt(14)

    p1 = tf1.add_paragraph()
    p1.text = "Banker's Algorithm for Deadlock Avoidance"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = PRIMARY_COLOR
    p1.space_after = Pt(10)

    p2 = tf1.add_paragraph()
    p2.text = "Dynamic Resource-Allocation Request Verification and State Safety Analysis"
    p2.font.size = Pt(18)
    p2.font.color.rgb = TEXT_MUTED
    p2.space_after = Pt(30)

    p3 = tf1.add_paragraph()
    p3.text = "Student Name: Avignya Hjakku (and Team)  |  Guide: Faculty Guide  |  Dept. of Computer Science & Engineering"
    p3.font.size = Pt(13)
    p3.font.color.rgb = TEXT_DARK

    # Slide 2: Concurrency & Deadlocks
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Concurrency and the Deadlock Hazard")
    add_bullet_list(s2, [
        ("Multiprogrammed OS Context:", "Concurrent processes share scarce resources (CPU, Memory, I/O devices, Files)."),
        ("What is a Deadlock?", "A permanent state where a set of processes are blocked because every process holds resources and waits for resources held by another process in the set."),
        ("Real-World Impact:", "System freezing, severe throughput collapse, transaction halts, and unresponsive kernels."),
        ("Fundamental Problem:", "How can an OS allocate multi-instance resources dynamically without leading the system into an inescapable circular freeze?"),
    ])

    # Slide 3: Coffman Conditions
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "The Four Necessary Coffman Conditions (1971)")
    add_bullet_list(s3, [
        ("1. Mutual Exclusion:", "At least one resource must be held in non-shareable mode (exclusive single-process access)."),
        ("2. Hold and Wait:", "A process must hold at least one resource while waiting to acquire additional resources held by peers."),
        ("3. No Preemption:", "Resources cannot be forcibly confiscated from a process; they must be released voluntarily."),
        ("4. Circular Wait:", "A closed loop {P0 -> P1 -> ... -> Pn -> P0} exists where each process awaits a resource held by the next."),
    ])

    # Slide 4: Deadlock Handling Strategies
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Comparison of Deadlock Handling Strategies")
    add_bullet_list(s4, [
        ("Deadlock Ignorance (Ostrich):", "Assume deadlocks never happen. Used in Linux/Windows because deadlocks are infrequent and avoidance overhead is deemed high."),
        ("Deadlock Prevention:", "Statically invalidate one of the 4 Coffman conditions. Highly restrictive, leads to low device utilization and thread starvation."),
        ("Deadlock Detection & Recovery:", "Allow deadlocks to occur, run periodic graph cycle checks, and kill processes to break deadlocks. High recovery cost."),
        ("Deadlock Avoidance (Our Focus):", "Dynamically inspects resource requests in real-time. Only grants requests that leave the system in a guaranteed SAFE STATE."),
    ])

    # Slide 5: Banker's Concept
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Dijkstra's Banker's Algorithm Concept")
    add_bullet_list(s5, [
        ("Banking Metaphor (1965):", "A small-town banker has a limited pool of cash credit. Clients have maximum credit ceilings. The banker never lends cash if it leaves the bank unable to satisfy at least one client's full demand to completion."),
        ("Safe State Definition:", "A state is SAFE if there exists at least one sequence <P0, P1, ..., Pn> such that for each Pi, its remaining need can be satisfied by current Available plus resources already held by preceding processes."),
        ("Unsafe ≠ Deadlock:", "An unsafe state is NOT necessarily deadlocked yet, but the OS cannot prevent processes from eventually deadlocking if they request their maximum claims."),
    ])

    # Slide 6: Mathematical Model
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Mathematical Model and Data Structures")
    add_bullet_list(s6, [
        ("Available[m]:", "Vector of length m. Available[j] = k indicates k unallocated instances of resource type Rj."),
        ("Max[n][m]:", "Matrix n x m. Max[i][j] = k defines the maximum demand of process Pi for resource Rj."),
        ("Allocation[n][m]:", "Matrix n x m. Allocation[i][j] = k defines the number of instances of Rj currently held by Pi."),
        ("Need[n][m]:", "Matrix n x m. Need[i][j] = Max[i][j] - Allocation[i][j], representing remaining demand."),
        ("System Invariant:", "Total_Resources[j] = Available[j] + Sum(Allocation[i][j] for all i)."),
    ])

    # Slide 7: Safety Algorithm Workflow
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Banker's Safety Algorithm Workflow")
    add_bullet_list(s7, [
        ("Step 1 (Initialization):", "Work = Available (length m); Finish[i] = False for all i = 0, ..., n-1."),
        ("Step 2 (Candidate Search):", "Find an index i such that: Finish[i] == False AND Need[i][j] <= Work[j] (for all j). If no such i exists, jump to Step 4."),
        ("Step 3 (Reclaim Resources):", "Work = Work + Allocation[i]; Finish[i] = True; Append Pi to safe sequence. Loop back to Step 2."),
        ("Step 4 (Verification):", "If Finish[i] == True for all i, system is SAFE (safe sequence found). Else, system is UNSAFE."),
    ])

    # Slide 8: Resource Request & Rollback
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Resource-Request Algorithm & State Rollback")
    add_bullet_list(s8, [
        ("Rule 1 (Claim Bound):", "If Request[i] > Need[i], raise Error: Process exceeded its declared maximum claim."),
        ("Rule 2 (Availability Bound):", "If Request[i] > Available, Process Pi MUST WAIT: Resources currently unavailable."),
        ("Rule 3 (Provisional Simulation):", "Pretend to allocate: Available -= Request; Allocation[i] += Request; Need[i] -= Request."),
        ("Rule 4 (Safety Check & Rollback):", "Run Safety Algorithm on provisional state: If SAFE, grant permanently; if UNSAFE, ROLLBACK state and force process to wait."),
    ])

    # Slide 9: Architecture
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Software Architecture and Features")
    add_bullet_list(s9, [
        ("Python Core Engine:", "Modular object-oriented design (BankerState, BankerEngine, SafetyResult)."),
        ("Interactive Terminal CLI:", "Formatted ASCII tables, interactive request simulation, and real-time step traces."),
        ("Modern Web Dashboard:", "Flask REST API + modern CSS Grid/Flexbox UI + step-by-step visual animation."),
        ("Backtracking DFS Engine:", "Computes ALL valid topological safe sequence permutations."),
        ("C++17 & ANSI C Impls:", "Standalone native implementations for classical systems programming labs."),
        ("Automated Test Suite:", "Comprehensive unit tests covering boundary edge cases and invalid claims."),
    ])

    # Slide 10: Experimental Results
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Experimental Validation & Results")
    add_bullet_list(s10, [
        ("Canonical Silberschatz Test:", "5 Processes, 3 Resources. Found primary sequence: P1 -> P3 -> P0 -> P2 -> P4 (16 valid safe paths)."),
        ("Valid Request Evaluation:", "P1 requested [1, 0, 2]. Successfully granted; system remained safe with updated Available = [2, 3, 0]."),
        ("Exceeding Claim Rejection:", "P0 requested [0, 6, 0] (exceeds Need [7, 4, 3]). Caught and denied with DENIED_EXCEEDS_MAX."),
        ("Unsafe Request Prevention:", "P0 requested [3, 3, 0]. Provisional safety failed; state automatically rolled back."),
        ("Unsafe / Deadlock Scenario:", "Available [0, 0, 0] with pending needs correctly flagged as UNSAFE STATE."),
    ])

    # Slide 11: Complexity
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Algorithmic Complexity & Practical Tradeoffs")
    add_bullet_list(s11, [
        ("Time Complexity: O(m · n²):", "With n processes and m resources, at most n passes are made, each evaluating Need <= Work in m operations. Empirically verified via benchmark runner."),
        ("Space Complexity: O(m + n):", "Requires only linear auxiliary space for Work and Finish vectors."),
        ("Strengths:", "Mathematically guaranteed deadlock freedom; avoids destructive aborts/rollbacks required by detection algorithms."),
        ("Practical Limitations:", "Requires advance knowledge of maximum resource demands; processes and resource quantities must be fixed; conservative denial of requests that might not have deadlocked."),
    ])

    # Slide 12: Conclusion & Viva
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Conclusion and Viva Summary")
    add_bullet_list(s12, [
        ("Project Achievements:", "Engineered a complete, validated deadlock avoidance platform with dual UI and cross-language support."),
        ("Educational Value:", "Transforms abstract theoretical matrices into intuitive, interactive visual simulations."),
        ("Key Viva Takeaway 1:", "Safe State vs Unsafe State: Safe guarantees an execution path; Unsafe means deadlock is possible, not guaranteed."),
        ("Key Viva Takeaway 2:", "Banker's Algorithm is an AVOIDANCE technique, NOT prevention or detection."),
        ("Demonstration Ready:", "Live Web GUI & interactive CLI tested and verified!"),
    ])

    output_path = os.path.join(os.path.dirname(__file__), "presentation_slides.pptx")
    prs.save(output_path)
    print(f"Presentation successfully generated at: {output_path}")


if __name__ == "__main__":
    build_presentation()
