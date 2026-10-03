# -*- coding: utf-8 -*-
"""
대망(大望) 독서 노트 & 형세 변화 추적 웹앱
- 일본 68개 율령국 지도를 기반으로 권수별 세력 판도를 확인하고,
  각 율령국에 대한 독서 메모를 기록/관리하는 Streamlit 앱.
"""

import sqlite3
from datetime import datetime, timezone, timedelta
from io import BytesIO

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import provinces as prov
import timeline_data as tl

DB_PATH = "daemang_notes.db"
KST = timezone(timedelta(hours=9))


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            volume INTEGER NOT NULL,
            province_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    return conn


def add_note(volume: int, province_id: int, content: str):
    conn = get_conn()
    conn.execute(
        "INSERT INTO notes (volume, province_id, content, created_at) VALUES (?, ?, ?, ?)",
        (volume, province_id, content, datetime.now(KST).strftime("%Y-%m-%d %H:%M")),
    )
    conn.commit()
    conn.close()


def update_note(note_id: int, content: str):
    conn = get_conn()
    conn.execute("UPDATE notes SET content = ? WHERE id = ?", (content, note_id))
    conn.commit()
    conn.close()


def delete_note(note_id: int):
    conn = get_conn()
    conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()


def get_notes(volume: int = None, province_id: int = None) -> list:
    conn = get_conn()
    query = "SELECT id, volume, province_id, content, created_at FROM notes WHERE 1=1"
    params = []
    if volume is not None:
        query += " AND volume = ?"
        params.append(volume)
    if province_id is not None:
        query += " AND province_id = ?"
        params.append(province_id)
    query += " ORDER BY created_at DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [
        {"id": r[0], "volume": r[1], "province_id": r[2], "content": r[3], "created_at": r[4]}
        for r in rows
    ]


def get_all_notes_df() -> pd.DataFrame:
    notes = get_notes()
    if not notes:
        return pd.DataFrame(columns=["id", "volume", "province_id", "province", "content", "created_at"])
    df = pd.DataFrame(notes)
    df["province"] = df["province_id"].apply(
        lambda pid: f"{pid}. {prov.get_province(pid)['hanja']}({prov.get_province(pid)['hangul']})"
    )
    return df[["id", "volume", "province", "province_id", "content", "created_at"]]


# ---------------------------------------------------------------------------
# Page config & style
# ---------------------------------------------------------------------------
st.set_page_config(page_title="대망 독서노트 · 68율령국 지도", page_icon="🗺️", layout="wide")

st.markdown(
    """
    <style>
    .block-container { padding-top: 1.5rem; }
    .province-card {
        background-color: #f8f9fb;
        border: 1px solid #dde1e8;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 12px;
        color: #1a1a1a;
    }
    .faction-chip {
        display: inline-block; padding: 2px 10px; border-radius: 999px;
        font-size: 0.85rem; color: white; margin-right: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "selected_id" not in st.session_state:
    st.session_state.selected_id = 44  # 기본값: 오와리(오다 노부나가 본거지)
if "highlight_faction" not in st.session_state:
    st.session_state.highlight_faction = None  # 세력 클릭 강조 필터

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("🗾 대망 독서노트")
    st.caption("일본 68개 율령국 지도 기반 독서노트 & 형세 변화 추적")

    volume = st.slider("권수 선택", min_value=1, max_value=36, value=1, step=1)
    period = tl.get_period(volume)
    st.markdown(f"**연도:** {tl.get_year_label(volume)}")
    st.markdown(f"**시대:** {period['label']}")
    st.caption(period["note"])

    st.divider()
    query = st.text_input("🔍 율령국 검색 (이름/한자/번호)", placeholder="예: 미카와, 51, 尾張")
    if query:
        results = prov.search_provinces(query)
        if results:
            for r in results:
                if st.button(r["display"], key=f"search_{r['id']}", use_container_width=True):
                    st.session_state.selected_id = r["id"]
        else:
            st.caption("검색 결과가 없습니다.")

    st.divider()
    st.caption(
        "※ 권수별 세력 판도는 전국시대 실제 역사 흐름을 바탕으로 한 근사치 데이터입니다. "
        "`timeline_data.py`에서 직접 수정할 수 있습니다."
    )

# ---------------------------------------------------------------------------
# Build map figure
# ---------------------------------------------------------------------------
territories = tl.get_territory_map(volume)
all_prov = prov.all_provinces()
factions_in_period = set(territories.values())
highlight = st.session_state.highlight_faction

GRAY_COLOR = "#c9ccd1"

colors, opacities, hover_text = [], [], []
for p in all_prov:
    fkey = territories.get(p["id"])
    if fkey:
        base_color = tl.FACTIONS[fkey]["color"]
        base_opacity = 1.0
        faction_label = tl.FACTIONS[fkey]["name"]
    else:
        base_color = prov.REGIONS[p["region"]]["color"]
        base_opacity = 0.75
        faction_label = "미상 (세력 변동 없음)"

    if highlight and fkey != highlight:
        colors.append(GRAY_COLOR)
        opacities.append(0.35)
    else:
        colors.append(base_color)
        opacities.append(base_opacity)

    hover_text.append(
        f"{p['id']}. {p['hanja']} ({p['hangul']})<br>"
        f"현재 세력: {faction_label}<br>"
        f"지방: {p['region_name']}<br>"
        f"현대 지명: {p['modern']}"
    )

is_selected = [p["id"] == st.session_state.selected_id for p in all_prov]
sizes = [26 if sel else 19 for sel in is_selected]
line_widths = [3 if sel else 0.8 for sel in is_selected]
line_colors = ["#111318" if sel else "#2c313c" for sel in is_selected]

# Plotly에 내장된 실제 세계 해안선 데이터(Natural Earth) 위에 점을 찍는다.
# 주변국(한반도 등)까지 함께 표시되어 실제 지도처럼 보인다.
fig = go.Figure(
    data=go.Scattergeo(
        lon=[p["lon"] for p in all_prov],
        lat=[p["lat"] for p in all_prov],
        mode="markers+text",
        text=[str(p["id"]) for p in all_prov],
        textposition="middle center",
        textfont=dict(size=13, color="#1a1a1a"),
        marker=dict(
            size=sizes,
            color=colors,
            opacity=opacities,
            line=dict(width=line_widths, color=line_colors),
        ),
        hovertext=hover_text,
        hoverinfo="text",
    )
)
fig.update_geos(
    scope="asia",
    resolution=50,
    lonaxis_range=[127.5, 142.5],
    lataxis_range=[29.5, 41.0],
    showland=True,
    landcolor="#f7f3ea",
    showocean=True,
    oceancolor="#cfe3f0",
    showcountries=True,
    countrycolor="#9aa0ab",
    showlakes=False,
    showcoastlines=True,
    coastlinecolor="#8a90a0",
    projection_type="mercator",
    bgcolor="#eef1f6",
)
fig.update_layout(
    height=680,
    margin=dict(l=10, r=10, t=10, b=10),
    paper_bgcolor="#eef1f6",
    showlegend=False,
)

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
col_map, col_info = st.columns([3, 2])

with col_map:
    st.caption("지도의 점을 클릭해 율령국을 선택하세요. 번호는 범례 참고.")

    active_factions = sorted(factions_in_period)
    if active_factions:
        st.caption("● 세력 색상 라벨을 클릭하면 해당 세력 영토만 강조되고 나머지는 회색 처리됩니다")

        # 범례(색상)와 필터 버튼을 하나로 합친다: 버튼 자체를 세력 색으로 칠해서
        # "클릭 가능한 색상 라벨"로 동작하게 만든다 (st-key-* CSS 훅 이용).
        style_rules = []
        for fkey in active_factions:
            color = tl.FACTIONS[fkey]["color"]
            is_active = highlight == fkey
            border = "3px solid #111318" if is_active else "2px solid rgba(0,0,0,0.15)"
            style_rules.append(
                f"""
                .st-key-filter_{fkey} button {{
                    background-color: {color} !important;
                    color: #ffffff !important;
                    border: {border} !important;
                    border-radius: 999px !important;
                    font-weight: {"700" if is_active else "500"} !important;
                }}
                """
            )
        style_rules.append(
            """
            .st-key-filter_clear button {
                border-radius: 999px !important;
            }
            """
        )
        st.markdown(f"<style>{''.join(style_rules)}</style>", unsafe_allow_html=True)

        btn_cols = st.columns(len(active_factions) + 1)
        for i, fkey in enumerate(active_factions):
            with btn_cols[i]:
                is_active = highlight == fkey
                short_name = tl.FACTIONS[fkey]["name"].split(" (")[0]
                if st.button(short_name, key=f"filter_{fkey}", use_container_width=True):
                    st.session_state.highlight_faction = None if is_active else fkey
                    st.rerun()
        with btn_cols[-1]:
            if st.button("전체 보기", key="filter_clear", use_container_width=True):
                st.session_state.highlight_faction = None
                st.rerun()

    with st.expander("지방별 기본색 안내 (세력 미지정 지역)", expanded=False):
        region_legend_html = " ".join(
            f'<span class="faction-chip" style="background-color:{info["color"]}; opacity:0.7">{info["name"]}</span>'
            for info in prov.REGIONS.values()
        )
        st.markdown(region_legend_html, unsafe_allow_html=True)

    event = st.plotly_chart(
        fig, use_container_width=True, on_select="rerun", key="province_map", selection_mode="points"
    )
    if event and event.get("selection", {}).get("points"):
        point_index = event["selection"]["points"][0]["point_index"]
        st.session_state.selected_id = all_prov[point_index]["id"]

with col_info:
    sel = prov.get_province(st.session_state.selected_id)
    sel_faction_key = territories.get(sel["id"], "unknown")
    sel_faction = tl.FACTIONS[sel_faction_key]

    st.markdown(
        f"""
        <div class="province-card">
            <h3 style="margin-top:0">{sel['id']}. {sel['hanja']} ({sel['hangul']})</h3>
            <span class="faction-chip" style="background-color:{sel_faction['color']}">{sel_faction['name']}</span>
            <span class="faction-chip" style="background-color:#333">{sel['region_name']}</span>
            <p style="margin-top:10px;margin-bottom:4px;"><b>현대 지명:</b> {sel['modern']}</p>
            <p style="margin-top:0;">{sel['desc']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader(f"📝 {volume}권 메모 — {sel['hangul']}")

    with st.form(key="new_note_form", clear_on_submit=True):
        new_content = st.text_area("새 메모 작성", placeholder="이 권, 이 지역에서 있었던 사건이나 감상을 적어보세요.")
        submitted = st.form_submit_button("저장", use_container_width=True)
        if submitted and new_content.strip():
            add_note(volume, sel["id"], new_content.strip())
            st.success("메모가 저장되었습니다.")
            st.rerun()

    existing_notes = get_notes(volume=volume, province_id=sel["id"])
    if existing_notes:
        st.markdown(f"**기존 메모 ({len(existing_notes)}개)**")
        for note in existing_notes:
            with st.expander(f"{note['created_at']}", expanded=False):
                edited = st.text_area("내용", value=note["content"], key=f"edit_{note['id']}", label_visibility="collapsed")
                c1, c2 = st.columns(2)
                if c1.button("수정 저장", key=f"save_{note['id']}", use_container_width=True):
                    update_note(note["id"], edited)
                    st.success("수정되었습니다.")
                    st.rerun()
                if c2.button("삭제", key=f"del_{note['id']}", use_container_width=True):
                    delete_note(note["id"])
                    st.rerun()
    else:
        st.caption("이 권·지역에 대한 메모가 아직 없습니다.")

# ---------------------------------------------------------------------------
# 전체 메모 모아보기
# ---------------------------------------------------------------------------
st.divider()
with st.expander("📚 전체 메모 모아보기 & 다운로드", expanded=False):
    df = get_all_notes_df()
    if df.empty:
        st.caption("아직 작성된 메모가 없습니다.")
    else:
        display_df = df[["volume", "province", "content", "created_at"]].rename(
            columns={"volume": "권수", "province": "율령국", "content": "메모", "created_at": "작성일시"}
        )
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        csv_bytes = df.drop(columns=["province_id"]).to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "⬇ CSV 다운로드", data=csv_bytes, file_name="daemang_notes.csv", mime="text/csv"
        )

        md_lines = ["# 대망 독서노트 전체 메모\n"]
        for v in sorted(df["volume"].unique()):
            md_lines.append(f"\n## {v}권\n")
            vol_df = df[df["volume"] == v]
            for _, row in vol_df.iterrows():
                md_lines.append(f"- **{row['province']}** ({row['created_at']}): {row['content']}")
        md_bytes = "\n".join(md_lines).encode("utf-8")
        st.download_button(
            "⬇ Markdown 다운로드", data=md_bytes, file_name="daemang_notes.md", mime="text/markdown"
        )
