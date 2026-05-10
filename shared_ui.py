from __future__ import annotations

import base64

import streamlit as st

from branding import APP_PRODUCT, APP_TAGLINE, FIT_PAGE_LABEL


def _pressuretest_logo_svg(dark_bg: bool = False) -> str:
    pressure_fill = "#F8FAFC" if dark_bg else "#0B1730"
    ring_fill = "#F8FAFC" if dark_bg else "#0B1730"
    handle_fill = "#E5E7EB" if dark_bg else "#0B1730"
    handle_shine = "#94A3B8" if dark_bg else "#475569"
    line_fill = "#F97316"

    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="1600" height="360" viewBox="0 0 1600 360" fill="none">
      <defs>
        <linearGradient id="testGrad" x1="860" y1="55" x2="1180" y2="210" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stop-color="#FFB020"/>
          <stop offset="55%" stop-color="#FF7A00"/>
          <stop offset="100%" stop-color="#F04438"/>
        </linearGradient>
        <linearGradient id="needleGrad" x1="118" y1="122" x2="214" y2="70" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stop-color="#FF7A00"/>
          <stop offset="100%" stop-color="#EF4444"/>
        </linearGradient>
      </defs>

      <g transform="translate(24 34)">
        <circle cx="132" cy="132" r="88" fill="none" stroke="{ring_fill}" stroke-width="12"/>
        <circle cx="132" cy="132" r="64" fill="none" stroke="{ring_fill}" stroke-width="8" opacity="0.92"/>

        <path d="M88 86 A64 64 0 0 1 114 70" stroke="#84CC16" stroke-width="18" stroke-linecap="round"/>
        <path d="M122 68 A64 64 0 0 1 162 73" stroke="#FBBF24" stroke-width="18" stroke-linecap="round"/>
        <path d="M171 80 A64 64 0 0 1 192 106" stroke="#F97316" stroke-width="18" stroke-linecap="round"/>
        <path d="M196 117 A64 64 0 0 1 190 154" stroke="#EF4444" stroke-width="18" stroke-linecap="round"/>
        <path d="M93 187 A64 64 0 0 1 71 161" stroke="#64748B" stroke-width="18" stroke-linecap="round"/>

        <circle cx="132" cy="132" r="24" fill="white" stroke="{ring_fill}" stroke-width="8"/>
        <circle cx="132" cy="132" r="6" fill="#0B1730"/>

        <path d="M132 132 L190 86" stroke="url(#needleGrad)" stroke-width="10" stroke-linecap="round"/>
        <path d="M132 132 L110 147" stroke="#0B1730" stroke-width="5" stroke-linecap="round" opacity="0.65"/>

        <path d="M79 184 L26 237" stroke="{handle_fill}" stroke-width="16" stroke-linecap="round"/>
        <rect x="10" y="226" width="86" height="26" rx="13" transform="rotate(-45 10 226)" fill="{handle_fill}"/>
        <rect x="24" y="221" width="50" height="10" rx="5" transform="rotate(-45 24 221)" fill="{handle_shine}" opacity="0.5"/>
      </g>

      <g transform="translate(265 48)">
        <text x="0" y="118"
              font-family="Arial, Helvetica, sans-serif"
              font-size="112"
              font-style="italic"
              font-weight="800"
              letter-spacing="-3"
              fill="{pressure_fill}">
          Pressure<tspan fill="url(#testGrad)">Test</tspan>
        </text>
        <line x1="6" y1="146" x2="760" y2="146" stroke="{line_fill}" stroke-width="6" stroke-linecap="round"/>
      </g>
    </svg>
    """


def _svg_data_uri(svg: str) -> str:
    encoded = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{encoded}"


def render_sidebar_branding() -> None:
    logo_uri = _svg_data_uri(_pressuretest_logo_svg(dark_bg=False))

    st.sidebar.markdown(
        f"""
        <div style="margin-bottom: 0.8rem;">
            <img
                src="{logo_uri}"
                style="
                    width: 100%;
                    max-width: 255px;
                    height: auto;
                    display: block;
                    margin: 0 0 0.3rem 0;
                "
            />
            <div style="
                font-size: 0.78rem;
                color: #5B6577;
                line-height: 1.35;
                margin-top: 0.05rem;
            ">
                {APP_TAGLINE}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_brand_header(title: str, subtitle: str = "") -> None:
    logo_uri = _svg_data_uri(_pressuretest_logo_svg(dark_bg=False))

    st.markdown(
        f"""
        <div style="margin: 0 0 0.4rem 0;">
            <img
                src="{logo_uri}"
                style="
                    width: 100%;
                    max-width: 700px;
                    height: auto;
                    display: block;
                    margin: 0 0 0.08rem 0;
                "
            />
            <div style="
                font-size: 0.98rem;
                color: #5B6577;
                line-height: 1.3;
                margin: 0;
            ">
                {subtitle or APP_TAGLINE}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_compact_brand_bar() -> None:
    logo_uri = _svg_data_uri(_pressuretest_logo_svg(dark_bg=False))

    st.markdown(
        f"""
        <div style="margin: 0 0 0.12rem 0;">
            <img
                src="{logo_uri}"
                style="
                    width: 100%;
                    max-width: 560px;
                    height: auto;
                    display: block;
                    margin: 0;
                "
            />
        </div>
        <hr style="margin: 0.05rem 0 0.45rem 0; border: none; border-top: 1px solid #d1d5db;" />
        """,
        unsafe_allow_html=True,
    )


def render_profile_strip() -> None:
    full_name = st.session_state.get("full_name")
    franchise_name = st.session_state.get("franchise_name")
    units = st.session_state.get("units_considered")
    ownership_style = st.session_state.get("ownership_style")

    if not any([full_name, franchise_name, units, ownership_style]):
        return

    st.markdown("### Your Profile")

    chips: list[str] = []
    if full_name:
        chips.append(f"<span class='rc-badge'>{full_name}</span>")
    if franchise_name:
        chips.append(f"<span class='rc-badge'>{franchise_name}</span>")
    if units:
        chips.append(f"<span class='rc-badge'>{units} unit(s)</span>")
    if ownership_style:
        chips.append(f"<span class='rc-badge'>{ownership_style}</span>")

    if chips:
        st.markdown("".join(chips), unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="rc-card-soft">
            <div class="rc-kicker">{FIT_PAGE_LABEL}</div>
            <div class="rc-muted">Work through the pages to build your recommendation and report.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_carry_forward_warning() -> None:
    return
<<<<<<< HEAD


def render_pressuretest_boundary_notice(compact: bool = True) -> None:
    """Small, persistent boundary notice so the product stays blunt without drifting into legal advice."""
    padding = "0.65rem 0.8rem" if compact else "0.9rem 1rem"
    st.markdown(
        f"""
        <div style="
            margin: 0.35rem 0 0.85rem 0;
            padding: {padding};
            border: 1px solid #FED7AA;
            background: #FFF7ED;
            border-radius: 14px;
            color: #431407;
            font-size: 0.86rem;
            line-height: 1.45;
        ">
            <strong>PressureTest boundary:</strong> This is a blunt operating and diligence screen — not legal, tax, lending, accounting, or investment advice.
            Use it to identify weak assumptions, missing evidence, and questions to validate with qualified advisors before signing anything.
        </div>
        """,
        unsafe_allow_html=True,
    )

# Compatibility override for older positional render_card calls
def render_card(title=None, value=None, body=None, *, soft=False, **kwargs):
    import streamlit as st

    bg = "#F8FAFC" if soft else "#FFFFFF"
    border = "#E5E7EB"

    st.markdown(
        f"""
        <div style="background:{bg}; border:1px solid {border}; border-radius:14px; padding:18px; margin:10px 0;">
            <div style="font-size:0.85rem; color:#64748B; font-weight:600; margin-bottom:6px;">{title or ""}</div>
            <div style="font-size:1.25rem; color:#0F172A; font-weight:700; margin-bottom:6px;">{value or ""}</div>
            <div style="font-size:0.95rem; color:#475569; line-height:1.5;">{body or ""}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Final compatibility override for positional render_card calls
def render_card(*args, soft=False, **kwargs):
    import streamlit as st

    title = kwargs.get("title", args[0] if len(args) > 0 else "")
    value = kwargs.get("value", args[1] if len(args) > 1 else "")
    body = kwargs.get("body", args[2] if len(args) > 2 else kwargs.get("content", ""))

    bg = "#F8FAFC" if soft else "#FFFFFF"
    border = "#E5E7EB"

    st.markdown(
        f"""
        <div style="background:{bg}; border:1px solid {border}; border-radius:14px; padding:18px; margin:10px 0;">
            <div style="font-size:0.85rem; color:#64748B; font-weight:600; margin-bottom:6px;">{title}</div>
            <div style="font-size:1.25rem; color:#0F172A; font-weight:700; margin-bottom:6px;">{value}</div>
            <div style="font-size:0.95rem; color:#475569; line-height:1.5;">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
=======
>>>>>>> fec65288cb896b4679e84e61241f185fa625e150
