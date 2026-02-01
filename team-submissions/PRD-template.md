# Product Requirements Document (PRD)

**Project Name:** QE-LABS
**Team Name:** EigenHackers
**GitHub Repository:** https://github.com/diiwik/2026-NVIDIA

---

> **Note to Students:** > The questions and examples provided in the specific sections below are **prompts to guide your thinking**, not a rigid checklist. 
> * **Adaptability:** If a specific question doesn't fit your strategy, you may skip or adapt it.
> * **Depth:** You are encouraged to go beyond these examples. If there are other critical technical details relevant to your specific approach, please include them.
> * **Goal:** The objective is to convince the reader that you have a solid plan, not just to fill in boxes.

---

## 1. Team Roles & Responsibilities [You can DM the judges this information instead of including it in the repository]

| Role | Name | GitHub Handle | Discord Handle
| :--- | :--- | :--- | :--- |
| **Project Lead** (Architect) | [Name] | [@handle] | [@handle] |
| **GPU Acceleration PIC** (Builder) | [Name] | [@handle] | [@handle] |
| **Quality Assurance PIC** (Verifier) | [Name] | [@handle] | [@handle] |
| **Technical Marketing PIC** (Storyteller) | [Name] | [@handle] | [@handle] |

---

## 2. The Architecture
**Owner:** Project Lead

### Choice of Quantum Algorithm
* **Algorithm:** VQE powered population generation for LABS problem
    
* **Motivation:** [Why this algorithm? Connect it to the problem structure or learning goals.]
    Uses VQE to generate structured bitstrings. Those bitstrings are biased toward low-energy regions. Classical search then refines them.
---

## 3. The Acceleration Strategy
**Owner:** GPU Acceleration PIC

### Quantum Acceleration (CUDA-Q)
* **Strategy:** [How will you use the GPU for the quantum part?]
    * After testing with a single L4, we will target the `nvidia-mgpu` backend to distribute the circuit simulation across B300 for large $N$.
 

### Classical Acceleration (MTS)
* **Strategy:** [The classical search has many opportuntities for GPU acceleration. What will you chose to do?]
    * The standard MTS evaluates neighbors one by one. We will use `cupy` to rewrite the energy function to evaluate a batch of 1,000 neighbor flips simultaneously on the GPU.

### Hardware Targets
* **Dev Environment:** Qbraid (CPU) for logic, Brev L4 for initial GPU testing
* **Production Environment:** Brev B300-288GB for final N=40 benchmarks

---

## 4. The Verification Plan
**Owner:** Quality Assurance PIC

### Unit Testing Strategy
* **Framework:** [e.g., `pytest`, `unittest`]
* **AI Hallucination Guardrails:** [How do you know the AI code is right?]
      We first check whether it fits the logic and there are no syntax error present in them. 

### Core Correctness Checks
* **Check 1 (Symmetry):** 
      LABS sequence $S$ and its negation $-S$ must have identical energies. By printing the result generated from the function. We saw there were no instance of symmetry multiple times.
* **Check 2 (Identity):**
    * no weird evolution should happen when dt = 0, and none happens in our case.The circuit should reduce to identity.Output state = input state.Measured bitstring distribution should be unchanged. Energy must match the trivial baseline

---

## 5. Execution Strategy & Success Metrics
**Owner:** Technical Marketing PIC

### Agentic Workflow
* **Plan:** [How will you orchestrate your tools?]
    * Checking whether the tools are working properly or not.

### Success Metrics
* **Metric 1 (Improvement in E):** the Etc - Evqe > 0, i.e., VQE initialization is closer to the true ground state.
* **Metric 2 (Lowest Energy):** Running Trotter Circuit and VQE enhanced solution to see which gives correlation values and plotting graph for the same

### Visualization Plan
* **Plot 1:** [e.g., "Time-to-Solution vs. Problem Size (N)" comparing CPU vs. GPU]
* **Plot 2:** [e.g., "Convergence Rate" (Energy vs. Iteration count) for the Quantum Seed vs. Random Seed]

---

## 6. Resource Management Plan
**Owner:** GPU Acceleration PIC 

* **Plan:** [How will you avoid burning all your credits?]
    We will develop entirely on Qbraid (CPU) until the unit tests pass. We will then spin up a cheap L4 instance on Brev for porting. We will only spin up the expensive B300 instance for the final 2 hours of benchmarking.
    The GPU Acceleration PIC is responsible for manually shutting down the Brev instance whenever the team takes a meal break.
