/**
 * @file bankers_algorithm.cpp
 * @brief Banker's Algorithm for Deadlock Avoidance in C++17
 * Operating Systems Mini Project
 *
 * Implements:
 * 1. Safety Algorithm with execution trace
 * 2. Resource-Request Algorithm with automatic rollback
 * 3. Matrix formatting and file input loader
 */

#include <iostream>
#include <vector>
#include <string>
#include <iomanip>
#include <fstream>
#include <sstream>

using namespace std;

class BankersAlgorithm {
private:
    int n; // Number of processes
    int m; // Number of resources
    vector<string> process_names;
    vector<string> resource_names;
    vector<int> available;
    vector<vector<int>> max_claim;
    vector<vector<int>> allocation;
    vector<vector<int>> need;

    void calculate_need() {
        need.resize(n, vector<int>(m, 0));
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < m; ++j) {
                need[i][j] = max_claim[i][j] - allocation[i][j];
            }
        }
    }

public:
    BankersAlgorithm(int num_proc, int num_res,
                     const vector<int>& avail,
                     const vector<vector<int>>& max_mat,
                     const vector<vector<int>>& alloc_mat)
        : n(num_proc), m(num_res), available(avail),
          max_claim(max_mat), allocation(alloc_mat) {

        for (int i = 0; i < n; ++i) {
            process_names.push_back("P" + to_string(i));
        }
        for (int j = 0; j < m; ++j) {
            resource_names.push_back(string(1, (char)('A' + j)));
        }
        calculate_need();
    }

    void display_state() const {
        cout << "\n" << string(75, '=') << "\n";
        cout << setw(48) << "CURRENT SYSTEM STATE TABLE\n";
        cout << string(75, '=') << "\n";

        cout << left << setw(8) << "Process" << " | ";
        cout << "Allocation  | ";
        cout << "Max Claim   | ";
        cout << "Need        | ";
        cout << "Available\n";

        cout << left << setw(8) << "" << " | ";
        for (int k = 0; k < 4; ++k) {
            for (int j = 0; j < m; ++j) cout << resource_names[j] << " ";
            cout << (k < 3 ? "| " : "\n");
        }
        cout << string(75, '-') << "\n";

        for (int i = 0; i < n; ++i) {
            cout << left << setw(8) << process_names[i] << " | ";
            for (int j = 0; j < m; ++j) cout << allocation[i][j] << " ";
            cout << "| ";
            for (int j = 0; j < m; ++j) cout << max_claim[i][j] << " ";
            cout << "| ";
            for (int j = 0; j < m; ++j) cout << need[i][j] << " ";
            cout << "| ";
            if (i == 0) {
                for (int j = 0; j < m; ++j) cout << available[j] << " ";
            }
            cout << "\n";
        }
        cout << string(75, '=') << "\n";
    }

    bool is_safe(vector<string>& safe_sequence, bool verbose = true) const {
        vector<int> work = available;
        vector<bool> finish(n, false);
        safe_sequence.clear();

        if (verbose) {
            cout << "\n" << string(75, '-') << "\n";
            cout << setw(46) << "SAFETY ALGORITHM EXECUTION TRACE\n";
            cout << string(75, '-') << "\n";
            cout << left << setw(6) << "Step" << " | "
                 << setw(8) << "Process" << " | "
                 << setw(16) << "Work (Before)" << " | "
                 << setw(14) << "Need" << " | "
                 << setw(16) << "Work (After)" << "\n";
            cout << string(75, '-') << "\n";
        }

        int step = 1;
        while (safe_sequence.size() < (size_t)n) {
            bool found = false;
            for (int i = 0; i < n; ++i) {
                if (!finish[i]) {
                    bool can_allocate = true;
                    for (int j = 0; j < m; ++j) {
                        if (need[i][j] > work[j]) {
                            can_allocate = false;
                            break;
                        }
                    }

                    if (can_allocate) {
                        stringstream wb, wa, nd;
                        wb << "[";
                        for (int j = 0; j < m; ++j) wb << work[j] << (j + 1 < m ? " " : "");
                        wb << "]";

                        nd << "[";
                        for (int j = 0; j < m; ++j) nd << need[i][j] << (j + 1 < m ? " " : "");
                        nd << "]";

                        for (int j = 0; j < m; ++j) {
                            work[j] += allocation[i][j];
                        }
                        finish[i] = true;
                        safe_sequence.push_back(process_names[i]);

                        wa << "[";
                        for (int j = 0; j < m; ++j) wa << work[j] << (j + 1 < m ? " " : "");
                        wa << "]";

                        if (verbose) {
                            cout << left << setw(6) << step++ << " | "
                                 << setw(8) << process_names[i] << " | "
                                 << setw(16) << wb.str() << " | "
                                 << setw(14) << nd.str() << " | "
                                 << setw(16) << wa.str() << "\n";
                        }

                        found = true;
                        break;
                    }
                }
            }

            if (!found) break;
        }

        if (verbose) cout << string(75, '-') << "\n";

        for (bool f : finish) {
            if (!f) return false;
        }
        return true;
    }

    bool request_resources(int process_id, const vector<int>& req) {
        if (process_id < 0 || process_id >= n) {
            cout << "Error: Invalid process ID.\n";
            return false;
        }

        // Rule 1: Request <= Need
        for (int j = 0; j < m; ++j) {
            if (req[j] > need[process_id][j]) {
                cout << "[DENIED] Error: Process " << process_names[process_id]
                     << " exceeded maximum claim for resource " << resource_names[j] << ".\n";
                return false;
            }
        }

        // Rule 2: Request <= Available
        for (int j = 0; j < m; ++j) {
            if (req[j] > available[j]) {
                cout << "[WAIT] Process " << process_names[process_id]
                     << " must wait: Resource " << resource_names[j] << " unavailable.\n";
                return false;
            }
        }

        // Rule 3: Provisional allocation
        for (int j = 0; j < m; ++j) {
            available[j] -= req[j];
            allocation[process_id][j] += req[j];
            need[process_id][j] -= req[j];
        }

        // Rule 4: Safety test
        vector<string> temp_seq;
        if (is_safe(temp_seq, false)) {
            cout << "[GRANTED] Request granted safely! Safe sequence: ";
            for (size_t k = 0; k < temp_seq.size(); ++k) {
                cout << temp_seq[k] << (k + 1 < temp_seq.size() ? " -> " : "\n");
            }
            return true;
        } else {
            cout << "[ROLLBACK] Request denied: Leads to UNSAFE STATE (potential deadlock). Rolling back state.\n";
            for (int j = 0; j < m; ++j) {
                available[j] += req[j];
                allocation[process_id][j] -= req[j];
                need[process_id][j] += req[j];
            }
            return false;
        }
    }
};

int main() {
    cout << "===========================================================\n";
    cout << "  BANKER'S ALGORITHM SIMULATOR (C++17 IMPLEMENTATION)      \n";
    cout << "  Deadlock Avoidance & Resource Request Verification       \n";
    cout << "===========================================================\n";

    // Silberschatz standard problem
    int n = 5, m = 3;
    vector<int> avail = {3, 3, 2};
    vector<vector<int>> max_mat = {
        {7, 5, 3},
        {3, 2, 2},
        {9, 0, 2},
        {2, 2, 2},
        {4, 3, 3}
    };
    vector<vector<int>> alloc_mat = {
        {0, 1, 0},
        {2, 0, 0},
        {3, 0, 2},
        {2, 1, 1},
        {0, 0, 2}
    };

    BankersAlgorithm ba(n, m, avail, max_mat, alloc_mat);
    ba.display_state();

    vector<string> safe_seq;
    bool safe = ba.is_safe(safe_seq);

    if (safe) {
        cout << "\nRESULT: System is in a SAFE STATE!\n";
        cout << "Safe Sequence: ";
        for (size_t i = 0; i < safe_seq.size(); ++i) {
            cout << safe_seq[i] << (i + 1 < safe_seq.size() ? " -> " : "\n");
        }
    } else {
        cout << "\nRESULT: System is in an UNSAFE STATE!\n";
    }

    // Demonstrate resource request P1: [1, 0, 2]
    cout << "\n>>> Simulating Process P1 requesting resources [1, 0, 2] <<<\n";
    ba.request_resources(1, {1, 0, 2});
    ba.display_state();

    // Demonstrate invalid request exceeding Need
    cout << "\n>>> Simulating Process P0 requesting resources [0, 5, 0] (Exceeds Need) <<<\n";
    ba.request_resources(0, {0, 5, 0});

    // Demonstrate request leading to wait
    cout << "\n>>> Simulating Process P4 requesting resources [4, 3, 1] (Exceeds Available) <<<\n";
    ba.request_resources(4, {4, 3, 1});

    return 0;
}
