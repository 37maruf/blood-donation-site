(function () {
  "use strict";

  // ---- Theme toggle (the initial theme is set by a tiny inline script in <head>)
  var toggle = document.getElementById("theme-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var root = document.documentElement;
      var next = root.getAttribute("data-bs-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-bs-theme", next);
      try { localStorage.setItem("sj-theme", next); } catch (e) {}
    });
  }

  // ---- Dismiss flash messages
  document.querySelectorAll(".flash-close").forEach(function (b) {
    b.addEventListener("click", function () { b.closest(".flash").remove(); });
  });

  // ---- Show / hide password
  document.querySelectorAll('input[type="password"]').forEach(function (input) {
    var wrap = document.createElement("div");
    wrap.className = "pw-wrap";
    input.parentNode.insertBefore(wrap, input);
    wrap.appendChild(input);
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "pw-toggle";
    btn.setAttribute("aria-label", document.documentElement.lang === "bn" ? "পাসওয়ার্ড দেখান বা লুকান" : "Show or hide password");
    btn.innerHTML = '<svg class="ico" aria-hidden="true"><use href="#i-eye"/></svg>';
    btn.addEventListener("click", function () {
      input.type = input.type === "password" ? "text" : "password";
    });
    wrap.appendChild(btn);
  });

  // ---- Registration / profile form: show donor-only fields only for donors.
  var donor = document.getElementById("id_wants_to_donate");
  if (donor) {
    var names = ["blood_group", "never_donated", "confirmed_last_donation_date"];
    var sync = function () {
      names.forEach(function (n) {
        var el = document.querySelector('[data-field="' + n + '"]');
        if (el) { el.hidden = !donor.checked; }
      });
    };
    donor.addEventListener("change", sync);
    sync();
    var never = document.getElementById("id_never_donated");
    var last = document.getElementById("id_confirmed_last_donation_date");
    if (never && last) {
      var syncNever = function () { last.disabled = never.checked; if (never.checked) { last.value = ""; } };
      never.addEventListener("change", syncNever);
      syncNever();
    }
  }

  // ---- Confirm before irreversible-looking actions.
  document.querySelectorAll("form[data-confirm]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      if (!window.confirm(f.getAttribute("data-confirm"))) { e.preventDefault(); }
    });
  });
})();
