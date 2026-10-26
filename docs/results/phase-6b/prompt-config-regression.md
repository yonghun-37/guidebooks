# F09 프롬프트 계정 이름 회귀 확인

깨끗한 복사본: `/tmp/reelsbook-practice-6b-2oy0a2xh/starter-kit`
설정: `config.yaml.account_name: 퇴근길 생활 실험`

## RED: 설정 누락

```
$ python write_copy.py output/my-news/news.json --mode prompt --template cards --output output/my-news/copy.json
웹 채팅에 붙여 넣을 프롬프트: output/my-news/prompt.md. 답변 JSON을 output/my-news/copy.json에 저장하고 --validate로 확인하세요.
prompt.md account_name: ['하린의 한 장 실험실']
exit 0; 기존 copy.json 내용 보존
```

## GREEN: 설정 명시

```
$ python write_copy.py output/my-news/news.json --mode prompt --template cards --output output/my-news/copy.json --config config.yaml
웹 채팅에 붙여 넣을 프롬프트: output/my-news/prompt.md. 답변 JSON을 output/my-news/copy.json에 저장하고 --validate로 확인하세요.
prompt.md account_name: ['퇴근길 생활 실험']
exit 0; 기존 copy.json 내용 보존
```
