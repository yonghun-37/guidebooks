/* 선택한 원본 문서 하나만 재사용한다. 계산·도구 HTML의 사본을 만들지 않는다. */
(() => {
  'use strict';
  const picker = document.querySelector('#sim-picker');
  const frame = document.querySelector('#sim-frame');
  const original = document.querySelector('#sim-original');
  const tools = window.BlogCatalog;
  let observer;
  const selectedKey = new URL(location.href).searchParams.get('tool');
  if (tools.some(tool => `${tool.slug}:${tool.id}` === selectedKey)) picker.value = selectedKey;
  const applyTheme = () => {
    if (frame.contentDocument?.documentElement) frame.contentDocument.documentElement.dataset.theme = document.documentElement.dataset.theme;
  };
  const resize = () => {
    const doc = frame.contentDocument;
    if (!doc) return;
    frame.style.height = `${Math.ceil(doc.body.getBoundingClientRect().height) + 32}px`;
  };
  frame.addEventListener('load', () => {
    applyTheme();
    observer?.disconnect();
    observer = new ResizeObserver(resize);
    observer.observe(frame.contentDocument.body);
    resize();
  });
  const select = () => {
    const tool = tools.find(item => `${item.slug}:${item.id}` === picker.value) || tools[0];
    const path = `chapters/${tool.slug}.html`;
    original.href = `${path}#${tool.id}`;
    frame.title = `${tool.chapter}장 · ${tool.title}`;
    frame.src = `${path}?embed=${encodeURIComponent(tool.id)}`;
    frame.hidden = false;
    const locationUrl = new URL(location.href);
    locationUrl.searchParams.set('tool', `${tool.slug}:${tool.id}`);
    history.replaceState(null, '', locationUrl);
  };
  picker.addEventListener('change', select);
  new MutationObserver(applyTheme).observe(document.documentElement, {attributes: true, attributeFilter: ['data-theme']});
  select();
})();
