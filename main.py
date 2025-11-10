def login_page():
    """Display login page with Google OAuth"""
    sl.set_page_config(
        page_title="Margadarsaka - Login",
        page_icon="🎯",
        layout="centered"
    )
    
    col1, col2, col3 = sl.columns([1, 2, 1])
    
    with col2:
        sl.title("🌟 Welcome to Margadarsaka")
        sl.markdown("### Your AI-Powered Career Guide")
        
        # Lottie animation
        url = "https://lottie.host/179fa302-85e8-4b84-86ff-d6d44b671ae2/yuf3ctwVdH.json"
        try:
            response = requests.get(url)
            animation_json = response.json()
            st_lottie(animation_json, height=200, key="login_lottie")
        except:
            pass
        
        sl.markdown("---")
        sl.info("👋 Sign in to get personalized career guidance")
        
        # Your credentials
        project_id = sl.secrets.get("APPWRITE_PROJECT_ID", "69124432002faa341df2")
        endpoint = sl.secrets.get("APPWRITE_ENDPOINT", "https://sgp.cloud.appwrite.io/v1")
        
        # Detect environment
        app_url = sl.secrets.get("APP_URL", "https://margadarsaka.streamlit.app")
        
        # Build OAuth URL
        import urllib.parse
        success_url = urllib.parse.quote(app_url, safe='')
        failure_url = urllib.parse.quote(f"{app_url}?auth=failed", safe='')
        
        oauth_url = (
            f"{endpoint}/account/sessions/oauth2/google"
            f"?project={project_id}"
            f"&success={success_url}"
            f"&failure={failure_url}"
        )
        
        # Method 1: Direct Link (Most Reliable)
        sl.markdown("### 🔐 Sign in to Continue")
        sl.markdown(f"""
        <div style="text-align: center; padding: 20px;">
            <a href="{oauth_url}" target="_self" style="
                display: inline-block;
                padding: 12px 24px;
                background-color: #4285f4;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 16px;
            ">
                🔐 Sign in with Google
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        sl.markdown("---")
        
        # Debug information (expandable)
        with sl.expander("🔧 Debug Information"):
            sl.write("**Configuration:**")
            sl.code(f"Project ID: {project_id}")
            sl.code(f"Endpoint: {endpoint}")
            sl.code(f"App URL: {app_url}")
            sl.write("**OAuth URL:**")
            sl.code(oauth_url)
            
            # Test button
            if sl.button("🧪 Test OAuth URL", key="test_oauth"):
                sl.info("Opening OAuth URL in new window...")
                sl.markdown(f'<meta http-equiv="refresh" content="0;url={oauth_url}">', unsafe_allow_html=True)
        
        # Alternative method with st.link_button (if available in your Streamlit version)
        try:
            if sl.button("Alternative: Click Here to Sign In", type="primary", use_container_width=True):
                # Use JavaScript redirect
                sl.markdown(f"""
                <script>
                    window.location.href = "{oauth_url}";
                </script>
                """, unsafe_allow_html=True)
                st.rerun()
        except:
            pass
        
        sl.markdown("---")
        sl.caption("🔒 Your data is secure and private")
        
        # Manual link as last resort
        sl.markdown(f"**Not working?** [Click this direct link]({oauth_url})")