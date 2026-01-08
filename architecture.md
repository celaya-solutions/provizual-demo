# System Architecture Diagrams

## Overall System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        A[Claude Desktop]
        B[Custom Applications]
        C[GUI Interface]
    end
    
    subgraph "MCP Server Layer"
        D[Construction Scraper Server]
        E[Pattern Manager]
        F[Playwright Engine]
        G[AI Extractor]
    end
    
    subgraph "Data Layer"
        H[Pattern Library]
        I[Result Cache]
        J[Screenshot Storage]
    end
    
    subgraph "Target Sources"
        K[Construction Sites]
        L[Government Portals]
        M[Supplier Databases]
    end
    
    A --> D
    B --> D
    C --> D
    
    D --> E
    D --> F
    D --> G
    
    E --> H
    F --> K
    F --> L
    F --> M
    
    D --> I
    D --> J
```

## Data Flow: Pattern-Based Scraping

```mermaid
sequenceDiagram
    participant User
    participant MCP as MCP Server
    participant Pattern as Pattern Library
    participant Browser as Playwright Browser
    participant Target as Target Website
    participant LLM as AI Extractor
    
    User->>MCP: Request data extraction
    MCP->>Pattern: Load scraping pattern
    Pattern-->>MCP: Return selectors
    
    MCP->>Browser: Initialize
    Browser->>Target: Navigate to URL
    Target-->>Browser: Return HTML
    
    Browser->>Target: Apply selectors
    Target-->>Browser: Extract elements
    
    alt Extraction Successful
        Browser-->>MCP: Return structured data
        MCP-->>User: Success + Data
    else Selectors Failed
        Browser-->>MCP: Extraction errors
        MCP->>LLM: Fallback AI extraction
        LLM-->>MCP: Semantic extraction
        MCP-->>User: Success + Data (AI mode)
    end
    
    Browser->>Browser: Capture screenshot
    Browser-->>MCP: Screenshot saved
    MCP-->>User: Validation artifacts
```

## Error Handling Flow

```mermaid
flowchart TD
    A[Start Scraping] --> B{URL Valid?}
    B -->|No| C[Return URL Error]
    B -->|Yes| D[Navigate to Page]
    
    D --> E{Page Loaded?}
    E -->|No| F[Retry with Timeout]
    E -->|Yes| G[Apply Selectors]
    
    F --> H{Retry Successful?}
    H -->|No| I[Return Timeout Error]
    H -->|Yes| G
    
    G --> J{Elements Found?}
    J -->|All Found| K[Extract Data]
    J -->|Some Missing| L[Log Warnings]
    J -->|None Found| M[Trigger AI Fallback]
    
    K --> N[Validate Data]
    L --> N
    M --> O[AI Extraction]
    
    O --> P{AI Success?}
    P -->|Yes| N
    P -->|No| Q[Return Extraction Error]
    
    N --> R[Capture Screenshot]
    R --> S[Return Results]
```

## Pattern Adaptation Workflow

```mermaid
graph LR
    A[Original Pattern] -->|Site Changes| B[Selector Fails]
    B --> C{Diagnose Issue}
    
    C -->|Class Changed| D[Update Selector]
    C -->|Structure Changed| E[Add Fallback Selectors]
    C -->|Dynamic Content| F[Add Wait Logic]
    
    D --> G[Test Pattern]
    E --> G
    F --> G
    
    G --> H{Validation Pass?}
    H -->|Yes| I[Deploy Updated Pattern]
    H -->|No| C
    
    I --> J[Monitor in Production]
    J --> K{Issues Found?}
    K -->|Yes| C
    K -->|No| L[Pattern Stable]
```

## Integration Options

```mermaid
graph TB
    subgraph "Deployment Options"
        A[MCP Server]
    end
    
    A --> B[Claude Desktop Integration]
    A --> C[Standalone Server]
    A --> D[Docker Container]
    A --> E[AWS Lambda]
    
    B --> F[AI-Assisted Development]
    C --> G[REST API Service]
    D --> H[Kubernetes Deployment]
    E --> I[Serverless Cron Jobs]
    
    F --> J[Development Workflow]
    G --> J
    H --> K[Production Scale]
    I --> L[Scheduled Tasks]
```

## Data Pipeline

```mermaid
flowchart LR
    A[Web Sources] --> B[Scraper]
    B --> C{Validation}
    
    C -->|Valid| D[Transform Data]
    C -->|Invalid| E[Error Queue]
    
    D --> F[Data Lake]
    F --> G[ETL Process]
    
    G --> H[(Database)]
    G --> I[API]
    G --> J[Analytics]
    
    E --> K[Alert System]
    K --> L[Manual Review]
```

## Provizual Integration

```mermaid
graph TB
    subgraph "Provizual Existing"
        A[NestJS Backend]
        B[TypeORM]
        C[Playwright Scrapers]
    end
    
    subgraph "New MCP Server"
        D[Python Scraper]
        E[Pattern Library]
        F[AI Fallback]
    end
    
    subgraph "Shared Services"
        G[Database]
        H[Message Queue]
        I[Monitoring]
    end
    
    C -.->|Gradual Migration| D
    D --> E
    D --> F
    
    A --> G
    D --> G
    
    A --> H
    D --> H
    
    C --> I
    D --> I
```
