# Dashboard, Unity, and Hyperfy Flow Diagrams

## Unified Platform Flow

```mermaid
flowchart TD
    U[User] --> D[Dashboard<br/>dashboard.metadyn.xyz]
    D --> S[Supabase Auth]
    S --> C[Shared Cookie<br/>metadyn_token<br/>Domain=.metadyn.xyz]

    C --> Y[Unity Space<br/>pavilion.metadyn.xyz]
    C --> H[Hyperfy Space<br/>hyperfy.metadyn.xyz]

    D --> API[Host Deployment API]
    API --> N[Nginx / SSL Proxy]
    API --> T1[Unity Space Template]
    API --> T2[Hyperfy Space Template]

    T1 --> Y
    T2 --> H
    N --> Y
    N --> H
```

## Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant Dashboard as Dashboard
    participant Supabase
    participant Cookie as Browser Cookie
    participant Unity as Unity App
    participant Hyperfy as Hyperfy App

    User->>Dashboard: Open login/signup
    Dashboard->>Supabase: Authenticate user
    Supabase-->>Dashboard: access_token + user session
    Dashboard->>Cookie: Set metadyn_token for .metadyn.xyz

    alt User opens Unity
        User->>Unity: Visit pavilion.metadyn.xyz
        Unity->>Cookie: Read metadyn_token
        alt Token missing
            Unity-->>User: Redirect to dashboard login?redirect=unity_url
        else Token present
            Unity-->>User: Continue into Unity experience
        end
    else User opens Hyperfy
        User->>Hyperfy: Visit hyperfy.metadyn.xyz
        Hyperfy->>Cookie: Read metadyn_token
        alt Token missing
            Hyperfy-->>User: Redirect to dashboard login?redirect=hyperfy_url
        else Token present
            Hyperfy-->>User: Continue into Hyperfy experience
        end
    end
```

## Hyperfy Login and Identity Flow

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant HyperfyClient as Hyperfy Client
    participant HyperfyServer as Hyperfy Server
    participant LocalDB as Hyperfy Users Table

    User->>Browser: Open hyperfy.metadyn.xyz
    Browser->>HyperfyClient: Load app
    HyperfyClient->>Browser: Check metadyn_token cookie

    alt Cookie missing
        HyperfyClient-->>Browser: Redirect to dashboard login with redirect param
    else Cookie present
        HyperfyClient->>HyperfyServer: Open websocket with authToken
        HyperfyServer->>HyperfyServer: Validate trusted external JWT

        alt JWT valid
            HyperfyServer->>LocalDB: Upsert user by trusted identity
            LocalDB-->>HyperfyServer: User record
            HyperfyServer-->>HyperfyClient: Snapshot with authenticated user
            HyperfyClient-->>User: Enter world with synced identity
        else JWT invalid
            HyperfyServer->>HyperfyServer: Try local legacy JWT fallback
            alt Local fallback valid
                HyperfyServer-->>HyperfyClient: Snapshot with legacy local user
            else No valid auth
                HyperfyServer->>LocalDB: Create Anonymous user
                HyperfyServer-->>HyperfyClient: Snapshot with anonymous identity
            end
        end
    end
```

## Unity Login Flow

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant UnityApp as Unity WebGL App
    participant Dashboard
    participant Supabase

    User->>Browser: Open Unity space
    UnityApp->>Browser: Check metadyn_token cookie

    alt Cookie missing
        UnityApp-->>Dashboard: Redirect with ?redirect=current_unity_url
        User->>Dashboard: Login/signup
        Dashboard->>Supabase: Authenticate
        Supabase-->>Dashboard: Session token
        Dashboard->>Browser: Set metadyn_token cookie
        Dashboard-->>UnityApp: Redirect back
        UnityApp->>Browser: Read cookie again
        UnityApp-->>User: Continue into world
    else Cookie present
        UnityApp-->>User: Continue into world immediately
    end
```

## Deployment and Provisioning Flow

```mermaid
flowchart LR
    User[Operator / Creator] --> Dashboard[Dashboard UI]
    Dashboard --> DeployAPI[Host Deployment API]

    DeployAPI --> Choice{Space Type}
    Choice --> Unity[Unity Template]
    Choice --> Hyperfy[Hyperfy Template]

    Unity --> Build[Build / Copy Unity Artifacts]
    Hyperfy --> Instance[Provision Hyperfy Instance]

    Build --> Config[Generate Runtime Config]
    Instance --> Config

    Config --> DNS[Create / Update DNS]
    DNS --> Proxy[Generate Nginx Site Config]
    Proxy --> Validate[nginx -t]
    Validate --> Reload[Reload Nginx]
    Reload --> PublicURL[Return Public URL + Status]
    PublicURL --> Dashboard
```

## Custom Domain Extension Flow

```mermaid
flowchart TD
    Canonical[Canonical Space URL<br/>myspace.metadyn.xyz] --> Optional[Optional Custom Domain]
    Optional --> CName[Customer sets CNAME]
    CName --> Verify[MetaDyn verifies routing]
    Verify --> HostAPI[Host Deployment API updates routing]
    HostAPI --> Nginx[Nginx host config]
    Nginx --> Live[Custom domain live]

    Live --> Auth{Authenticated?}
    Auth -->|No| DashboardLogin[Redirect to dashboard login]
    DashboardLogin --> Return[Return to custom domain]
    Auth -->|Yes| Enter[Enter space]
    Return --> Enter
```

## Notes

- The dashboard is the control plane.
- Unity and Hyperfy are consumer apps under the shared MetaDyn domain model.
- The host deployment API is the execution plane for provisioning and routing.
- Shared-cookie SSO works naturally under `*.metadyn.xyz`.
- Custom domains require a separate auth handoff strategy because they cannot read `.metadyn.xyz` cookies directly.
