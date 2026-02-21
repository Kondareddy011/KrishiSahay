"""
Setup script for ML Model Repository
Installs dependencies and builds the FAISS index
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        print("\n💡 Try installing manually:")
        print("   pip install sentence-transformers faiss-cpu transformers torch numpy")
        return False

def build_index():
    """Build FAISS index"""
    print("\n🔨 Building FAISS index...")
    try:
        import model
        print("✅ Index built successfully")
        return True
    except ImportError as e:
        print(f"❌ Error building index: {e}")
        print("   Make sure all dependencies are installed")
        return False

if __name__ == "__main__":
    print("="*60)
    print("🚀 ML Model Repository Setup")
    print("="*60 + "\n")
    
    # Install requirements
    if install_requirements():
        # Build index
        build_index()
        print("\n✅ Setup complete!")
        print("\n📝 Next steps:")
        print("   1. Run 'python query.py' to test queries")
        print("   2. Run 'python rag_pipeline.py' for full RAG pipeline")
    else:
        print("\n⚠️  Setup incomplete. Please install dependencies manually.")
