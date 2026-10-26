# 실습 명령 검증

깨끗한 복사본: /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit

```
$ python --version
Python 3.11.15

exit 0
```

```
$ python run_pipeline.py --offline --output output/first-post
검수 대기: /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/output/first-post/REVIEW.md

exit 0
```

```
$ python write_copy.py output/first-post/news.json --mode prompt --template cards --output output/first-post/copy.json
웹 채팅에 붙여 넣을 프롬프트: output/first-post/prompt.md. 답변 JSON을 output/first-post/copy.json에 저장하고 --validate로 확인하세요.

exit 0
```

```
$ python write_copy.py output/first-post/news.json --validate --output output/first-post/copy.json
구조 검증 OK: output/first-post/copy.json (사실 확인은 사람이 해야 합니다)

exit 0
```

```
$ python run_pipeline.py render output/first-post
검수 대기: /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/output/first-post/REVIEW.md

exit 0
```

```
$ python run_pipeline.py --offline --config config.yaml --feed my-feed.xml --output output/my-news
검수 대기: /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/output/my-news/REVIEW.md

exit 0
```

```
$ python write_copy.py output/my-news/news.json --validate --output output/my-news/copy.json
구조 검증 OK: output/my-news/copy.json (사실 확인은 사람이 해야 합니다)

exit 0
```

```
$ python run_pipeline.py render output/my-news
검수 대기: /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/output/my-news/REVIEW.md

exit 0
```

```
$ python run_pipeline.py approve output/first-post
{
  "mode": "dry-run",
  "login": "Instagram Login",
  "authorization": "Bearer <REDACTED>",
  "requests": [
    {
      "step": "컨테이너 생성",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media",
      "params": {
        "image_url": "https://example.invalid/output/cards/card-01.jpg",
        "is_carousel_item": "true"
      },
      "save_as": "CHILD_1"
    },
    {
      "step": "상태 확인",
      "method": "GET",
      "endpoint": "https://graph.instagram.com/v26.0/{CHILD_1}",
      "params": {
        "fields": "status_code"
      },
      "until": "FINISHED"
    },
    {
      "step": "컨테이너 생성",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media",
      "params": {
        "image_url": "https://example.invalid/output/cards/card-02.jpg",
        "is_carousel_item": "true"
      },
      "save_as": "CHILD_2"
    },
    {
      "step": "상태 확인",
      "method": "GET",
      "endpoint": "https://graph.instagram.com/v26.0/{CHILD_2}",
      "params": {
        "fields": "status_code"
      },
      "until": "FINISHED"
    },
    {
      "step": "컨테이너 생성",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media",
      "params": {
        "image_url": "https://example.invalid/output/cards/card-03.jpg",
        "is_carousel_item": "true"
      },
      "save_as": "CHILD_3"
    },
    {
      "step": "상태 확인",
      "method": "GET",
      "endpoint": "https://graph.instagram.com/v26.0/{CHILD_3}",
      "params": {
        "fields": "status_code"
      },
      "until": "FINISHED"
    },
    {
      "step": "컨테이너 생성",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media",
      "params": {
        "image_url": "https://example.invalid/output/cards/card-04.jpg",
        "is_carousel_item": "true"
      },
      "save_as": "CHILD_4"
    },
    {
      "step": "상태 확인",
      "method": "GET",
      "endpoint": "https://graph.instagram.com/v26.0/{CHILD_4}",
      "params": {
        "fields": "status_code"
      },
      "until": "FINISHED"
    },
    {
      "step": "컨테이너 생성",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media",
      "params": {
        "image_url": "https://example.invalid/output/cards/card-05.jpg",
        "is_carousel_item": "true"
      },
      "save_as": "CHILD_5"
    },
    {
      "step": "상태 확인",
      "method": "GET",
      "endpoint": "https://graph.instagram.com/v26.0/{CHILD_5}",
      "params": {
        "fields": "status_code"
      },
      "until": "FINISHED"
    },
    {
      "step": "컨테이너 생성",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media",
      "params": {
        "media_type": "CAROUSEL",
        "children": "{CHILD_1},{CHILD_2},{CHILD_3},{CHILD_4},{CHILD_5}",
        "caption": "합성 데이터 · 실제 뉴스 아님\n가상 별빛도서관, 조용한 독서 모임을 열다\nhttps://example.invalid/library\n가상 초록작업실, 종이 재사용 실험을 시작하다\nhttps://example.invalid/paper\n가상 달빛마을, 산책 지도를 함께 그리다\nhttps://example.invalid/walk",
        "is_ai_generated": "false"
      },
      "save_as": "CAROUSEL"
    },
    {
      "step": "상태 확인",
      "method": "GET",
      "endpoint": "https://graph.instagram.com/v26.0/{CAROUSEL}",
      "params": {
        "fields": "status_code"
      },
      "until": "FINISHED"
    },
    {
      "step": "게시",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media_publish",
      "params": {
        "creation_id": "{CAROUSEL}"
      },
      "save_as": "CAROUSEL_MEDIA"
    },
    {
      "step": "컨테이너 생성",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media",
      "params": {
        "media_type": "REELS",
        "video_url": "https://example.invalid/output/reel.mp4",
        "caption": "합성 데이터 · 실제 뉴스 아님\n가상 별빛도서관, 조용한 독서 모임을 열다\nhttps://example.invalid/library\n가상 초록작업실, 종이 재사용 실험을 시작하다\nhttps://example.invalid/paper\n가상 달빛마을, 산책 지도를 함께 그리다\nhttps://example.invalid/walk",
        "is_ai_generated": "false"
      },
      "save_as": "REEL"
    },
    {
      "step": "상태 확인",
      "method": "GET",
      "endpoint": "https://graph.instagram.com/v26.0/{REEL}",
      "params": {
        "fields": "status_code"
      },
      "until": "FINISHED"
    },
    {
      "step": "게시",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media_publish",
      "params": {
        "creation_id": "{REEL}"
      },
      "save_as": "REEL_MEDIA"
    }
  ]
}

exit 0
```

```
$ python publish.py output/first-post
{
  "mode": "dry-run",
  "login": "Instagram Login",
  "authorization": "Bearer <REDACTED>",
  "requests": [
    {
      "step": "컨테이너 생성",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media",
      "params": {
        "image_url": "https://example.invalid/output/cards/card-01.jpg",
        "is_carousel_item": "true"
      },
      "save_as": "CHILD_1"
    },
    {
      "step": "상태 확인",
      "method": "GET",
      "endpoint": "https://graph.instagram.com/v26.0/{CHILD_1}",
      "params": {
        "fields": "status_code"
      },
      "until": "FINISHED"
    },
    {
      "step": "컨테이너 생성",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media",
      "params": {
        "image_url": "https://example.invalid/output/cards/card-02.jpg",
        "is_carousel_item": "true"
      },
      "save_as": "CHILD_2"
    },
    {
      "step": "상태 확인",
      "method": "GET",
      "endpoint": "https://graph.instagram.com/v26.0/{CHILD_2}",
      "params": {
        "fields": "status_code"
      },
      "until": "FINISHED"
    },
    {
      "step": "컨테이너 생성",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media",
      "params": {
        "image_url": "https://example.invalid/output/cards/card-03.jpg",
        "is_carousel_item": "true"
      },
      "save_as": "CHILD_3"
    },
    {
      "step": "상태 확인",
      "method": "GET",
      "endpoint": "https://graph.instagram.com/v26.0/{CHILD_3}",
      "params": {
        "fields": "status_code"
      },
      "until": "FINISHED"
    },
    {
      "step": "컨테이너 생성",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media",
      "params": {
        "image_url": "https://example.invalid/output/cards/card-04.jpg",
        "is_carousel_item": "true"
      },
      "save_as": "CHILD_4"
    },
    {
      "step": "상태 확인",
      "method": "GET",
      "endpoint": "https://graph.instagram.com/v26.0/{CHILD_4}",
      "params": {
        "fields": "status_code"
      },
      "until": "FINISHED"
    },
    {
      "step": "컨테이너 생성",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media",
      "params": {
        "image_url": "https://example.invalid/output/cards/card-05.jpg",
        "is_carousel_item": "true"
      },
      "save_as": "CHILD_5"
    },
    {
      "step": "상태 확인",
      "method": "GET",
      "endpoint": "https://graph.instagram.com/v26.0/{CHILD_5}",
      "params": {
        "fields": "status_code"
      },
      "until": "FINISHED"
    },
    {
      "step": "컨테이너 생성",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media",
      "params": {
        "media_type": "CAROUSEL",
        "children": "{CHILD_1},{CHILD_2},{CHILD_3},{CHILD_4},{CHILD_5}",
        "caption": "합성 데이터 · 실제 뉴스 아님\n가상 별빛도서관, 조용한 독서 모임을 열다\nhttps://example.invalid/library\n가상 초록작업실, 종이 재사용 실험을 시작하다\nhttps://example.invalid/paper\n가상 달빛마을, 산책 지도를 함께 그리다\nhttps://example.invalid/walk",
        "is_ai_generated": "false"
      },
      "save_as": "CAROUSEL"
    },
    {
      "step": "상태 확인",
      "method": "GET",
      "endpoint": "https://graph.instagram.com/v26.0/{CAROUSEL}",
      "params": {
        "fields": "status_code"
      },
      "until": "FINISHED"
    },
    {
      "step": "게시",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media_publish",
      "params": {
        "creation_id": "{CAROUSEL}"
      },
      "save_as": "CAROUSEL_MEDIA"
    },
    {
      "step": "컨테이너 생성",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media",
      "params": {
        "media_type": "REELS",
        "video_url": "https://example.invalid/output/reel.mp4",
        "caption": "합성 데이터 · 실제 뉴스 아님\n가상 별빛도서관, 조용한 독서 모임을 열다\nhttps://example.invalid/library\n가상 초록작업실, 종이 재사용 실험을 시작하다\nhttps://example.invalid/paper\n가상 달빛마을, 산책 지도를 함께 그리다\nhttps://example.invalid/walk",
        "is_ai_generated": "false"
      },
      "save_as": "REEL"
    },
    {
      "step": "상태 확인",
      "method": "GET",
      "endpoint": "https://graph.instagram.com/v26.0/{REEL}",
      "params": {
        "fields": "status_code"
      },
      "until": "FINISHED"
    },
    {
      "step": "게시",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media_publish",
      "params": {
        "creation_id": "{REEL}"
      },
      "save_as": "REEL_MEDIA"
    }
  ]
}

exit 0
```

```
$ python prepare_hosting.py output/first-post --dest hosting/first-post
공개 준비 완료: 6개 JPEG/MP4 → /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/hosting/first-post
작은 비민감 교육 실습용입니다. 합성 자료를 실제 뉴스로 게시하지 마세요.
1. 본인 GitHub의 별도 공개 저장소에서 Add file > Upload files를 엽니다.
2. 이 폴더 안 cards 폴더와 reel.mp4를 함께 드래그 앤 드롭하고 Commit changes로 저장합니다.
3. Settings > Pages > Build and deployment > Source: Deploy from a branch에서 branch와 /(root)를 선택합니다.
4. 배포 완료 후 로그인하지 않은 창에서 파일 자체가 열리는지 확인합니다.
기본 URL 규칙: https://사용자.github.io/저장소 (하위 폴더에 올렸다면 그 경로까지)
파일 URL: <기본 URL>/cards/card-01.jpg 및 <기본 URL>/reel.mp4
미리보기: python publish.py "/tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/output/first-post" --base-url "<기본 URL>"
실제 2개 게시 시도: python publish.py "/tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/output/first-post" --live --base-url "<기본 URL>"
.env·토큰·검수/설정 파일은 복사하지 않습니다. Pages 이용정책·Meta 파일 수신은 별도 확인하세요.

exit 0
```

```
$ python run_pipeline.py approve output/my-news
{
  "mode": "dry-run",
  "login": "Instagram Login",
  "authorization": "Bearer <REDACTED>",
  "requests": [
    {
      "step": "컨테이너 생성",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media",
      "params": {
        "image_url": "https://example.invalid/output/cards/card-01.jpg",
        "is_carousel_item": "true"
      },
      "save_as": "CHILD_1"
    },
    {
      "step": "상태 확인",
      "method": "GET",
      "endpoint": "https://graph.instagram.com/v26.0/{CHILD_1}",
      "params": {
        "fields": "status_code"
      },
      "until": "FINISHED"
    },
    {
      "step": "컨테이너 생성",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media",
      "params": {
        "image_url": "https://example.invalid/output/cards/card-02.jpg",
        "is_carousel_item": "true"
      },
      "save_as": "CHILD_2"
    },
    {
      "step": "상태 확인",
      "method": "GET",
      "endpoint": "https://graph.instagram.com/v26.0/{CHILD_2}",
      "params": {
        "fields": "status_code"
      },
      "until": "FINISHED"
    },
    {
      "step": "컨테이너 생성",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media",
      "params": {
        "image_url": "https://example.invalid/output/cards/card-03.jpg",
        "is_carousel_item": "true"
      },
      "save_as": "CHILD_3"
    },
    {
      "step": "상태 확인",
      "method": "GET",
      "endpoint": "https://graph.instagram.com/v26.0/{CHILD_3}",
      "params": {
        "fields": "status_code"
      },
      "until": "FINISHED"
    },
    {
      "step": "컨테이너 생성",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media",
      "params": {
        "media_type": "CAROUSEL",
        "children": "{CHILD_1},{CHILD_2},{CHILD_3}",
        "caption": "합성 데이터 · 실제 뉴스 아님\n가상 별빛도서관, 조용한 독서 모임을 열다\nhttps://example.invalid/library",
        "is_ai_generated": "false"
      },
      "save_as": "CAROUSEL"
    },
    {
      "step": "상태 확인",
      "method": "GET",
      "endpoint": "https://graph.instagram.com/v26.0/{CAROUSEL}",
      "params": {
        "fields": "status_code"
      },
      "until": "FINISHED"
    },
    {
      "step": "게시",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media_publish",
      "params": {
        "creation_id": "{CAROUSEL}"
      },
      "save_as": "CAROUSEL_MEDIA"
    },
    {
      "step": "컨테이너 생성",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media",
      "params": {
        "media_type": "REELS",
        "video_url": "https://example.invalid/output/reel.mp4",
        "caption": "합성 데이터 · 실제 뉴스 아님\n가상 별빛도서관, 조용한 독서 모임을 열다\nhttps://example.invalid/library",
        "is_ai_generated": "false"
      },
      "save_as": "REEL"
    },
    {
      "step": "상태 확인",
      "method": "GET",
      "endpoint": "https://graph.instagram.com/v26.0/{REEL}",
      "params": {
        "fields": "status_code"
      },
      "until": "FINISHED"
    },
    {
      "step": "게시",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media_publish",
      "params": {
        "creation_id": "{REEL}"
      },
      "save_as": "REEL_MEDIA"
    }
  ]
}

exit 0
```

```
$ python publish.py output/my-news
{
  "mode": "dry-run",
  "login": "Instagram Login",
  "authorization": "Bearer <REDACTED>",
  "requests": [
    {
      "step": "컨테이너 생성",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media",
      "params": {
        "image_url": "https://example.invalid/output/cards/card-01.jpg",
        "is_carousel_item": "true"
      },
      "save_as": "CHILD_1"
    },
    {
      "step": "상태 확인",
      "method": "GET",
      "endpoint": "https://graph.instagram.com/v26.0/{CHILD_1}",
      "params": {
        "fields": "status_code"
      },
      "until": "FINISHED"
    },
    {
      "step": "컨테이너 생성",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media",
      "params": {
        "image_url": "https://example.invalid/output/cards/card-02.jpg",
        "is_carousel_item": "true"
      },
      "save_as": "CHILD_2"
    },
    {
      "step": "상태 확인",
      "method": "GET",
      "endpoint": "https://graph.instagram.com/v26.0/{CHILD_2}",
      "params": {
        "fields": "status_code"
      },
      "until": "FINISHED"
    },
    {
      "step": "컨테이너 생성",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media",
      "params": {
        "image_url": "https://example.invalid/output/cards/card-03.jpg",
        "is_carousel_item": "true"
      },
      "save_as": "CHILD_3"
    },
    {
      "step": "상태 확인",
      "method": "GET",
      "endpoint": "https://graph.instagram.com/v26.0/{CHILD_3}",
      "params": {
        "fields": "status_code"
      },
      "until": "FINISHED"
    },
    {
      "step": "컨테이너 생성",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media",
      "params": {
        "media_type": "CAROUSEL",
        "children": "{CHILD_1},{CHILD_2},{CHILD_3}",
        "caption": "합성 데이터 · 실제 뉴스 아님\n가상 별빛도서관, 조용한 독서 모임을 열다\nhttps://example.invalid/library",
        "is_ai_generated": "false"
      },
      "save_as": "CAROUSEL"
    },
    {
      "step": "상태 확인",
      "method": "GET",
      "endpoint": "https://graph.instagram.com/v26.0/{CAROUSEL}",
      "params": {
        "fields": "status_code"
      },
      "until": "FINISHED"
    },
    {
      "step": "게시",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media_publish",
      "params": {
        "creation_id": "{CAROUSEL}"
      },
      "save_as": "CAROUSEL_MEDIA"
    },
    {
      "step": "컨테이너 생성",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media",
      "params": {
        "media_type": "REELS",
        "video_url": "https://example.invalid/output/reel.mp4",
        "caption": "합성 데이터 · 실제 뉴스 아님\n가상 별빛도서관, 조용한 독서 모임을 열다\nhttps://example.invalid/library",
        "is_ai_generated": "false"
      },
      "save_as": "REEL"
    },
    {
      "step": "상태 확인",
      "method": "GET",
      "endpoint": "https://graph.instagram.com/v26.0/{REEL}",
      "params": {
        "fields": "status_code"
      },
      "until": "FINISHED"
    },
    {
      "step": "게시",
      "method": "POST",
      "endpoint": "https://graph.instagram.com/v26.0/<IG_USER_ID>/media_publish",
      "params": {
        "creation_id": "{REEL}"
      },
      "save_as": "REEL_MEDIA"
    }
  ]
}

exit 0
```

```
$ python prepare_hosting.py output/my-news --dest hosting/my-news
공개 준비 완료: 4개 JPEG/MP4 → /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/hosting/my-news
작은 비민감 교육 실습용입니다. 합성 자료를 실제 뉴스로 게시하지 마세요.
1. 본인 GitHub의 별도 공개 저장소에서 Add file > Upload files를 엽니다.
2. 이 폴더 안 cards 폴더와 reel.mp4를 함께 드래그 앤 드롭하고 Commit changes로 저장합니다.
3. Settings > Pages > Build and deployment > Source: Deploy from a branch에서 branch와 /(root)를 선택합니다.
4. 배포 완료 후 로그인하지 않은 창에서 파일 자체가 열리는지 확인합니다.
기본 URL 규칙: https://사용자.github.io/저장소 (하위 폴더에 올렸다면 그 경로까지)
파일 URL: <기본 URL>/cards/card-01.jpg 및 <기본 URL>/reel.mp4
미리보기: python publish.py "/tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/output/my-news" --base-url "<기본 URL>"
실제 2개 게시 시도: python publish.py "/tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/output/my-news" --live --base-url "<기본 URL>"
.env·토큰·검수/설정 파일은 복사하지 않습니다. Pages 이용정책·Meta 파일 수신은 별도 확인하세요.

exit 0
```

```
$ python -c import imageio_ffmpeg,subprocess; subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-f','lavfi','-i','sine=frequency=440:duration=2','my-voice.m4a'],check=True)
ffmpeg version 7.0.2-static https://johnvansickle.com/ffmpeg/  Copyright (c) 2000-2024 the FFmpeg developers
  built with gcc 8 (Debian 8.3.0-6)
  configuration: --enable-gpl --enable-version3 --enable-static --disable-debug --disable-ffplay --disable-indev=sndio --disable-outdev=sndio --cc=gcc --enable-fontconfig --enable-frei0r --enable-gnutls --enable-gmp --enable-libgme --enable-gray --enable-libaom --enable-libfribidi --enable-libass --enable-libvmaf --enable-libfreetype --enable-libmp3lame --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-librubberband --enable-libsoxr --enable-libspeex --enable-libsrt --enable-libvorbis --enable-libopus --enable-libtheora --enable-libvidstab --enable-libvo-amrwbenc --enable-libvpx --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxml2 --enable-libdav1d --enable-libxvid --enable-libzvbi --enable-libzimg
  libavutil      59.  8.100 / 59.  8.100
  libavcodec     61.  3.100 / 61.  3.100
  libavformat    61.  1.100 / 61.  1.100
  libavdevice    61.  1.100 / 61.  1.100
  libavfilter    10.  1.100 / 10.  1.100
  libswscale      8.  1.100 /  8.  1.100
  libswresample   5.  1.100 /  5.  1.100
  libpostproc    58.  1.100 / 58.  1.100
Input #0, lavfi, from 'sine=frequency=440:duration=2':
  Duration: N/A, start: 0.000000, bitrate: 705 kb/s
  Stream #0:0: Audio: pcm_s16le, 44100 Hz, mono, s16, 705 kb/s
Stream mapping:
  Stream #0:0 -> #0:0 (pcm_s16le (native) -> aac (native))
Press [q] to stop, [?] for help
Output #0, ipod, to 'my-voice.m4a':
  Metadata:
    encoder         : Lavf61.1.100
  Stream #0:0: Audio: aac (LC) (mp4a / 0x6134706D), 44100 Hz, mono, fltp, 69 kb/s
      Metadata:
        encoder         : Lavc61.3.100 aac
[out#0/ipod @ 0x16420a40] video:0KiB audio:17KiB subtitle:0KiB other streams:0KiB global headers:0KiB muxing overhead: 6.568349%
size=      18KiB time=00:00:02.00 bitrate=  75.2kbits/s speed=70.3x    
[aac @ 0x16421c00] Qavg: 851.020

exit 0
```

```
$ python -c import imageio_ffmpeg,subprocess; subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-i','my-voice.m4a','-vn','-c:a','pcm_s16le','my-voice.wav'],check=True)
ffmpeg version 7.0.2-static https://johnvansickle.com/ffmpeg/  Copyright (c) 2000-2024 the FFmpeg developers
  built with gcc 8 (Debian 8.3.0-6)
  configuration: --enable-gpl --enable-version3 --enable-static --disable-debug --disable-ffplay --disable-indev=sndio --disable-outdev=sndio --cc=gcc --enable-fontconfig --enable-frei0r --enable-gnutls --enable-gmp --enable-libgme --enable-gray --enable-libaom --enable-libfribidi --enable-libass --enable-libvmaf --enable-libfreetype --enable-libmp3lame --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-librubberband --enable-libsoxr --enable-libspeex --enable-libsrt --enable-libvorbis --enable-libopus --enable-libtheora --enable-libvidstab --enable-libvo-amrwbenc --enable-libvpx --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxml2 --enable-libdav1d --enable-libxvid --enable-libzvbi --enable-libzimg
  libavutil      59.  8.100 / 59.  8.100
  libavcodec     61.  3.100 / 61.  3.100
  libavformat    61.  1.100 / 61.  1.100
  libavdevice    61.  1.100 / 61.  1.100
  libavfilter    10.  1.100 / 10.  1.100
  libswscale      8.  1.100 /  8.  1.100
  libswresample   5.  1.100 /  5.  1.100
  libpostproc    58.  1.100 / 58.  1.100
Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'my-voice.m4a':
  Metadata:
    major_brand     : M4A 
    minor_version   : 512
    compatible_brands: M4A isomiso2
    encoder         : Lavf61.1.100
  Duration: 00:00:02.00, start: 0.000000, bitrate: 75 kb/s
  Stream #0:0[0x1](und): Audio: aac (LC) (mp4a / 0x6134706D), 44100 Hz, mono, fltp, 69 kb/s (default)
      Metadata:
        handler_name    : SoundHandler
        vendor_id       : [0][0][0][0]
Stream mapping:
  Stream #0:0 -> #0:0 (aac (native) -> pcm_s16le (native))
Press [q] to stop, [?] for help
Output #0, wav, to 'my-voice.wav':
  Metadata:
    major_brand     : M4A 
    minor_version   : 512
    compatible_brands: M4A isomiso2
    ISFT            : Lavf61.1.100
  Stream #0:0(und): Audio: pcm_s16le ([1][0][0][0] / 0x0001), 44100 Hz, mono, s16, 705 kb/s (default)
      Metadata:
        handler_name    : SoundHandler
        vendor_id       : [0][0][0][0]
        encoder         : Lavc61.3.100 pcm_s16le
[out#0/wav @ 0x1d8b2640] video:0KiB audio:174KiB subtitle:0KiB other streams:0KiB global headers:0KiB muxing overhead: 0.043777%
size=     174KiB time=00:00:02.02 bitrate= 705.9kbits/s speed= 699x    

exit 0
```

```
$ python schedule_setup.py --os windows --time 09:00 --config config.yaml --feed my-feed.xml
안내만 생성했습니다. 아래 등록 명령은 직접 확인한 뒤 실행하세요.
컴퓨터의 현지 시간 기준이며 컴퓨터가 켜져 있어야 합니다. 생성 후 검수 대기에서 멈춥니다.
로그: /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/output/daily/daily.log
기존 날짜 폴더는 덮어쓰지 않습니다. 로그의 오류와 날짜별 REVIEW.md를 확인하세요.
PowerShell에서 cmd.exe를 입력해 명령 프롬프트로 바꾼 뒤 아래 명령을 실행하세요.
등록 (같은 이름의 기존 작업은 자동 교체하지 않습니다):
schtasks /Create /SC DAILY /ST 09:00 /TN ReelsBookDaily /TR "/tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/.venv/bin/python /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/daily.py --config /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/config.yaml --output-root /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/output/daily --log /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/output/daily/daily.log --feed /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/my-feed.xml"
확인:
schtasks /Query /TN ReelsBookDaily /V /FO LIST
수동 실행 (오늘 폴더가 이미 있으면 중복 오류가 정상입니다):
schtasks /Run /TN ReelsBookDaily
삭제:
schtasks /Delete /TN ReelsBookDaily


exit 0
```

```
$ python schedule_setup.py --os macos --time 09:00 --config config.yaml --feed my-feed.xml
안내만 생성했습니다. 아래 등록 명령은 직접 확인한 뒤 실행하세요.
컴퓨터의 현지 시간 기준이며 컴퓨터가 켜져 있어야 합니다. 생성 후 검수 대기에서 멈춥니다.
로그: /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/output/daily/daily.log
기존 날짜 폴더는 덮어쓰지 않습니다. 로그의 오류와 날짜별 REVIEW.md를 확인하세요.
등록: crontab -e 를 열고 아래 한 줄만 추가해 저장하세요.
0 9 * * * /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/.venv/bin/python /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/daily.py --config /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/config.yaml --output-root /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/output/daily --log /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/output/daily/daily.log --feed /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/my-feed.xml
확인:
crontab -l
수동 실행 (터미널에 붙여넣기):
/tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/.venv/bin/python /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/daily.py --config /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/config.yaml --output-root /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/output/daily --log /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/output/daily/daily.log --feed /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/my-feed.xml
삭제: crontab -e 를 열어 위 ReelsBook daily.py 실행 줄만 지우고 저장하세요.
다른 예약은 유지하세요. macOS에서 권한 오류가 나면 시스템 설정의 개인정보 보호에서 터미널 권한을 확인하세요.


exit 0
```

```
$ python schedule_setup.py --os linux --time 09:00 --config config.yaml --feed my-feed.xml
안내만 생성했습니다. 아래 등록 명령은 직접 확인한 뒤 실행하세요.
컴퓨터의 현지 시간 기준이며 컴퓨터가 켜져 있어야 합니다. 생성 후 검수 대기에서 멈춥니다.
로그: /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/output/daily/daily.log
기존 날짜 폴더는 덮어쓰지 않습니다. 로그의 오류와 날짜별 REVIEW.md를 확인하세요.
등록: crontab -e 를 열고 아래 한 줄만 추가해 저장하세요.
0 9 * * * /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/.venv/bin/python /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/daily.py --config /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/config.yaml --output-root /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/output/daily --log /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/output/daily/daily.log --feed /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/my-feed.xml
확인:
crontab -l
수동 실행 (터미널에 붙여넣기):
/tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/.venv/bin/python /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/daily.py --config /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/config.yaml --output-root /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/output/daily --log /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/output/daily/daily.log --feed /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/my-feed.xml
삭제: crontab -e 를 열어 위 ReelsBook daily.py 실행 줄만 지우고 저장하세요.
다른 예약은 유지하세요. macOS에서 권한 오류가 나면 시스템 설정의 개인정보 보호에서 터미널 권한을 확인하세요.


exit 0
```

```
$ python daily.py --config config.yaml --feed my-feed.xml --date 2026-10-27 --output-root output/daily-rehearsal
검수 대기: /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/output/daily-rehearsal/2026-10-27/REVIEW.md

exit 0
```

```
$ python daily.py --config config.yaml --feed my-feed.xml --date 2026-10-27 --log output/daily/daily.log

exit 0
```

동일 날짜 재실행: exit 1; 오류: 이미 있는 날짜 폴더입니다: /tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit/output/daily/2026-10-27. 덮어쓰지 않았습니다. REVIEW.md를 확인하거나 예행연습은 --date 다른날짜 또는 --output-root 다른폴더를 사용하세요.

```
$ python -c import io;from unittest.mock import patch;import token_check;response=io.BytesIO(b'{"user_id":"123456789012345","username":"my_example_account"}');
with patch.object(token_check,'urlopen',return_value=response),patch.object(token_check,'getpass',return_value='TEST_SECRET'):token_check.main()
user_id: 123456789012345
username: my_example_account

exit 0
```

