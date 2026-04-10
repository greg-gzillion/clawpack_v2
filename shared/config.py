"""Unified Configuration System with Validation"""

import os
import json
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime

class ConfigSource(str, Enum):
    """Priority: ENV > USER > PROJECT > DEFAULT"""
    DEFAULT = "default"
    PROJECT = "project"
    USER = "user"
    ENV = "env"

@dataclass
class LLMConfig:
    provider: str = "openrouter"
    model: str = "z-ai/glm-5.1"
    max_tokens: int = 8000
    temperature: float = 0.7
    timeout_seconds: int = 30
    retry_attempts: int = 3

@dataclass
class MemoryConfig:
    enabled: bool = True
    max_files: int = 100
    staleness_warning_days: int = 7
    auto_record_feedback: bool = True

@dataclass
class RateLimitConfig:
    requests_per_minute: int = 60
    requests_per_day: int = 10000
    tokens_per_minute: int = 100000
    burst_size: int = 10

@dataclass
class LoggingConfig:
    level: str = "INFO"
    format: str = "json"
    output: str = "stderr"
    include_traceback: bool = True

@dataclass
class AgentConfig:
    name: str
    enabled: bool = True
    max_turns: int = 50
    tools: List[str] = field(default_factory=list)

@dataclass
class ClawpackConfig:
    """Master configuration"""
    version: str = "2.0.0"
    
    # Sub-configs
    llm: LLMConfig = field(default_factory=LLMConfig)
    memory: MemoryConfig = field(default_factory=MemoryConfig)
    rate_limit: RateLimitConfig = field(default_factory=RateLimitConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    
    # Agent configs
    agents: Dict[str, AgentConfig] = field(default_factory=dict)
    
    # Runtime
    debug: bool = False
    workspace: Optional[Path] = None
    
    def __post_init__(self):
        if self.workspace is None:
            self.workspace = Path.cwd()

class ConfigValidator:
    """Validate configuration values"""
    
    @staticmethod
    def validate_llm(config: LLMConfig) -> List[str]:
        errors = []
        if config.max_tokens < 100 or config.max_tokens > 200000:
            errors.append(f"max_tokens must be between 100 and 200000, got {config.max_tokens}")
        if config.temperature < 0 or config.temperature > 2:
            errors.append(f"temperature must be between 0 and 2, got {config.temperature}")
        if config.timeout_seconds < 1 or config.timeout_seconds > 300:
            errors.append(f"timeout_seconds must be between 1 and 300, got {config.timeout_seconds}")
        return errors
    
    @staticmethod
    def validate(config: ClawpackConfig) -> List[str]:
        errors = []
        errors.extend(ConfigValidator.validate_llm(config.llm))
        
        if config.rate_limit.requests_per_minute < 1:
            errors.append("requests_per_minute must be >= 1")
        
        if config.logging.level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            errors.append(f"Invalid log level: {config.logging.level}")
        
        return errors

class ConfigManager:
    """Unified configuration manager"""
    
    def __init__(self, workspace: Path = None):
        self.workspace = workspace or Path.cwd()
        self.config = ClawpackConfig(workspace=self.workspace)
        self.sources: Dict[str, ConfigSource] = {}
        self._load_all()
    
    def _load_all(self):
        """Load config from all sources with priority"""
        # 1. Defaults (already set)
        
        # 2. Project config (.clawpack/config.yml)
        project_config = self.workspace / ".clawpack" / "config.yml"
        if project_config.exists():
            self._merge_from_file(project_config, ConfigSource.PROJECT)
        
        # 3. User config (~/.clawpack/config.yml)
        user_config = Path.home() / ".clawpack" / "config.yml"
        if user_config.exists():
            self._merge_from_file(user_config, ConfigSource.USER)
        
        # 4. Environment variables (highest priority)
        self._merge_from_env()
        
        # Validate
        errors = ConfigValidator.validate(self.config)
        if errors:
            print(f"⚠️ Config validation warnings:")
            for e in errors:
                print(f"   - {e}")
    
    def _merge_from_file(self, path: Path, source: ConfigSource):
        """Merge YAML/JSON config file"""
        try:
            if path.suffix == '.yml' or path.suffix == '.yaml':
                data = yaml.safe_load(path.read_text())
            else:
                data = json.loads(path.read_text())
            
            self._update_config(data, source)
        except Exception as e:
            print(f"⚠️ Error loading config {path}: {e}")
    
    def _merge_from_env(self):
        """Merge from environment variables"""
        env_mappings = {
            "CLAWPACK_LLM_PROVIDER": ("llm", "provider"),
            "CLAWPACK_LLM_MODEL": ("llm", "model"),
            "CLAWPACK_MAX_TOKENS": ("llm", "max_tokens", int),
            "CLAWPACK_DEBUG": ("debug", None, lambda x: x.lower() == "true"),
            "CLAWPACK_LOG_LEVEL": ("logging", "level"),
        }
        
        for env_var, target in env_mappings.items():
            value = os.environ.get(env_var)
            if value:
                self._set_nested(target, value, ConfigSource.ENV)
    
    def _set_nested(self, target: tuple, value: Any, source: ConfigSource):
        """Set nested config value"""
        if len(target) == 2:
            section, key = target
            if hasattr(self.config, section):
                setattr(getattr(self.config, section), key, value)
        elif len(target) == 3:
            section, key, converter = target
            if hasattr(self.config, section):
                setattr(getattr(self.config, section), key, converter(value))
    
    def _update_config(self, data: Dict, source: ConfigSource):
        """Update config from dict"""
        for key, value in data.items():
            if hasattr(self.config, key):
                if isinstance(value, dict) and hasattr(getattr(self.config, key), '__dataclass_fields__'):
                    # Nested config
                    sub_config = getattr(self.config, key)
                    for sub_key, sub_value in value.items():
                        if hasattr(sub_config, sub_key):
                            setattr(sub_config, sub_key, sub_value)
                            self.sources[f"{key}.{sub_key}"] = source
                else:
                    setattr(self.config, key, value)
                    self.sources[key] = source
    
    def get(self) -> ClawpackConfig:
        return self.config
    
    def save(self, path: Path = None, format: str = "yaml"):
        """Save current config to file"""
        path = path or self.workspace / ".clawpack" / "config.yml"
        path.parent.mkdir(parents=True, exist_ok=True)
        
        config_dict = asdict(self.config)
        # Convert Path to string
        config_dict['workspace'] = str(config_dict['workspace'])
        
        if format == "yaml":
            path.write_text(yaml.dump(config_dict, default_flow_style=False))
        else:
            path.write_text(json.dumps(config_dict, indent=2))
    
    def generate_example(self) -> str:
        """Generate example config file"""
        return """# Clawpack V2 Configuration

llm:
  provider: openrouter  # anthropic, openai, openrouter, groq, ollama
  model: z-ai/glm-5.1
  max_tokens: 8000
  temperature: 0.7
  timeout_seconds: 30
  retry_attempts: 3

memory:
  enabled: true
  max_files: 100
  staleness_warning_days: 7
  auto_record_feedback: true

rate_limit:
  requests_per_minute: 60
  requests_per_day: 10000
  tokens_per_minute: 100000
  burst_size: 10

logging:
  level: INFO
  format: json
  output: stderr
  include_traceback: true

debug: false
"""

# Global instance
_config_manager = None

def get_config(workspace: Path = None) -> ConfigManager:
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager(workspace)
    return _config_manager
# Add to existing config.py
class SharedMemory:
    """Memory management integrated with config"""
    pass
