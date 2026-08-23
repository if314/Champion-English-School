/*
 * Champion / Чемпиън — English level test.
 * All questions are rendered server-side in plain HTML (readable without
 * JavaScript). This script only paginates them, tracks progress and scores
 * the result client-side. It is a preliminary/internal self-assessment,
 * not an official CEFR certification.
 */
(function () {
  "use strict";

  var form = document.getElementById("level-test-form");
  if (!form) return;

  var questions = Array.prototype.slice.call(form.querySelectorAll(".test-question"));
  var total = questions.length;
  var current = 0;

  var progressFill = document.getElementById("progressFill");
  var progressLabel = document.getElementById("progressLabel");
  var prevBtn = document.getElementById("prevBtn");
  var nextBtn = document.getElementById("nextBtn");
  var errorEl = document.getElementById("testError");
  var resultPanel = document.getElementById("resultPanel");

  var progressTemplate = progressLabel.getAttribute("data-template") || "{current} / {total}";

  function render() {
    questions.forEach(function (q, i) {
      q.classList.toggle("is-active", i === current);
    });
    progressFill.style.width = (((current + 1) / total) * 100).toFixed(0) + "%";
    progressLabel.textContent = progressTemplate
      .replace("{current}", current + 1)
      .replace("{total}", total);
    prevBtn.disabled = current === 0;
    nextBtn.textContent =
      current === total - 1
        ? nextBtn.getAttribute("data-label-finish")
        : nextBtn.getAttribute("data-label-next");
    if (errorEl) errorEl.style.display = "none";
  }

  function currentAnswered() {
    return !!questions[current].querySelector("input:checked");
  }

  prevBtn.addEventListener("click", function () {
    if (current > 0) {
      current--;
      render();
      form.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });

  nextBtn.addEventListener("click", function () {
    if (!currentAnswered()) {
      if (errorEl) {
        errorEl.textContent = form.getAttribute("data-msg-select");
        errorEl.style.display = "block";
      }
      return;
    }
    if (current < total - 1) {
      current++;
      render();
      form.scrollIntoView({ behavior: "smooth", block: "start" });
    } else {
      showResult();
    }
  });

  function showResult() {
    var score = 0;
    questions.forEach(function (q) {
      var checked = q.querySelector("input:checked");
      if (checked && checked.getAttribute("data-correct") === "true") score++;
    });

    var levelDataEl = document.getElementById("levelData");
    var levels = JSON.parse(levelDataEl.textContent);
    var match =
      levels.find(function (l) {
        return score >= l.min && score <= l.max;
      }) || levels[levels.length - 1];

    document.getElementById("resultLevelName").textContent = match.name;
    document.getElementById("resultLevelCefr").textContent = match.cefr;
    document.getElementById("resultDescription").textContent = match.description;

    var scoreEl = document.getElementById("resultScore");
    var scoreTemplate = form.getAttribute("data-score-template");
    if (scoreEl && scoreTemplate) {
      scoreEl.textContent = scoreTemplate
        .replace("{score}", score)
        .replace("{total}", total);
    }

    form.hidden = true;
    resultPanel.classList.add("is-active");
    resultPanel.setAttribute("tabindex", "-1");
    resultPanel.focus();
    resultPanel.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  var retakeBtn = document.getElementById("retakeBtn");
  if (retakeBtn) {
    retakeBtn.addEventListener("click", function () {
      window.location.reload();
    });
  }

  render();
})();
