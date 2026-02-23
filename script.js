// ===== GLOBAL CONFIG & MOBILE DETECTION =====
const isMobileDevice = () => window.matchMedia("(max-width: 768px)").matches || /Mobi|Android/i.test(navigator.userAgent);
const config = {
    isMobile: isMobileDevice(),
    folder: isMobileDevice() ? 'grid_mobile' : 'grid_web'
};

let projects = [];
let currentIndex = 0;

// Intro fade
(function runIntro() {
    const overlay = document.getElementById('intro-overlay');
    if (!overlay) return;
    setTimeout(() => {
        overlay.classList.add('exit');
        setTimeout(() => overlay.remove(), 600);
    }, 1300);
})();

async function init() {
    let metadata = [];

    // Load metadata - This is now the source of truth for projects and their images directly from the folders
    try {
        const resp = await fetch(`assets/projects_manifest.json?t=${Date.now()}`);
        if (resp.ok) {
            let json = await resp.json();
            metadata = json.projects ? json.projects : json;
        }
    } catch (e) {
        console.warn("Could not load projects_manifest.json");
    }

    if (metadata.length === 0) {
        console.error("No projects found in metadata");
        return;
    }

    // Projects ALREADY sorted alphabetically in the generator but sorting again to be safe
    projects = metadata.sort((a, b) => a.title.localeCompare(b.title));

    renderSidebar();

    if (projects.length > 0) {
        selectProject(0);
    }

    setupDetailsToggle();
}

function renderSidebar() {
    const container = document.getElementById('sidebar-projects');
    if (!container) return;
    container.innerHTML = '';

    projects.forEach((proj, idx) => {
        const div = document.createElement('div');
        div.className = 'sidebar-list-item';
        div.dataset.index = idx;
        div.textContent = proj.title;

        div.addEventListener('click', () => {
            selectProject(idx);
            div.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        });
        container.appendChild(div);
    });
}

function selectProject(index) {
    currentIndex = index;
    const proj = projects[index];

    // Update main display container
    const container = document.getElementById('image-scroll-container');
    if (container) {
        // Fade out existing content
        container.style.opacity = '0';

        setTimeout(() => {
            container.innerHTML = ''; // Clear existing images

            // Determine which array of images to pull based on device
            const imgArray = config.isMobile && proj.mobile_images && proj.mobile_images.length > 0
                ? proj.mobile_images
                : proj.web_images;

            // Determine subfolder
            const subfolder = config.isMobile && proj.mobile_images && proj.mobile_images.length > 0
                ? "mobile"
                : "web";

            if (imgArray && imgArray.length > 0) {
                imgArray.forEach(filename => {
                    const slide = document.createElement('div');
                    slide.className = 'image-slide';
                    const img = document.createElement('img');
                    // Handle both CMS paths (starts with / or assets/) and old bare filenames
                    img.src = filename.includes('/') ? filename : `assets/extracted_pdf_images/${proj.folder}/${filename}`;
                    img.alt = proj.title;
                    img.onload = () => { img.style.opacity = '1'; };
                    slide.appendChild(img);
                    container.appendChild(slide);
                });
            } else {
                const fallbackImg = document.createElement('p');
                fallbackImg.textContent = "Images are not currently grouped in 'web'/'mobile' subfolders for this project.";
                fallbackImg.style.opacity = '0.5';
                fallbackImg.style.textAlign = 'center';
                fallbackImg.style.marginTop = '40px';
                container.appendChild(fallbackImg);
                setTimeout(() => fallbackImg.style.opacity = '1', 50);
            }
            // Fade container back in
            container.style.opacity = '1';

            // Scroll to the top of the container
            container.scrollTop = 0;
        }, 300);
    }

    const titleEl = document.getElementById('current-project-title');
    if (titleEl) titleEl.textContent = proj.title;

    const counterEl = document.getElementById('project-counter');
    if (counterEl) counterEl.textContent = `${index + 1} / ${projects.length}`;

    // Update details panel content
    const yearEl = document.getElementById('detail-year');
    if (yearEl) yearEl.textContent = proj.year || "2024";

    const servicesEl = document.getElementById('detail-services');
    if (servicesEl) servicesEl.textContent = proj.services || "VISUAL CONTENT";

    const descEl = document.getElementById('detail-description');
    if (descEl) descEl.textContent = proj.description || "Sem descrição disponível.";

    // Update sidebar active state
    document.querySelectorAll('.sidebar-list-item').forEach((el, idx) => {
        if (idx === index) el.classList.add('active');
        else el.classList.remove('active');
    });

    // Auto-close details if open
    const panel = document.getElementById('details-panel');
    if (panel) panel.classList.remove('active');

    const btn = document.querySelector('.details-btn');
    if (btn) btn.textContent = 'DETAILS';
}

function setupDetailsToggle() {
    const btn = document.querySelector('.details-btn');
    const panel = document.getElementById('details-panel');

    if (btn && panel) {
        btn.addEventListener('click', () => {
            const isActive = panel.classList.toggle('active');
            btn.textContent = isActive ? 'CLOSE' : 'DETAILS';
        });
    }
}

document.addEventListener("DOMContentLoaded", () => {
    init();

    // Enable manual navigation with arrows
    const scrollContainer = document.getElementById('image-scroll-container');
    const navLeft = document.getElementById('nav-left');
    const navRight = document.getElementById('nav-right');

    if (scrollContainer && navLeft && navRight) {
        let isScrolling = false;

        const scrollImages = (direction) => {
            if (isScrolling) return;
            isScrolling = true;

            // Scroll by exactly one slide's width
            const scrollAmount = scrollContainer.clientWidth;

            scrollContainer.scrollBy({
                left: direction * scrollAmount,
                behavior: 'smooth'
            });

            setTimeout(() => {
                isScrolling = false;
            }, 500); // Wait for smooth scroll to finish
        };

        navLeft.addEventListener('click', () => scrollImages(-1));
        navRight.addEventListener('click', () => scrollImages(1));

        // Disable horizontal wheel scrolling so arrows are the only way
        scrollContainer.addEventListener('wheel', (evt) => {
            if (Math.abs(evt.deltaX) > Math.abs(evt.deltaY)) {
                evt.preventDefault();
            }
        }, { passive: false });
    }
});
