import streamlit as st
import streamlit.components.v1 as components

@st.cache_resource
def create_session():
    ### creating session for Streamlit in Snowflake (SiS)
    try:
        from snowflake.snowpark import Session
        from snowflake.snowpark.context import get_active_session
        session = get_active_session()
    ### creating session for local development via python connector using credentials found in config.toml file.
    except:
        from snowflake.snowpark import Session
        session = Session.builder.config("connection_name", "my_conn").create()
    return session

def download_pdf():
    show_print_button = """
    <script>
        function toggleSidebar(action) {
            var sidebar = window.parent.document.querySelector("[data-testid='stSidebar']");
            if (sidebar) {
                if (action === "close") {
                    sidebar.style.display = "none";
                } else {
                    sidebar.style.display = "block";
                }
            }
        }

        function print_page(obj) {
            toggleSidebar("close");  // Hide sidebar before printing
            obj.style.display = "none";  // Hide button before printing

            setTimeout(() => {
                parent.window.print();  // Open print dialog

                setTimeout(() => {
                    toggleSidebar("open");  // Show sidebar after printing
                    obj.style.display = "block";  // Show button again
                }, 2000);  // Ensure sidebar reappears after print dialog closes
            }, 500);
        }
    </script>
    <button onclick="print_page(this)" style="
        background-color: #007bff;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        border-radius: 5px;
        display: block;
        width:100%;
        margin: 10px auto;">
        Export Page as PDF
    </button>
    """

    return components.html(show_print_button, height=60)