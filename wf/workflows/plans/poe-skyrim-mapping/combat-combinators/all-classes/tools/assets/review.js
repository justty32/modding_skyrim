function reveal(id){let t=document.getElementById(id);
if(!t)return;
let d=t.matches('details.classgroup')?t:t.closest('details.classgroup');
if(d)d.open=true;
setTimeout(()=>t.scrollIntoView(),0);
}document.querySelectorAll('a[href^="#"]').forEach(a=>a.addEventListener('click',()=>reveal(a.hash.slice(1))));
window.addEventListener('hashchange',()=>reveal(location.hash.slice(1)));
if(location.hash)reveal(location.hash.slice(1));
