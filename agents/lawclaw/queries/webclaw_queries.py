"""Convert legal commands to WebClaw search queries"""

class WebClawQueryBuilder:
    def build(self, cmd_type: str, args: str) -> str:
        """Build query based on command type"""
        if not args:
            return self._default_query(cmd_type)
        
        handlers = {
            "court": lambda a: f"{a} court jurisdiction address phone hours",
            "federal": lambda a: f"federal court {a} circuit district",
            "state": lambda a: f"{a} state court system supreme appeals",
            "search": lambda a: a,
            "cite": lambda a: f"legal citation {a} case law",
            "statute": lambda a: f"statute {a} text",
            "judge": lambda a: f"judge {a} biography rulings",
            "docket": lambda a: f"court docket {a}",
        }
        
        handler = handlers.get(cmd_type, lambda a: f"{cmd_type} {a}")
        return handler(args)
    
    def _default_query(self, cmd_type: str) -> str:
        defaults = {
            "federal": "federal court system circuit courts",
            "jurisdiction": "court jurisdiction types",
            "pacer": "PACER system access",
        }
        return defaults.get(cmd_type, cmd_type)
