import time
import random
import ctypes
from ctypes import wintypes
from typing import Callable, Any, List

class BehavioralRandomizer:
    def __init__(self, aggression_level: str = "moderate"):
        self.aggression = aggression_level.lower()
        self.kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

    def human_delay(self, base_seconds: float = 2.0, variance: float = 1.5) -> None:
        delay = random.lognormvariate(mu=base_seconds, sigma=variance / 3.0)
        delay = max(0.5, min(delay, base_seconds + variance * 2))
        if self.aggression == "aggressive":
            delay *= 2.0
        elif self.aggression == "subtle":
            delay *= 0.5
        time.sleep(delay)

    def execute_with_noise(self, operation: Callable, *args, **kwargs) -> Any:
        if random.random() < 0.3:
            self.mouse_movement_noise()
        self.human_delay()
        if random.random() < 0.4 and self.aggression != "subtle":
            for op in self.generate_benign_operations(1):
                try: op()
                except: pass
        result = operation(*args, **kwargs)
        self.human_delay(base_seconds=1.0, variance=0.8)
        if random.random() < 0.2:
            self.keyboard_simulation(key_count=3)
        return result
    
    def mouse_movement_noise(self) -> None:
        """
        Simulate mouse movement to create UI interaction noise
        Many behavioral systems track interactive vs automated behavior
        """
        
        # Get current cursor position
        class POINT(ctypes.Structure):
            _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
        
        point = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
        
        # Make small random movement
        new_x = point.x + random.randint(-50, 50)
        new_y = point.y + random.randint(-50, 50)
        
        ctypes.windll.user32.SetCursorPos(new_x, new_y)
        
        # Micro delay
        time.sleep(random.uniform(0.01, 0.05))

    def keyboard_simulation(self, 
                          key_count: int = 5,
                          include_mistakes: bool = True) -> None:
        """
        Simulate keyboard activity patterns
        Creates process-level events that look interactive
        """
        
        for _ in range(key_count):
            # Simulate key press with human timing variance
            time.sleep(random.uniform(0.05, 0.3))
            
            if include_mistakes and random.random() < 0.1:
                # Occasional "typo" - press backspace
                time.sleep(random.uniform(0.1, 0.2))

    def generate_benign_operations(self, count: int = 3) -> List[Callable]:
        """
        Generate benign operations that create behavioral noise
        
        Returns:
            List of callable functions that perform benign actions
        """
        
        operations = []
        
        # Query system information
        def query_system_info():
            kernel32 = ctypes.WinDLL('kernel32')
            kernel32.GetComputerNameW(None, None)
            kernel32.GetSystemTime(None)
        
        # Enumerate environment variables
        def enum_env_vars():
            import os
            _ = list(os.environ.keys())[:5]
        
        # Check disk space
        def check_disk_space():
            import shutil
            try:
                _ = shutil.disk_usage("C:\\")
            except:
                pass
        
        # Read benign registry key
        def read_registry():
            try:
                import winreg
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SOFTWARE\Microsoft\Windows\CurrentVersion"
                )
                winreg.CloseKey(key)
            except:
                pass
        
        # List of available benign operations
        available = [
            query_system_info,
            enum_env_vars,
            check_disk_space,
            read_registry
        ]
        
        # Randomly select operations
        selected = random.sample(available, min(count, len(available)))
        
        return selected
    
    def randomize_api_call_sequence(self,
                                   api_calls: List[tuple]) -> List[tuple]:
        """
        Reorder API calls where dependencies allow
        Creates unique syscall sequences for each execution
        
        Args:
            api_calls: List of (function, args, kwargs) tuples
            
        Returns:
            Reordered list maintaining dependencies
        """
        
        # This is simplified - production code would need
        # dependency graph analysis
        
        # Separate calls into groups that can be reordered
        reorderable = []
        sequential = []
        
        for call in api_calls:
            # Simplified heuristic - production needs real dependency analysis
            func_name = call[0].__name__ if hasattr(call[0], '__name__') else str(call[0])
            
            # Some operations must maintain order
            critical_order = ['CreateProcess', 'WriteProcessMemory', 'CreateRemoteThread']
            
            if any(crit in func_name for crit in critical_order):
                sequential.append(call)
            else:
                reorderable.append(call)
        
        # Shuffle reorderable calls
        random.shuffle(reorderable)
        
        # Merge back together
        result = []
        reorder_idx = 0
        
        for call in api_calls:
            if call in sequential:
                result.append(call)
            else:
                result.append(reorderable[reorder_idx])
                reorder_idx += 1
        
        return result
    


