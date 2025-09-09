function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

document.addEventListener('DOMContentLoaded', function(){
  const buttons = document.querySelectorAll('.add-cart');
  if(!buttons.length) return;
  const avatar = document.querySelector('.nav-avatar');

  buttons.forEach(btn=>{
    btn.addEventListener('click', async (e)=>{
      e.preventDefault();
      const id = btn.dataset.id;
      // try to animate a clone of the product image
      const card = btn.closest('.card');
      const prodImg = card ? card.querySelector('img') : null;
      if(prodImg && avatar){
        animateFly(prodImg, avatar);
      }

      try{
        const res = await fetch(`/cart/add/${id}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
          },
          body: JSON.stringify({})
        });
        const data = await res.json();
        if(data.success){
          // update cart count in header
          const el = document.querySelector('.cart-count');
          if(el) el.textContent = data.cart_count;
          // show a tiny toast
          const t = document.createElement('div');
          t.className = 'mini-toast';
          t.textContent = 'Added to cart';
          document.body.appendChild(t);
          setTimeout(()=>t.classList.add('visible'),50);
          setTimeout(()=>{ t.classList.remove('visible'); setTimeout(()=>t.remove(),300); },1500);
        }
      }catch(err){
        console.error(err);
      }
    });
  });

    function animateFly(imgEl, targetEl){
    try{
      const rect = imgEl.getBoundingClientRect();
      const targetRect = targetEl.getBoundingClientRect();
      const clone = imgEl.cloneNode(true);
      clone.style.position = 'fixed';
      clone.style.left = rect.left + 'px';
      clone.style.top = rect.top + 'px';
      clone.style.width = rect.width + 'px';
      clone.style.height = rect.height + 'px';
      clone.style.objectFit = 'cover';
      clone.style.borderRadius = '8px';
      clone.style.zIndex = 9999;
      clone.style.transformOrigin = 'center center';
      clone.classList.add('fly-img');
      document.body.appendChild(clone);

      // compute translate and scale to target center
      requestAnimationFrame(()=>{
        const dx = (targetRect.left + targetRect.width/2) - (rect.left + rect.width/2);
        const dy = (targetRect.top + targetRect.height/2) - (rect.top + rect.height/2);
        // smoother easing and a slight arc using translate and rotate
        const targetScale = Math.max(0.12, Math.min(0.22, (targetRect.width / rect.width) * 0.9));
        clone.style.transition = 'transform 0.95s cubic-bezier(.18,.9,.28,1), opacity 0.6s ease';
        clone.style.transform = `translate(${dx}px, ${dy - 20}px) scale(${targetScale}) rotate(-8deg)`;
        clone.style.opacity = '0.55';
      });

      setTimeout(()=>{ try{ clone.remove(); }catch(e){} }, 1050);
    }catch(e){
      // ignore animation errors
      console.error(e);
    }
  }
});
