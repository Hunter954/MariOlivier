function toggleSidebar(){
  const el = document.getElementById("sidebar");
  if(!el) return;
  el.classList.toggle("open");
}

function toast(msg){
  // simple toast
  const t = document.createElement("div");
  t.textContent = msg;
  t.style.position = "fixed";
  t.style.left = "50%";
  t.style.bottom = "22px";
  t.style.transform = "translateX(-50%)";
  t.style.padding = "10px 14px";
  t.style.borderRadius = "16px";
  t.style.border = "1px solid rgba(255,255,255,.14)";
  t.style.background = "rgba(0,0,0,.55)";
  t.style.backdropFilter = "blur(8px)";
  t.style.zIndex = 9999;
  document.body.appendChild(t);
  setTimeout(()=>t.remove(), 2200);
}

(function(){
  const input = document.getElementById("searchInput");
  if(!input) return;
  input.addEventListener("input", () => {
    const q = (input.value || "").trim().toLowerCase();
    document.querySelectorAll("[data-search]").forEach(el => {
      const hay = el.getAttribute("data-search") || "";
      el.style.display = (!q || hay.includes(q)) ? "" : "none";
    });
  });

  // close sidebar when clicking outside (mobile)
  document.addEventListener("click", (e) => {
    const sidebar = document.getElementById("sidebar");
    if(!sidebar) return;
    const isMobile = window.matchMedia("(max-width: 860px)").matches;
    if(!isMobile) return;
    if(sidebar.classList.contains("open")){
      const clickedInside = sidebar.contains(e.target) || (e.target.closest && e.target.closest(".icon-btn"));
      if(!clickedInside) sidebar.classList.remove("open");
    }
  });
})();
