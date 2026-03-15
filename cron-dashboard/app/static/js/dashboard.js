document.addEventListener('DOMContentLoaded', function () {
  const base = document.querySelector('meta[name="base-url"]')?.content || '';

  // Toggle switches
  document.querySelectorAll('.task-toggle').forEach(function (el) {
    el.addEventListener('change', function () {
      const taskId = this.dataset.taskId;
      const row = document.getElementById('task-row-' + taskId);
      fetch(base + '/api/tasks/' + taskId + '/toggle', { method: 'POST' })
        .then(r => r.json())
        .then(data => {
          if (row) {
            row.classList.toggle('text-muted', !data.enabled);
          }
        })
        .catch(() => location.reload());
    });
  });

  // Run Now buttons
  document.querySelectorAll('.run-now-btn').forEach(function (el) {
    el.addEventListener('click', function () {
      const taskId = this.dataset.taskId;
      const btn = this;
      btn.disabled = true;
      btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
      fetch(base + '/api/tasks/' + taskId + '/run', { method: 'POST' })
        .then(r => r.json())
        .then(() => {
          btn.innerHTML = '<i class="bi bi-check"></i>';
          setTimeout(() => location.reload(), 2000);
        })
        .catch(() => {
          btn.disabled = false;
          btn.innerHTML = '<i class="bi bi-play-fill"></i>';
        });
    });
  });

  // Delete buttons
  const deleteModal = document.getElementById('deleteModal');
  if (deleteModal) {
    const modal = new bootstrap.Modal(deleteModal);
    document.querySelectorAll('.delete-btn').forEach(function (el) {
      el.addEventListener('click', function () {
        const taskId = this.dataset.taskId;
        const taskName = this.dataset.taskName;
        document.getElementById('deleteTaskName').textContent = taskName;
        document.getElementById('deleteForm').action = base + '/tasks/' + taskId + '/delete';
        modal.show();
      });
    });
  }
});
