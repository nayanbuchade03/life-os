document.addEventListener('DOMContentLoaded', () => {
    const modals = document.querySelectorAll('.modal-overlay');
    const openModalBtns = document.querySelectorAll('[data-modal-target]');
    const closeBtns = document.querySelectorAll('.close-modal, [data-modal-close]');

    openModalBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const target = document.querySelector(btn.dataset.modalTarget);
            
            if (btn.hasAttribute('data-edit-task')) {
                const form = target.querySelector('form');
                form.action = `/tasks/edit/${btn.dataset.id}`;
                form.querySelector('[name="title"]').value = btn.dataset.title;
                form.querySelector('[name="category"]').value = btn.dataset.category;
                form.querySelector('[name="priority"]').value = btn.dataset.priority;
                form.querySelector('[name="frequency"]').value = btn.dataset.frequency;
                form.querySelector('[name="start_date"]').value = btn.dataset.start;
                form.querySelector('[name="description"]').value = btn.dataset.description || '';
            }

            if (target) target.classList.add('active');
        });
    });

    closeBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            btn.closest('.modal-overlay').classList.remove('active');
        });
    });

    modals.forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.classList.remove('active');
        });
    });
});