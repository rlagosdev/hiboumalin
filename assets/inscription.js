// Houlou Débranché — formulaires d'inscription (liste d'attente Brevo) et menu mobile.
(function () {
  var ACTION = "https://46c1f093.sibforms.com/serve/MUIFADWjOSKsRt3lbGfNRTUiLQ0XtbbQDfXmL2wFoU2KcZzVWgUjFb0xtJ0tcVdWN2tcPtShggDcm9NTptMwARPsxnq83e7XQ7tbKDgbhS6vGy6APxUDMAqIdIsLOHONFhVtC5BxHcR6DsPNS08mreYyTp4mVaHSZpiaCZRc6kHPrhxmZhoJgYGP0yE9ub9_Yf3i_mIRHePlMXqUwQ==";
  var KEY = "hm_source";

  // Provenance : ?source=... (ex. jeux-sans-ecran), mémorisée pour la visite si l'on change de page.
  function clean(s) { return (s || "").toLowerCase().replace(/[^a-z0-9_-]/g, "").slice(0, 60); }
  var source = "";
  try {
    var p = new URLSearchParams(location.search);
    source = clean(p.get("source") || p.get("utm_source"));
    if (source) sessionStorage.setItem(KEY, source);
    else source = sessionStorage.getItem(KEY) || "";
  } catch (e) {}
  if (!source) source = "site";

  // Menu mobile
  var burger = document.querySelector(".burger"), nav = document.getElementById("nav");
  if (burger && nav) burger.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    burger.setAttribute("aria-expanded", open ? "true" : "false");
  });

  // Formulaires
  document.querySelectorAll("form.signup-form").forEach(function (f) {
    var btn = f.querySelector("button[type=submit]"), msg = f.querySelector(".msg");
    var label = btn.textContent;
    function show(kind, text) { msg.className = "msg " + kind; msg.textContent = text; }
    f.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var email = f.querySelector("input[type=email]").value.trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { show("err", "Merci d'indiquer une adresse e-mail valide."); return; }
      if (!f.querySelector(".consent input").checked) { show("err", "Merci de cocher la case d'accord pour recevoir nos e-mails."); return; }
      var ages = Array.prototype.map.call(f.querySelectorAll('input[name="age"]:checked'), function (x) { return x.value; });
      var data = new FormData();
      data.append("EMAIL", email);
      data.append("AGE_ENFANTS", ages.length ? ages.join(",") : "non-precise");
      data.append("SOURCE", source);
      data.append("OPT_IN", "1");
      data.append("email_address_check", f.querySelector('input[name="email_address_check"]').value);
      data.append("locale", "fr");
      btn.disabled = true; btn.textContent = "Envoi…";
      fetch(ACTION + "?isAjax=1", { method: "POST", body: data, mode: "no-cors" })
        .then(function () {
          f.querySelectorAll("input,button").forEach(function (el) { el.disabled = true; });
          btn.textContent = "Merci !";
          show("ok", "C'est presque fini ! Nous venons de vous envoyer un e-mail : cliquez sur « Je confirme mon inscription » pour rejoindre la liste d'attente. Pensez à regarder dans vos spams.");
        })
        .catch(function () {
          btn.disabled = false; btn.textContent = label;
          show("err", "L'envoi n'a pas fonctionné. Vérifiez votre connexion et réessayez, ou écrivez-nous à contact@houlou.fr.");
        });
    });
  });

  // Filtres du catalogue
  var fbar = document.querySelector(".filters");
  if (fbar) {
    var cards = document.querySelectorAll("[data-ages]");
    fbar.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      fbar.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      var f = b.getAttribute("data-f");
      cards.forEach(function (c) {
        var a = c.getAttribute("data-ages").split("-").map(Number), ok = true;
        if (f !== "all") { var r = f.split("-").map(Number); ok = a[0] <= r[1] && a[1] >= r[0]; }
        c.style.display = ok ? "" : "none";
      });
    });
  }
})();
