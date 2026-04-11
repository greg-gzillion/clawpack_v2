"""Test Generation Module"""

from pathlib import Path

class TestGenerator:
    def __init__(self, ai_assistant, project_path):
        self.ai = ai_assistant
        self.project_path = Path(project_path)
    
    def generate_tests(self, contract_name):
        """Generate test suite for a contract"""
        contract_path = self.project_path / "contracts" / contract_name
        
        if not contract_path.exists():
            return {'error': f'Contract {contract_name} not found'}
        
        prompt = f"""Generate comprehensive integration tests for CosmWasm contract: {contract_name}

Include:
- Instantiate test
- Execute message tests
- Query tests
- Error case tests
- Multi-test scenarios

Use cosmwasm-std testing framework.
Return ONLY the Rust test code."""
        
        code = self.ai.generate_code(prompt)
        
        if code:
            tests_dir = contract_path / "src"
            test_file = tests_dir / "tests.rs"
            test_file.write_text(code)
            return {'success': True, 'path': str(test_file)}
        
        return self._template_tests(contract_name)
    
    def _template_tests(self, contract_name):
        tests_dir = self.project_path / "contracts" / contract_name / "src"
        tests_dir.mkdir(exist_ok=True)
        test_file = tests_dir / "tests.rs"
        test_file.write_text(f'''#[cfg(test)]
mod tests {{
    use super::*;
    use cosmwasm_std::testing::{{mock_dependencies, mock_env, mock_info}};
    
    #[test]
    fn test_instantiate() {{
        // Add instantiation test for {contract_name}
        assert!(true);
    }}
    
    #[test]
    fn test_execute() {{
        // Add execute test for {contract_name}
        assert!(true);
    }}
    
    #[test]
    fn test_query() {{
        // Add query test for {contract_name}
        assert!(true);
    }}
}}''')
        return {'success': True, 'path': str(test_file), 'template': True}
    
    def run_tests(self, contract_name):
        """Run tests for a contract"""
        import subprocess
        contract_path = self.project_path / "contracts" / contract_name
        
        if not contract_path.exists():
            return {'error': f'Contract {contract_name} not found'}
        
        try:
            result = subprocess.run(
                ['cargo', 'test', '--lib'],
                cwd=contract_path,
                capture_output=True,
                text=True
            )
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'errors': result.stderr
            }
        except Exception as e:
            return {'error': str(e)}
