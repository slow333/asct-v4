document.addEventListener('DOMContentLoaded', function () {
    // 사이드바의 collapse 요소들을 가져옵니다.
    const sidebarCollapses = document.querySelectorAll('.col-md-3 .collapse');
    const storageKey = 'sidebarCollapseState';

    // localStorage에서 현재 상태를 가져오는 함수
    function getStoredState() {
        const storedState = localStorage.getItem(storageKey);
        return storedState ? JSON.parse(storedState) : [];
    }

    // localStorage에 상태를 저장하는 함수
    function saveState(openItems) {
        localStorage.setItem(storageKey, JSON.stringify(openItems));
    }

    // 페이지 로드 시 저장된 상태 복원
    const openItems = getStoredState();
    openItems.forEach(function(itemId) {
        const element = document.getElementById(itemId);
        if (element) {
            element.classList.add('show');
            const button = document.querySelector(`[data-bs-target="#${itemId}"]`);
            if (button) {
                button.setAttribute('aria-expanded', 'true');
            }
        }
    });

    // collapse 이벤트 리스너를 추가하여 상태 변경 시 저장
    sidebarCollapses.forEach(function (collapseEl) {
        collapseEl.addEventListener('shown.bs.collapse', function () {
            let openItems = getStoredState();
            if (!openItems.includes(this.id)) {
                openItems.push(this.id);
                saveState(openItems);
            }
        });

        collapseEl.addEventListener('hidden.bs.collapse', function () {
            let openItems = getStoredState();
            const index = openItems.indexOf(this.id);
            if (index > -1) {
                openItems.splice(index, 1);
                saveState(openItems);
            }
        });
    });

    // Sidebar show/hide toggle
    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
    const mainCol = document.getElementById('mainContentCol');
    const sidebarCol = document.getElementById('sidebarCol');
    const storageKeyHidden = 'sidebarHidden';

    function applySidebarState(hidden) {
        if (!mainCol || !sidebarCol || !sidebarToggleBtn) return;
        if (hidden) {
            sidebarCol.style.display = 'none';
            mainCol.classList.remove('col-md-10');
            mainCol.classList.add('col-md-12');
            sidebarToggleBtn.setAttribute('aria-expanded', 'false');
        } else {
            sidebarCol.style.display = '';
            mainCol.classList.remove('col-md-12');
            mainCol.classList.add('col-md-10');
            sidebarToggleBtn.setAttribute('aria-expanded', 'true');
        }
    }

    // initialize from localStorage
    try {
        const hidden = localStorage.getItem(storageKeyHidden) === 'true';
        applySidebarState(hidden);
    } catch (e) {}

    if (sidebarToggleBtn) {
        sidebarToggleBtn.addEventListener('click', function () {
            try {
                const currentlyHidden = localStorage.getItem(storageKeyHidden) === 'true';
                const toHide = !currentlyHidden;
                applySidebarState(toHide);
                localStorage.setItem(storageKeyHidden, toHide ? 'true' : 'false');
            } catch (e) {
                // fallback toggle
                const isHidden = sidebarCol.style.display === 'none';
                applySidebarState(!isHidden);
            }
        });
    }
});
