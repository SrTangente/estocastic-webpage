/* esτocasτic — fondo generativo (ondas que colapsan) + color variable del logo */
(function(){
  var root=document.documentElement;
  function sget(){try{return sessionStorage.getItem('est_h')}catch(e){return null}}
  function sset(v){try{sessionStorage.setItem('est_h',v)}catch(e){}}
  var h=sget(); h=h===null?(Math.random()<.5?Math.round(Math.random()*24-12):Math.floor(Math.random()*360)):+h; if(isNaN(h))h=0;
  function setH(v){h=((v%360)+360)%360;root.style.setProperty('--h',h);sset(h)}
  setH(h);

  /* clic en el símbolo: siguiente color */
  document.addEventListener('click',function(e){
    var m=e.target.closest&&e.target.closest('.mark');
    if(m){setH(h+47+Math.random()*60)}
  });

  /* ---------- canvas ---------- */
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var cv=document.createElement('canvas');cv.className='gen-bg';cv.setAttribute('aria-hidden','true');
  document.body.insertBefore(cv,document.body.firstChild);
  var ctx=cv.getContext('2d'),W=0,H=0,dpr=1,px=-9999,py=-9999,tx=-9999,ty=-9999,ripples=[],t0=performance.now(),run=true,small=false;
  function size(){
    dpr=Math.min(window.devicePixelRatio||1,1.5);W=innerWidth;H=innerHeight;small=W<700;
    cv.width=W*dpr;cv.height=H*dpr;cv.style.width=W+'px';cv.style.height=H+'px';ctx.setTransform(dpr,0,0,dpr,0,0);
  }
  size();addEventListener('resize',size);
  function move(e){var p=e.touches?e.touches[0]:e;tx=p.clientX;ty=p.clientY}
  addEventListener('pointermove',move,{passive:true});
  addEventListener('touchmove',move,{passive:true});
  addEventListener('pointerdown',function(e){ripples.push({x:e.clientX,y:e.clientY,t:performance.now()})},{passive:true});
  addEventListener('pointerleave',function(){tx=ty=-9999});
  document.addEventListener('visibilitychange',function(){run=!document.hidden;if(run)requestAnimationFrame(frame)});

  var LINES=7;
  function frame(now){
    if(!run)return;
    var t=(now-t0)/1000;
    px+=(tx-px)*.12;py+=(ty-py)*.12;               /* cursor suavizado */
    ctx.clearRect(0,0,W,H);
    var hue=(270+h)%360,step=small?14:8,sy=(window.scrollY||0)*.15;
    for(var i=0;i<LINES;i++){
      var base=H*(i+.7)/(LINES+.4)-sy%(H/LINES),amp=22+i*3,f=.0035+i*.0007,sp=.35+i*.07;
      ctx.beginPath();
      for(var x=0;x<=W+step;x+=step){
        var a=amp*Math.sin(x*f+t*sp+i*1.7)+amp*.55*Math.sin(x*f*2.3-t*sp*1.3+i);
        /* colapso: la onda se aplana cerca del cursor */
        var dx=x-px,dy=base-py,d2=dx*dx+dy*dy,k=1-.96*Math.exp(-d2/(2*150*150));
        for(var r=0;r<ripples.length;r++){
          var R=ripples[r],age=(now-R.t)/1000,rad=age*520,dd=Math.hypot(x-R.x,base-R.y);
          k*=1-.9*Math.exp(-Math.pow(dd-rad,2)/(2*70*70))*Math.max(0,1-age/1.6);
        }
        var y=base+a*k;
        x===0?ctx.moveTo(x,y):ctx.lineTo(x,y);
      }
      ctx.strokeStyle='hsla('+(hue+i*9)+',80%,68%,'+(.17+i*.015).toFixed(3)+')';
      ctx.lineWidth=1.1;ctx.stroke();
    }
    ripples=ripples.filter(function(R){return now-R.t<1600});
    if(!reduce)requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
  if(reduce){addEventListener('resize',function(){requestAnimationFrame(frame)})}
})();
