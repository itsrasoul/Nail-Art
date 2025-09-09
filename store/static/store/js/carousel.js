document.addEventListener('DOMContentLoaded', function(){
  const grid = document.querySelector('.carousel-grid');
  if(!grid) return;

  // Each .banner-card cycles its own .banner images
  const cards = Array.from(grid.querySelectorAll('.banner-card'));
  // a bit faster rotation
  // slower, smoother rotation
  const baseInterval = 2000;

  cards.forEach((card, cardIndex) => {
    const imgs = Array.from(card.querySelectorAll('.banner'));
    if(imgs.length <= 1) return;

    // position images absolutely and set initial opacity + gentle transform
    imgs.forEach((img, i) => {
      img.style.position = 'absolute';
      img.style.inset = '0';
      img.style.width = '100%';
      img.style.height = '100%';
      img.style.objectFit = 'cover';
      img.style.opacity = i === 0 ? '1' : '0';
      img.style.transform = i === 0 ? 'translateY(0) scale(1)' : 'translateY(6px) scale(0.995)';
      img.style.transition = 'opacity 1.2s cubic-bezier(.2,.8,.2,1), transform 1.2s cubic-bezier(.2,.8,.2,1)';
      card.style.position = 'relative';
      card.style.overflow = 'hidden';
    });

    let current = 0;
    const next = i => (i + 1) % imgs.length;

    // stagger start so cards don't all change at the exact same millisecond
    setTimeout(() => {
      setInterval(() => {
        const n = next(current);
        imgs[current].style.opacity = '0';
        imgs[current].style.transform = 'translateY(6px) scale(0.995)';
        imgs[n].style.transform = 'translateY(0) scale(1)';
        imgs[n].style.opacity = '1';
        current = n;
      }, baseInterval);
    }, cardIndex * 600);
  });
});
