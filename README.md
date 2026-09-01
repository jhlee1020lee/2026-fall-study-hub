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

## Sponsors

<p align="center">
  <a href="https://github.com/sponsors/jackyzha0">
    <img src="https://cdn.jsdelivr.net/gh/jackyzha0/jackyzha0/sponsorkit/sponsors.svg" />
  </a>
</p>
