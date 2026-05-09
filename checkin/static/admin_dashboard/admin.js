(function () {
  function setTheme(mode) {
    if (mode !== "light" && mode !== "dark") {
      mode = "light";
    }
    document.documentElement.dataset.theme = mode;
    localStorage.setItem("theme", mode);
    document.querySelectorAll("[data-dashboard-theme]").forEach(function (button) {
      button.classList.toggle("is-active", button.dataset.dashboardTheme === mode);
    });
  }

  function initTheme() {
    var saved = localStorage.getItem("theme");
    if (saved !== "light" && saved !== "dark") {
      saved = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    }
    setTheme(saved);
  }

  function initDashboardSearch() {
    var input = document.querySelector("[data-dashboard-search]");
    var moduleRoot = document.querySelector("[data-dashboard-modules]");
    if (!input || !moduleRoot) {
      return;
    }

    var emptyState = moduleRoot.querySelector("[data-dashboard-empty]");
    var apps = Array.prototype.slice.call(moduleRoot.querySelectorAll("[data-dashboard-app]"));

    input.addEventListener("input", function () {
      var query = input.value.trim().toLowerCase();
      var visibleApps = 0;

      apps.forEach(function (app) {
        var visibleModels = 0;
        app.querySelectorAll("[data-dashboard-model]").forEach(function (model) {
          var matched = !query || model.textContent.toLowerCase().indexOf(query) !== -1;
          model.hidden = !matched;
          if (matched) {
            visibleModels += 1;
          }
        });
        app.hidden = visibleModels === 0;
        if (visibleModels > 0) {
          visibleApps += 1;
        }
      });

      if (emptyState) {
        emptyState.hidden = visibleApps > 0;
      }
    });
  }

  window.addEventListener("DOMContentLoaded", function () {
    initTheme();
    initDashboardSearch();
    document.querySelectorAll("[data-dashboard-theme]").forEach(function (button) {
      button.addEventListener("click", function () {
        setTheme(button.dataset.dashboardTheme);
      });
    });
  });
})();
