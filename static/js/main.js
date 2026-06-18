/**
 * TrainWise AI — client-side interactions
 */

document.addEventListener('DOMContentLoaded', () => {
    initDayTabs();
    initFlashMessages();
});

function initDayTabs() {
    const tabs = document.querySelectorAll('[data-day-tab]');
    const panels = document.querySelectorAll('[data-day-panel]');

    if (!tabs.length || !panels.length) return;

    // Check if there's a saved tab index in sessionStorage (useful after page reload like image gen)
    const savedTabIndex = sessionStorage.getItem('activeDayTab');
    
    if (savedTabIndex !== null) {
        let found = false;
        tabs.forEach(t => {
            if (t.getAttribute('data-day-tab') === savedTabIndex) {
                found = true;
            }
        });
        
        if (found) {
            activateTab(savedTabIndex, tabs, panels);
        }
    }

    tabs.forEach((tab) => {
        tab.addEventListener('click', () => {
            const index = tab.getAttribute('data-day-tab');
            activateTab(index, tabs, panels);
        });
    });
}

function activateTab(index, tabs, panels) {
    tabs.forEach((t) => {
        if (t.getAttribute('data-day-tab') === index) {
            t.classList.add('active');
            t.setAttribute('aria-selected', 'true');
        } else {
            t.classList.remove('active');
            t.setAttribute('aria-selected', 'false');
        }
    });

    panels.forEach((panel) => {
        const panelIndex = panel.getAttribute('data-day-panel');
        if (panelIndex === index) {
            panel.classList.add('active');
            panel.style.display = 'block';
            panel.removeAttribute('hidden');
            panel.setAttribute('aria-hidden', 'false');
        } else {
            panel.classList.remove('active');
            panel.style.display = 'none';
            panel.setAttribute('hidden', '');
            panel.setAttribute('aria-hidden', 'true');
        }
    });

    // Save active tab
    sessionStorage.setItem('activeDayTab', index);
}

function initFlashMessages() {
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(flash => {
        // Create dismiss button
        const closeBtn = document.createElement('span');
        closeBtn.innerHTML = '&times;';
        closeBtn.style.float = 'right';
        closeBtn.style.cursor = 'pointer';
        closeBtn.style.fontSize = '1.2rem';
        closeBtn.style.lineHeight = '1';
        closeBtn.style.marginLeft = '1rem';
        closeBtn.style.opacity = '0.7';
        
        closeBtn.addEventListener('click', () => {
            flash.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            flash.style.opacity = '0';
            flash.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                flash.remove();
            }, 300);
        });
        
        closeBtn.addEventListener('mouseover', () => closeBtn.style.opacity = '1');
        closeBtn.addEventListener('mouseout', () => closeBtn.style.opacity = '0.7');
        
        flash.insertBefore(closeBtn, flash.firstChild);
    });
}
