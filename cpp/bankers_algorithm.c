/**
 * @file bankers_algorithm.c
 * @brief ANSI C implementation of Banker's Algorithm for Deadlock Avoidance
 * Operating Systems Mini Project
 */

#include <stdio.h>
#include <stdbool.h>

#define MAX_PROC 20
#define MAX_RES 10

int n = 5; // Number of processes
int m = 3; // Number of resources

int available[MAX_RES] = {3, 3, 2};
int max_claim[MAX_PROC][MAX_RES] = {
    {7, 5, 3},
    {3, 2, 2},
    {9, 0, 2},
    {2, 2, 2},
    {4, 3, 3}
};
int allocation[MAX_PROC][MAX_RES] = {
    {0, 1, 0},
    {2, 0, 0},
    {3, 0, 2},
    {2, 1, 1},
    {0, 0, 2}
};
int need[MAX_PROC][MAX_RES];

void calculate_need() {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            need[i][j] = max_claim[i][j] - allocation[i][j];
        }
    }
}

void print_state() {
    printf("\n=======================================================================\n");
    printf("                  SYSTEM RESOURCE ALLOCATION TABLE                     \n");
    printf("=======================================================================\n");
    printf("Process | Allocation  | Max Claim   | Need        | Available\n");
    printf("        | A  B  C     | A  B  C     | A  B  C     | A  B  C\n");
    printf("-----------------------------------------------------------------------\n");
    for (int i = 0; i < n; i++) {
        printf("P%-6d |", i);
        for (int j = 0; j < m; j++) printf(" %2d", allocation[i][j]);
        printf("   |");
        for (int j = 0; j < m; j++) printf(" %2d", max_claim[i][j]);
        printf("   |");
        for (int j = 0; j < m; j++) printf(" %2d", need[i][j]);
        printf("   |");
        if (i == 0) {
            for (int j = 0; j < m; j++) printf(" %2d", available[j]);
        }
        printf("\n");
    }
    printf("=======================================================================\n");
}

bool is_safe(int safe_seq[], bool print_trace) {
    int work[MAX_RES];
    bool finish[MAX_PROC];

    for (int j = 0; j < m; j++) work[j] = available[j];
    for (int i = 0; i < n; i++) finish[i] = false;

    int count = 0;
    if (print_trace) {
        printf("\n--- SAFETY ALGORITHM EXECUTION TRACE ---\n");
        printf("Step | Process | Work (Before) | Need      | Work (After)\n");
        printf("----------------------------------------------------------\n");
    }

    while (count < n) {
        bool found = false;
        for (int i = 0; i < n; i++) {
            if (!finish[i]) {
                bool can_run = true;
                for (int j = 0; j < m; j++) {
                    if (need[i][j] > work[j]) {
                        can_run = false;
                        break;
                    }
                }

                if (can_run) {
                    int work_before[MAX_RES];
                    for (int j = 0; j < m; j++) work_before[j] = work[j];

                    for (int j = 0; j < m; j++) work[j] += allocation[i][j];
                    finish[i] = true;
                    safe_seq[count++] = i;
                    found = true;

                    if (print_trace) {
                        printf("%-4d | P%-6d | [%d, %d, %d]     | [%d, %d, %d] | [%d, %d, %d]\n",
                               count, i,
                               work_before[0], work_before[1], work_before[2],
                               need[i][0], need[i][1], need[i][2],
                               work[0], work[1], work[2]);
                    }
                    break;
                }
            }
        }
        if (!found) break;
    }

    for (int i = 0; i < n; i++) {
        if (!finish[i]) return false;
    }
    return true;
}

bool request_resources(int pid, int req[]) {
    // 1. Check Request <= Need
    for (int j = 0; j < m; j++) {
        if (req[j] > need[pid][j]) {
            printf("[DENIED] Error: Process P%d requested more than declared maximum claim.\n", pid);
            return false;
        }
    }

    // 2. Check Request <= Available
    for (int j = 0; j < m; j++) {
        if (req[j] > available[j]) {
            printf("[WAIT] Process P%d must wait: requested resources not currently available.\n", pid);
            return false;
        }
    }

    // 3. Provisional allocation
    for (int j = 0; j < m; j++) {
        available[j] -= req[j];
        allocation[pid][j] += req[j];
        need[pid][j] -= req[j];
    }

    // 4. Check safety
    int temp_seq[MAX_PROC];
    if (is_safe(temp_seq, false)) {
        printf("[GRANTED] Request by P%d GRANTED successfully. System remains SAFE.\n", pid);
        return true;
    } else {
        printf("[DENIED - ROLLBACK] Request by P%d leads to UNSAFE state. Rolled back.\n", pid);
        for (int j = 0; j < m; j++) {
            available[j] += req[j];
            allocation[pid][j] -= req[j];
            need[pid][j] += req[j];
        }
        return false;
    }
}

int main() {
    calculate_need();
    print_state();

    int safe_sequence[MAX_PROC];
    if (is_safe(safe_sequence, true)) {
        printf("\nResult: System is in a SAFE STATE!\nSafe Sequence: ");
        for (int i = 0; i < n; i++) {
            printf("P%d%s", safe_sequence[i], (i + 1 < n) ? " -> " : "\n");
        }
    } else {
        printf("\nResult: System is in an UNSAFE STATE!\n");
    }

    // Test request
    printf("\nSimulating P1 requesting [1, 0, 2]:\n");
    int req1[] = {1, 0, 2};
    request_resources(1, req1);
    print_state();

    return 0;
}
