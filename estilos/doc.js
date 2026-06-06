/* doc.js · Prompt Amplificado · interacción compartida · homólogo a Jarvis OS runbook/playbook */
(function(){
  var html=document.documentElement;
  /* persisted theme + lang */
  try{var t=localStorage.getItem('mdg_theme');if(t==='dark')html.dataset.theme='dark';var l=localStorage.getItem('mdg_locale');if(l==='en'||l==='pt')html.lang=l;}catch(e){}
  var langs=['es','en','pt'];
  function setLang(l){if(langs.indexOf(l)<0)l='es';html.lang=l;try{localStorage.setItem('mdg_locale',l)}catch(e){}var lb=document.getElementById('langbtn');if(lb)lb.textContent=l.toUpperCase();}
  function setTheme(v){html.dataset.theme=v;try{localStorage.setItem('mdg_theme',v)}catch(e){}var tb=document.getElementById('theme');if(tb)tb.textContent=v==='dark'?'☀':'☾';}
  document.addEventListener('DOMContentLoaded',function(){
    setLang(html.lang||'es');
    var tb=document.getElementById('theme'); if(tb){tb.textContent=html.dataset.theme==='dark'?'☀':'☾';tb.onclick=function(){setTheme(html.dataset.theme==='dark'?'light':'dark')};}
    var lb=document.getElementById('langbtn'); if(lb)lb.onclick=function(){var i=langs.indexOf(html.lang);setLang(langs[(i+1)%langs.length]);};
    /* reading progress */
    var rp=document.querySelector('.reading-progress');
    if(rp)window.addEventListener('scroll',function(){var h=document.documentElement;var sc=(h.scrollTop)/((h.scrollHeight-h.clientHeight)||1);rp.style.width=(sc*100)+'%';},{passive:true});
    /* sidebar lateral homologado */
    try{ buildSidebar(); initSpy(); loadLucide(); }catch(e){}
  });

  /* ---- Lucide icons (CDN) ---- */
  function loadLucide(){
    function draw(){ if(window.lucide&&lucide.createIcons) lucide.createIcons(); }
    if(window.lucide){ draw(); return; }
    if(document.getElementById('lucide-cdn')){ return; }
    var s=document.createElement('script'); s.id='lucide-cdn'; s.defer=true;
    s.src='https://unpkg.com/lucide@0.469.0/dist/umd/lucide.js';
    s.onload=draw; document.head.appendChild(s);
  }
  /* ---- sidebar builder ---- */
  function slugify(s){return (s||'').normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/§\s*\d+/,'').replace(/[^a-z0-9]+/gi,'-').replace(/^-+|-+$/g,'').toLowerCase().slice(0,40);}
  function iconFor(txt){
    var t=(txt||'').toLowerCase();
    var map=[['hub','home'],['inicio','home'],['hero','home'],['empez','rocket'],['experiencia','compass'],
      ['catálogo','library'],['catalog','library'],['cómo crear','pen-tool'],['crear','pen-tool'],['create','pen-tool'],
      ['estándar','shield-check'],['standard','shield-check'],['concepto','layers'],['concept','layers'],
      ['cómo','list-checks'],['how','list-checks'],['usar','list-checks'],['qué es','info'],['what','info'],
      ['masterclass','graduation-cap'],['workbook','notebook-pen'],['playbook','book-open'],['runbook','route'],
      ['prompt','terminal'],['contexto','database'],['context','database'],['harness','cpu'],['arnés','cpu'],
      ['meta','wand-2'],['material','folder'],['contact','mail'],['format','grid-2x2'],['natural','message-square'],
      ['par','sliders-horizontal'],['spec','file-cog'],['dupla','bot']];
    for(var i=0;i<map.length;i++){ if(t.indexOf(map[i][0])>=0) return map[i][1]; }
    return 'file-text';
  }
  function labelHTML(h){
    var c=h.cloneNode(true);
    [].forEach.call(c.querySelectorAll('.num'),function(n){n.remove();});
    var html=c.innerHTML.trim();
    return html||c.textContent.trim();
  }
  function buildSidebar(){
    if(document.querySelector('.sidebar-nav')) return;
    var root=document.querySelector('main')||document.body;
    var items=[];
    [].forEach.call(root.querySelectorAll('section'),function(s){
      if(s.closest('dialog')) return;
      var h=s.querySelector('h1,h2'); if(!h) return;
      var base=(h.querySelector('.l-es')||h).textContent.replace(/§\s*\d+/,'').trim();
      if(!s.id) s.id=slugify(base)||('sec'+items.length);
      items.push({id:s.id,h:h,base:base});
    });
    if(items.length<2) return;
    var nav=document.createElement('nav'); nav.className='sidebar-nav'; nav.setAttribute('aria-label','Navegación por secciones');
    var logo=document.createElement('div'); logo.className='sidebar-logo';
    logo.innerHTML='<svg viewBox="0 0 36 36" aria-label="MetodologIA"><defs><linearGradient id="sbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#122562"/><stop offset="1" stop-color="#1a3580"/></linearGradient></defs><rect width="36" height="36" rx="10" fill="url(#sbg)"/><rect x="10" y="12" width="4" height="12" rx=".5" fill="#fff"/><rect x="16" y="12" width="4" height="8" rx=".5" fill="#fff"/><rect x="16" y="22" width="4" height="2" rx=".5" fill="#fff"/><rect x="22" y="12" width="4" height="6" rx=".5" fill="#fff"/><rect x="22" y="20" width="4" height="4" rx=".5" fill="#fff"/><circle cx="18" cy="8" r="2" fill="#FFD700"/></svg>';
    nav.appendChild(logo);
    var links=document.createElement('div'); links.className='sidebar-links';
    items.forEach(function(it){
      var a=document.createElement('a'); a.href='#'+it.id;
      a.setAttribute('aria-label', it.base);
      a.innerHTML='<i data-lucide="'+iconFor(it.base)+'"></i><span class="sb-label">'+labelHTML(it.h)+'</span>';
      a.addEventListener('click',function(e){e.preventDefault();var t=document.getElementById(it.id);if(t){t.scrollIntoView({behavior:'smooth',block:'start'});history.replaceState(null,'','#'+it.id);}});
      links.appendChild(a);
    });
    nav.appendChild(links);
    var bottom=document.createElement('div'); bottom.className='sidebar-bottom';
    bottom.innerHTML='<a href="https://metodologia.info" target="_blank" rel="noopener" aria-label="metodologia.info" title="metodologia.info"><img src="favicon.svg" alt="MetodologIA"><span class="sb-label">metodologia.info</span></a>';
    nav.appendChild(bottom);
    document.body.appendChild(nav);
    window.__sb={nav:nav,items:items};
  }
  function initSpy(){
    if(!window.__sb||!('IntersectionObserver' in window)) return;
    var links=document.querySelectorAll('.sidebar-links a');
    function setActive(id){ links.forEach(function(l){ l.classList.toggle('active', l.getAttribute('href')==='#'+id); }); }
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting) setActive(e.target.id); });
    },{rootMargin:'-30% 0px -60% 0px',threshold:0});
    window.__sb.items.forEach(function(it){ var el=document.getElementById(it.id); if(el) io.observe(el); });
  }

  /* ----- row-modal: click en fila con data-detail o data-modal ----- */
  function openRowModal(title,h){
    var m=document.getElementById('row-modal');if(!m)return;
    var t=m.querySelector('#row-modal-title');if(t)t.innerHTML=title||'Detalle';
    var b=m.querySelector('#row-modal-body');if(b)b.innerHTML=h||'';
    if(m.showModal)m.showModal();else m.setAttribute('open','');
  }
  document.addEventListener('click',function(e){
    /* close buttons / backdrop */
    if(e.target.matches('[data-close]')){var dlg=e.target.closest('dialog');if(dlg)dlg.close();return;}
    var dial=e.target.closest('dialog.smodal');
    if(dial&&e.target===dial){dial.close();return;}
    if(e.target.closest('a,button,input,label,.codebox,.prompt-copyable'))return;
    var tr=e.target.closest('tr');if(!tr)return;
    var mid=tr.getAttribute('data-modal');
    if(mid){var d=document.getElementById(mid);if(d){if(d.showModal)d.showModal();else d.setAttribute('open','');}return;}
    var det=tr.getAttribute('data-detail');
    if(det){openRowModal(tr.getAttribute('data-title')||'Detalle',det);}
  });

  /* ----- prompts copiables ----- */
  function visiblePre(box){
    var lang=document.documentElement.lang||'es';
    return box.querySelector('.prompt-text.l-'+lang+',pre.l-'+lang)||box.querySelector('.prompt-text,pre');
  }
  window.copyPrompt=function(btn){
    var box=btn.closest('.prompt-copyable')||btn.closest('.codebox');if(!box)return;
    var pre=visiblePre(box);if(!pre)return;
    var tx=pre.textContent.trim();
    function flash(){var done={es:'Copiado ✓',en:'Copied ✓',pt:'Copiado ✓'}[document.documentElement.lang]||'Copiado ✓';var old=btn.textContent;btn.textContent=done;btn.classList.add('ok');setTimeout(function(){btn.textContent=old;btn.classList.remove('ok')},1600);}
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(tx).then(flash).catch(fb);}else{fb();}
    function fb(){var ta=document.createElement('textarea');ta.value=tx;ta.style.position='absolute';ta.style.left='-9999px';document.body.appendChild(ta);ta.select();try{document.execCommand('copy')}catch(e){}document.body.removeChild(ta);flash();}
  };
  window.downloadPrompt=function(btn,filename){
    var box=btn.closest('.prompt-copyable')||btn.closest('.codebox');if(!box)return;
    var pre=visiblePre(box);if(!pre)return;
    var blob=new Blob([pre.textContent.trim()],{type:'text/markdown'});
    var u=URL.createObjectURL(blob);var a=document.createElement('a');a.href=u;a.download=filename||'prompt.md';a.click();URL.revokeObjectURL(u);
  };
})();
