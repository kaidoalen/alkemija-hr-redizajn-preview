/* Minimal JS: mobile menu, header state, reveal-on-scroll, package preselect, form validation. */
(function(){
  var d=document, root=d.documentElement; root.classList.add('js');
  var MSG=__MSG__;
  // Mobile menu
  var b=d.querySelector('.burger'), m=d.getElementById('mnav');
  b.addEventListener('click',function(){var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o)});
  m.addEventListener('click',function(ev){if(ev.target.tagName==='A'){m.classList.remove('open');b.setAttribute('aria-expanded','false')}});
  // Header border + mobile CTA bar (hidden over hero and contact)
  var h=d.querySelector('.hdr'), bar=d.querySelector('.mbar'), hero=d.querySelector('.hero'), kont=d.getElementById('kontakt');
  function onScroll(){var y=window.scrollY;h.classList.toggle('scrolled',y>8);
    var k=kont.getBoundingClientRect().top<window.innerHeight;bar.classList.toggle('show',y>hero.offsetHeight*0.8&&!k)}
  window.addEventListener('scroll',onScroll,{passive:true});onScroll();
  // Reveal on scroll
  var els=d.querySelectorAll('.rv');
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{rootMargin:'0px 0px -8% 0px'});els.forEach(function(x){io.observe(x)})}
  else els.forEach(function(x){x.classList.add('in')});
  // Package buttons preselect the package in the form
  d.querySelectorAll('[data-book]').forEach(function(a){a.addEventListener('click',function(){var g=d.getElementById('f-goal');if(g&&!g.value)g.value=a.getAttribute('data-book');setTimeout(function(){var n=d.getElementById('f-name');if(n)n.focus({preventScroll:true})},600)})});
  d.querySelectorAll('[data-pack]').forEach(function(a){a.addEventListener('click',function(){d.getElementById('f-pack').value=a.getAttribute('data-pack')})});
  // Inquiry form
  var f=d.getElementById('inquiry'), st=f.querySelector('.fstatus');
  f.addEventListener('submit',function(ev){
    ev.preventDefault(); st.className='fstatus'; st.textContent='';
    var bad=null;
    f.querySelectorAll('[required]').forEach(function(i){
      var ok=i.type==='checkbox'?i.checked:i.value.trim()!=='';
      if(ok&&i.type==='email')ok=/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(i.value.trim());
      i.setAttribute('aria-invalid',ok?'false':'true'); if(!ok&&!bad)bad=i;
    });
    if(bad){st.className='fstatus err';st.textContent=(bad.type==='email'&&bad.value)?MSG.err_email:MSG.err;bad.focus();return}
    if(f.website.value)return; // honeypot
    var ids=['f-name','f-company','f-email','f-market','f-goal','f-pack'];
    var body=ids.map(function(id,i){return MSG.labels[i]+': '+d.getElementById(id).value}).join('\n');
    var ep=f.getAttribute('data-endpoint');
    if(!ep){ // No backend configured yet: never fake success, hand over to the visitor's email app
      st.textContent=MSG.mailto;
      window.location.href='mailto:'+f.getAttribute('data-mailto')+'?subject='+encodeURIComponent(MSG.subject)+'&body='+encodeURIComponent(body);
      return;
    }
    st.textContent=MSG.sending; var sb=f.querySelector('[type=submit]'); sb.disabled=true;
    var id=f.getAttribute('data-cf7'), fd=new FormData(f); fd.append('_wpcf7',id); fd.append('_wpcf7_unit_tag','wpcf7-f'+id+'-o1'); fd.append('_wpcf7_container_post','0'); fd.append('_wpcf7_locale',document.documentElement.lang);
    fetch(ep,{method:'POST',body:fd}).then(function(r){return r.json()}).then(function(j){sb.disabled=false;
      if(j&&(j.status==='mail_sent'||j.ok===true)){st.textContent=MSG.ok;f.reset()}else{st.className='fstatus err';st.textContent=MSG.fail}
    }).catch(function(){sb.disabled=false;st.className='fstatus err';st.textContent=MSG.fail});
  });
})();
