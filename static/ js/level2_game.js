//static/js/level2_game.js

// level2_game.js
document.addEventListener('DOMContentLoaded', function() {
  // Render items from ITEMS_FOR_GAME declared in template
  const itemsContainer = document.getElementById('items');
  if (itemsContainer && typeof ITEMS_FOR_GAME !== 'undefined') {
    ITEMS_FOR_GAME.forEach(it => {
      const el = document.createElement('div');
      el.className = 'p-2 border rounded draggable';
      el.draggable = true;
      el.id = it.id;
      el.dataset.correct = it.bin;
      el.innerText = it.label;
      el.style.cursor = 'grab';
      el.style.margin = '4px';
      itemsContainer.appendChild(el);
    });
  }

  let dragged = null;
  document.addEventListener('dragstart', e => {
    if (e.target.classList.contains('draggable')) {
      dragged = e.target;
    }
  });

  document.addEventListener('dragover', e => {
    if (e.target.classList.contains('bin') || e.target.closest('.bin')) e.preventDefault();
  });

  document.addEventListener('drop', e => {
    e.preventDefault();
    const bin = e.target.closest('.bin');
    if (!bin || !dragged) return;
    bin.appendChild(dragged);
    dragged.style.cursor = 'default';
    dragged = null;
  });

  const submitBtn = document.getElementById('submitGame');
  if (submitBtn) {
    submitBtn.addEventListener('click', () => {
      let score = 0;
      if (typeof ITEMS_FOR_GAME !== 'undefined') {
        ITEMS_FOR_GAME.forEach(it => {
          const el = document.getElementById(it.id);
          let parent = el.parentElement;
          // parent may be bin or items container
          const parentBin = parent.getAttribute('data-bin') || (parent.closest && parent.closest('.bin') ? parent.closest('.bin').getAttribute('data-bin') : null);
          if (parentBin === it.bin) score += 10;
        });
      }
      document.getElementById('gameScore').innerText = score;

      // send points to server
      const url = (window.ECO_CONFIG && window.ECO_CONFIG.awardPointsUrl) ? window.ECO_CONFIG.awardPointsUrl : '/api/award_points/';
      fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `points=${score}`
      }).then(r => r.json()).then(data => {
        if (data.status === 'ok') {
          const pointsEl = document.getElementById('points');
          const levelEl = document.getElementById('level');
          if (pointsEl) pointsEl.innerText = data.points;
          if (levelEl) levelEl.innerText = data.current_level;
          alert('Points awarded: ' + score);
        } else {
          alert('Could not award points: ' + (data.message || 'unknown'));
        }
      }).catch(e => {
        console.error(e);
        alert('Network error');
      });
    });
  }

  // Quiz handling — simple client-side reveal of explanation
  const submitQuizBtn = document.getElementById('submitQuiz');
  if (submitQuizBtn) {
    submitQuizBtn.addEventListener('click', () => {
      // For each question block, find selected radio and show explanation if present
      const forms = document.querySelectorAll('[id^="quizForm"], form');
      // We target explanation divs by id pattern 'explain_<qid>'
      const explainDivs = document.querySelectorAll('[id^="explain_"]');
      explainDivs.forEach(div => { div.style.display = 'none'; });

      // Show explanation text — since explanation text is rendered into HTML at server side in template,
      // We will let the server-side code when building template define correct explanation content in hidden elements.
      // Simpler approach (already handled in template's inline JS in earlier version) — here we only show all explanation divs:
      explainDivs.forEach(div => { div.style.display = 'block'; });
      alert('Quiz submitted — explanations shown. (Server-side grading can be added later.)');
    });
  }
});
