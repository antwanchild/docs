window.MathJax = {
    tex: {
      inlineMath: [["\\(", "\\)"]],
      displayMath: [["\\[", "\\]"]],
      processEscapes: true,
      processEnvironments: true
    },
    options: {
      ignoreHtmlClass: ".*|",
      processHtmlClass: "arithmatex"
    }
  };

let mathJaxLoading = false;

function typesetMath() {
  if (!document.querySelector(".arithmatex")) {
    return;
  }

  if (window.MathJax.typesetPromise) {
    window.MathJax.startup.output.clearCache();
    window.MathJax.typesetClear();
    window.MathJax.texReset();
    window.MathJax.typesetPromise().catch((error) => {
      console.error("Unable to typeset math:", error);
    });
    return;
  }

  if (mathJaxLoading) {
    return;
  }

  mathJaxLoading = true;
  const script = document.createElement("script");
  script.src = "https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js";
  script.async = true;
  script.onload = () => {
    mathJaxLoading = false;
    typesetMath();
  };
  script.onerror = () => {
    mathJaxLoading = false;
    console.error("Unable to load MathJax.");
  };
  document.head.appendChild(script);
}

document$.subscribe(typesetMath);