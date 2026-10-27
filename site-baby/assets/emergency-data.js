/* BRIEFING ④: 채택된 응급 문구의 유일한 원본. */
(function(root){
  const rows = [
  {
    "id": "fever",
    "text": "생후 3개월 미만 아기가 38.0℃ 이상이면, 상태가 좋아 보여도 즉시 응급실에서 진료받으세요.",
    "tier": "urgent",
    "sources": [
      "N001"
    ]
  },
  {
    "id": "breathing",
    "text": "숨을 쉬기 힘들어 하거나, 입술·혀가 파래지거나, 깨우기 어렵거나 평소처럼 반응하지 않거나, 경련하면 즉시 119에 연락하세요.",
    "tier": "call",
    "sources": [
      "N001",
      "N085",
      "N090"
    ]
  },
  {
    "id": "feeding",
    "text": "평소와 달리 잘 먹지 못하거나, 소변이 뚜렷하게 줄거나, 평소보다 처지면 지체하지 말고 진료받으세요.",
    "tier": "urgent",
    "sources": [
      "N001",
      "N090"
    ]
  },
  {
    "id": "jaundice",
    "text": "생후 첫날부터 노랗거나, 황달이 심해지거나 오래 지속되거나, 흰색·회백색 변을 보면 바로 의료진에게 알리고 진료받으세요. 잘 먹지 못하거나 처지면 지체하지 마세요.",
    "tier": "urgent",
    "sources": [
      "N003",
      "N031"
    ]
  },
  {
    "id": "vomit",
    "text": "초록색·노란색이나 피가 섞인 구토, 분수처럼 힘차게 뿜는 구토, 먹지 못하거나 처지는 구토는 즉시 진료받으세요.",
    "tier": "urgent",
    "sources": [
      "N060"
    ]
  },
  {
    "id": "navel",
    "text": "배꼽 주변이 붉어지거나, 만질 때 아파하거나, 고름·악취가 나면 진료받으세요. 피가 계속 나면 즉시 진료받으세요.",
    "tier": "urgent",
    "sources": [
      "N007"
    ]
  },
  {
    "id": "parent",
    "text": "나 자신이나 아기를 해칠 것 같으면 혼자 버티지 말고 즉시 다른 어른과 119·112에 도움을 요청하세요.",
    "tier": "call",
    "sources": [
      "N052",
      "N054"
    ]
  },
  {
    "id": "cold",
    "text": "영국 NHS는 체온이 36℃ 미만으로 낮은 경우도 응급 신호로 안내합니다. 5세 미만은 전자체온계로 겨드랑이에서 재도록 안내합니다. 36℃ 미만이거나 몸이 차고 평소와 다르면 즉시 응급의료 도움을 받으세요.",
    "tier": "urgent",
    "sources": [
      "N090",
      "N130"
    ]
  },
  {
    "id": "cry",
    "text": "울음이 매우 약하거나 날카롭게 달라지면 즉시 응급의료 도움을 받으세요.",
    "tier": "urgent",
    "sources": [
      "N026"
    ]
  },
  {
    "id": "rash",
    "text": "눌러도 옅어지지 않는 발진이 있으면 즉시 응급의료 도움을 받으세요.",
    "tier": "urgent",
    "sources": [
      "N001"
    ]
  }
];
  const data = Object.freeze(rows.map(row => Object.freeze({...row,sources:Object.freeze(row.sources)})));
  if(typeof module!=="undefined" && module.exports) module.exports=data;
  else root.BabyEmergency=data;
})(typeof window!=="undefined"?window:globalThis);
