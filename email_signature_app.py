import streamlit as st
import re
import time

# HTML template as a Python string (with placeholders)
HTML_TEMPLATE = """
<table cellpadding="0" cellspacing="0" border="0" style="font-family: Arial, sans-serif; font-size: medium;">
<tr>
<td>
<table cellpadding="0" cellspacing="0" border="0" style="font-family: Arial, sans-serif; font-size: medium;">
<tr>
<td style="padding: 0; vertical-align: middle;">
<div style="color: #dcdcdc; font-size: 14px; margin: 0;">—</div>
<table><tr><td height="6" style="font-size: 6px; line-height: 0;">&nbsp;</td></tr></table>
<div style="margin: 0; color: #000; font-size: 14px; font-weight: 600;"><span>{full_name}</span></div>
<div style="margin: 0; color: #787878; font-size: 14px; line-height: 22px; font-weight: 550;"><span>{job_title}</span></div>
<table><tr><td height="12" style="font-size: 0; line-height: 0;">&nbsp;</td></tr></table>

<table cellpadding="0" cellspacing="0" border="0" style="font-family: Arial, sans-serif; font-size: medium;">
<tr>
<td><img src="https://www.flarehr.com/wp-content/uploads/2020/09/Flare_Master-Logo-01.png" alt="Flare logo" width="144" style="display: block;"></td>
<td width="4" style="font-size: 10; line-height: 0;">&nbsp;</td>
<td><img src="https://www.flarehr.com/wp-content/uploads/2025/07/signature-divider.png" alt="Flare logo" width="24" style="display: block;"></td>
<td width="6" style="font-size: 10; line-height: 0;">&nbsp;</td>

<td>
<table cellpadding="0" cellspacing="0" border="0" style="font-family: Arial, sans-serif; font-size: medium;">
<tr>
<td style="padding: 0; color: #000;"><a href="mailto:{email}" style="text-decoration: underline; color: #1d4ed8; font-size: 14px; font-weight: 500;"><span style="text-decoration: underline;">{email}</span></a></td>
</tr>
<tr>
<td style="padding: 0; color: #000;"><span style="font-size: 14px;">{phone_numbers}</span></td>
</tr>
</table>
</td>
</tr>
</table>
{banner_html}
<table cellpadding="0" cellspacing="0" border="0" style="font-family: Arial, sans-serif; font-size: medium;"><tr><td height="30"></td></tr></table>
{trustpilot_html}
</td>
</tr>
</table>
"""

TRUSTPILOT_HTML = '''
<table cellpadding="0" cellspacing="0" border="0" style="width:100%;">
    <tr>
      <td>
        <p
          style="
            font-family: Arial, Arial Black, Tahoma, Trebuchet MS, Verdana, sans-serif;
            font-size: 12px;
            color: #aaa;
            text-decoration: none;
          "
        >
          <a
            href="https://www.trustpilot.com/review/flarehr.com?utm_medium=Trustbox&utm_source=EmailSignature2"
            target="_blank"
            rel="noopener noreferrer"
            style="text-decoration: none; text-underline: none"
          >
            <img
              src="https://emailsignature.trustpilot.com/signature/en-US/2/603317a0bffb3c0001779b88/text.png"
              border="0"
              height="16"
              style="max-height: 16px; margin: 0; padding: 0; width: auto; border: none"
              alt="Trustpilot rating"
            />
            <br />
            <img
              src="https://emailsignature.trustpilot.com/signature/en-US/2/603317a0bffb3c0001779b88/stars.png"
              border="0"
              width="160"
              height="40"
              style="max-width: 128px; width: 100%; max-height: 32px; border: none"
              alt="Trustpilot Stars"
            />
          </a>
          <br />
          <a
            href="https://www.trustpilot.com/review/flarehr.com?utm_medium=Trustbox&utm_source=EmailSignature2"
            target="_blank"
            rel="noopener noreferrer"
            style="text-decoration: none; text-underline: none"
          >
            <img
              src="https://emailsignature.trustpilot.com/brand/s/2/logo.png"
              border="0"
              width="79"
              height="20"
              style="max-width: 80px; width: 100%; max-height: 20px; border: none"
              alt="Trustpilot Logo"
            />
          </a>
        </p>
      </td>
    </tr>
  </table>
'''

st.set_page_config(page_title="Flare signature creator", layout="centered")

st.markdown(
    """
    <style>
    table, th, tr, td {
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

st.header("Flare signature creator")
if not st.session_state['authenticated']:
    with st.form("login_form"):
        password = st.text_input("Password", type="password", disabled=st.session_state['authenticated'])
        submitted = st.form_submit_button("Login", disabled=st.session_state['authenticated'])
        if submitted and not st.session_state['authenticated']:
            if password == "opensesame123":
                st.session_state['authenticated'] = True
                try:
                    time.sleep(1)
                    st.experimental_rerun()
                except Exception:
                    pass
            else:
                st.error("Incorrect password.")

if st.session_state['authenticated']:
    with st.sidebar:
        st.image("https://www.flarehr.com/wp-content/uploads/2020/09/Flare_Master-Logo-01.png", width=120)
        st.header("Your details")
        short_name = ""
        full_name = st.text_input(label="Full name", placeholder="e.g. Sam Smith", key="full_name", value="")
        job_title = st.text_input(label="Job title", placeholder="e.g. Professional Salaryman", value="")
        # Email autofill logic
        if "email" not in st.session_state:
            st.session_state.email = ""
        if full_name and not st.session_state.email:
            name_parts = full_name.strip().split()
            if len(name_parts) >= 2:
                first = name_parts[0].lower()
                last = name_parts[-1].lower()
                st.session_state.email = f"{first}.{last}@flarehr.com"
                short_name = f"{first}_{last}"
        email = st.text_input("Email", placeholder="e.g. sam.smith@flarehr.com", key="email")
        # Phone number input as digits only
        phone1_raw = st.text_input("Primary phone number", placeholder="e.g. 0405123456", value="")
        phone2_raw = st.text_input("Secondary phone number (optional)", placeholder="e.g. 0370123456", value="")
        # Format phone numbers for display
        def format_phone(num):
            if len(num) == 10 and num.startswith('04'):
                return f"{num[:4]} {num[4:7]} {num[7:]}"
            elif len(num) == 10:
                return f"{num[:2]} {num[2:6]} {num[6:]}"
            elif len(num) == 8:
                return f"{num[:4]} {num[4:]}"
            return num
        phone_links = []
        if phone1_raw.strip():
            phone1_digits = re.sub(r'\D', '', phone1_raw)
            phone1_disp = format_phone(phone1_digits)
            phone_links.append(f'<a href="tel:{phone1_digits}" style="text-decoration:none; color:rgb(0,0,0); font:inherit;">{phone1_disp}</a>')
        if phone2_raw.strip():
            phone2_digits = re.sub(r'\D', '', phone2_raw)
            phone2_disp = format_phone(phone2_digits)
            phone_links.append(f'<a href="tel:{phone2_digits}" style="text-decoration:none; color:rgb(0,0,0); font:inherit;">{phone2_disp}</a>')
        phone_numbers = f' <span style="font-weight: 400; color: rgb(220,220,220);">&nbsp;|&nbsp;</span> '.join(phone_links)
        st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)
        st.subheader("Campaign")
        has_campaign = st.toggle("Show campaign banner", value=False)
        banner_html = ""
        if has_campaign:
            banner_url = st.text_input("Banner Image URL")
            banner_link = st.text_input("Banner Link")
            banner_alt = st.text_input("Banner Alt Text")
            banner_html = f'<table><tr><td height="24" style="font-size: 0; line-height: 0;">&nbsp;</td></tr></table>\n<a href="{banner_link}"><img src="{banner_url}" alt="{banner_alt}" width="400" style="display: block;"></a>'
        st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)
        st.subheader("Trustpilot")
        show_trustpilot = st.toggle("Show Trustpilot", value=True)
        trustpilot_html = TRUSTPILOT_HTML if show_trustpilot else ""

    
    st.divider()
    st.markdown("<div style='font-size: 14px; color: rgb(160,160,160);'>// COPY BELOW THIS LINE</div>", unsafe_allow_html=True)
    st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)
    
    html_out = HTML_TEMPLATE.format(
        full_name=full_name,
        job_title=job_title,
        email=email,
        phone_numbers=phone_numbers,
        banner_html=banner_html,
        trustpilot_html=trustpilot_html
    )
    st.markdown(html_out, unsafe_allow_html=True)
    st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 14px; color: rgb(160,160,160);'>// COPY ABOVE THIS LINE</div>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)
    st.subheader("How do add this to my Outlook?")
    st.markdown("""
    **Method 1 - Copy from this page**
    1. Use your mouse to highlight the signature above the line
    2. Copy (**Ctrl + C** / **Cmd + C**)
    3. Navigate to "Outlook" &gt; "Settings" &gt; "Signatures"
    3. Add a new signature > Paste (**Ctrl + V** / **Cmd + V**)
    
    --
    
    **Method 2 - Share signature**
    Recommended if you're creating the signature for someone else
    1. Download the file (.htm)
    2. Open the file in your browser
    3. Select all (**Ctrl + A** / **Cmd + A**)
    2. Copy (**Ctrl + C** / **Cmd + C**)
    3. Navigate to "Outlook" &gt; "Settings" &gt; "Signatures"
    3. Add a new signature > Paste (**Ctrl + V** / **Cmd + V**)
    """)
    st.download_button(label="Download signature", data=html_out, file_name=short_name+"-email_signature.htm",)

    # Add debug output of the raw HTML for inspection
    # st.code(html_out, language="html") 
        

