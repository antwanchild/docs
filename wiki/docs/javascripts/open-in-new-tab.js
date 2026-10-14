// Preserve external and downloadable link behavior without a build plugin.
(() => {
  const extensions = /\.(pdf|docx?|json|xlsx?|pptx?|zip|rar|tar|gz|7z|bz2|xz|tgz)$/i;
  const applyRules = () => {
    document.querySelectorAll("a[href]").forEach((link) => {
      const url = new URL(link.href, window.location.href);
      if (url.host !== window.location.host || extensions.test(url.pathname)) {
        link.target = "_blank";
        link.relList.add("noopener");
      }
    });
  };

  if (typeof document$ !== "undefined") {
    document$.subscribe(applyRules);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", applyRules);
  } else {
    applyRules();
  }
})();
