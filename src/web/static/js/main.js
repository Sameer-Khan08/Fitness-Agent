/**
 * TrainWise AI — client-side interactions
 */

document.addEventListener('DOMContentLoaded', () => {
    initDayTabs();
});

function initDayTabs() {
    const tabs = document.querySelectorAll('[data-day-tab]');
    const panels = document.querySelectorAll('[data-day-panel]');

    if (!tabs.length || !panels.length) return;

    tabs.forEach((tab) => {
        tab.addEventListener('click', () => {
            const index = tab.getAttribute('data-day-tab');

            tabs.forEach((t) => t.classList.remove('active'));
            tab.classList.add('active');

            panels.forEach((panel) => {
                const panelIndex = panel.getAttribute('data-day-panel');
                if (panelIndex === index) {
                    panel.classList.add('active');
                    panel.removeAttribute('hidden');
                } else {
                    panel.classList.remove('active');
                    panel.setAttribute('hidden', '');
                }
            });
        });
    });
}
