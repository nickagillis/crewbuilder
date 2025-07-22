"""
Test Interface Generation - Verify users get complete runnable systems
"""

from crewbuilder_crew_v2 import get_crewbuilder_v2

def test_heygen_example():
    """Test with the user's HeyGen video generation requirement"""
    
    requirement = """
    I need set up an agent that will take in a list of content ideas. 
    Research the topics and news using open ai deep research or something similar. 
    generate a short 2-3 minute script then generate videos using hey gen with a 
    certain avatar id that I've created and then send them to people in my crm gohighlevel.
    """
    
    print("🎯 Testing Interface Generation with HeyGen Example")
    print("=" * 60)
    
    crewbuilder = get_crewbuilder_v2()
    result = crewbuilder.build_from_requirement(requirement)
    
    if result['success']:
        print("\n✅ System built successfully!")
        print(f"⏱️  Execution time: {result.get('execution_time', 0):.1f} seconds")
        
        # Check for interface code
        interface_code = result.get('interface_code', '')
        if interface_code:
            print(f"\n📱 Interface Code Generated: {len(interface_code)} characters")
            print("\nInterface Preview:")
            print("-" * 40)
            print(interface_code[:500] + "..." if len(interface_code) > 500 else interface_code)
            print("-" * 40)
        else:
            print("\n❌ NO INTERFACE CODE GENERATED - Users can't use the system!")
            
        # Check for deployment package
        deployment_package = result.get('deployment_package', '')
        if deployment_package:
            print(f"\n📦 Deployment Package: {len(deployment_package)} characters")
        else:
            print("\n❌ NO DEPLOYMENT PACKAGE - System can't be deployed!")
            
        # Show what the user actually gets
        print("\n📋 What the user receives:")
        print(f"- Generated Code: {'✅' if result.get('generated_code') else '❌'}")
        print(f"- Interface (API + UI): {'✅' if interface_code else '❌'}")
        print(f"- Deployment Package: {'✅' if deployment_package else '❌'}")
        print(f"- Documentation: {'✅' if result.get('documentation') else '❌'}")
        
    else:
        print(f"\n❌ Build failed: {result.get('error')}")

if __name__ == "__main__":
    test_heygen_example()