import tempfile
import os
import sys
import pytest
import io
from contextlib import redirect_stdout, redirect_stderr
from typing import Dict, List
import re


class TestRunner:
    def __init__(self):
        self.temp_dir = None

    def setup_test_files(self, source_code, test_code):
        """Create temporary files for the source code and tests"""
        self.temp_dir = tempfile.mkdtemp()

        # Save source code with UTF-8 encoding
        source_path = os.path.join(self.temp_dir, "source.py")
        with open(source_path, "w", encoding='utf-8') as f:
            f.write(source_code)

        # Save test code with UTF-8 encoding
        test_path = os.path.join(self.temp_dir, "test_source.py")
        with open(test_path, "w", encoding='utf-8') as f:
            complete_test_code = f"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from source import *

{test_code}
"""
            f.write(complete_test_code)

        return source_path, test_path

    def _parse_test_results(self, output: str) -> Dict:
        """Parse pytest output into a structured format"""
        # Extract test results
        test_results = []
        for line in output.split('\n'):
            if 'PASSED' in line or 'FAILED' in line:
                # Extract test name and result using regex
                match = re.search(r'::(.+?)\s+(PASSED|FAILED)', line)
                if match:
                    test_name = match.group(1)
                    result = match.group(2)
                    # Clean up test name
                    test_name = test_name.replace('_', ' ').title()
                    test_results.append({
                        'name': test_name,
                        'result': result,
                        'passed': result == 'PASSED'
                    })

        # Extract summary
        summary_match = re.search(
            r'([\d]+) passed(?:, ([\d]+) failed)?(?:, ([\d]+) warning)?', output)
        if summary_match:
            passed = int(summary_match.group(1) or 0)
            failed = int(summary_match.group(2) or 0)
            warnings = int(summary_match.group(3) or 0)
        else:
            passed = failed = warnings = 0

        return {
            'tests': test_results,
            'summary': {
                'total': passed + failed,
                'passed': passed,
                'failed': failed,
                'warnings': warnings
            }
        }

    def _format_results(self, parsed_results: Dict) -> str:
        """Format the parsed results into a readable output"""
        output = []

        output.append("🧪 Test Results Summary")
        output.append("=" * 50)

        output.append("\n📝 Test Details:")
        for test in parsed_results['tests']:
            icon = "✅" if test['passed'] else "❌"
            output.append(f"{icon} {test['name']}")

        summary = parsed_results['summary']
        output.append("\n📊 Overall Summary")
        output.append("-" * 20)
        output.append(f"Total Tests: {summary['total']}")
        output.append(f"Passed: ✅ {summary['passed']}")
        if summary['failed'] > 0:
            output.append(f"Failed: ❌ {summary['failed']}")
        if summary['warnings'] > 0:
            output.append(f"Warnings: ⚠️ {summary['warnings']}")

        if summary['total'] > 0:
            pass_rate = (summary['passed'] / summary['total']) * 100
            output.append(f"\nPass Rate: {pass_rate:.1f}%")

        return "\n".join(output)

    def run_tests(self, source_code, test_code):
        """Run the generated tests and return results"""
        try:
            source_path, test_path = self.setup_test_files(
                source_code, test_code)

            stdout = io.StringIO()
            stderr = io.StringIO()

            with redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = pytest.main(["-v", test_path])

            stdout_content = stdout.getvalue()
            stderr_content = stderr.getvalue()

            # Parse and format the results
            parsed_results = self._parse_test_results(stdout_content)
            formatted_output = self._format_results(parsed_results)

            return {
                "success": exit_code == 0,
                "output": formatted_output,
                "detailed_output": formatted_output
            }

        except Exception as e:
            return {
                "success": False,
                "output": f"Error running tests: {str(e)}",
                "detailed_output": f"Error details:\n{str(e)}"
            }

        finally:
            if self.temp_dir and os.path.exists(self.temp_dir):
                import shutil
                shutil.rmtree(self.temp_dir)
