<template>
  <section class="tour-3d-block">
    <h2 class="tour-title">Виртуальный 3D-тур по ЖК</h2>
    <div class="tour-3d-viewer">
      <iframe
        src="https://rz360.avalin.space"
        width="100%"
        height="100%"
        frameborder="0"
        allowfullscreen
        title="3D-тур по ЖК"
      ></iframe>
    </div>
  </section>
</template>

<style scoped>
.tour-3d-block {
  margin: 3rem auto;
  max-width: 1200px;
  padding: 0 1rem;
}
.tour-title {
  text-align: center;
  margin-bottom: 2rem;
  color: #007aff;
  font-size: 2rem;
  font-weight: 700;
}
.tour-3d-viewer {
  width: 100%;
  aspect-ratio: 16 / 9;
  min-height: 320px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 24px rgba(0, 122, 255, 0.08);
  background: #000;
}
.tour-3d-viewer iframe {
  width: 100%;
  height: 100%;
  border: none;
  display: block;
}
@media (max-width: 768px) {
  .tour-title {
    font-size: 1.3rem;
  }
  .tour-3d-viewer {
    min-height: 200px;
    aspect-ratio: 16 / 10;
  }
}
</style> 