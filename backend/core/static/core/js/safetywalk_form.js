document.addEventListener("DOMContentLoaded", function () {
  if (window.djangoMessages && window.djangoMessages.length) {
    window.djangoMessages.forEach((msg) => alert(msg));
  }

  const form = document.getElementById("safetywalkForm");
  const container = document.getElementById("obsContainer");
  const addBtn = document.getElementById("addObsBtn");
  const totalFormsInput = document.querySelector('input[name$="-TOTAL_FORMS"]');

  // Guard: jeśli to nie ta strona (np. list/detail), nie rób nic
  if (!form || !container || !addBtn || !totalFormsInput) return;

  function hideDeleteControls(scope) {
    scope
      .querySelectorAll('input[type="checkbox"][name$="-DELETE"]')
      .forEach((cb) => {
        cb.style.display = "none";
        const lbl = scope.querySelector(`label[for="${cb.id}"]`);
        if (lbl) lbl.style.display = "none";
      });
  }

  function wireRemoveButtons(scope) {
    scope.querySelectorAll(".removeObsBtn").forEach((btn) => {
      btn.onclick = function () {
        const block = btn.closest(".obs-form");
        if (!block) return; // <-- kluczowe (naprawia błąd z null)

        const del = block.querySelector('input[type="checkbox"][name$="-DELETE"]');

        if (del) {
          del.checked = true;            // Django: oznacz jako do usuniecia
          block.style.display = "none";  // UX: schowaj
        } else {
          block.remove(); // nowy niezapisany
        }
      };
    });
  }

  // ========== WALIDACJA (JEDEN submit handler) ==========
  form.addEventListener("submit", function (e) {
    const blocks = container.querySelectorAll(".obs-form");
    let hasAnyActive = false;
    let needsReaction = false;

    blocks.forEach((b) => {
      // pomijamy ukryte / usunięte
      if (b.style.display === "none") return;
      const del = b.querySelector('input[type="checkbox"][name$="-DELETE"]');
      if (del && del.checked) return;

      const ppe = b.querySelector('input[name$="-ppe"]')?.checked;
      const work = b.querySelector('input[name$="-work"]')?.checked;
      const env = b.querySelector('input[name$="-environment"]')?.checked;
      const commentLen = ((b.querySelector('textarea[name$="-comment"]')?.value || "").trim().length);

      const anyChecked = !!(ppe || work || env);
      const commentOk = commentLen >= 3;

      if (anyChecked || commentOk) hasAnyActive = true;
      if (anyChecked) {
        const reaction = b.querySelector('select[name$="-reaction"]');
        if (reaction && !reaction.value) needsReaction = true;
      }
    });

    if (!hasAnyActive) {
      e.preventDefault();
      alert(
        "Dodaj przynajmniej jedna obserwacje:\n" +
        "- zaznacz PPE / Work / Environment\n" +
        "ALBO\n" +
        "- wpisz komentarz (min. 3 znaki)."
      );
      return;
    }

    if (needsReaction) {
      e.preventDefault();
      alert("Wybierz Reaction, jesli zaznaczono PPE / Work / Environment.");
      return;
    }
  });

  // Init
  hideDeleteControls(document);
  wireRemoveButtons(document);

  // ========== DODAWANIE OBS ==========
  addBtn.addEventListener("click", function () {
    const forms = container.querySelectorAll(".obs-form");
    if (forms.length === 0) return; // <-- kluczowe (naprawia cloneNode undefined)

    const lastForm = forms[forms.length - 1];
    const newIndex = parseInt(totalFormsInput.value, 10);

    const newForm = lastForm.cloneNode(true);
    newForm.style.display = "block";

    // Odznacz DELETE w klonie
    newForm.querySelectorAll('input[type="checkbox"][name$="-DELETE"]').forEach((cb) => {
      cb.checked = false;
    });

    // Podmień indeks i wyczyść pola
    newForm.querySelectorAll("input, textarea, select, label").forEach((el) => {
      if (el.name) el.name = el.name.replace(/-\d+-/, `-${newIndex}-`);
      if (el.id) el.id = el.id.replace(/-\d+-/, `-${newIndex}-`);

      if (el.tagName.toLowerCase() === "label" && el.htmlFor) {
        el.htmlFor = el.htmlFor.replace(/-\d+-/, `-${newIndex}-`);
      }

      const tag = el.tagName.toLowerCase();
      if (tag === "input") {
        if (el.type === "checkbox" || el.type === "radio") el.checked = false;
        else el.value = "";
      } else if (tag === "textarea") {
        el.value = "";
      } else if (tag === "select") {
        el.selectedIndex = 0;
      }
    });

    container.appendChild(newForm);
    totalFormsInput.value = newIndex + 1;

    hideDeleteControls(newForm);
    wireRemoveButtons(newForm);
  });
});
