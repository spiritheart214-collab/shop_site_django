// static/js/toasts.js
document.addEventListener('DOMContentLoaded', function() {
    // Находим все тосты
    const toasts = document.querySelectorAll('[data-toast]');

    toasts.forEach(toast => {
        // Автоматическое закрытие через 3 секунды
        setTimeout(() => {
            closeToast(toast);
        }, 3000);

        // Закрытие по кнопке
        const closeBtn = toast.querySelector('[data-toast-close]');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                closeToast(toast);
            });
        }

        // Закрытие по клику вне тоста (опционально)
        toast.addEventListener('click', function(e) {
            if (e.target === toast) {
                closeToast(toast);
            }
        });
    });

    function closeToast(toast) {
        toast.style.animation = 'slideIn 0.3s reverse';
        setTimeout(() => {
            toast.remove();

            // Если не осталось тостов, удаляем контейнер (опционально)
            const container = document.querySelector('.toast-container');
            if (container && container.children.length === 0) {
                container.remove();
            }
        }, 300);
    }
});