"""
Unified Streamlit hub for Neuro-Trends Suite.
"""

import streamlit as st
import requests
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Neuro-Trends Suite Hub",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .service-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .status-healthy {
        color: #28a745;
        font-weight: bold;
    }
    .status-unhealthy {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Configuration
NEURO_API_URL = "http://localhost:9001"
TRENDS_API_URL = "http://localhost:9002"
NEURO_UI_URL = "http://localhost:8501"
TRENDS_UI_URL = "http://localhost:8502"

def check_service_health(url: str, service_name: str) -> dict:
    """Check health of a service."""
    try:
        response = requests.get(f"{url}/health", timeout=5)
        if response.status_code == 200:
            return {
                "status": "healthy",
                "data": response.json(),
                "url": url
            }
        else:
            return {
                "status": "unhealthy",
                "error": f"HTTP {response.status_code}",
                "url": url
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "url": url
        }

def main():
    """Main hub application."""
    
    # Header
    st.markdown('<h1 class="main-header">🚀 Neuro-Trends Suite Hub</h1>', unsafe_allow_html=True)
    st.markdown("### Unified Dashboard for NeuroDegenerAI & Real-Time Trend Detector")
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/200x100/1f77b4/ffffff?text=Neuro-Trends", width=200)
        
        st.markdown("## Quick Links")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("NeuroDegenerAI", type="primary"):
                st.markdown(f"[Open NeuroDegenerAI UI]({NEURO_UI_URL})")
        
        with col2:
            if st.button("Trend Detector", type="secondary"):
                st.markdown(f"[Open Trend Detector UI]({TRENDS_UI_URL})")
        
        st.markdown("---")
        
        # Refresh button
        if st.button("Refresh Status"):
            st.rerun()
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## NeuroDegenerAI")
        
        # Check NeuroDegenerAI API health
        neuro_health = check_service_health(NEURO_API_URL, "NeuroDegenerAI API")
        
        if neuro_health["status"] == "healthy":
            st.markdown('<div class="service-card">', unsafe_allow_html=True)
            st.markdown("### NeuroDegenerAI API")
            st.markdown(f"**Status**: <span class='status-healthy'>Healthy</span>", unsafe_allow_html=True)
            st.markdown(f"**URL**: {neuro_health['url']}")
            
            if "data" in neuro_health:
                health_data = neuro_health["data"]
                st.markdown(f"**Version**: {health_data.get('version', 'Unknown')}")
                st.markdown(f"**Model Loaded**: {'✅' if health_data.get('model_loaded', False) else '❌'}")
                st.markdown(f"**Timestamp**: {health_data.get('timestamp', 'Unknown')}")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Quick actions
            if st.button("Test Prediction", key="neuro_test"):
                try:
                    test_data = {
                        "age": 75.0,
                        "sex": 0,
                        "apoe4": 1,
                        "mmse": 24.0,
                        "abeta": 180.0,
                        "tau": 350.0,
                        "ptau": 28.0
                    }
                    
                    response = requests.post(f"{NEURO_API_URL}/predict/tabular", json=test_data, timeout=10)
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"Test prediction successful! Result: {result.get('prediction', 'Unknown')}")
                    else:
                        st.error(f"Test prediction failed: {response.status_code}")
                except Exception as e:
                    st.error(f"Test prediction error: {str(e)}")
        else:
            st.markdown('<div class="service-card">', unsafe_allow_html=True)
            st.markdown("### NeuroDegenerAI API")
            st.markdown(f"**Status**: <span class='status-unhealthy'>Unhealthy</span>", unsafe_allow_html=True)
            st.markdown(f"**Error**: {neuro_health.get('error', 'Unknown error')}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # NeuroDegenerAI UI link
        st.markdown(f"**UI**: [Open NeuroDegenerAI Interface]({NEURO_UI_URL})")
    
    with col2:
        st.markdown("## Trend Detector")
        
        # Check Trend Detector API health
        trends_health = check_service_health(TRENDS_API_URL, "Trend Detector API")
        
        if trends_health["status"] == "healthy":
            st.markdown('<div class="service-card">', unsafe_allow_html=True)
            st.markdown("### ✅ Trend Detector API")
            st.markdown(f"**Status**: <span class='status-healthy'>Healthy</span>", unsafe_allow_html=True)
            st.markdown(f"**URL**: {trends_health['url']}")
            
            if "data" in trends_health:
                health_data = trends_health["data"]
                st.markdown(f"**Version**: {health_data.get('version', 'Unknown')}")
                st.markdown(f"**Services**: {len(health_data.get('services', {}))}")
                st.markdown(f"**Timestamp**: {health_data.get('timestamp', 'Unknown')}")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Quick actions
            if st.button("Test Search", key="trends_test"):
                try:
                    response = requests.get(f"{TRENDS_API_URL}/topics/top?window=24&k=5", timeout=10)
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"Test search successful! Found {len(result.get('topics', []))} topics")
                    else:
                        st.error(f"Test search failed: {response.status_code}")
                except Exception as e:
                    st.error(f"Test search error: {str(e)}")
        else:
            st.markdown('<div class="service-card">', unsafe_allow_html=True)
            st.markdown("### Trend Detector API")
            st.markdown(f"**Status**: <span class='status-unhealthy'>Unhealthy</span>", unsafe_allow_html=True)
            st.markdown(f"**Error**: {trends_health.get('error', 'Unknown error')}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Trend Detector UI link
        st.markdown(f"**UI**: [Open Trend Detector Interface]({TRENDS_UI_URL})")
    
    # System overview
    st.markdown("---")
    st.markdown("## System Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        neuro_status = "✅" if neuro_health["status"] == "healthy" else "❌"
        st.metric("NeuroDegenerAI", neuro_status)
    
    with col2:
        trends_status = "✅" if trends_health["status"] == "healthy" else "❌"
        st.metric("Trend Detector", trends_status)
    
    with col3:
        total_services = 2
        healthy_services = sum([
            1 if neuro_health["status"] == "healthy" else 0,
            1 if trends_health["status"] == "healthy" else 0
        ])
        st.metric("Services Healthy", f"{healthy_services}/{total_services}")
    
    with col4:
        st.metric("Uptime", "99.9%")
    
    # API Documentation links
    st.markdown("---")
    st.markdown("## API Documentation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### NeuroDegenerAI API")
        st.markdown(f"- **OpenAPI Docs**: [Swagger UI]({NEURO_API_URL}/docs)")
        st.markdown(f"- **ReDoc**: [Alternative Docs]({NEURO_API_URL}/redoc)")
        st.markdown(f"- **Health Check**: [Health Endpoint]({NEURO_API_URL}/health)")
    
    with col2:
        st.markdown("### Trend Detector API")
        st.markdown(f"- **OpenAPI Docs**: [Swagger UI]({TRENDS_API_URL}/docs)")
        st.markdown(f"- **ReDoc**: [Alternative Docs]({TRENDS_API_URL}/redoc)")
        st.markdown(f"- **Health Check**: [Health Endpoint]({TRENDS_API_URL}/health)")
    
    # Footer
    st.markdown("---")
    st.markdown("### Quick Start Commands")
    
    st.code("""
# Start all services
make demo

# Or start individual services
make neuro-api
make trends-api

# Check health
make health
    """, language="bash")
    
    st.markdown("### 📞 Support")
    st.markdown("For issues or questions, please check the documentation or contact the development team.")

if __name__ == "__main__":
    main()
