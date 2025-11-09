gsap.from("#hero-title", {
  duration: 1.5,
  y: -50,
  opacity: 0,
  ease: "power2.out"
});

gsap.from("#hero-desc", {
  duration: 1.5,
  y: -20,
  opacity: 0,
  delay: 0.5,
  ease: "power2.out"
});

gsap.from("#hero-buttons a", {
  duration: 1.5,
  opacity: 0,
  y: 20,
  stagger: 0.3,
  delay: 1,
  ease: "power2.out"
});

gsap.to(".circle", {
  duration: 20,
  x: "random(-50, 50)",
  y: "random(-50, 50)",
  repeat: -1,
  yoyo: true,
  ease: "sine.inOut"
});