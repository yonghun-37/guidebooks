# 실제 생성한 오프라인 샘플 — Phase 4b

모든 인물·사건·단체·링크는 **합성 데이터이며 실제 뉴스가 아닙니다.** 표지 1장·번호 본문 3장·마무리 1장의 PNG(1080×1350), 릴스 MP4(1080×1920, 24fps, 20초, H.264/AAC), 자막 SRT와 사용한 문안·피드 JSON을 동봉합니다. 카드·영상의 카드 하단에도 작은 합성 표시를 유지했습니다.

릴스는 장면별 페이드, 느린 줌/팬, 자막 페이드·슬라이드 등장, 전체 진행 막대를 포함합니다. **무음+자막** 기본 경로로 제작했으며 음성 합성·외부 LLM 호출은 하지 않았습니다. 모션을 추가해도 수익화 적격을 보장하지 않는 연습용 예제입니다. 직접 촬영·본인 내레이션 등 독창적 요소를 더해야 합니다([README](../README.md)).

2026-10-26, Ubuntu 22.04 x86_64 / Python 3.11.15 / pip 동봉 FFmpeg 7.0.2에서 생성했습니다. 저장소 루트 기준:

```bash
starter-kit/.venv/bin/python starter-kit/run_pipeline.py --offline --output starter-kit/output/phase-4b-final
```

`output/phase-4b-final/cards/*.png`, `reel.mp4`, `subtitles.srt`, `copy.json`, `news.json`을 이 폴더로 복사했습니다. 재현할 때는 새 출력 폴더 이름을 사용하세요. 운영체제에 맞는 가상환경 Python을 사용하면 됩니다. 검수·승인 기록·설정의 로컬 절대 경로·개인 음원은 샘플에 포함하지 않았습니다.

폴더 전체는 **약 1.6MB로 10MB 이하**입니다. 테스트가 전체 용량, PNG/MP4 규격, 실제 영상의 모션·장면 전환·무음 트랙을 확인합니다. [Phase 4b 결과와 검증](../../docs/results/phase-4b.md), [표지·본문·마무리 및 중간 프레임](../../docs/results/phase-4b/)도 참고하세요.

코드·합성 데이터·샘플의 이용 조건은 [MIT](../LICENSE), 폰트 소프트웨어는 [OFL](../assets/fonts/OFL.txt)입니다. 실제 뉴스·사진·음원을 추가하면 해당 자료의 이용 조건을 별도로 확인하세요. 이 동봉 합성 샘플은 live 게시 경로에서 거부합니다.
