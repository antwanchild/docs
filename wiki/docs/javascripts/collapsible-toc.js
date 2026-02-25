// Collapsible TOC for Material for MkDocs
(function() {
  "use strict";
  
  function initCollapsibleTOC() {
  console.log("Starting TOC initialization…");
  
  // Wait for Material theme to fully load
  setTimeout(function() {
    // Try multiple selectors to find the TOC
    var tocSelectors = [
      ".md-sidebar--secondary .md-nav__list",
      ".md-sidebar--secondary nav > ul",
      "[data-md-component=\"toc\"] .md-nav__list",
      ".md-nav--secondary > .md-nav__list"
    ];
    
    var toc = null;
    for (var i = 0; i < tocSelectors.length; i++) {
      toc = document.querySelector(tocSelectors[i]);
      if (toc) {
        console.log("Found TOC with selector: " + tocSelectors[i]);
        break;
      }
    }
    
    if (!toc) {
      console.log("TOC not found. Page may not have headings.");
      return;
    }
    
    // Get all li elements that contain nested ul elements
    var allListItems = toc.querySelectorAll("li");
    console.log("Total list items found: " + allListItems.length);
    
    var collapsibleCount = 0;
    
    for (var i = 0; i < allListItems.length; i++) {
      var item = allListItems[i];
      var childNav = null;
      
      // Find direct child nav element
      for (var j = 0; j < item.children.length; j++) {
        if (item.children[j].tagName === "NAV") {
          childNav = item.children[j];
          break;
        }
      }
      
      if (childNav) {
        collapsibleCount++;
        
        // Initially hide the nested nav
        childNav.style.display = "none";
        
        // Find the direct child link
        var link = null;
        for (var k = 0; k < item.children.length; k++) {
          if (item.children[k].tagName === "A") {
            link = item.children[k];
            break;
          }
        }
        
        if (link) {
          // Create toggle button
          var toggle = document.createElement("span");
          toggle.innerHTML = "&#9654; ";
          toggle.className = "toc-toggle";
          toggle.style.cssText = "cursor: pointer; margin-right: 3px; display: inline-flex; align-items: center; transition: transform 0.2s ease; user-select: none; font-size: 0.7em;";
          toggle.setAttribute("data-collapsed", "true");
          
          // Wrap both toggle and link in a flex container
          var wrapper = document.createElement("div");
          wrapper.style.cssText = "display: flex; align-items: center;";
          
          // Insert wrapper before link
          item.insertBefore(wrapper, link);
          
          // Move link into wrapper
          wrapper.appendChild(toggle);
          wrapper.appendChild(link);
          
          // Add click handler
          (function(toggleBtn, nestedNav, listItem) {
            toggleBtn.addEventListener("click", function(e) {
              e.preventDefault();
              e.stopPropagation();
              
              var isCollapsed = toggleBtn.getAttribute("data-collapsed") === "true";
              
              if (isCollapsed) {
                nestedNav.style.display = "block";
                toggleBtn.style.transform = "rotate(90deg)";
                toggleBtn.setAttribute("data-collapsed", "false");
              } else {
                nestedNav.style.display = "none";
                toggleBtn.style.transform = "rotate(0deg)";
                toggleBtn.setAttribute("data-collapsed", "true");
              }
            });
          })(toggle, childNav, item);
        }
      }
    }
    
    console.log("Made " + collapsibleCount + " sections collapsible");
    
    // Expand sections containing active link
    var activeLinks = toc.querySelectorAll(".md-nav__link--active");
    console.log("Active links found: " + activeLinks.length);
    
    for (var i = 0; i < activeLinks.length; i++) {
      var current = activeLinks[i];
      
      // Walk up the tree
      while (current && current !== toc) {
        if ((current.tagName === "UL" || current.tagName === "NAV") && current !== toc && current.style.display === "none") {
          current.style.display = "block";
          
          // Find and update toggle button
          var parentLi = current.parentElement;
          if (parentLi && parentLi.tagName === "LI") {
            var toggleBtn = parentLi.querySelector(".toc-toggle");
            if (toggleBtn) {
              toggleBtn.style.transform = "rotate(90deg)";
              toggleBtn.setAttribute("data-collapsed", "false");
            }
          }
        }
        current = current.parentElement;
      }
    }
    
    console.log("Collapsible TOC setup complete!");
    
    // Keep track of previously expanded sections
    var previouslyExpanded = [];
    
    // Function to expand active sections and collapse others
    function updateActiveSections() {
      var toc = document.querySelector(".md-sidebar--secondary .md-nav__list");
      if (!toc) return;
      
      var activeLinks = toc.querySelectorAll(".md-nav__link--active");
      var currentExpanded = [];
      
      // Find all nav elements that should be expanded (contain active links)
      for (var i = 0; i < activeLinks.length; i++) {
        var current = activeLinks[i];
        
        while (current && current !== toc) {
          if (current.tagName === "NAV") {
            currentExpanded.push(current);
            current.style.display = "block";
            
            var parentLi = current.parentElement;
            if (parentLi && parentLi.tagName === "LI") {
              var toggleBtn = parentLi.querySelector(".toc-toggle");
              if (toggleBtn) {
                toggleBtn.style.transform = "rotate(90deg)";
                toggleBtn.setAttribute("data-collapsed", "false");
              }
            }
          }
          current = current.parentElement;
        }
      }
      
      // Collapse sections that were expanded but are no longer active
      for (var i = 0; i < previouslyExpanded.length; i++) {
        if (currentExpanded.indexOf(previouslyExpanded[i]) === -1) {
          previouslyExpanded[i].style.display = "none";
          
          var parentLi = previouslyExpanded[i].parentElement;
          if (parentLi && parentLi.tagName === "LI") {
            var toggleBtn = parentLi.querySelector(".toc-toggle");
            if (toggleBtn) {
              toggleBtn.style.transform = "rotate(0deg)";
              toggleBtn.setAttribute("data-collapsed", "true");
            }
          }
        }
      }
      
      previouslyExpanded = currentExpanded;
    }
    
    // Initial expansion
    updateActiveSections();
    
    // Watch for active link changes (when scrolling)
    var observer = new MutationObserver(function() {
      updateActiveSections();
    });
    
    observer.observe(toc, {
      attributes: true,
      attributeFilter: ["class"],
      subtree: true
    });
    
  }, 250);
  
  }
  
  // Run on page load
  if (document.readyState === "loading...") {
  document.addEventListener("DOMContentLoaded", initCollapsibleTOC);
  } else {
  initCollapsibleTOC();
  }
  
  // Re-run when navigating with instant loading (Material feature)
  document.addEventListener("DOMContentSwitch", initCollapsibleTOC);
  
  })();