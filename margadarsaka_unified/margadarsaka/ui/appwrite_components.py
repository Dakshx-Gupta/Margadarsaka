"""
Streamlit Appwrite Integration
Provides client-side Appwrite functionality for Streamlit apps including
authentication, real-time updates, and file uploads.
"""

import streamlit as st
import streamlit.components.v1 as components
from typing import Dict, Any, Optional
import json
import logging
import os

logger = logging.getLogger(__name__)


def inject_appwrite_sdk():
    """
    Inject Appwrite JavaScript SDK into Streamlit app.
    This should be called once at the start of your Streamlit app.
    """
    # Get Appwrite configuration from environment variables
    # Use VITE variables for client-side compatibility, fallback to regular variables
    endpoint = os.getenv(
        "VITE_APPWRITE_ENDPOINT",
        os.getenv("APPWRITE_ENDPOINT", "https://fra.cloud.appwrite.io/v1"),
    )
    project_id = os.getenv(
        "VITE_APPWRITE_PROJECT_ID",
        os.getenv("APPWRITE_PROJECT_ID", "68cd30a60005e3521af6"),
    )

    # Inject Appwrite SDK and initialize client
    components.html(
        f"""
    <script src="https://cdn.jsdelivr.net/npm/appwrite@20.0.0"></script>
    <script>
        // Initialize Appwrite client
        window.appwrite = new Appwrite.Client()
            .setEndpoint('{endpoint}')
            .setProject('{project_id}');
        
        // Initialize services
        window.appwriteAccount = new Appwrite.Account(window.appwrite);
        window.appwriteDatabase = new Appwrite.Databases(window.appwrite);
        window.appwriteStorage = new Appwrite.Storage(window.appwrite);
        
        // Global state management
        window.appwriteState = {{
            user: null,
            session: null,
            isLoggedIn: false
        }};
        
        // Helper functions
        window.appwriteHelpers = {{
            // Get current user
            getCurrentUser: async function() {{
                try {{
                    const user = await window.appwriteAccount.get();
                    window.appwriteState.user = user;
                    window.appwriteState.isLoggedIn = true;
                    return user;
                }} catch (error) {{
                    console.log('No active session');
                    window.appwriteState.user = null;
                    window.appwriteState.isLoggedIn = false;
                    return null;
                }}
            }},
            
            // Login with email and password
            login: async function(email, password) {{
                try {{
                    const session = await window.appwriteAccount.createEmailPasswordSession({{
                        email: email,
                        password: password
                    }});
                    window.appwriteState.session = session;
                    const user = await this.getCurrentUser();
                    return {{ success: true, user: user }};
                }} catch (error) {{
                    console.error('Login failed:', error);
                    return {{ success: false, error: error.message }};
                }}
            }},
            
            // Register new user
            register: async function(email, password, name) {{
                try {{
                    const user = await window.appwriteAccount.create({{
                        userId: 'unique()',
                        email: email,
                        password: password,
                        name: name
                    }});
                    // Auto-login after registration
                    const loginResult = await this.login(email, password);
                    return {{ success: true, user: user }};
                }} catch (error) {{
                    console.error('Registration failed:', error);
                    return {{ success: false, error: error.message }};
                }}
            }},
            
            // Logout
            logout: async function() {{
                try {{
                    await window.appwriteAccount.deleteSession('current');
                    window.appwriteState.user = null;
                    window.appwriteState.session = null;
                    window.appwriteState.isLoggedIn = false;
                    return {{ success: true }};
                }} catch (error) {{
                    console.error('Logout failed:', error);
                    return {{ success: false, error: error.message }};
                }}
            }},
            
            // OAuth login
            loginWithOAuth: function(provider) {{
                try {{
                    window.appwriteAccount.createOAuth2Session(
                        provider,
                        window.location.origin + '/success',
                        window.location.origin + '/failure'
                    );
                }} catch (error) {{
                    console.error('OAuth login failed:', error);
                }}
            }},
            
            // Send Streamlit message
            sendToStreamlit: function(type, data) {{
                window.parent.postMessage({{
                    type: 'appwrite_' + type,
                    data: data
                }}, '*');
            }}
        }};
        
        // Check for existing session on load
        window.appwriteHelpers.getCurrentUser().then(user => {{
            if (user) {{
                window.appwriteHelpers.sendToStreamlit('user_logged_in', user);
            }}
        }});
        
        console.log('Appwrite SDK initialized successfully');
    </script>
    """,
        height=0,
    )


def appwrite_auth_component():
    """
    Create an authentication component with login/register forms.
    Returns authentication state and user data.
    """

    # Create the authentication UI
    auth_html = """
    <div id="appwrite-auth" style="max-width: 400px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
        <div id="auth-status"></div>
        
        <!-- Login Form -->
        <div id="login-form">
            <h3>Login</h3>
            <form id="login-form-element">
                <div style="margin-bottom: 10px;">
                    <input type="email" id="login-email" placeholder="Email" required 
                           style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px;">
                </div>
                <div style="margin-bottom: 10px;">
                    <input type="password" id="login-password" placeholder="Password" required 
                           style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px;">
                </div>
                <button type="submit" style="width: 100%; padding: 10px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">
                    Login
                </button>
            </form>
            
            <hr style="margin: 20px 0;">
            
            <!-- OAuth Buttons -->
            <div style="display: flex; gap: 10px; margin-bottom: 10px;">
                <button onclick="handleOAuthLogin('google')" 
                        style="flex: 1; padding: 8px; background: #db4437; color: white; border: none; border-radius: 4px; cursor: pointer;">
                    Google
                </button>
                <button onclick="handleOAuthLogin('github')" 
                        style="flex: 1; padding: 8px; background: #333; color: white; border: none; border-radius: 4px; cursor: pointer;">
                    GitHub
                </button>
            </div>
            
            <p style="text-align: center; margin-top: 10px;">
                Don't have an account? 
                <a href="#" onclick="showRegisterForm()" style="color: #007bff; text-decoration: none;">Register</a>
            </p>
        </div>
        
        <!-- Register Form -->
        <div id="register-form" style="display: none;">
            <h3>Register</h3>
            <form id="register-form-element">
                <div style="margin-bottom: 10px;">
                    <input type="text" id="register-name" placeholder="Full Name" required 
                           style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px;">
                </div>
                <div style="margin-bottom: 10px;">
                    <input type="email" id="register-email" placeholder="Email" required 
                           style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px;">
                </div>
                <div style="margin-bottom: 10px;">
                    <input type="password" id="register-password" placeholder="Password" required 
                           style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px;">
                </div>
                <button type="submit" style="width: 100%; padding: 10px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer;">
                    Register
                </button>
            </form>
            
            <p style="text-align: center; margin-top: 10px;">
                Already have an account? 
                <a href="#" onclick="showLoginForm()" style="color: #007bff; text-decoration: none;">Login</a>
            </p>
        </div>
        
        <!-- User Profile (shown when logged in) -->
        <div id="user-profile" style="display: none;">
            <h3>Welcome!</h3>
            <div id="user-info"></div>
            <button onclick="handleLogout()" 
                    style="width: 100%; padding: 10px; background: #dc3545; color: white; border: none; border-radius: 4px; cursor: pointer; margin-top: 10px;">
                Logout
            </button>
        </div>
    </div>
    
    <script>
        // Form toggle functions
        function showRegisterForm() {
            document.getElementById('login-form').style.display = 'none';
            document.getElementById('register-form').style.display = 'block';
        }
        
        function showLoginForm() {
            document.getElementById('register-form').style.display = 'none';
            document.getElementById('login-form').style.display = 'block';
        }
        
        function showUserProfile(user) {
            document.getElementById('login-form').style.display = 'none';
            document.getElementById('register-form').style.display = 'none';
            document.getElementById('user-profile').style.display = 'block';
            document.getElementById('user-info').innerHTML = `
                <p><strong>Name:</strong> ${user.name || user.email}</p>
                <p><strong>Email:</strong> ${user.email}</p>
                <p><strong>ID:</strong> ${user.$id}</p>
            `;
        }
        
        function showAuthForms() {
            document.getElementById('user-profile').style.display = 'none';
            document.getElementById('login-form').style.display = 'block';
        }
        
        // Authentication handlers
        async function handleLogin(event) {
            event.preventDefault();
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;
            
            const result = await window.appwriteHelpers.login(email, password);
            if (result.success) {
                showUserProfile(result.user);
                window.appwriteHelpers.sendToStreamlit('login_success', result.user);
            } else {
                alert('Login failed: ' + result.error);
            }
        }
        
        async function handleRegister(event) {
            event.preventDefault();
            const name = document.getElementById('register-name').value;
            const email = document.getElementById('register-email').value;
            const password = document.getElementById('register-password').value;
            
            const result = await window.appwriteHelpers.register(email, password, name);
            if (result.success) {
                showUserProfile(result.user);
                window.appwriteHelpers.sendToStreamlit('register_success', result.user);
            } else {
                alert('Registration failed: ' + result.error);
            }
        }
        
        async function handleLogout() {
            const result = await window.appwriteHelpers.logout();
            if (result.success) {
                showAuthForms();
                window.appwriteHelpers.sendToStreamlit('logout_success', null);
            }
        }
        
        function handleOAuthLogin(provider) {
            window.appwriteHelpers.loginWithOAuth(provider);
        }
        
        // Attach event listeners
        document.getElementById('login-form-element').addEventListener('submit', handleLogin);
        document.getElementById('register-form-element').addEventListener('submit', handleRegister);
        
        // Check if user is already logged in
        if (window.appwriteState && window.appwriteState.isLoggedIn && window.appwriteState.user) {
            showUserProfile(window.appwriteState.user);
        }
    </script>
    """

    # Render the component and capture any returned data
    result = components.html(auth_html, height=400)

    return result


def handle_appwrite_messages():
    """
    Handle messages from Appwrite JavaScript components.
    Call this in your Streamlit app to process authentication events.
    """
    # Check for authentication state in session
    if "appwrite_user" not in st.session_state:
        st.session_state.appwrite_user = None
        st.session_state.appwrite_logged_in = False

    # This would typically be handled by JavaScript postMessage
    # For now, we'll use Streamlit's session state
    return {
        "user": st.session_state.appwrite_user,
        "logged_in": st.session_state.appwrite_logged_in,
    }


def appwrite_file_upload_component(bucket_id: str = "files"):
    """
    Create a file upload component that uploads directly to Appwrite Storage.
    """

    upload_html = f"""
    <div id="appwrite-upload" style="max-width: 400px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
        <h3>Upload File</h3>
        <input type="file" id="file-input" style="margin-bottom: 10px; width: 100%;">
        <button onclick="handleFileUpload()" id="upload-btn" 
                style="width: 100%; padding: 10px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">
            Upload
        </button>
        <div id="upload-status" style="margin-top: 10px;"></div>
    </div>
    
    <script>
        async function handleFileUpload() {{
            const fileInput = document.getElementById('file-input');
            const statusDiv = document.getElementById('upload-status');
            const uploadBtn = document.getElementById('upload-btn');
            
            if (!fileInput.files[0]) {{
                statusDiv.innerHTML = '<p style="color: red;">Please select a file</p>';
                return;
            }}
            
            const file = fileInput.files[0];
            uploadBtn.disabled = true;
            uploadBtn.textContent = 'Uploading...';
            statusDiv.innerHTML = '<p>Uploading file...</p>';
            
            try {{
                const result = await window.appwriteStorage.createFile(
                    '{bucket_id}',
                    'unique()',
                    file
                );
                
                statusDiv.innerHTML = `
                    <p style="color: green;">File uploaded successfully!</p>
                    <p><strong>File ID:</strong> ${{result.$id}}</p>
                `;
                
                // Send result to Streamlit
                window.appwriteHelpers.sendToStreamlit('file_uploaded', result);
                
            }} catch (error) {{
                statusDiv.innerHTML = `<p style="color: red;">Upload failed: ${{error.message}}</p>`;
            }} finally {{
                uploadBtn.disabled = false;
                uploadBtn.textContent = 'Upload';
            }}
        }}
    </script>
    """

    return components.html(upload_html, height=200)


def get_appwrite_config() -> Dict[str, str]:
    """
    Get Appwrite configuration for use in Streamlit components.
    """
    return {
        "endpoint": os.getenv("APPWRITE_ENDPOINT", "https://fra.cloud.appwrite.io/v1"),
        "project_id": os.getenv("APPWRITE_PROJECT_ID", "68cd30a60005e3521af6"),
        "database_id": os.getenv("APPWRITE_DATABASE_ID", "margadarsaka_db"),
        "storage_bucket_id": os.getenv("APPWRITE_BUCKET_ID", "margadarsaka_files"),
    }
