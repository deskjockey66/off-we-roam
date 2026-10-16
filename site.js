const button=document.querySelector('.menu');
const nav=document.querySelector('#navigation');
const menus=[...nav.querySelectorAll('.nav-drop')];
const fine=window.matchMedia('(min-width: 1001px) and (hover: hover) and (pointer: fine)');
function closeMenu(){button.setAttribute('aria-expanded','false');nav.classList.remove('open');menus.forEach(menu=>menu.open=false)}
button.addEventListener('click',()=>{const open=button.getAttribute('aria-expanded')!=='true';if(!open)closeMenu();else{button.setAttribute('aria-expanded','true');nav.classList.add('open')}});
menus.forEach(menu=>{
 menu.addEventListener('pointerenter',()=>{if(fine.matches){menus.forEach(other=>{if(other!==menu)other.open=false});menu.open=true}});
 menu.addEventListener('pointerleave',()=>{if(fine.matches&&!menu.contains(document.activeElement))menu.open=false});
 menu.addEventListener('focusout',e=>{if(!menu.contains(e.relatedTarget))menu.open=false});
 menu.addEventListener('keydown',e=>{if(e.key==='Escape'){e.stopPropagation();menu.open=false;menu.querySelector('summary').focus()}});
 menu.addEventListener('toggle',()=>{if(menu.open)menus.forEach(other=>{if(other!==menu)other.open=false})});
});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeMenu();if(getComputedStyle(button).display!=='none')button.focus()}});
document.addEventListener('click',e=>{if(!e.target.closest('header'))closeMenu();else menus.forEach(menu=>{if(!menu.contains(e.target))menu.open=false})});
nav.addEventListener('click',e=>{if(e.target.closest('a'))closeMenu()});

// Reset transient navigation when switching between phone and desktop layouts.
const compact=window.matchMedia('(max-width: 1000px), (hover: none)');
compact.addEventListener('change',closeMenu);
