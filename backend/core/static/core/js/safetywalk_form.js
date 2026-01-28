document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("safetywalkForm");
  if (!form) return;

  const clearErrors = () => {
    form.querySelectorAll(".field-error").forEach((el) =>
      el.classList.remove("field-error")
    );
    form.querySelectorAll(".field-error-group").forEach((el) =>
      el.classList.remove("field-error-group")
    );
    form.querySelectorAll(".field-error-msg").forEach((el) => el.remove());
  };

  const showErrorAfter = (node, message) => {
    const msg = document.createElement("div");
    msg.className = "field-error-msg";
    msg.innerText = message;
    node.insertAdjacentElement("afterend", msg);
  };

  const showFieldError = (field, message) => {
    field.classList.add("field-error");
    showErrorAfter(field, message);
  };

  const showGroupError = (groupEl, message) => {
    groupEl.classList.add("field-error-group");
    showErrorAfter(groupEl, message);
  };

  form.addEventListener("submit", (e) => {
    clearErrors();
    let hasError = false;

    // 1) Min. 1 checkbox: PPE/Work/Environment
    const group = document.getElementById("obsTypeGroup");
    const ppe = form.querySelector('input[name$="ppe"]');
    const work = form.querySelector('input[name$="work"]');
    const env = form.querySelector('input[name$="environment"]');

    if (group && ppe && work && env && !ppe.checked && !work.checked && !env.checked) {
      showGroupError(group, "Wybierz przynajmniej jeden typ obserwacji.");
      hasError = true;
    }

    // 2) Reaction wymagane
    const reaction = form.querySelector('select[name$="reaction"]');
    if (!reaction || reaction.value === "") {
      showFieldError(reaction, "Wybierz reakcję.");
      hasError = true;
    }

    // 3) Comment wymagane
    const comment = form.querySelector('textarea[name$="comment"]');
    if (!comment || comment.value.trim() === "") {
      showFieldError(comment, "Komentarz jest wymagany.");
      hasError = true;
    }

    if (hasError) e.preventDefault();
  });
});
