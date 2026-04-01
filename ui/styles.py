# ui/styles.py
import streamlit as st
import html

# --- Custom CSS for Legible, Modern Theme ---
def inject_custom_css():
    st.markdown(
        """
        <style>
        html, body {
            font-size: 16px;
            background: #f8fafc;
            color: #1a1a1a;
        }
        .main {
            padding: 2rem 2.5rem;
            margin-top: 2rem;
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
        }
        .stButton>button {
            font-weight: 600;
            font-size: 1.1rem;
            width: 100%;
            min-height: 48px;
            border-radius: 6px;
            outline: 2px solid transparent;
            outline-offset: 2px;
            transition: outline 0.2s, box-shadow 0.2s, transform 0.1s, background 0.2s;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            background: #f3f4f6;
        }
        .stButton>button:hover {
            box-shadow: 0 4px 16px rgba(55, 65, 81, 0.12);
            background: #fbbf24;
            color: #7c4700;
            transform: scale(1.03);
            transition: box-shadow 0.2s, background 0.2s, color 0.2s, transform 0.1s;
        }
        .stButton>button:active {
            background: #fde68a;
            color: #a16207;
            transform: scale(0.98);
            box-shadow: 0 2px 8px rgba(55, 65, 81, 0.10);
        }
        .rainbow-btn {
            width: 100%;
            margin-top: 1.2rem;
            padding: 0.7rem 0;
            font-size: 1.1rem;
            border-radius: 6px;
            background: linear-gradient(90deg, #fbbf24, #a78bfa, #34d399, #f472b6);
            color: #1a1a1a;
            font-weight: 700;
            border: none;
            cursor: pointer;
            outline: 2px solid transparent;
            outline-offset: 2px;
            transition: outline 0.2s;
        }
        .rainbow-btn:focus {
            outline: 2px solid #3b82f6;
            outline-offset: 2px;
        }
        .rainbow-btn:active {
            filter: brightness(0.95);
        }
        .rainbow-btn[aria-disabled="true"] {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .royal-banner {
            padding: 1rem 1.5rem;
            margin-bottom: 1.5rem;
            font-size: 2rem;
            text-align: center;
            font-weight: 700;
            letter-spacing: 1px;
            background: #fffbe6;
            color: #7c4700;
            border-radius: 0.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }
        .royal-card {
            padding: 1.2rem;
            margin-bottom: 1.2rem;
            border-radius: 0.5rem;
            background: #ffffff;
            color: #1a1a1a;
            box-shadow: 0 1px 4px rgba(0,0,0,0.04);
            transition: box-shadow 0.2s, transform 0.1s;
        }
        .royal-card:hover {
            box-shadow: 0 6px 24px rgba(55, 65, 81, 0.13);
            transform: scale(1.01);
            background: #f3f4f6;
        }
        .royal-card:active {
            box-shadow: 0 2px 8px rgba(55, 65, 81, 0.10);
            transform: scale(0.98);
            background: #fbbf24;
        }
        .royal-divider {
            margin: 1.2rem 0;
            border: none;
            border-top: 2px solid #e5e7eb;
        }
        .royal-label {
            font-size: 1.15rem;
            font-weight: 700;
            color: #3b3b3b;
        }
        .stTextInput>div>input, .stTextArea>div>textarea {
            font-size: 1.08rem;
            min-height: 44px;
            border-radius: 6px;
        }
        .stTextInput>div>input:focus, .stTextArea>div>textarea:focus {
            outline: 2px solid #3b82f6 !important;
            outline-offset: 2px;
        }
        /* Sidebar layout */
        section[data-testid="stSidebar"] {
            padding-top: 1.5rem;
            background: #f3f4f6;
        }
        .sidebar-title {
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 0.7rem;
            text-align: center;
            color: #3b3b3b;
        }
        .sidebar-card {
            padding: 1rem 1rem 0.7rem 1rem;
            margin-bottom: 1rem;
            border-radius: 0.5rem;
            font-size: 1.08rem;
            background: #fff;
            color: #1a1a1a;
            box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        }
        .sidebar-critical {
            color: #fff;
            background: #dc2626;
            padding: 0.7rem 1rem;
            border-radius: 0.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        .sidebar-btn > button {
            background: #fbbf24 !important;
            color: #7c4700 !important;
            border: none !important;
            font-weight: 700 !important;
            margin-bottom: 0.5rem !important;
        }
        /* Focus outline for all interactive elements */
        button:focus, input:focus, textarea:focus {
            outline: 2px solid #3b82f6 !important;
            outline-offset: 2px;
        }
        /* Responsive adjustments */
        @media (max-width: 700px) {
            .main {
                padding: 1rem 0.5rem;
                margin-top: 1rem;
            }
            .royal-banner {
                font-size: 1.3rem;
                padding: 0.7rem 0.5rem;
            }
            .royal-card {
                padding: 0.7rem;
                font-size: 1rem;
            }
            .sidebar-title, .sidebar-card {
                font-size: 1rem;
                padding: 0.7rem 0.5rem;
            }
            .stButton>button, .rainbow-btn {
                font-size: 1rem;
                min-height: 40px;
            }
            .stTextInput>div>input, .stTextArea>div>textarea {
                font-size: 1rem;
                min-height: 36px;
            }
        }
        /* High contrast for accessibility */
        @media (prefers-contrast: more) {
            .royal-banner, .royal-card, .sidebar-card {
                background: #fff !important;
                color: #000 !important;
                border: 2px solid #000 !important;
            }
            .rainbow-btn {
                color: #000 !important;
            }
        }
        /* Accessibility: visually hidden utility class for screen readers */
        .sr-only {
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0,0,0,0);
            border: 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- Input Sanitization Utilities ---
def sanitize_input(user_input, max_length=100, allow_chars=None):
    """Sanitize user input to prevent code/HTML/script injection and limit length."""
    if not isinstance(user_input, str):
        return ""
    sanitized = user_input.strip()[:max_length]
    sanitized = html.escape(sanitized)
    if allow_chars:
        sanitized = ''.join(c for c in sanitized if c in allow_chars)
    return sanitized
