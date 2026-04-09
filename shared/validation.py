"""Schema-based Input Validation"""

from typing import Any, Dict, List, Optional, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import re

class ValidationError(Exception):
    """Validation error with field details"""
    def __init__(self, message: str, field: str = None, value: Any = None):
        self.message = message
        self.field = field
        self.value = value
        super().__init__(message)

@dataclass
class Field:
    """Schema field definition"""
    name: str
    type: type
    required: bool = True
    default: Any = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    pattern: Optional[str] = None
    choices: Optional[List[Any]] = None
    custom_validator: Optional[Callable] = None
    description: str = ""
    
    def validate(self, value: Any, field_name: str) -> List[str]:
        """Validate a value against this field"""
        errors = []
        
        # Required check
        if value is None:
            if self.required:
                errors.append(f"{field_name} is required")
            return errors
        
        # Type check
        if not isinstance(value, self.type):
            errors.append(f"{field_name} must be {self.type.__name__}, got {type(value).__name__}")
            return errors
        
        # String validations
        if isinstance(value, str):
            if self.min_length and len(value) < self.min_length:
                errors.append(f"{field_name} must be at least {self.min_length} characters")
            if self.max_length and len(value) > self.max_length:
                errors.append(f"{field_name} must be at most {self.max_length} characters")
            if self.pattern and not re.match(self.pattern, value):
                errors.append(f"{field_name} must match pattern {self.pattern}")
        
        # Numeric validations
        if isinstance(value, (int, float)):
            if self.min_value is not None and value < self.min_value:
                errors.append(f"{field_name} must be >= {self.min_value}")
            if self.max_value is not None and value > self.max_value:
                errors.append(f"{field_name} must be <= {self.max_value}")
        
        # Choices
        if self.choices and value not in self.choices:
            errors.append(f"{field_name} must be one of {self.choices}")
        
        # Custom validator
        if self.custom_validator:
            try:
                self.custom_validator(value)
            except Exception as e:
                errors.append(f"{field_name}: {str(e)}")
        
        return errors

class Schema:
    """Validation schema"""
    
    def __init__(self, name: str):
        self.name = name
        self._fields: Dict[str, Field] = {}
    
    def add_field(self, field: Field) -> 'Schema':
        self._fields[field.name] = field
        return self
    
    def string(self, name: str, required: bool = True, **kwargs) -> 'Schema':
        return self.add_field(Field(name=name, type=str, required=required, **kwargs))
    
    def integer(self, name: str, required: bool = True, **kwargs) -> 'Schema':
        return self.add_field(Field(name=name, type=int, required=required, **kwargs))
    
    def float(self, name: str, required: bool = True, **kwargs) -> 'Schema':
        return self.add_field(Field(name=name, type=float, required=required, **kwargs))
    
    def boolean(self, name: str, required: bool = True, **kwargs) -> 'Schema':
        return self.add_field(Field(name=name, type=bool, required=required, **kwargs))
    
    def list(self, name: str, required: bool = True, **kwargs) -> 'Schema':
        return self.add_field(Field(name=name, type=list, required=required, **kwargs))
    
    def dict(self, name: str, required: bool = True, **kwargs) -> 'Schema':
        return self.add_field(Field(name=name, type=dict, required=required, **kwargs))
    
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data against schema, return validated data with defaults"""
        errors = []
        validated = {}
        
        for name, field in self._fields.items():
            value = data.get(name)
            
            field_errors = field.validate(value, name)
            if field_errors:
                errors.extend(field_errors)
            else:
                if value is None and field.default is not None:
                    validated[name] = field.default
                elif value is not None:
                    validated[name] = value
        
        if errors:
            raise ValidationError(f"Validation failed for {self.name}: " + "; ".join(errors))
        
        return validated

# Pre-defined schemas for common operations
TranslateSchema = (Schema("translate")
    .string("text", min_length=1, max_length=5000)
    .string("target_lang", min_length=2, max_length=5, pattern=r"^[a-z]{2,5}$")
    .string("source_lang", required=False, min_length=2, max_length=5)
)

CropImageSchema = (Schema("crop_image")
    .string("file_path", min_length=1)
    .integer("width", min_value=1, max_value=4096)
    .integer("height", min_value=1, max_value=4096)
)

LLMRequestSchema = (Schema("llm_request")
    .string("prompt", min_length=1, max_length=100000)
    .integer("max_tokens", required=False, min_value=100, max_value=200000, default=8000)
    .float("temperature", required=False, min_value=0, max_value=2, default=0.7)
)

def validate_schema(schema: Schema, data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate data against a schema"""
    return schema.validate(data)

def validate_translate(text: str, target_lang: str, source_lang: str = None) -> Dict:
    return validate_schema(TranslateSchema, {
        "text": text,
        "target_lang": target_lang,
        "source_lang": source_lang
    })

def validate_crop(file_path: str, width: int, height: int) -> Dict:
    return validate_schema(CropImageSchema, {
        "file_path": file_path,
        "width": width,
        "height": height
    })
