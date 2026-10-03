# 🗾 대망(大望) 독서노트 — 68율령국 지도 기반 독서 노트 & 형세 변화 추적 웹앱

소설 《대망》(도쿠가와 이에야스, 전 36권) 독자를 위한 Streamlit 웹앱입니다.
일본의 68개 율령국(令制國) 지도를 바탕으로, 권수를 넘기면서 변하는 주요 다이묘 세력의
판도를 확인하고, 각 지역·권수별로 독서 메모를 남길 수 있습니다.

완전 무료 스택(Streamlit Community Cloud + SQLite)만으로 동작합니다.

## 주요 기능

- **권수 슬라이더 (1~36권)**: 권을 넘기면 해당 시기 연도와 주요 세력 판도가 지도에 반영됩니다.
- **인터랙티브 지도**: 68개 율령국을 점으로 표시, 클릭하면 우측 패널에 상세 정보가 표시됩니다.
- **검색**: 율령국 이름(한글/한자) 또는 번호로 빠르게 찾기.
- **독서 메모 CRUD**: 권수 + 율령국 단위로 메모를 작성/수정/삭제 (SQLite에 자동 저장).
- **전체 메모 모아보기**: 작성한 모든 메모를 표로 확인하고 CSV/Markdown으로 다운로드.
- **다크 모드** 기본 적용.

## 프로젝트 구조

```
.
├── app.py                 # Streamlit 메인 애플리케이션
├── provinces.py            # 68개 율령국 데이터 (번호/한자/한글/현대지명/좌표)
├── timeline_data.py         # 권수별 주요 세력 판도 데이터셋
├── requirements.txt
├── .streamlit/
│   └── config.toml          # 다크 테마 설정
└── README.md
```

실행 시 같은 폴더에 `daemang_notes.db` (SQLite) 파일이 자동으로 생성됩니다.

## 데이터에 대한 안내

- `provinces.py`의 좌표는 각 율령국의 **대략적인 중심 위치 근사치**로, 실제 행정구역 경계가
  아닌 지도 시각화용 참고 수치입니다.
- `timeline_data.py`의 권수별 세력 판도는 전국시대 실제 역사 흐름(오케하자마 → 나가시노 →
  혼노지의 변 → 세키가하라 → 오사카 전투 등)을 바탕으로 구성한 **근사치**입니다. 읽고 있는
  번역판의 권 구성과 다를 수 있으니, 필요하면 `timeline_data.py`의 `PERIODS` 리스트를 직접
  수정해 보고 있는 판본에 맞춰 조정하세요.

## 로컬에서 실행하기

```bash
pip install -r requirements.txt
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 이 자동으로 열립니다.

## GitHub 저장소 생성 및 Streamlit Community Cloud 무료 배포 가이드

### 1. GitHub 저장소 만들기

```bash
cd "대망_독서노트_프로젝트_폴더"
git init
git add app.py provinces.py timeline_data.py requirements.txt README.md .streamlit
git commit -m "Initial commit: 대망 독서노트 앱"
```

GitHub에서 새 저장소(예: `daemang-reading-notes`)를 생성한 뒤 연결하고 푸시합니다.

```bash
git branch -M main
git remote add origin https://github.com/<your-username>/daemang-reading-notes.git
git push -u origin main
```

> **참고**: `daemang_notes.db`는 로컬 실행 시 자동 생성되는 파일입니다. 저장소에는
> 커밋하지 않는 것을 권장합니다(`.gitignore`에 `*.db` 추가). Streamlit Community Cloud는
> 매 배포/재시작 시 파일 시스템이 초기화될 수 있어, 장기 보관이 필요한 메모는 주기적으로
> "전체 메모 모아보기"에서 CSV/Markdown으로 백업해두는 것을 권장합니다.

`.gitignore` 예시:

```
daemang_notes.db
__pycache__/
*.pyc
```

### 2. Streamlit Community Cloud 배포

1. https://share.streamlit.io 접속 후 GitHub 계정으로 로그인합니다.
2. **"New app"** 버튼 클릭.
3. 방금 만든 저장소(`<your-username>/daemang-reading-notes`)와 브랜치(`main`)를 선택합니다.
4. **Main file path**에 `app.py`를 입력합니다.
5. **Deploy** 버튼을 클릭하면 몇 분 안에 배포가 완료되고, 공개 URL
   (예: `https://daemang-reading-notes.streamlit.app`)이 발급됩니다.
6. 이후 GitHub `main` 브랜치에 새로운 커밋을 푸시하면 Streamlit Cloud가 자동으로 재배포합니다.

### 3. 배포 후 확인 사항

- 앱이 정상적으로 열리고 지도가 표시되는지 확인합니다.
- 지도의 점을 클릭했을 때 우측 패널에 정보가 바뀌는지 확인합니다.
- 메모 작성 후 새로고침해도 유지되는지 확인합니다 (단, Streamlit Cloud 재배포/슬립 후에는
  SQLite 파일이 초기화될 수 있다는 점에 유의하세요).

## 커스터마이징 팁

- 세력(다이묘) 색상·이름은 `timeline_data.py`의 `FACTIONS` 딕셔너리에서 수정할 수 있습니다.
- 새로운 권수 구간이나 세력 판도를 추가하려면 `PERIODS` 리스트에 항목을 추가하세요.
- 율령국 설명(`desc`)이나 현대 지명을 더 상세히 적고 싶다면 `provinces.py`의 `PROVINCES`
  딕셔너리를 편집하세요.
