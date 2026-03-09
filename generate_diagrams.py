import base64
import requests
import os

diagrams = {
    "title": """graph LR
    A[Aviation Business Problem] --> B(Quantum Fleet Optimizer)
    B --> C{QAOA Execution}
    C -->|MaxCut| D[Optimized Flight Routes]
    style A fill:#0D1117,stroke:#58A6FF,stroke-width:2px,color:#C9D1D9
    style B fill:#0D1117,stroke:#A371F7,stroke-width:2px,color:#C9D1D9
    style C fill:#0D1117,stroke:#3FB950,stroke-width:2px,color:#C9D1D9
    style D fill:#0D1117,stroke:#A371F7,stroke-width:2px,color:#C9D1D9
    """,
    
    "architecture": """graph TD
    subgraph "Data Layer"
        F[Flight Schedules]
        S[Station Distances]
    end
    
    subgraph "Optimizer Engine"
        GE[Graph Extractor]
        CM[Conflict Matrix Builder]
    end
    
    subgraph "Quantum Processor"
        CO[Cost Operator]
        RO[RX Mixer]
        QAOA[QAOA Instance]
    end
    
    F --> GE
    S --> GE
    GE --> CM
    CM --> CO
    CM --> RO
    CO --> QAOA
    RO --> QAOA
    QAOA --> R[Optimal Routes]
    
    style F fill:#0D1117,stroke:#1F6FEB,stroke-width:2px,color:#FFF
    style S fill:#0D1117,stroke:#1F6FEB,stroke-width:2px,color:#FFF
    style GE fill:#0D1117,stroke:#238636,stroke-width:2px,color:#FFF
    style CM fill:#0D1117,stroke:#238636,stroke-width:2px,color:#FFF
    style CO fill:#0D1117,stroke:#8957E5,stroke-width:2px,color:#FFF
    style RO fill:#0D1117,stroke:#8957E5,stroke-width:2px,color:#FFF
    style QAOA fill:#0D1117,stroke:#8957E5,stroke-width:2px,color:#FFF
    style R fill:#0D1117,stroke:#238636,stroke-width:2px,color:#FFF
    """,
    
    "sequence": """sequenceDiagram
    participant User
    participant Optimizer
    participant Qrisp
    
    User->>Optimizer: Provide Flight Schedules
    Optimizer->>Optimizer: Build Conflict Graph
    Optimizer->>Qrisp: Initialize QAOA Problem
    Qrisp->>Qrisp: Create MaxCut Cost Operator
    Qrisp->>Qrisp: Create X-Mixer Operator
    loop Optimization
        Qrisp->>Qrisp: Run VQE cycle
    end
    Qrisp-->>Optimizer: Top Probability States
    Optimizer->>User: Return Distinct Partitions
    """,
    
    "flow": """graph TD
    Start[Initialize Data] --> ReadG[Build Conflict Graph]
    ReadG --> Weights[Assign Edge Priorities]
    Weights --> Q[Setup QAOA MaxCut]
    Q --> Depth[Define Circuit Depth p]
    Depth --> Run[Execute QAOA Result]
    Run --> Check{High Probability?}
    Check -->|Yes| Decode[Decode Bitstring]
    Check -->|No| Iterate[Increase p / Re-run]
    Iterate --> Depth
    Decode --> Output[Final Route Assigments]
    """
}

def generate_diagrams():
    os.makedirs("images", exist_ok=True)
    for name, code in diagrams.items():
        print(f"Generating {name} diagram...")
        try:
            # Strip extra whitespace matching
            cleaned_code = "\\n".join(line.strip() for line in code.strip().split("\\n"))
            encoded = base64.b64encode(cleaned_code.encode('utf-8')).decode('utf-8')
            url = f"https://mermaid.ink/img/{encoded}?bgColor=0D1117"
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            with open(f"images/{name}_diagram.png", 'wb') as f:
                f.write(response.content)
            print(f"Successfully generated images/{name}_diagram.png")
        except Exception as e:
            print(f"Failed to generate {name} diagram: {e}")
            raise

if __name__ == "__main__":
    generate_diagrams()
    # Verify we got all exactly
    expected = ["title_diagram.png", "architecture_diagram.png", "sequence_diagram.png", "flow_diagram.png"]
    missing = [e for e in expected if not os.path.exists(os.path.join("images", e))]
    if missing:
        raise Exception(f"Missing diagram files: {missing}")
    print("All diagrams verified successfully.")
