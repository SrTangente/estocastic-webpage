(function(){
  var mb=document.querySelector('.menu-btn'),mn=document.getElementById('menu');
  if(mb&&mn)mb.addEventListener('click',function(){var o=mn.classList.toggle('open');mb.setAttribute('aria-expanded',o)});
  if(mb&&mn){document.addEventListener('click',function(e){if(mn.classList.contains('open')&&!mn.contains(e.target)&&e.target!==mb){mn.classList.remove('open');mb.setAttribute('aria-expanded','false')}});document.addEventListener('keydown',function(e){if(e.key==='Escape'){var was=mn.classList.contains('open'),inside=mn.contains(document.activeElement);mn.classList.remove('open');mb.setAttribute('aria-expanded','false');if(was&&inside)mb.focus()}})}

  var KEY='est_unlocked_v1';
  function get(){try{return localStorage.getItem(KEY)==='1'}catch(e){return false}}
  function set(){try{localStorage.setItem(KEY,'1')}catch(e){}}

  /* ---------- lightbox ---------- */
  var links=[].slice.call(document.querySelectorAll('a.ph'));
  var lb=document.getElementById('lb');
  if(lb&&links.length){
    var img=lb.querySelector('img'),cnt=lb.querySelector('.cnt'),dl=lb.querySelector('.dl'),i=0,last=null;
    function pad(n,l){n=String(n);while(n.length<l)n='0'+n;return n}
    function show(n){
      i=(n+links.length)%links.length;var a=links[i];
      img.src=a.getAttribute('data-full');img.alt=a.querySelector('img').alt||'';
      cnt.textContent=pad(i+1,3)+' / '+pad(links.length,3);
      dl.href=a.getAttribute('data-full');dl.setAttribute('download',a.getAttribute('data-name'));
      [1,-1].forEach(function(d){var p=links[(i+d+links.length)%links.length];(new Image()).src=p.getAttribute('data-full')});
    }
    /* el resto de la página queda inerte mientras el visor está abierto (foco y lectores de pantalla) */
    function setInert(on){[].forEach.call(document.body.children,function(el){if(el===lb||el.tagName==='SCRIPT')return;if(on)el.setAttribute('inert','');else el.removeAttribute('inert')})}
    function open(n){last=document.activeElement;show(n);lb.classList.add('open');document.body.style.overflow='hidden';setInert(true);lb.querySelector('.x').focus()}
    function close(){lb.classList.remove('open');document.body.style.overflow='';img.removeAttribute('src');setInert(false);if(last)last.focus()}
    links.forEach(function(a,n){a.addEventListener('click',function(e){e.preventDefault();open(n)})});
    lb.querySelector('.x').addEventListener('click',close);
    lb.querySelector('.prev').addEventListener('click',function(){show(i-1)});
    lb.querySelector('.next').addEventListener('click',function(){show(i+1)});
    lb.addEventListener('click',function(e){if(e.target===lb||e.target.classList.contains('lb-stage'))close()});
    document.addEventListener('keydown',function(e){
      if(!lb.classList.contains('open'))return;
      if(e.key==='Escape')close();else if(e.key==='ArrowLeft')show(i-1);else if(e.key==='ArrowRight')show(i+1);
    });
    var sx=null;
    lb.addEventListener('touchstart',function(e){sx=e.touches[0].clientX},{passive:true});
    lb.addEventListener('touchend',function(e){
      if(sx===null)return;var dx=e.changedTouches[0].clientX-sx;sx=null;
      if(Math.abs(dx)>50)show(i+(dx<0?1:-1));
    });
  }

  /* ---------- gate (email -> unlock) ---------- */
  var gate=document.getElementById('gate');
  if(gate){
    var target='';try{target=atob(gate.getAttribute('data-s'))}catch(e){}
    var openLink=gate.querySelector('.open-link');
    if(openLink)openLink.href=target;
    if(get())gate.classList.add('unlocked');
    var form=gate.querySelector('form'),msg=gate.querySelector('.msg');
    var endpoint=(window.EST&&window.EST.endpoint)||'';var M=(window.EST&&window.EST.m)||{};
    if(form)form.addEventListener('submit',function(e){
      e.preventDefault();
      var email=form.email.value.trim(),ok=form.consent.checked;
      if(form.website&&form.website.value)return; // honeypot
      if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)){msg.textContent=M.email||'Email?';return}
      if(!ok){msg.textContent=M.consent||'Consent?';return}
      var local=/^(localhost|127\.0\.0\.1)$/.test(location.hostname);
      if(!endpoint&&!local){msg.textContent=M.na||'N/A';return}
      var btn=form.querySelector('button');btn.disabled=true;msg.textContent='…';
      function done(){set();gate.classList.add('unlocked');msg.textContent='';if(target)location.href=target}
      if(!endpoint){console.warn('EST endpoint not set (local demo)');done();return}
      fetch(endpoint,{method:'POST',mode:'no-cors',headers:{'Content-Type':'text/plain;charset=utf-8'},
        body:JSON.stringify({email:email,consent:true,source:location.pathname,ts:new Date().toISOString()})})
        .then(done).catch(function(){btn.disabled=false;msg.textContent=M.fail||'Error'});
    });
  }

  /* ---------- home: faders en reposo con deriva estocástica ---------- */
  var chs=[].slice.call(document.querySelectorAll('.ch'));
  if(chs.length){
    var calm=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var base=[];try{base=JSON.parse(sessionStorage.getItem('est_lv')||'[]')}catch(e){}
    if(base.length!==chs.length){base=chs.map(function(){return +(0.15+Math.random()*0.65).toFixed(2)});try{sessionStorage.setItem('est_lv',JSON.stringify(base))}catch(e){}}
    chs.forEach(function(c,n){c.style.setProperty('--lvl',base[n])});
    if(!calm)setInterval(function(){
      var c=chs[Math.floor(Math.random()*chs.length)],n=chs.indexOf(c);
      if(document.hidden||c.matches(':hover,:focus-visible'))return;
      base[n]=Math.min(.85,Math.max(.12,base[n]+(Math.random()-.5)*.3));c.style.setProperty('--lvl',base[n].toFixed(2));
    },1400);
  }
})();
