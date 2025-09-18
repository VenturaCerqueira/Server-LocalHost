// servidor_app/static/js/main.js

document.addEventListener('DOMContentLoaded', function () {
    // Função para criar e exibir alertas dinamicamente com animação
    const showAlert = (message, category) => {
        const container = document.getElementById('alert-container');
        if (!container) return;

        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${category} alert-dismissible fade show animated fadeInDown`;
        alertDiv.role = 'alert';
        alertDiv.style.animationDuration = '0.5s';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        container.appendChild(alertDiv);

        // Auto-dismiss with fade out animation
        setTimeout(() => {
            alertDiv.classList.replace('fadeInDown', 'fadeOutUp');
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alertDiv);
                bsAlert.close();
            }, 500);
        }, 5000);
    };

    // Lógica de atualização de banco de dados com AJAX
    document.querySelectorAll('.btn-update-db').forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            const dbName = this.dataset.dbName;
            
            // Elementos do botão
            const spinner = this.querySelector('.spinner-border');
            const icon = this.querySelector('.icon-default');
            const btnText = this.querySelector('.btn-text');

            // Ativar estado de carregamento
            this.disabled = true;
            spinner.style.display = 'inline-block';
            icon.style.display = 'none';
            btnText.textContent = 'Atualizando...';

            try {
                const response = await fetch(`/update_database/${dbName}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                const result = await response.json();

                if (response.ok) {
                    showAlert(result.message, 'success');
                    // Add success animation
                    this.classList.add('pulse');
                    setTimeout(() => this.classList.remove('pulse'), 1000);
                } else {
                    showAlert(`Erro: ${result.message}`, 'danger');
                    // Add error animation
                    this.classList.add('shake');
                    setTimeout(() => this.classList.remove('shake'), 1000);
                }

            } catch (error) {
                console.error('Erro na requisição:', error);
                showAlert('Erro de conexão com o servidor. Verifique o console para mais detalhes.', 'danger');
                // Add error animation
                this.classList.add('shake');
                setTimeout(() => this.classList.remove('shake'), 1000);
            } finally {
                // Restaurar estado do botão
                this.disabled = false;
                spinner.style.display = 'none';
                icon.style.display = 'inline-block';
                btnText.textContent = 'Atualizar';
            }
        });
    });

// Common elements and functions for all pages
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebar-toggle');
const mainContent = document.getElementById('main-content');
const loadingOverlay = document.getElementById('loading-overlay');
const searchModal = document.getElementById('search-modal');
const searchOverlay = document.getElementById('search-overlay');
const searchToggle = document.getElementById('search-toggle');
const searchInput = document.getElementById('search-input');
const searchResultsList = document.getElementById('search-results-list');
const propertiesModal = document.getElementById('propertiesModal');
const themeToggle = document.getElementById('theme-toggle');
const themeIcon = themeToggle ? themeToggle.querySelector('i') : null;

let isSidebarCollapsed = false;

// Lógica do Sidebar
const updateSidebarState = () => {
    if (isSidebarCollapsed) {
        document.body.classList.add('body-collapsed');
    } else {
        document.body.classList.remove('body-collapsed');
    }
};

/* Removed sidebar toggle functionality to disable collapsing sidebar */
if (sidebarToggle) {
    sidebarToggle.style.display = 'none'; // Hide the toggle button
}

// Fix back button in sistemas.html
const backBtn = document.getElementById('back-btn');
if (backBtn) {
    backBtn.addEventListener('click', () => {
        window.history.back();
    });
}

    // Lógica do Theme Toggle
    const isDarkMode = localStorage.getItem('dark-mode') === 'true';

    const applyTheme = (isDark) => {
        if (isDark) {
            document.documentElement.classList.add('dark-mode');
            if (themeIcon) themeIcon.className = 'bi bi-moon-fill';
        } else {
            document.documentElement.classList.remove('dark-mode');
            if (themeIcon) themeIcon.className = 'bi bi-sun-fill';
        }
    };

    applyTheme(isDarkMode);

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const newTheme = document.documentElement.classList.toggle('dark-mode');
            localStorage.setItem('dark-mode', newTheme);
            applyTheme(newTheme);

            // Add animation to theme toggle
            themeToggle.classList.add('bounceIn');
            setTimeout(() => themeToggle.classList.remove('bounceIn'), 800);
        });
    }

    // Função para atualizar data e hora
    const updateDateTime = () => {
        const now = new Date();
        const days = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado'];
        const dayName = days[now.getDay()];
        const dateStr = now.toLocaleDateString('pt-BR');
        const timeStr = now.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
        const display = `${dayName}, ${dateStr} ${timeStr}`;
        const element = document.getElementById('date-time-text');
        if (element) element.textContent = display;
    };

    // Atualizar data e hora inicialmente e a cada minuto
    updateDateTime();
    setInterval(updateDateTime, 60000);

    // Lógica do Search
    const showSearchModal = () => {
        if (searchModal && searchOverlay) {
            searchModal.classList.add('show');
            searchOverlay.classList.add('show');
            if (searchInput) searchInput.focus();
        }
    };

    const hideSearchModal = () => {
        if (searchModal && searchOverlay) {
            searchModal.classList.remove('show');
            searchOverlay.classList.remove('show');
            if (searchInput) searchInput.value = '';
            if (searchResultsList) searchResultsList.innerHTML = '';
        }
    };

    if (searchToggle) {
        searchToggle.addEventListener('click', () => {
            showSearchModal();

            // Add animation to search toggle
            searchToggle.classList.add('bounceIn');
            setTimeout(() => searchToggle.classList.remove('bounceIn'), 800);
        });
    }
    if (searchOverlay) {
        searchOverlay.addEventListener('click', hideSearchModal);
    }
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'k') {
            e.preventDefault();
            showSearchModal();
        }
        if (e.key === 'Escape') {
            hideSearchModal();
        }
    });

    let searchTimeout;
    if (searchInput) {
        searchInput.addEventListener('input', () => {
            clearTimeout(searchTimeout);
            const query = searchInput.value;
            if (query.length > 1) {
                searchTimeout = setTimeout(async () => {
                    const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
                    const results = await response.json();
                    if (searchResultsList) {
                        searchResultsList.innerHTML = '';
                        if (results.length > 0) {
                            results.forEach(item => {
                                const li = document.createElement('li');

                                let iconClass;
                                let iconColor = 'var(--text-color)';
                                if (item.is_dir) {
                                    iconClass = 'bi-folder-fill';
                                } else {
                                    const fileExtension = item.nome.split('.').pop().toLowerCase();
                                    switch (fileExtension) {
                                        case 'pdf': iconClass = 'bi-filetype-pdf'; iconColor = '#dc3545'; break;
                                        case 'doc': case 'docx': iconClass = 'bi-filetype-doc'; iconColor = '#007bff'; break;
                                        case 'txt': iconClass = 'bi-filetype-txt'; iconColor = '#6c757d'; break;
                                        case 'jpg': case 'jpeg': case 'png': case 'gif': case 'svg': iconClass = 'bi-file-earmark-image-fill'; iconColor = '#28a745'; break;
                                        case 'zip': iconClass = 'bi-file-earmark-zip-fill'; iconColor = '#17a2b8'; break;
                                        default: iconClass = 'bi-file-earmark-text-fill'; break;
                                    }
                                }

                                li.innerHTML = `
                                <a href="${item.is_dir ? '/browse/' + item.path : '/download/' + item.path}" class="search-results-item nav-link-loader">
                                    <i class="bi ${iconClass} me-3 fs-5" style="color: ${iconColor};"></i>
                                    <span class="d-flex flex-column me-auto">
                                        <span class="fw-bold">${item.nome}</span>
                                        <small class="text-muted">${item.path}</small>
                                    </span>
                                </a>
                                `;
                                searchResultsList.appendChild(li);
                            });
                        } else {
                            searchResultsList.innerHTML = `<li class="list-group-item text-muted p-3">Nenhum resultado encontrado.</li>`;
                        }
                    }
                }, 300);
            } else {
                if (searchResultsList) searchResultsList.innerHTML = '';
            }
        });
    }

    // Lógica do Loading Overlay
    document.body.addEventListener('click', function(e) {
        const link = e.target.closest('.nav-link-loader');
        if (link) {
            const href = link.getAttribute('href');
            if (href && href !== '#') {
                e.preventDefault();
                if (loadingOverlay) loadingOverlay.classList.add('show');
                window.location.href = href;
            }
        }
    });

    // Lógica do Properties Modal
    if (propertiesModal) {
        propertiesModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const name = button.getAttribute('data-name');
            const type = button.getAttribute('data-type');
            const size = button.getAttribute('data-size');
            const sizeBytes = button.getAttribute('data-size-bytes');
            const modified = button.getAttribute('data-modified');
            const created = button.getAttribute('data-created');
            const fileCount = button.getAttribute('data-file-count');
            const folderCount = button.getAttribute('data-folder-count');
            const createdBy = button.getAttribute('data-created-by');
            const updatedBy = button.getAttribute('data-updated-by');

            document.getElementById('prop-name').textContent = name;
            document.getElementById('prop-type').textContent = type;
            document.getElementById('prop-modified').textContent = modified;
            document.getElementById('prop-created').textContent = created;
            document.getElementById('prop-created-by').textContent = createdBy;
            document.getElementById('prop-updated-by').textContent = updatedBy;

            const fileSizeRow = document.getElementById('file-size-row');
            const fileSizeInBytesRow = document.getElementById('file-size-bytes-row');
            const folderCountRow = document.getElementById('folder-count-row');

            if (type === 'Arquivo') {
                if (fileSizeRow) fileSizeRow.style.display = '';
                if (fileSizeInBytesRow) fileSizeInBytesRow.style.display = '';
                if (folderCountRow) folderCountRow.style.display = 'none';
                document.getElementById('prop-size').textContent = size;
                document.getElementById('prop-size-bytes').textContent = `${sizeBytes} bytes`;
            } else {
                if (fileSizeRow) fileSizeRow.style.display = 'none';
                if (fileSizeInBytesRow) fileSizeInBytesRow.style.display = 'none';
                if (folderCountRow) folderCountRow.style.display = '';
                document.getElementById('prop-counts').textContent = `${fileCount} arquivos, ${folderCount} pastas`;
            }
        });
    }

    // File system specific code
    const fileSystemView = document.getElementById('file-system-view');
    if (!fileSystemView) {
        return;
    }

    const pastasData = JSON.parse(fileSystemView.dataset.pastas || '[]');
    const allFiles = Array.isArray(pastasData) ? pastasData : [];
    let currentFilteredFiles = [...allFiles];
    let currentLayout = localStorage.getItem('layout') || 'list';
    let currentFilters = { type: 'all', date: 'all' };

    const fileListContainer = document.getElementById('file-list-container');
    const layoutToggle = document.getElementById('layout-toggle');

    // Lógica do Layout
    const applyLayout = (layout) => {
        if (!fileListContainer || !layoutToggle) return;
        const icon = layoutToggle.querySelector('i');
        if (layout === 'grid') {
            fileListContainer.classList.remove('list-group', 'list-group-flush');
            fileListContainer.classList.add('grid-view');
            if (icon) icon.className = 'bi bi-list';
        } else {
            fileListContainer.classList.remove('grid-view');
            fileListContainer.classList.add('list-group', 'list-group-flush');
            if (icon) icon.className = 'bi bi-grid-3x3-gap';
        }
        localStorage.setItem('layout', layout);
        renderFiles(currentFilteredFiles);

        // Add animation to layout toggle
        layoutToggle.classList.add('bounceIn');
        setTimeout(() => layoutToggle.classList.remove('bounceIn'), 800);
    };

    if (layoutToggle) {
        layoutToggle.addEventListener('click', () => {
            const newLayout = currentLayout === 'grid' ? 'list' : 'grid';
            currentLayout = newLayout;
            applyLayout(newLayout);
        });
    }

    const renderFiles = (files) => {
        if (!fileListContainer) return;
        fileListContainer.innerHTML = '';
        if (files.length === 0) {
            fileListContainer.innerHTML = `
                <div class="empty-folder">
                    <i class="bi bi-box-seam"></i>
                    <p class="mb-0">Nenhum item encontrado com os filtros selecionados.</p>
                </div>
            `;
            return;
        }

        // Determine download prefix based on current page
        let downloadPrefix = '';
        if (window.location.pathname.startsWith('/dropbox')) {
            downloadPrefix = 'Dropbox/';
        } else if (window.location.pathname.startsWith('/sistemas')) {
            downloadPrefix = 'Sistemas/';
        } else if (window.location.pathname.startsWith('/licitacoes')) {
            downloadPrefix = 'Licitações/';
        }

        files.forEach(item => {
            const itemElement = document.createElement('div');

            const isGrid = currentLayout === 'grid';
            if (isGrid) {
                itemElement.classList.add('grid-item-card');
            } else {
                itemElement.classList.add('list-group-item', 'px-0', 'list-item');
            }

            let iconClass;
            let iconColor = 'var(--text-color)';
            let lockIcon = '';
            if (item.is_dir) {
                iconClass = 'bi-folder-fill';
                iconColor = 'var(--primary-color)';
                if (item.is_secure) {
                    lockIcon = '<i class="bi bi-lock-fill ms-1" style="color: var(--warning-color); font-size: 0.8em;" title="Pasta protegida por senha"></i>';
                }
            } else {
                switch (item.type) {
                    case 'pdf': iconClass = 'bi-filetype-pdf'; iconColor = '#dc3545'; break;
                    case 'doc': case 'docx': case 'txt': iconClass = 'bi-filetype-doc'; iconColor = '#007bff'; break;
                    case 'jpg': case 'jpeg': case 'png': case 'gif': case 'svg': iconClass = 'bi-file-earmark-image-fill'; iconColor = '#28a745'; break;
                    case 'zip': iconClass = 'bi-file-earmark-zip-fill'; iconColor = '#17a2b8'; break;
                    default: iconClass = 'bi-file-earmark-text-fill'; iconColor = '#6c757d'; break;
                }
            }

            const isDropbox = window.location.pathname.includes('/dropbox');
            const folderLink = isDropbox ? `/dropbox?path=${item.path}` : `/browse/${item.path}`;

            if (isGrid) {
                itemElement.innerHTML = `
                    <div class="grid-item-preview">
                        <a href="${item.is_dir ? folderLink : '#'}" class="nav-link-loader">
                            <i class="bi ${iconClass} preview-icon" style="color: ${iconColor};"></i>
                        </a>
                    </div>
                    <div class="grid-item-info">
                        <i class="bi ${iconClass} item-icon" style="color: ${iconColor};"></i>
                        <span class="grid-item-filename">${item.nome}${lockIcon}</span>
                        <div class="dropdown grid-item-actions">
                            <button class="btn btn-sm btn-link dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                <i class="bi bi-three-dots-vertical"></i>
                            </button>
                            <ul class="dropdown-menu dropdown-menu-end">
                                <li>
                                    <button class="dropdown-item move-item-btn" type="button" data-item-path="${item.path}" data-item-name="${item.nome}">
                                        <i class="bi bi-folder-symlink me-2"></i>Mover
                                    </button>
                                </li>
                                <li>
                                    <a class="dropdown-item" href="/download/${downloadPrefix}${item.path}">
                                        <i class="bi bi-download me-2"></i>Download
                                    </a>
                                </li>
                                <li>
                                    <button class="dropdown-item" type="button" data-bs-toggle="modal" data-bs-target="#propertiesModal"
                                        data-name="${item.nome}" data-modified="${item.modified_at}" data-created="${item.created_at}" data-type="${item.is_dir ? 'Pasta' : 'Arquivo'}"
                                        data-file-count="${item.file_count}" data-folder-count="${item.folder_count}"
                                        data-size="${item.size}" data-size-bytes="${item.size_bytes}" data-file-type="${item.type}"
                                        data-created-by="${item.created_by || 'N/A'}" data-updated-by="${item.updated_by || 'N/A'}">
                                        <i class="bi bi-info-circle me-2"></i>Propriedades
                                    </button>
                                </li>
                            </ul>
                        </div>
                    </div>
                `;
            } else {
                itemElement.innerHTML = `
                    <a href="${item.is_dir ? folderLink : '#'}" class="list-item-link nav-link-loader">
                        <i class="bi ${iconClass} me-3 fs-5" style="color: ${iconColor};"></i>
                        <span class="d-flex flex-column me-auto">
                            <span class="fw-bold text-primary">${item.nome}${lockIcon}</span>
                            <small class="text-muted folder-size-placeholder">
                                ${item.is_dir ? `${item.file_count} arquivos, ${item.folder_count} pastas` : item.size}
                            </small>
                        </span>
                    </a>
                    <div class="item-actions-container dropdown">
                        <button class="btn btn-sm btn-link dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="bi bi-three-dots-vertical"></i>
                        </button>
                        <ul class="dropdown-menu dropdown-menu-end">
                            <li>
                                <button class="dropdown-item move-item-btn" type="button" data-item-path="${item.path}" data-item-name="${item.nome}">
                                    <i class="bi bi-folder-symlink me-2"></i>Mover
                                </button>
                            </li>
                            <li>
                                <a class="dropdown-item" href="/download/${downloadPrefix}${item.path}">
                                    <i class="bi bi-download me-2"></i>Baixar
                                </a>
                            </li>
                            <li>
                                <button class="dropdown-item" type="button" data-bs-toggle="modal" data-bs-target="#propertiesModal"
                                    data-name="${item.nome}" data-modified="${item.modified_at}" data-created="${item.created_at}" data-type="${item.is_dir ? 'Pasta' : 'Arquivo'}"
                                    data-file-count="${item.file_count}" data-folder-count="${item.folder_count}"
                                    data-size="${item.size}" data-size-bytes="${item.size_bytes}" data-file-type="${item.type}"
                                    data-created-by="${item.created_by || 'N/A'}" data-updated-by="${item.updated_by || 'N/A'}">
                                    <i class="bi bi-info-circle me-2"></i>Propriedades
                                </button>
                            </li>
                        </ul>
                    </div>
                `;
            }
            fileListContainer.appendChild(itemElement);
        });
    };

    const filterFiles = () => {
        currentFilteredFiles = allFiles.filter(item => {
            const typeMatch = (currentFilters.type === 'all' ||
                               (currentFilters.type === 'dir' && item.is_dir) ||
                               (currentFilters.type === 'document' && (item.type === 'doc' || item.type === 'docx' || item.type === 'txt')) ||
                               (item.is_dir === false && item.type === currentFilters.type));

            if (!typeMatch) return false;

            const today = new Date();
            const dateParts = item.modified_at.split(' ')[0].split('/');
            const itemDate = new Date(`${dateParts[2]}-${dateParts[1]}-${dateParts[0]}`);
            const diffTime = today - itemDate;
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

            if (currentFilters.date === 'all') return true;
            if (currentFilters.date === 'today' && diffDays <= 1) return true;
            if (currentFilters.date === 'week' && diffDays <= 7) return true;
            if (currentFilters.date === 'month' && diffDays <= 30) return true;

            return false;
        });
        renderFiles(currentFilteredFiles);
    };

    document.querySelectorAll('#filter-type .dropdown-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            currentFilters.type = e.target.getAttribute('data-filter-type');
            filterFiles();
        });
    });

    document.querySelectorAll('#filter-date .dropdown-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            currentFilters.date = e.target.getAttribute('data-filter-date');
            filterFiles();
        });
    });

    applyLayout(currentLayout);
    if (allFiles && allFiles.length > 0) {
        renderFiles(allFiles);
    }
});

const uploadForm = document.getElementById('upload-form');
if (uploadForm) {
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);
        const uploadBtn = document.getElementById('upload-btn');
        const spinner = document.getElementById('upload-spinner');

        spinner.style.display = 'inline-block';
        uploadBtn.disabled = true;

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
            });
            const result = await response.json();

            if (response.ok) {
                window.location.href = result.redirect_url;
            } else {
                alert('Erro no upload: ' + result.message);
            }
        } catch (error) {
            console.error('Erro:', error);
            alert('Erro na conexão com o servidor.');
        } finally {
            spinner.style.display = 'none';
            uploadBtn.disabled = false;
        }
    });
}

const newFolderForm = document.getElementById('new-folder-form');
if (newFolderForm) {
    newFolderForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);
        const createFolderBtn = document.getElementById('create-folder-btn');
        const spinner = document.getElementById('create-folder-spinner');

        spinner.style.display = 'inline-block';
        createFolderBtn.disabled = true;

        try {
            const response = await fetch('/create_folder', {
                method: 'POST',
                body: formData,
            });
            const result = await response.json();

            if (response.ok) {
                window.location.href = result.redirect_url;
            } else {
                alert('Erro ao criar pasta: ' + result.message);
            }
        } catch (error) {
            console.error('Erro:', error);
            alert('Erro na conexão com o servidor.');
        } finally {
            spinner.style.display = 'none';
            createFolderBtn.disabled = false;
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const currentPathInput = document.getElementById('current-path-input');
    const newFolderPathInput = document.getElementById('new-folder-path-input');
    if (window.location.pathname.includes('/browse/')) {
        const pathSegments = window.location.pathname.split('/browse/');
        if (pathSegments.length > 1) {
            const currentPath = decodeURIComponent(pathSegments[1]);
            if(currentPathInput) currentPathInput.value = currentPath;
            if(newFolderPathInput) newFolderPathInput.value = currentPath;
        }
    } else {
        if(currentPathInput) currentPathInput.value = '';
        if(newFolderPathInput) newFolderPathInput.value = '';
    }
});

// Move item functionality
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('move-item-btn') || e.target.closest('.move-item-btn')) {
        const button = e.target.classList.contains('move-item-btn') ? e.target : e.target.closest('.move-item-btn');
        const itemPath = button.getAttribute('data-item-path');
        const itemName = button.getAttribute('data-item-name');

        // Show move modal
        document.getElementById('move-source-path').value = itemPath;
        document.getElementById('move-item-name').textContent = itemName;

        // Pre-fill destination path with current directory or suggest a valid path
        const currentPath = window.location.pathname.includes('/browse/')
            ? decodeURIComponent(window.location.pathname.split('/browse/')[1])
            : '';
        document.getElementById('move-destination-path').value = currentPath || '';

        const moveModal = new bootstrap.Modal(document.getElementById('moveModal'));
        moveModal.show();
    }
});

const moveForm = document.getElementById('move-form');
if (moveForm) {
    moveForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);
        const moveBtn = document.getElementById('move-btn');
        const spinner = document.getElementById('move-spinner');

        spinner.style.display = 'inline-block';
        moveBtn.disabled = true;

        try {
            const response = await fetch('/move_item', {
                method: 'POST',
                body: formData,
            });
            const result = await response.json();

            if (response.ok) {
                window.location.href = result.redirect_url;
            } else {
                alert('Erro ao mover item: ' + result.message);
            }
        } catch (error) {
            console.error('Erro:', error);
            alert('Erro na conexão com o servidor.');
        } finally {
            spinner.style.display = 'none';
            moveBtn.disabled = false;
        }
    });
}

async function moveItem(sourcePath, destinationPath) {
    try {
        const formData = new FormData();
        formData.append('source_path', sourcePath);
        formData.append('destination_path', destinationPath);

        const response = await fetch('/move_item', {
            method: 'POST',
            body: formData,
        });
        const result = await response.json();

        if (response.ok) {
            window.location.href = result.redirect_url;
        } else {
            alert('Erro ao mover item: ' + result.message);
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro na conexão com o servidor.');
    }
}

// Portal icon selection functionality
document.addEventListener('DOMContentLoaded', function() {
    const iconOptions = document.querySelectorAll('.icon-option');
    const iconInput = document.getElementById('icon');

    if (iconOptions.length > 0 && iconInput) {
        iconOptions.forEach(button => {
            button.addEventListener('click', function() {
                const iconClass = this.getAttribute('data-icon');
                iconInput.value = iconClass;

                // Add visual feedback
                iconOptions.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');

                // Remove active class after a short delay
                setTimeout(() => {
                    this.classList.remove('active');
                }, 300);
            });
        });
    }

    // Add Block Modal functionality
    const addBlockModal = document.getElementById('addBlockModal');
    const newBlockNameInput = document.getElementById('newBlockName');
    const addBlockBtn = document.getElementById('addBlockBtn');
    const blockSelect = document.getElementById('block');
    const blockIconOptions = document.querySelectorAll('.block-icon-option');

    let selectedBlockIcon = 'bi bi-folder'; // Default icon

    if (addBlockModal) {
        // Reset modal when opened
        addBlockModal.addEventListener('show.bs.modal', function() {
            if (newBlockNameInput) newBlockNameInput.value = '';
            selectedBlockIcon = 'bi bi-folder';
            blockIconOptions.forEach(btn => {
                btn.classList.remove('active');
                if (btn.getAttribute('data-icon') === selectedBlockIcon) {
                    btn.classList.add('active');
                }
            });
        });

        // Handle block icon selection
        blockIconOptions.forEach(button => {
            button.addEventListener('click', function() {
                selectedBlockIcon = this.getAttribute('data-icon');
                blockIconOptions.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');

                // Add animation effect
                this.classList.add('pulse');
                setTimeout(() => this.classList.remove('pulse'), 300);
            });
        });

        // Handle add block button
        if (addBlockBtn) {
            addBlockBtn.addEventListener('click', function() {
                const blockName = newBlockNameInput.value.trim();
                if (!blockName) {
                    alert('Por favor, insira um nome para o bloco.');
                    return;
                }

                // Check if block already exists
                const existingOptions = Array.from(blockSelect.options).map(opt => opt.value);
                if (existingOptions.includes(blockName)) {
                    alert('Este bloco já existe.');
                    return;
                }

                // Add new option to select
                const newOption = document.createElement('option');
                newOption.value = blockName;
                newOption.textContent = blockName;
                newOption.selected = true;
                blockSelect.appendChild(newOption);

                // Close modal
                const modal = bootstrap.Modal.getInstance(addBlockModal);
                modal.hide();

                // Show success feedback
                showAlert(`Bloco "${blockName}" adicionado com sucesso!`, 'success');
            });
        }
    }
});

// Database analysis functions
function analyzeDatabase(dbName) {
    // Criar modal para mostrar o progresso da análise
    const modal = document.getElementById('analyzeModal');
    const bsModal = new bootstrap.Modal(modal, {
        backdrop: 'static',
        keyboard: false
    });
    bsModal.show();

    // Iniciar análise com progresso
    startAnalysisWithProgress(dbName, modal);
}

function startAnalysisWithProgress(dbName, modal) {
    const logContent = modal.querySelector('#analyzeLogContent');
    const progressBar = modal.querySelector('#analyzeProgress');
    const startTime = new Date();

    // Limpar conteúdo anterior
    logContent.innerHTML = '';

    // Adicionar timestamp inicial
    addLogEntry(logContent, `Iniciando análise do banco ${dbName}...`, 'info');
    addLogEntry(logContent, `Timestamp: ${startTime.toLocaleString()}`, 'info');
    addLogEntry(logContent, '', 'info');

    // Simular processo de análise com barra de progresso
    simulateAnalysisProcessWithProgress(logContent, progressBar, dbName, startTime, () => {
        // Após análise completa, fechar modal e redirecionar
        const bsModal = bootstrap.Modal.getInstance(modal);
        bsModal.hide();
        window.location.href = `/databases/analyze/${dbName}`;
    });
}

function simulateAnalysisProcessWithProgress(logContent, progressBar, dbName, startTime, onComplete) {
    const steps = [
        { message: 'Conectando ao banco de dados...', delay: 500 },
        { message: 'Verificando permissões e estrutura...', delay: 300 },
        { message: 'Coletando metadados das tabelas...', delay: 800 },
        { message: 'Analisando colunas e relacionamentos...', delay: 1000 },
        { message: 'Gerando diagrama ERD...', delay: 1500 },
        { message: 'Gerando diagrama de fluxo de dados...', delay: 1200 },
        { message: 'Criando documentação em Markdown...', delay: 600 },
        { message: 'Salvando diagramas e arquivos...', delay: 400 },
        { message: 'Análise concluída com sucesso!', delay: 200, type: 'success' }
    ];

    let currentStep = 0;

    function executeStep() {
        if (currentStep < steps.length) {
            const step = steps[currentStep];
            addLogEntry(logContent, step.message, step.type || 'info');

            // Atualizar barra de progresso
            const progress = ((currentStep + 1) / steps.length) * 100;
            progressBar.style.width = `${progress}%`;
            progressBar.setAttribute('aria-valuenow', progress);

            currentStep++;
            setTimeout(executeStep, step.delay);
        } else {
            // Finalizar
            const endTime = new Date();
            const duration = (endTime - startTime) / 1000;
            addLogEntry(logContent, '', 'info');
            addLogEntry(logContent, `Tempo total: ${duration.toFixed(2)} segundos`, 'success');
            addLogEntry(logContent, `Redirecionando para página de análise...`, 'success');

            // Chamar callback para redirecionamento
            setTimeout(onComplete, 500);
        }
    }

    executeStep();
}

function analyzeLocalDatabase(dbName) {
    // Criar modal para mostrar o progresso da análise
    const modal = document.getElementById('analyzeModal');
    const bsModal = new bootstrap.Modal(modal, {
        backdrop: 'static',
        keyboard: false
    });
    bsModal.show();

    // Iniciar análise com progresso
    startAnalysisWithProgress(dbName, modal);
}

function startComparisonWithProgress(dbName, modal) {
    const logContent = modal.querySelector('#compareLogContent');
    const progressBar = modal.querySelector('#compareProgress');
    const resultsContainer = modal.querySelector('#compareResults');
    const startTime = new Date();

    // Limpar conteúdo anterior
    if (logContent) logContent.innerHTML = '';
    if (resultsContainer) resultsContainer.style.display = 'none';

    // Adicionar timestamp inicial
    if (logContent) {
        addLogEntry(logContent, `Iniciando comparação do banco ${dbName}...`, 'info');
        addLogEntry(logContent, `Timestamp: ${startTime.toLocaleString()}`, 'info');
        addLogEntry(logContent, '', 'info');
    }

    // Simular processo de comparação com barra de progresso
    simulateComparisonProcessWithProgress(logContent, progressBar, dbName, startTime, () => {
        // Após comparação completa, fazer requisição AJAX para obter resultados
        if (logContent) addLogEntry(logContent, 'Obtendo resultados da comparação...', 'info');

        fetch(`/databases/compare/${dbName}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    if (resultsContainer) {
                        displayComparisonResults(resultsContainer, data.comparison, dbName);
                        resultsContainer.style.display = 'block';
                    }
                    if (logContent) addLogEntry(logContent, 'Comparação concluída com sucesso!', 'success');
                } else {
                    if (logContent) addLogEntry(logContent, `Erro: ${data.error}`, 'error');
                }
            })
            .catch(error => {
                console.error('Erro na comparação:', error);
                if (logContent) addLogEntry(logContent, `Erro na comparação: ${error.message}`, 'error');
            });
    });
}

function compareDatabase(dbName) {
    // Criar modal para mostrar o progresso da comparação
    const modal = document.getElementById('compareModal');
    const bsModal = new bootstrap.Modal(modal, {
        backdrop: 'static',
        keyboard: false
    });
    bsModal.show();

    // Iniciar comparação com progresso
    startComparisonWithProgress(dbName, modal);
}

function simulateComparisonProcessWithProgress(logContent, progressBar, dbName, startTime, onComplete) {
    const steps = [
        { message: 'Conectando ao banco de dados local...', delay: 500 },
        { message: 'Conectando ao banco de dados de produção...', delay: 500 },
        { message: 'Obtendo lista de tabelas...', delay: 400 },
        { message: 'Comparando tabelas...', delay: 800 },
        { message: 'Comparando colunas...', delay: 1000 },
        { message: 'Comparando dados...', delay: 1200 },
        { message: 'Gerando relatório de comparação...', delay: 600 },
        { message: 'Finalizando...', delay: 400 },
        { message: 'Comparação concluída com sucesso!', delay: 200, type: 'success' }
    ];

    let currentStep = 0;

    function executeStep() {
        if (currentStep < steps.length) {
            const step = steps[currentStep];
            addLogEntry(logContent, step.message, step.type || 'info');

            // Atualizar barra de progresso
            const progress = ((currentStep + 1) / steps.length) * 100;
            progressBar.style.width = `${progress}%`;
            progressBar.setAttribute('aria-valuenow', progress);

            currentStep++;
            setTimeout(executeStep, step.delay);
        } else {
            // Finalizar
            const endTime = new Date();
            const duration = (endTime - startTime) / 1000;
            addLogEntry(logContent, '', 'info');
            addLogEntry(logContent, `Tempo total: ${duration.toFixed(2)} segundos`, 'success');
            addLogEntry(logContent, `Redirecionando para página de comparação...`, 'success');

            // Chamar callback para redirecionamento
            setTimeout(onComplete, 500);
        }
    }

    executeStep();
}

function displayComparisonResults(container, comparisonData, dbName) {
    if (!container) return;

    const hasDifferences = (comparisonData.tables && comparisonData.tables.some(t => t.status !== 'matching')) ||
                          (comparisonData.columns && comparisonData.columns.length > 0) ||
                          (comparisonData.data && comparisonData.data.some(d => d.differences > 0));

    container.innerHTML = `
        <div class="comparison-results">
            <!-- Header with gradient background -->
            <div class="comparison-header mb-4">
                <div class="header-content">
                    <div class="header-icon">
                        <i class="bi bi-arrow-left-right"></i>
                    </div>
                    <div class="header-text">
                        <h4 class="mb-1">Comparação de Banco de Dados</h4>
                        <p class="mb-0 text-muted">${dbName}</p>
                    </div>
                </div>
            </div>

            <!-- Enhanced Nav tabs -->
            <ul class="nav nav-tabs custom-tabs mb-4" id="comparisonTabs" role="tablist">
                <li class="nav-item" role="presentation">
                    <button class="nav-link active" id="overview-tab" data-bs-toggle="tab" data-bs-target="#overview" type="button" role="tab" aria-controls="overview" aria-selected="true">
                        <i class="bi bi-bar-chart-line me-2"></i>
                        <span class="tab-text">Visão Geral</span>
                    </button>
                </li>
                ${hasDifferences ? `
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="differences-tab" data-bs-toggle="tab" data-bs-target="#differences" type="button" role="tab" aria-controls="differences" aria-selected="false">
                        <i class="bi bi-exclamation-triangle-fill me-2"></i>
                        <span class="tab-text">Diferenças</span>
                        <span class="badge bg-danger ms-2">${getDifferencesCount(comparisonData)}</span>
                    </button>
                </li>
                ` : ''}
            </ul>

            <!-- Tab panes -->
            <div class="tab-content" id="comparisonTabContent">
                <!-- Overview Tab -->
                <div class="tab-pane fade show active" id="overview" role="tabpanel" aria-labelledby="overview-tab">
                    <!-- Enhanced Statistics Cards -->
                    <div class="stats-grid mb-4">
                        <div class="stat-card total">
                            <div class="stat-icon">
                                <i class="bi bi-table"></i>
                            </div>
                            <div class="stat-content">
                                <div class="stat-number">${comparisonData.stats?.tables_total || 0}</div>
                                <div class="stat-label">Total de Tabelas</div>
                            </div>
                        </div>
                        <div class="stat-card matching">
                            <div class="stat-icon">
                                <i class="bi bi-check-circle-fill"></i>
                            </div>
                            <div class="stat-content">
                                <div class="stat-number">${comparisonData.stats?.tables_matching || 0}</div>
                                <div class="stat-label">Tabelas Iguais</div>
                            </div>
                        </div>
                        <div class="stat-card different">
                            <div class="stat-icon">
                                <i class="bi bi-exclamation-triangle-fill"></i>
                            </div>
                            <div class="stat-content">
                                <div class="stat-number">${comparisonData.stats?.tables_different || 0}</div>
                                <div class="stat-label">Tabelas Diferentes</div>
                            </div>
                        </div>
                        <div class="stat-card missing">
                            <div class="stat-icon">
                                <i class="bi bi-x-circle-fill"></i>
                            </div>
                            <div class="stat-content">
                                <div class="stat-number">${comparisonData.stats?.tables_missing || 0}</div>
                                <div class="stat-label">Tabelas Faltando</div>
                            </div>
                        </div>
                    </div>

                    ${!hasDifferences ? `
                    <div class="success-state">
                        <div class="success-icon">
                            <i class="bi bi-check-circle-fill"></i>
                        </div>
                        <h4 class="success-title">Bancos de dados idênticos!</h4>
                        <p class="success-message">Não foram encontradas diferenças entre os bancos local e de produção.</p>
                        <div class="success-decoration">
                            <i class="bi bi-stars"></i>
                        </div>
                    </div>
                    ` : `
                    <div class="differences-alert">
                        <div class="alert-icon">
                            <i class="bi bi-info-circle-fill"></i>
                        </div>
                        <div class="alert-content">
                            <h6>Foram encontradas diferenças</h6>
                            <p class="mb-0">Clique na aba "Diferenças" para ver os detalhes completos.</p>
                        </div>
                    </div>
                    `}
                </div>

                <!-- Differences Tab -->
                ${hasDifferences ? `
                <div class="tab-pane fade" id="differences" role="tabpanel" aria-labelledby="differences-tab">
                    <!-- Tables Comparison -->
                    ${comparisonData.tables && comparisonData.tables.some(t => t.status !== 'matching') ? `
                        <div class="difference-section mb-4">
                            <div class="section-header">
                                <div class="section-icon">
                                    <i class="bi bi-table"></i>
                                </div>
                                <div class="section-title">
                                    <h5>Diferenças nas Tabelas</h5>
                                    <span class="section-count">${comparisonData.tables.filter(t => t.status !== 'matching').length} diferenças</span>
                                </div>
                            </div>
                            <div class="section-content">
                                <div class="table-responsive">
                                    <table class="table custom-table">
                                        <thead>
                                            <tr>
                                                <th><i class="bi bi-tag me-2"></i>Tabela</th>
                                                <th><i class="bi bi-flag me-2"></i>Status</th>
                                                <th><i class="bi bi-info-circle me-2"></i>Detalhes</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            ${comparisonData.tables.filter(table => table.status !== 'matching').map(table => `
                                                <tr class="difference-row ${table.status === 'missing' ? 'missing' : 'different'}">
                                                    <td>
                                                        <div class="table-name">
                                                            <i class="bi bi-table me-2"></i>
                                                            <strong>${table.name}</strong>
                                                        </div>
                                                    </td>
                                                    <td>
                                                        <span class="status-badge ${table.status === 'missing' ? 'missing' : 'different'}">
                                                            <i class="bi ${table.status === 'missing' ? 'bi-x-circle' : 'bi-exclamation-triangle'} me-1"></i>
                                                            ${table.status === 'missing' ? 'Faltando' : 'Diferente'}
                                                        </span>
                                                    </td>
                                                    <td>
                                                        <div class="details-text">
                                                            ${table.details ? table.details : 'Diferenças encontradas na estrutura da tabela'}
                                                        </div>
                                                    </td>
                                                </tr>
                                            `).join('')}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    ` : ''}

                    <!-- Columns Comparison -->
                    ${comparisonData.columns && comparisonData.columns.length > 0 ? `
                        <div class="difference-section mb-4">
                            <div class="section-header">
                                <div class="section-icon">
                                    <i class="bi bi-columns"></i>
                                </div>
                                <div class="section-title">
                                    <h5>Diferenças nas Colunas</h5>
                                    <span class="section-count">${comparisonData.columns.length} diferenças</span>
                                </div>
                            </div>
                            <div class="section-content">
                                <div class="table-responsive">
                                    <table class="table custom-table">
                                        <thead>
                                            <tr>
                                                <th><i class="bi bi-diagram-3 me-2"></i>Tabela</th>
                                                <th><i class="bi bi-tag me-2"></i>Coluna</th>
                                                <th><i class="bi bi-flag me-2"></i>Status</th>
                                                <th><i class="bi bi-info-circle me-2"></i>Detalhes</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            ${comparisonData.columns.map(col => `
                                                <tr class="difference-row ${col.status === 'missing' ? 'missing' : 'different'}">
                                                    <td>
                                                        <div class="table-name">
                                                            <i class="bi bi-table me-2"></i>
                                                            ${col.table}
                                                        </div>
                                                    </td>
                                                    <td>
                                                        <div class="column-name">
                                                            <i class="bi bi-tag me-2"></i>
                                                            <strong>${col.name}</strong>
                                                        </div>
                                                    </td>
                                                    <td>
                                                        <span class="status-badge ${col.status === 'missing' ? 'missing' : 'different'}">
                                                            <i class="bi ${col.status === 'missing' ? 'bi-x-circle' : 'bi-exclamation-triangle'} me-1"></i>
                                                            ${col.status === 'missing' ? 'Faltando' : 'Diferente'}
                                                        </span>
                                                    </td>
                                                    <td>
                                                        <div class="details-text">
                                                            ${col.details ? col.details : 'Diferenças encontradas na coluna'}
                                                        </div>
                                                    </td>
                                                </tr>
                                            `).join('')}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    ` : ''}

                    <!-- Data Comparison -->
                    ${comparisonData.data && comparisonData.data.some(d => d.differences > 0) ? `
                        <div class="difference-section">
                            <div class="section-header">
                                <div class="section-icon">
                                    <i class="bi bi-database"></i>
                                </div>
                                <div class="section-title">
                                    <h5>Diferenças nos Dados</h5>
                                    <span class="section-count">${comparisonData.data.filter(d => d.differences > 0).length} tabelas afetadas</span>
                                </div>
                            </div>
                            <div class="section-content">
                                <div class="table-responsive">
                                    <table class="table custom-table">
                                        <thead>
                                            <tr>
                                                <th><i class="bi bi-table me-2"></i>Tabela</th>
                                                <th><i class="bi bi-flag me-2"></i>Status</th>
                                                <th><i class="bi bi-pc-display me-2"></i>Local</th>
                                                <th><i class="bi bi-cloud me-2"></i>Produção</th>
                                                <th><i class="bi bi-graph-up me-2"></i>Diferenças</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            ${comparisonData.data.filter(data => data.differences > 0).map(data => `
                                                <tr class="difference-row different">
                                                    <td>
                                                        <div class="table-name">
                                                            <i class="bi bi-table me-2"></i>
                                                            <strong>${data.table}</strong>
                                                        </div>
                                                    </td>
                                                    <td>
                                                        <span class="status-badge different">
                                                            <i class="bi bi-exclamation-triangle me-1"></i>
                                                            Dados Diferentes
                                                        </span>
                                                    </td>
                                                    <td>
                                                        <div class="count-badge local">
                                                            <span class="count">${data.local_count}</span>
                                                            <small>registros</small>
                                                        </div>
                                                    </td>
                                                    <td>
                                                        <div class="count-badge production">
                                                            <span class="count">${data.production_count}</span>
                                                            <small>registros</small>
                                                        </div>
                                                    </td>
                                                    <td>
                                                        <div class="differences-highlight">
                                                            <span class="differences-number">${data.differences}</span>
                                                            <small>diferenças</small>
                                                        </div>
                                                    </td>
                                                </tr>
                                            `).join('')}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    ` : ''}
                </div>
                ` : ''}
            </div>
        </div>

        <style>
        .comparison-results {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        .comparison-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            color: white;
        }

        .header-content {
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }

        .header-icon {
            background: rgba(255,255,255,0.2);
            border-radius: 50%;
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8rem;
            backdrop-filter: blur(10px);
        }

        .header-text h4 {
            margin: 0;
            font-weight: 600;
            font-size: 1.5rem;
        }

        .header-text p {
            margin: 0;
            opacity: 0.9;
            font-size: 1.1rem;
        }

        .custom-tabs {
            border: none;
            background: #f8f9fa;
            border-radius: 10px;
            padding: 0.5rem;
            gap: 0.5rem;
        }

        .custom-tabs .nav-link {
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            color: #6c757d;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .custom-tabs .nav-link.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }

        .custom-tabs .nav-link:hover:not(.active) {
            background: rgba(108, 117, 125, 0.1);
            color: #495057;
        }

        .tab-text {
            font-weight: 500;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .stat-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            border: 1px solid #e9ecef;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }

        .stat-card.total {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .stat-card.matching {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
        }

        .stat-card.different {
            background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
            color: white;
        }

        .stat-card.missing {
            background: linear-gradient(135deg, #dc3545 0%, #e83e8c 100%);
            color: white;
        }

        .stat-icon {
            font-size: 2rem;
            opacity: 0.9;
        }

        .stat-content {
            flex: 1;
        }

        .stat-number {
            font-size: 2.5rem;
            font-weight: 700;
            line-height: 1;
            margin-bottom: 0.25rem;
        }

        .stat-label {
            font-size: 0.9rem;
            opacity: 0.9;
            font-weight: 500;
        }

        .success-state {
            text-align: center;
            padding: 3rem 2rem;
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            border-radius: 15px;
            border: 1px solid #c3e6cb;
            position: relative;
            overflow: hidden;
        }

        .success-icon {
            font-size: 4rem;
            color: #28a745;
            margin-bottom: 1rem;
            animation: bounceIn 0.8s ease;
        }

        .success-title {
            color: #155724;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }

        .success-message {
            color: #155724;
            opacity: 0.8;
            font-size: 1.1rem;
        }

        .success-decoration {
            position: absolute;
            top: -20px;
            right: -20px;
            font-size: 3rem;
            color: rgba(40, 167, 69, 0.1);
            transform: rotate(15deg);
        }

        .differences-alert {
            background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
            border: 1px solid #ffeaa7;
            border-radius: 12px;
            padding: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .alert-icon {
            font-size: 2rem;
            color: #856404;
        }

        .alert-content h6 {
            color: #856404;
            margin-bottom: 0.25rem;
            font-weight: 600;
        }

        .alert-content p {
            color: #856404;
            opacity: 0.8;
            margin: 0;
        }

        .difference-section {
            background: white;
            border-radius: 12px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            border: 1px solid #e9ecef;
            overflow: hidden;
            margin-bottom: 2rem;
        }

        .section-header {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 1.5rem;
            border-bottom: 1px solid #dee2e6;
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .section-icon {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 50%;
            width: 45px;
            height: 45px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
        }

        .section-title h5 {
            margin: 0;
            font-weight: 600;
            color: #495057;
        }

        .section-count {
            background: rgba(108, 117, 125, 0.1);
            color: #6c757d;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }

        .section-content {
            padding: 1.5rem;
        }

        .custom-table {
            margin: 0;
            border: none;
        }

        .custom-table thead th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 1rem;
            font-weight: 600;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .custom-table tbody tr {
            transition: all 0.2s ease;
            border-bottom: 1px solid #f1f3f4;
        }

        .custom-table tbody tr:hover {
            background: rgba(102, 126, 234, 0.05);
            transform: scale(1.01);
        }

        .difference-row.missing {
            background: linear-gradient(90deg, rgba(220, 53, 69, 0.05) 0%, transparent 100%);
        }

        .difference-row.different {
            background: linear-gradient(90deg, rgba(255, 193, 7, 0.05) 0%, transparent 100%);
        }

        .table-name, .column-name {
            display: flex;
            align-items: center;
            font-weight: 500;
        }

        .status-badge {
            padding: 0.4rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
        }

        .status-badge.missing {
            background: linear-gradient(135deg, #dc3545 0%, #e83e8c 100%);
            color: white;
        }

        .status-badge.different {
            background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
            color: #212529;
        }

        .details-text {
            color: #6c757d;
            font-size: 0.9rem;
        }

        .count-badge {
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 0.5rem;
            text-align: center;
            min-width: 80px;
        }

        .count-badge.local {
            border-color: #28a745;
            background: rgba(40, 167, 69, 0.05);
        }

        .count-badge.production {
            border-color: #007bff;
            background: rgba(0, 123, 255, 0.05);
        }

        .count-badge .count {
            font-weight: 700;
            font-size: 1.2rem;
            display: block;
            line-height: 1;
        }

        .count-badge small {
            color: #6c757d;
            font-size: 0.7rem;
        }

        .differences-highlight {
            background: linear-gradient(135deg, #dc3545 0%, #e83e8c 100%);
            color: white;
            border-radius: 8px;
            padding: 0.5rem;
            text-align: center;
            min-width: 80px;
        }

        .differences-number {
            font-weight: 700;
            font-size: 1.2rem;
            display: block;
            line-height: 1;
        }

        .differences-highlight small {
            font-size: 0.7rem;
            opacity: 0.9;
        }

        @keyframes bounceIn {
            0% { transform: scale(0.3); opacity: 0; }
            50% { transform: scale(1.05); }
            70% { transform: scale(0.9); }
            100% { transform: scale(1); opacity: 1; }
        }

        @media (max-width: 768px) {
            .stats-grid {
                grid-template-columns: 1fr;
            }

            .header-content {
                flex-direction: column;
                text-align: center;
                gap: 1rem;
            }

            .stat-card {
                padding: 1rem;
            }

            .stat-number {
                font-size: 2rem;
            }
        }
        </style>
    `;

    // Add animation to stats cards
    setTimeout(() => {
        const statCards = container.querySelectorAll('.stat-card');
        statCards.forEach((card, index) => {
            setTimeout(() => {
                card.style.animation = 'bounceIn 0.6s ease forwards';
            }, index * 100);
        });
    }, 100);
}

function getDifferencesCount(comparisonData) {
    let count = 0;
    if (comparisonData.tables) count += comparisonData.tables.filter(t => t.status !== 'matching').length;
    if (comparisonData.columns) count += comparisonData.columns.length;
    if (comparisonData.data) count += comparisonData.data.filter(d => d.differences > 0).length;
    return count;
}

function addLogEntry(container, message, type = 'info') {
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry log-${type}`;

    let icon = '';
    switch(type) {
        case 'success':
            icon = '<i class="bi bi-check-circle text-success me-1"></i>';
            break;
        case 'error':
            icon = '<i class="bi bi-x-circle text-danger me-1"></i>';
            break;
        case 'warning':
            icon = '<i class="bi bi-exclamation-triangle text-warning me-1"></i>';
            break;
        default:
            icon = '<i class="bi bi-info-circle text-info me-1"></i>';
    }

    logEntry.innerHTML = `<span class="text-muted">[${timestamp}]</span> ${icon}${message}`;
    container.appendChild(logEntry);
    container.scrollTop = container.scrollHeight;
}

