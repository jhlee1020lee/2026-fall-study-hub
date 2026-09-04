# 2026 Fall Study Hub

Quartz 5 기반의 공개 학습 지식베이스입니다. 이 저장소에는 검토가 끝난 학습노트와 사이트 코드만 들어갑니다.

다음 자료는 절대 이 저장소에 커밋하지 않습니다.

- 강의 녹음과 영상
- 다글로 원시/정정 STT
- 수강생 명단
- 로컬 절대경로 또는 비공개 작업 파일
- 교수 제공 PDF/PPTX 원본(원본은 별도 GitHub Release로만 공개)

## 로컬 확인

```powershell
npm ci
npx quartz plugin install
python scripts/validate_public.py
npx quartz build --serve
```

노트 생성과 승인 명령은 상위 `snu_etl_downloader_portable` 프로젝트의 `study.ps1`을 사용합니다.

공개 검사와 로컬 승인 과정은 `scripts/note_validation.py`의 같은 품질 규칙을 사용합니다. frontmatter는 본문과 분리해 검사하며, 중복 키·지원하지 않는 YAML 문법은 오류로 처리합니다. 지원 형식은 단일 값과 문자열 목록입니다.

배포 전 회귀 검사는 다음 명령으로 실행합니다.

```powershell
python -m unittest discover -s scripts -p "test_*.py"
npm test
npx tsc --noEmit --incremental false
npx quartz build --output tmp/verification-build
python scripts/stage_page_cache_for_pages.py --public tmp/verification-build
python scripts/validate_links.py --public tmp/verification-build --site-base https://jhlee1020lee.github.io/2026-fall-study-hub --skip-release-assets
```

`--skip-release-assets`는 원본 Release 파일을 받지 않은 로컬 빌드에서만 사용합니다. 배포 CI는 원본을 내려받은 후 이 옵션 없이 페이지·이미지·스크립트 링크를 검사합니다. 운영체제는 보존 과목으로 취급하며, 수정 범위에서 제외된 기존 링크 세 건(과목 자료 링크 하나, PDF 추출문 태그 링크 둘)만 `scripts/public_validation_policy.json`에 명시되어 있습니다.

`python scripts/validate_public.py --index`는 실제 stage된 파일 내용을, `--revision HEAD`는 해당 commit의 내용을 검사합니다. 작업 폴더에서만 지운 비밀이 Git index나 commit에 남는 경우도 차단합니다. `.env`·인증 파일·원시 강의자료는 저장소 위치와 관계없이 금지하며, 키 문자열 검사는 사이트 본문 외 설정·코드에도 적용합니다. 환경설정 예제 파일에는 실제 키를 넣지 않습니다.

## PDF page cache

교수 제공 PDF 원본은 기존처럼 GitHub Release에만 둡니다. 조회용 캐시는 PDF별로 다음 위치에 커밋됩니다.

- 페이지 원문: `content/page_cache/<course>/<pdf>/page-001.md`
- PDF manifest: `content/page_cache/<course>/<pdf>/manifest.json`
- 페이지 이미지: `static/page_cache/<course>/<pdf>/page-001.png`

`Refresh PDF page cache` Action은 강의자료 목록이나 Release가 바뀌면 `pdftotext -layout`과 `pdftoppm`으로 변경된 PDF만 다시 처리하고, 삭제되거나 이름이 바뀐 PDF의 오래된 캐시는 정리합니다. 필요하면 Actions에서 수동 실행할 수 있습니다.

로컬에서 갱신하려면 Release 파일을 임시 폴더에 받은 뒤 다음을 실행합니다.

```powershell
python scripts/refresh_page_cache.py --pdf-root tmp/page-cache-releases --site-base https://jhlee1020lee.github.io/2026-fall-study-hub
```

## 운영체제 공개 강의자료 동기화

`Sync Operating Systems materials` Action은 교수 강의 사이트의 Schedule 표에서 Topic 열에 연결된 PDF만 수집합니다. 외부 교재 링크는 제외하며, 새 파일·변경 파일·이름이 바뀌거나 삭제된 파일을 운영체제 GitHub Release와 맞춘 뒤 위 PDF page cache 갱신을 실행합니다.

- 자동 확인: 2026-09-05 수강 철회 예정에 따라 중지
- 수동 확인: Actions → `Sync Operating Systems materials` → `Run workflow`
- 원본 설정: `scripts/external_course_sources/operating_systems.json`
- 동기화 상태: `scripts/external_course_state/operating_systems.json`

## Sponsors

<p align="center">
  <a href="https://github.com/sponsors/jackyzha0">
    <img src="https://cdn.jsdelivr.net/gh/jackyzha0/jackyzha0/sponsorkit/sponsors.svg" />
  </a>
</p>
