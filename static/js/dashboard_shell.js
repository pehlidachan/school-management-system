// Phase 3.4: remember sidebar collapsed/expanded state.
(function () {
    function applySidebarState() {
        var saved = localStorage.getItem('schoolhubSidebarCollapsed');
        if (saved === '1') {
            document.body.classList.add('sidebar-collapsed');
        }
    }

    function initSidebarToggle() {
        var toggle = document.getElementById('hubSidebarToggle');
        if (!toggle) return;
        toggle.addEventListener('click', function () {
            document.body.classList.toggle('sidebar-collapsed');
            localStorage.setItem(
                'schoolhubSidebarCollapsed',
                document.body.classList.contains('sidebar-collapsed') ? '1' : '0'
            );
        });
    }

    applySidebarState();
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSidebarToggle);
    } else {
        initSidebarToggle();
    }
})();
