document.addEventListener('DOMContentLoaded', () => {

    // Fonction pour animer le cercle de progression
    const animateProgressCircle = (circle, text, percentage) => {
        const radius = circle.r.baseVal.value;
        const circumference = 2 * Math.PI * radius;
        const offset = circumference - (percentage / 100) * circumference;

        circle.style.strokeDasharray = `${circumference} ${circumference}`;
        circle.style.strokeDashoffset = circumference;

        circle.getBoundingClientRect(); // Force un reflow

        circle.style.transition = 'stroke-dashoffset 1.5s ease-in-out';
        circle.style.strokeDashoffset = offset;

        let currentPercentage = 0;
        const interval = setInterval(() => {
            if (currentPercentage >= percentage) {
                clearInterval(interval);
                text.textContent = `${percentage}%`;
            } else {
                text.textContent = `${currentPercentage}%`;
                currentPercentage++;
            }
        }, 15);
    };

    // Fonction pour animer la barre de progression
    const animateProgressBar = (fill, label, percentage) => {
        fill.style.transition = 'width 1.5s ease-in-out';
        fill.style.width = `${percentage}%`;
        label.textContent = `${percentage}%`;
    };

    // --- 1. Animation du cercle de participation ---
    const participationContainer = document.querySelector('.progress-circle');
    const partNumElem = document.getElementById('part-num');
    const electeursElem = document.getElementById('electeurs');

    let partNum = 0; // Déclaration de la variable en dehors de la condition
    if (participationContainer && partNumElem && electeursElem) {
        partNum = parseInt(partNumElem.textContent);
        const electeurs = parseInt(electeursElem.textContent);

        if (!isNaN(partNum) && !isNaN(electeurs) && electeurs > 0) {
            const participationPercentage = Math.round((partNum / electeurs) * 100);
            const circle = participationContainer.querySelector('.progress-ring-circle');
            const text = participationContainer.querySelector('.progress-text');

            if (circle && text) {
                animateProgressCircle(circle, text, participationPercentage);
            }
        }
    }

    // --- 2. Animation des barres de progression des candidats ---
    // Le total des participants (partNum) est utilisé ici comme base pour les pourcentages.

    document.querySelectorAll('.progress-bar-container').forEach(container => {
        const votes = parseInt(container.closest('.card').querySelector('.vote-count').textContent);

        // On vérifie si partNum est valide et supérieur à 0 pour éviter la division par zéro
        if (partNum > 0) {
            // Le pourcentage est calculé par rapport au nombre total de participants (partNum)
            const candidatePercentage = Math.round((votes / partNum) * 100);
            const fill = container.querySelector('.progress-fill');
            const label = container.querySelector('.progress-label');

            if (fill && label) {
                animateProgressBar(fill, label, candidatePercentage);
            }
        } else {
            // Si partNum est 0, le pourcentage est 0
            const fill = container.querySelector('.progress-fill');
            const label = container.querySelector('.progress-label');
            if (fill && label) {
                animateProgressBar(fill, label, 0);
            }
        }
    });
});