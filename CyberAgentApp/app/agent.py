class CyberAgent:
    def __init__(self):
        pass

    # ---------------------------------------------------------
    # PROCESS SINGLE EVENT
    # ---------------------------------------------------------
    def process_event(self, event: dict):
        event_type = event.get("event_type", "unknown")
        payload = event.get("payload", {})

        risk = self._calculate_risk(payload)
        mitre = self._map_to_mitre(event_type, payload)

        return {
            "event_type": event_type,
            "risk_score": risk,
            "mitre_techniques": mitre,
            "details": "Event processed successfully"
        }

    # ---------------------------------------------------------
    # MANUAL ANALYSIS
    # ---------------------------------------------------------
    def analyze(self, payload: dict):
        return {
            "risk_score": self._calculate_risk(payload),
            "analysis": "Manual analysis completed"
        }

    # ---------------------------------------------------------
    # RISK ENGINE
    # ---------------------------------------------------------
    def _calculate_risk(self, payload: dict):
        score = 0

        if payload.get("failed_logins", 0) > 5:
            score += 40

        if payload.get("suspicious", False):
            score += 25

        if payload.get("privilege_escalation", False):
            score += 50

        if payload.get("malware_detected", False):
            score += 60

        return min(score, 100)

    # ---------------------------------------------------------
    # MITRE MAPPING
    # ---------------------------------------------------------
    def _map_to_mitre(self, event_type, payload):
        mapping = []

        if event_type == "failed_login":
            mapping.append("T1110 – Brute Force")

        if payload.get("privilege_escalation"):
            mapping.append("T1068 – Exploitation for Privilege Escalation")

        if payload.get("malware_detected"):
            mapping.append("T1059 – Command and Scripting Interpreter")

        return mapping

    # ---------------------------------------------------------
    # 🔥 CORRELATION ENGINE (NEW)
    # ---------------------------------------------------------
    def correlate(self, events):
        """
        Correlate multiple security events into a single incident.
        Always returns a structured incident dictionary.
        """

        if not events or not isinstance(events, list):
            return {"message": "No events provided"}

        incident = {
            "summary": "Correlated security incident",
            "event_count": len(events),
            "events": events,
            "rules_triggered": [],
            "mitre_techniques": [],
            "risk_score": 0
        }

        # Extract event types and payloads
        types = [e.get("event_type") for e in events]
        payloads = [e.get("payload", {}) for e in events]

        # ---------------------------------------------------------
        # RULE 1: Scan → Failed Login (Recon → Credential Attack)
        # ---------------------------------------------------------
        if "scan" in types and "failed_login" in types:
            incident["rules_triggered"].append("scan_to_failed_login")
            incident["summary"] = "Reconnaissance followed by credential attack"
            incident["mitre_techniques"].append("T1595 – Active Scanning")
            incident["mitre_techniques"].append("T1110 – Brute Force")

        # ---------------------------------------------------------
        # RULE 2: Multiple failed logins → Brute Force
        # ---------------------------------------------------------
        if types.count("failed_login") >= 3:
            incident["rules_triggered"].append("brute_force_attempt")
            incident["summary"] = "Multiple failed logins detected"
            incident["mitre_techniques"].append("T1110 – Brute Force")

        # ---------------------------------------------------------
        # RULE 3: Privilege escalation event
        # ---------------------------------------------------------
        if any(p.get("privilege_escalation") for p in payloads):
            incident["rules_triggered"].append("privilege_escalation")
            incident["summary"] = "Privilege escalation detected"
            incident["mitre_techniques"].append("T1068 – Exploitation for Privilege Escalation")

        # ---------------------------------------------------------
        # RULE 4: Malware detection
        # ---------------------------------------------------------
        if any(p.get("malware_detected") for p in payloads):
            incident["rules_triggered"].append("malware_detected")
            incident["summary"] = "Malware activity detected"
            incident["mitre_techniques"].append("T1059 – Command and Scripting Interpreter")

        # ---------------------------------------------------------
        # RISK SCORE (aggregate)
        # ---------------------------------------------------------
        total_risk = 0
        for p in payloads:
            total_risk += self._calculate_risk(p)

        incident["risk_score"] = min(total_risk, 100)

        # ---------------------------------------------------------
        # If no rules matched
        # ---------------------------------------------------------
        if not incident["rules_triggered"]:
            incident["rules_triggered"].append("no_correlation")
            incident["summary"] = "No correlation rules matched"

        return incident
