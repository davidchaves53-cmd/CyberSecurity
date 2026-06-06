const API = "http://127.0.0.1:8000";

/* ---------- Helpers ---------- */

function socCard(title, content) {
    return `
┌──────────────────────────────────────────┐
│  ${title}
├──────────────────────────────────────────┤
${content}
└──────────────────────────────────────────┘
`;
}

function severityLabel(score) {
    if (score >= 80) return "CRITICAL";
    if (score >= 50) return "HIGH";
    if (score >= 20) return "MEDIUM";
    return "LOW";
}

function severityColor(score) {
    if (score >= 80) return "#ff4d4d";
    if (score >= 50) return "#ff9900";
    if (score >= 20) return "#ffd11a";
    return "#00f0ff";
}

function safeParse(text) {
    try {
        return JSON.parse(text);
    } catch {
        alert("Invalid JSON");
        throw new Error("Invalid JSON");
    }
}

/* ---------- API Calls ---------- */

async function ingestEvent() {
    const body = safeParse(document.getElementById("ingestInput").value);

    const res = await fetch(`${API}/ingest_event`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });

    const data = await res.json();

    const pretty = socCard(
        "EVENT INGESTED",
        `Source: ${body.source}
Event Type: ${body.event_type}

Payload:
${JSON.stringify(body.payload, null, 2)}

Analysis:
${JSON.stringify(data.analysis, null, 2)}`
    );

    document.getElementById("ingestOutput").textContent = pretty;
}

async function analyze() {
    const body = safeParse(document.getElementById("analyzeInput").value);

    const res = await fetch(`${API}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });

    const data = await res.json();
    const score = data.result.risk_score;

    const pretty = socCard(
        "ANALYSIS RESULT",
        `Risk Score: ${score} (${severityLabel(score)})
Summary: ${data.result.analysis}`
    );

    const out = document.getElementById("analyzeOutput");
    out.textContent = pretty;
    out.style.color = severityColor(score);
}

async function takeAction() {
    const body = {
        action: document.getElementById("actionName").value,
        target: document.getElementById("actionTarget").value
    };

    const res = await fetch(`${API}/action`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });

    const data = await res.json();

    const pretty = socCard(
        "ACTION EXECUTED",
        `Action: ${body.action}
Target: ${body.target}

Result:
${JSON.stringify(data.result, null, 2)}`
    );

    document.getElementById("actionOutput").textContent = pretty;
}

async function explainEvent() {
    const body = { event: document.getElementById("explainInput").value };

    const res = await fetch(`${API}/explain`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });

    const data = await res.json();

    const pretty = socCard(
        "EVENT EXPLANATION",
        data.explanation
    );

    document.getElementById("explainOutput").textContent = pretty;
}

async function correlate() {
    const body = {
        events: safeParse(document.getElementById("correlateInput").value)
    };

    const res = await fetch(`${API}/correlate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });

    const data = await res.json();

    const pretty = socCard(
        "CORRELATED INCIDENT",
        JSON.stringify(data.incident, null, 2)
    );

    document.getElementById("correlateOutput").textContent = pretty;
}

/* ---------- Samples ---------- */

function loadSampleEvent() {
    document.getElementById("ingestInput").value = JSON.stringify({
        source: "firewall",
        event_type: "port_scan",
        payload: {
            ip: "192.168.1.50",
            ports: [22, 80, 443],
            count: 15
        }
    }, null, 2);
}

function loadSampleAnalyze() {
    document.getElementById("analyzeInput").value = JSON.stringify({
        ip: "10.0.0.5",
        event: "failed_login",
        count: 12
    }, null, 2);
}

function loadSampleCorrelation() {
    document.getElementById("correlateInput").value = JSON.stringify([
        {
            source: "firewall",
            event_type: "scan",
            payload: { ip: "1.2.3.4" }
        },
        {
            source: "auth",
            event_type: "failed_login",
            payload: { user: "admin" }
        }
    ], null, 2);
}



/* ---------- AI Event Generator ---------- */

function generateEvent() {
    const description = document.getElementById("aiGenInput").value.toLowerCase().trim();
    let generated = {};

    if (!description) {
        document.getElementById("aiGenOutput").textContent =
            "Type something like 'brute force attack on admin from 10.0.0.5'.";
        return;
    }

    if (description.includes("brute") || description.includes("failed login")) {
        generated = {
            ip: "10.0.0.5",
            event: "multiple_failed_logins",
            count: 25,
            user: "admin"
        };
    } else if (description.includes("scan")) {
        generated = {
            source: "firewall",
            event_type: "port_scan",
            payload: {
                ip: "192.168.1.50",
                ports: [22, 80, 443],
                count: 18
            }
        };
    } else if (description.includes("malware") || description.includes("beacon")) {
        generated = {
            ip: "10.0.0.22",
            event: "outbound_connection",
            destination: "185.199.110.153",
            count: 5
        };
    } else {
        generated = {
            note: "No matching pattern. Try: brute force, port scan, malware beacon."
        };
    }

    const pretty = socCard(
        "AI GENERATED EVENT",
        JSON.stringify(generated, null, 2)
    );

    document.getElementById("aiGenOutput").textContent = pretty;
    document.getElementById("analyzeInput").value = JSON.stringify(generated, null, 2);
}

/* ---------- Real-Time Event Stream ---------- */

let streamActive = false;

function startEventStream() {
    if (streamActive) return;
    streamActive = true;

    const box = document.getElementById("eventStreamOutput");

    function pushEvent() {
        if (!streamActive) return;

        const events = [
            "Firewall detected port scan from 192.168.1.77",
            "User admin failed login 5 times",
            "Suspicious outbound connection to 185.199.110.153",
            "Endpoint reported malware signature match",
            "Privilege escalation attempt detected"
        ];

        const event = events[Math.floor(Math.random() * events.length)];
        const ts = new Date().toLocaleTimeString();

        box.textContent += `[${ts}] ${event}\n`;
        box.scrollTop = box.scrollHeight;

        setTimeout(pushEvent, 1000 + Math.random() * 2000);
    }

    pushEvent();
}

function stopEventStream() {
    streamActive = false;
}
