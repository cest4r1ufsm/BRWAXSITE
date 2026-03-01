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

    // Load CMS information text
    try {
        const infoResp = await fetch(`assets/information.json?t=${Date.now()}`);
        if (infoResp.ok) {
            const infoData = await infoResp.json();
            const textContainer = document.getElementById('info-text-container');
            if (textContainer && infoData.text) {
                textContainer.textContent = infoData.text;
            }
        }
    } catch (e) {
        console.warn("Could not load information.json");
    }

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

    // Use the exact order provided by the JSON (which the CMS configures manually)
    projects = metadata;

    // ── Branch: mobile feed vs desktop viewer ──
    if (config.isMobile) {
        renderMobileFeed();
    } else {
        renderSidebar();
        if (projects.length > 0) {
            selectProject(0);
        }
    }

    setupDetailsToggle();
    setupInfoModal();
    setupSearch();
}

// ===== SEARCH =====
function setupSearch() {
    const btn = document.getElementById('search-btn');
    const bar = document.getElementById('search-bar');
    const input = document.getElementById('search-input');
    if (!btn || !bar || !input) return;

    btn.addEventListener('click', (e) => {
        e.preventDefault();
        const isOpen = bar.classList.toggle('active');
        if (isOpen) {
            input.focus();
        } else {
            input.value = '';
            filterProjects('');
        }
    });

    input.addEventListener('input', () => {
        filterProjects(input.value);
    });
}

function filterProjects(query) {
    const q = query.trim().toLowerCase();

    // Mobile feed cards
    document.querySelectorAll('.feed-card').forEach(card => {
        const name = card.querySelector('.feed-project-name');
        if (!name) return;
        const match = !q || name.textContent.toLowerCase().includes(q);
        card.style.display = match ? '' : 'none';
        // Also hide/show the divider after this card
        const next = card.nextElementSibling;
        if (next && next.classList.contains('feed-divider')) {
            next.style.display = match ? '' : 'none';
        }
    });

    // Desktop sidebar items
    document.querySelectorAll('.sidebar-list-item').forEach(item => {
        const match = !q || item.textContent.toLowerCase().includes(q);
        item.style.display = match ? '' : 'none';
    });
}

// ===== MOBILE FEED (Instagram-style) =====
function renderMobileFeed() {
    const feed = document.getElementById('mobile-feed');
    if (!feed) return;
    feed.innerHTML = '';

    projects.forEach((proj, idx) => {
        const imgArray = proj.mobile_images && proj.mobile_images.length > 0
            ? proj.mobile_images
            : proj.web_images;

        if (!imgArray || imgArray.length === 0) return;

        const sorted = [...imgArray].sort((a, b) =>
            a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' })
        );

        // ── Card wrapper ──
        const card = document.createElement('div');
        card.className = 'feed-card';

        // ── Header ──
        const header = document.createElement('div');
        header.className = 'feed-card-header';

        const name = document.createElement('span');
        name.className = 'feed-project-name';
        name.textContent = proj.title;

        const counter = document.createElement('span');
        counter.className = 'feed-img-counter';
        counter.textContent = `1 / ${sorted.length}`;

        header.appendChild(name);
        header.appendChild(counter);
        card.appendChild(header);

        // ── Carousel ──
        const carousel = document.createElement('div');
        carousel.className = 'feed-carousel';

        const track = document.createElement('div');
        track.className = 'feed-carousel-track';

        sorted.forEach(filename => {
            const slide = document.createElement('div');
            slide.className = 'feed-slide';
            const img = document.createElement('img');
            img.src = filename.includes('/') ? filename : `assets/extracted_pdf_images/${proj.folder}/${filename}`;
            img.alt = proj.title;
            img.loading = 'lazy';
            img.onload = () => { img.style.opacity = '1'; };
            img.onerror = () => {
                console.warn('Image not found, hiding slide:', img.src);
                slide.remove();
            };
            slide.appendChild(img);
            track.appendChild(slide);
        });

        carousel.appendChild(track);

        // ── Dots ──
        const dots = document.createElement('div');
        dots.className = 'feed-dots';
        if (sorted.length > 15) dots.classList.add('compact');

        sorted.forEach((_, i) => {
            const dot = document.createElement('div');
            dot.className = 'feed-dot';
            if (i === 0) dot.classList.add('active');
            dots.appendChild(dot);
        });

        carousel.appendChild(dots);
        card.appendChild(carousel);

        // ── Scroll listener for dots + counter ──
        track.addEventListener('scroll', () => {
            const slideW = track.clientWidth;
            if (slideW === 0) return;
            const current = Math.round(track.scrollLeft / slideW);

            // Update counter
            counter.textContent = `${current + 1} / ${sorted.length}`;

            // Update dots
            dots.querySelectorAll('.feed-dot').forEach((d, di) => {
                d.classList.toggle('active', di === current);
            });
        }, { passive: true });

        feed.appendChild(card);

        // ── Divider between cards ──
        if (idx < projects.length - 1) {
            const divider = document.createElement('div');
            divider.className = 'feed-divider';
            feed.appendChild(divider);
        }
    });
}

// ===== DESKTOP: SIDEBAR + VIEWER (unchanged) =====
function setupInfoModal() {
    const infoBtn = document.getElementById('nav-info-btn');
    const workBtn = document.getElementById('nav-work-btn');
    const modal = document.getElementById('info-modal');
    const closeBtn = document.getElementById('close-info-btn');

    if (infoBtn && modal && closeBtn) {
        infoBtn.addEventListener('click', (e) => {
            e.preventDefault();
            modal.classList.add('active');
            if (workBtn) workBtn.classList.remove('active');
            infoBtn.classList.add('active');
        });

        const closeModal = () => {
            modal.classList.remove('active');
            infoBtn.classList.remove('active');
            if (workBtn) workBtn.classList.add('active');
        };

        closeBtn.addEventListener('click', closeModal);

        // Close on clicking outside
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal();
            }
        });
    }
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
                // Sort images alphanumerically by filename (e.g., 1.jpg, 2.jpg, 10.jpg)
                const sortedArray = [...imgArray].sort((a, b) => a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' }));

                sortedArray.forEach(filename => {
                    const slide = document.createElement('div');
                    slide.className = 'image-slide';
                    const img = document.createElement('img');
                    // Handle both CMS paths (starts with / or assets/) and old bare filenames
                    img.src = filename.includes('/') ? filename : `assets/extracted_pdf_images/${proj.folder}/${filename}`;
                    img.alt = proj.title;
                    img.onload = () => { img.style.opacity = '1'; };
                    img.onerror = () => {
                        console.warn('Image removed from CMS, hiding empty slide:', img.src);
                        slide.remove();
                    };
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

    // Enable manual navigation with arrows (desktop only)
    if (!config.isMobile) {
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
    }
});
