# Quantum Aviation Optimizer

## Subtitle: How I Solved Complex Flight Routing Using QAOA and Quantum Computing

![Title Animation](https://raw.githubusercontent.com/aniket-work/QuantumAviation-Optimizer/main/images/title-animation.gif)

## Overview

The **Quantum Aviation Optimizer** is an experimental Proof-of-Concept (PoC) demonstrating how classical aviation scheduling and routing problems can be redefined as computational graph problems and effectively solved utilizing Quantum Computing principles. 

By translating flight conflicts into a **MaxCut** problem and solving it via the **Quantum Approximate Optimization Algorithm (QAOA)**, this tool splits a network of conflicting schedules into mathematically proven, non-overlapping fleets.

> **Disclaimer**: The views and opinions expressed here are solely my own and do not represent the views, positions, or opinions of my employer or any organization I am affiliated with. The content is based on my personal experience and experimentation and may be incomplete or incorrect. Any errors or misinterpretations are unintentional, and I apologize in advance if any statements are misunderstood or misrepresented.

## Architecture

![Architecture](https://raw.githubusercontent.com/aniket-work/QuantumAviation-Optimizer/main/images/architecture_diagram.png)

## Core Technologies
- **Python 3.12+**
- **Qrisp / Qiskit Compatibility**: Capable of abstracting away the complex gate-level calculus underlying quantum approximate algorithms.
- **NetworkX**: Conflict matrix modelling.

## Running the PoC

1. Clone the repository:
   ```bash
   git clone https://github.com/aniket-work/QuantumAviation-Optimizer.git
   cd QuantumAviation-Optimizer
   ```

2. Setup virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Execute the optimizer:
   ```bash
   python flight_optimizer_qaoa.py
   ```

## Development and Structure

![Flow Diagram](https://raw.githubusercontent.com/aniket-work/QuantumAviation-Optimizer/main/images/flow_diagram.png)

*This project was developed strictly as a personal experiment.*
