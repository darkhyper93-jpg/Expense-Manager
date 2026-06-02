/**
 * Premium UI: toasts, loading spinners, confirm dialogs, nav.
 */

(function () {
    'use strict';

    function dismissToast(toast) {
        toast.classList.add('toast-out');
        setTimeout(() => toast.remove(), 200);
    }

    function initToasts() {
        document.querySelectorAll('.toast').forEach((toast) => {
            const closeBtn = toast.querySelector('.toast-close');
            if (closeBtn) {
                closeBtn.addEventListener('click', () => dismissToast(toast));
            }
            setTimeout(() => dismissToast(toast), 5000);
        });
    }

    function initNav() {
        const toggle = document.getElementById('navToggle');
        const links = document.getElementById('navLinks');
        if (!toggle || !links) return;

        toggle.addEventListener('click', () => {
            links.classList.toggle('open');
        });

        links.querySelectorAll('a').forEach((link) => {
            link.addEventListener('click', () => links.classList.remove('open'));
        });
    }

    function initConfirmDialogs() {
        document.querySelectorAll('[data-confirm]').forEach((form) => {
            form.addEventListener('submit', (e) => {
                const message = form.getAttribute('data-confirm');
                if (!window.confirm(message)) {
                    e.preventDefault();
                }
            });
        });
    }

    function setButtonLoading(btn, loading) {
        if (!btn) return;
        if (loading) {
            btn.classList.add('is-loading');
            btn.disabled = true;
            if (!btn.querySelector('.btn-spinner')) {
                const spinner = document.createElement('span');
                spinner.className = 'btn-spinner';
                spinner.setAttribute('aria-hidden', 'true');
                btn.appendChild(spinner);
            }
        }
    }

    function initLoadingStates() {
        document.querySelectorAll('form[data-loading]').forEach((form) => {
            form.addEventListener('submit', () => {
                form.classList.add('is-loading');
                setButtonLoading(form.querySelector('button[type="submit"]'), true);
            });
        });
    }

    function initDefaultDate() {
        const dateInput = document.getElementById('date');
        if (dateInput && !dateInput.value) {
            dateInput.value = new Date().toISOString().split('T')[0];
        }
    }

    function initLanguageSelector() {
        document.querySelectorAll('.lang-selector').forEach((selector) => {
            const toggle = selector.querySelector('.lang-toggle');
            const menu = selector.querySelector('.lang-menu');
            if (!toggle || !menu) return;

            toggle.addEventListener('click', (e) => {
                e.stopPropagation();
                const isOpen = selector.classList.toggle('open');
                toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
            });
        });

        document.addEventListener('click', () => {
            document.querySelectorAll('.lang-selector.open').forEach((selector) => {
                selector.classList.remove('open');
                const toggle = selector.querySelector('.lang-toggle');
                if (toggle) toggle.setAttribute('aria-expanded', 'false');
            });
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        initNav();
        initToasts();
        initConfirmDialogs();
        initLoadingStates();
        initDefaultDate();
        initLanguageSelector();
    });
})();
