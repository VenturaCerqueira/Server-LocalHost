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

if (sidebarToggle) {
    sidebarToggle.addEventListener('click', () => {
        isSidebarCollapsed = !isSidebarCollapsed;
        updateSidebarState();

        // Add animation to sidebar toggle
        sidebarToggle.classList.add('bounceIn');
        setTimeout(() => sidebarToggle.classList.remove('bounceIn'), 800);
    });
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
            if (item.is_dir) {
                iconClass = 'bi-folder-fill';
                iconColor = 'var(--primary-color)';
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
                        <span class="grid-item-filename">${item.nome}</span>
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
                            <span class="fw-bold text-primary">${item.nome}</span>
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
