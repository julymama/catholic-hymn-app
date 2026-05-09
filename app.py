import streamlit as st
from PIL import Image
import pytesseract
import re
from urllib.parse import quote
import os

st.set_page_config(
    page_title="가톨릭 성가 테너 링크 생성기",
    page_icon="🎼",
    layout="wide"
)

st.title("🎼 가톨릭 성가 테너 링크 생성기")
st.caption("사진 업로드 → OCR 인식 → 유튜브 링크 자동 생성")

uploaded_file = st.file_uploader(
    "성가표 이미지를 업로드하세요",
    type=["png", "jpg", "jpeg"]
)

PART_NAMES = [
    "입당",
    "봉헌",
    "성체",
    "파견"
]

SPECIAL_NAMES = [
    "신앙의 신비여",
    "복음환호송"
]


def extract_hymns(text):
    lines = text.split("\n")
    results = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        numbers = re.findall(r"\d+", line)

        for part in PART_NAMES:
            if part in line:
                for num in numbers:
                    results.append((part, num))

        for special in SPECIAL_NAMES:
            if special in line:
                results.append((special, ""))

    return results


if uploaded_file:

    image = Image.open(uploaded_file)

    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption="업로드된 성가표")

    os.environ["TESSDATA_PREFIX"] = "/opt/homebrew/share/tessdata/"
    text = pytesseract.image_to_string(image, lang="kor")

    hymns = extract_hymns(text)

    with col2:
        st.subheader("🎵 자동 인식 결과")

        if hymns:

            for part, num in hymns:

                if num:
                    query = f"가톨릭성가 {num} 테너"
                    url = f"https://www.youtube.com/results?search_query={quote(query)}"

                    st.markdown(f"### 🎼 {part} {num}")
                    st.markdown(
                        f"▶️ [가톨릭성가 {num}번 – 테너 파트]({url})"
                    )

                else:
                    query = f"{part} 테너"
                    url = f"https://www.youtube.com/results?search_query={quote(query)}"

                    st.markdown(f"### 🎼 {part}")
                    st.markdown(
                        f"▶️ [{part} – 테너 파트]({url})"
                    )

                st.markdown("---")

        else:
            st.warning("성가 번호를 찾지 못했습니다.")

    with st.expander("📄 OCR 원본 텍스트 보기"):
        st.text(text)
