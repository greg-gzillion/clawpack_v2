//! Trauma Guard - Safety blocking for dangerous operations

use regex::Regex;

pub struct TraumaGuard {
    patterns: Vec<(Regex, String, String)>,
    enabled: bool,
}

impl TraumaGuard {
    pub fn new() -> Self {
        let patterns = vec![
            (Regex::new(r"rm\s+-rf\s+/?").unwrap(), "FATAL".to_string(), "Recursive delete of root directory".to_string()),
            (Regex::new(r"rm\s+-rf\s+~").unwrap(), "HIGH".to_string(), "Recursive delete of home directory".to_string()),
            (Regex::new(r"drop\s+database").unwrap(), "FATAL".to_string(), "Database deletion".to_string()),
            (Regex::new(r"truncate\s+table\s+\w+\s*;?").unwrap(), "HIGH".to_string(), "Table truncation without WHERE".to_string()),
            (Regex::new(r"git\s+push\s+--force").unwrap(), "HIGH".to_string(), "Force push to remote".to_string()),
            (Regex::new(r"chmod\s+777").unwrap(), "MEDIUM".to_string(), "Overly permissive permissions".to_string()),
        ];
        
        Self {
            patterns,
            enabled: false,
        }
    }

    pub fn enable(&mut self) {
        self.enabled = true;
    }

    pub fn disable(&mut self) {
        self.enabled = false;
    }

    pub fn check(&self, command: &str) -> CheckResult {
        if !self.enabled {
            return CheckResult { blocked: false, severity: None, reason: None };
        }

        for (regex, severity, reason) in &self.patterns {
            if regex.is_match(command) {
                return CheckResult {
                    blocked: true,
                    severity: Some(severity.clone()),
                    reason: Some(reason.clone()),
                };
            }
        }

        CheckResult { blocked: false, severity: None, reason: None }
    }
}

pub struct CheckResult {
    pub blocked: bool,
    pub severity: Option<String>,
    pub reason: Option<String>,
}
