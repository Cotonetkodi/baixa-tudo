// Variáveis globais
let selectedFiles = [];
let socket = null;
let currentUploadId = null;

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Inicializar Socket.IO
    socket = io();
    
    // Event listeners para navegação
    setupNavigation();
    
    // Event listeners para upload
    setupUpload();
    
    // Event listeners para pesquisa
    setupSearch();
    
    // Socket.IO event listeners
    setupSocketListeners();
    
    // Carregar ficheiros na página de pesquisa
    loadFiles();
}

// Configurar navegação entre secções
function setupNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    const sections = document.querySelectorAll('.section');
    
    navButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (this.getAttribute('href')) return; // Skip admin link
            
            e.preventDefault();
            const targetSection = this.getAttribute('data-section');
            
            // Remover classe active de todos os botões e secções
            navButtons.forEach(btn => btn.classList.remove('active'));
            sections.forEach(section => section.classList.remove('active'));
            
            // Adicionar classe active ao botão e secção selecionados
            this.classList.add('active');
            document.getElementById(targetSection + '-section').classList.add('active');
            
            // Se for a secção de pesquisa, carregar ficheiros
            if (targetSection === 'search') {
                loadFiles();
            }
        });
    });
}

// Configurar funcionalidades de upload
function setupUpload() {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const selectBtn = document.getElementById('select-btn');
    const categoryInputs = document.querySelectorAll('input[name="category"]');
    const startUploadBtn = document.getElementById('start-upload-btn');
    const newUploadBtn = document.getElementById('new-upload-btn');
    
    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // Click para selecionar ficheiros
    selectBtn.addEventListener('click', () => fileInput.click());
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // Seleção de ficheiros
    fileInput.addEventListener('change', handleFileSelection);
    
    // Seleção de categoria
    categoryInputs.forEach(input => {
        input.addEventListener('change', function() {
            startUploadBtn.disabled = false;
        });
    });
    
    // Iniciar upload
    startUploadBtn.addEventListener('click', startUpload);
    
    // Novo upload
    newUploadBtn.addEventListener('click', resetUpload);
}

// Configurar funcionalidades de pesquisa
function setupSearch() {
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    const categoryFilter = document.getElementById('category-filter');
    
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
    
    categoryFilter.addEventListener('change', performSearch);
}

// Configurar Socket.IO listeners
function setupSocketListeners() {
    socket.on('upload_progress', function(data) {
        updateUploadProgress(data);
    });
    
    socket.on('upload_complete', function(data) {
        handleUploadComplete(data);
    });
    
    socket.on('upload_error', function(data) {
        handleUploadError(data);
    });
}

// Handlers para drag and drop
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    this.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    this.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    this.classList.remove('dragover');
    
    const files = Array.from(e.dataTransfer.files);
    processSelectedFiles(files);
}

// Handler para seleção de ficheiros
function handleFileSelection(e) {
    const files = Array.from(e.target.files);
    processSelectedFiles(files);
}

// Processar ficheiros selecionados
function processSelectedFiles(files) {
    // Validar tamanho dos ficheiros (5GB = 5 * 1024 * 1024 * 1024 bytes)
    const maxSize = 5 * 1024 * 1024 * 1024;
    const validFiles = files.filter(file => {
        if (file.size > maxSize) {
            showNotification(`Ficheiro "${file.name}" é muito grande (máximo 5GB)`, 'error');
            return false;
        }
        return true;
    });
    
    if (validFiles.length === 0) {
        return;
    }
    
    selectedFiles = validFiles;
    showCategorySelection();
}

// Mostrar seleção de categoria
function showCategorySelection() {
    document.getElementById('upload-area').style.display = 'none';
    document.getElementById('category-section').style.display = 'block';
    
    // Reset categoria selecionada
    document.querySelectorAll('input[name="category"]').forEach(input => {
        input.checked = false;
    });
    document.getElementById('start-upload-btn').disabled = true;
}

// Iniciar upload
function startUpload() {
    const selectedCategory = document.querySelector('input[name="category"]:checked').value;
    
    // Gerar ID único para este upload
    currentUploadId = 'upload_' + Date.now();
    
    // Mostrar progresso
    document.getElementById('category-section').style.display = 'none';
    document.getElementById('upload-progress').style.display = 'block';
    
    // Preparar lista de ficheiros
    const fileList = document.getElementById('upload-file-list');
    fileList.innerHTML = '';
    
    selectedFiles.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.innerHTML = `
            <div class="file-info">
                <i class="fas fa-file"></i>
                <span>${file.name}</span>
                <span>(${formatFileSize(file.size)})</span>
            </div>
            <div class="file-status uploading" id="status-${index}">
                <i class="fas fa-spinner fa-spin"></i> A carregar...
            </div>
        `;
        fileList.appendChild(fileItem);
    });
    
    // Iniciar upload de cada ficheiro
    uploadFiles(selectedCategory);
}

// Upload de ficheiros
async function uploadFiles(category) {
    let totalSize = selectedFiles.reduce((sum, file) => sum + file.size, 0);
    let uploadedSize = 0;
    
    for (let i = 0; i < selectedFiles.length; i++) {
        const file = selectedFiles[i];
        
        try {
            await uploadSingleFile(file, category, i);
            uploadedSize += file.size;
            
            // Atualizar progresso geral
            const progress = Math.round((uploadedSize / totalSize) * 100);
            updateProgressBar(progress);
            
            // Atualizar status do ficheiro
            const statusElement = document.getElementById(`status-${i}`);
            statusElement.innerHTML = '<i class="fas fa-check"></i> Concluído';
            statusElement.className = 'file-status completed';
            
        } catch (error) {
            console.error('Erro no upload:', error);
            const statusElement = document.getElementById(`status-${i}`);
            statusElement.innerHTML = '<i class="fas fa-times"></i> Erro';
            statusElement.className = 'file-status error';
        }
    }
}

// Upload de um ficheiro individual
function uploadSingleFile(file, category, index) {
    return new Promise((resolve, reject) => {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('category', category);
        formData.append('upload_id', currentUploadId);
        formData.append('file_index', index);
        
        const xhr = new XMLHttpRequest();
        
        xhr.upload.addEventListener('progress', function(e) {
            if (e.lengthComputable) {
                const progress = Math.round((e.loaded / e.total) * 100);
                // Atualizar progresso individual se necessário
            }
        });
        
        xhr.addEventListener('load', function() {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                resolve(response);
            } else {
                reject(new Error('Upload failed'));
            }
        });
        
        xhr.addEventListener('error', function() {
            reject(new Error('Upload error'));
        });
        
        xhr.open('POST', '/api/upload');
        xhr.send(formData);
    });
}

// Atualizar barra de progresso
function updateProgressBar(progress) {
    const progressFill = document.getElementById('progress-fill');
    const progressText = document.querySelector('.progress-text');
    
    progressFill.style.width = progress + '%';
    progressText.textContent = progress + '%';
    
    if (progress === 100) {
        setTimeout(() => {
            showUploadComplete();
        }, 500);
    }
}

// Mostrar upload completo
function showUploadComplete() {
    document.getElementById('upload-progress').style.display = 'none';
    document.getElementById('upload-complete').style.display = 'block';
    
    // Aqui você pode mostrar os links dos ficheiros carregados
    // Por agora, vamos mostrar uma mensagem genérica
    const uploadedFilesList = document.getElementById('uploaded-files-list');
    uploadedFilesList.innerHTML = '';
    
    selectedFiles.forEach(file => {
        const fileDiv = document.createElement('div');
        fileDiv.className = 'uploaded-file';
        fileDiv.innerHTML = `
            <div class="file-details">
                <h4>${file.name}</h4>
                <p>Tamanho: ${formatFileSize(file.size)}</p>
            </div>
            <a href="#" class="share-link">
                <i class="fas fa-share"></i> Partilhar
            </a>
        `;
        uploadedFilesList.appendChild(fileDiv);
    });
}

// Reset do upload
function resetUpload() {
    selectedFiles = [];
    currentUploadId = null;
    
    // Reset UI
    document.getElementById('upload-complete').style.display = 'none';
    document.getElementById('upload-progress').style.display = 'none';
    document.getElementById('category-section').style.display = 'none';
    document.getElementById('upload-area').style.display = 'block';
    
    // Reset form
    document.getElementById('file-input').value = '';
    document.querySelectorAll('input[name="category"]').forEach(input => {
        input.checked = false;
    });
    document.getElementById('start-upload-btn').disabled = true;
}

// Carregar ficheiros para pesquisa
async function loadFiles() {
    const resultsGrid = document.getElementById('results-grid');
    const loading = document.getElementById('search-loading');
    const noResults = document.getElementById('no-results');
    
    loading.style.display = 'block';
    resultsGrid.style.display = 'none';
    noResults.style.display = 'none';
    
    try {
        const response = await fetch('/api/files');
        const files = await response.json();
        
        loading.style.display = 'none';
        
        if (files.length === 0) {
            noResults.style.display = 'block';
        } else {
            displayFiles(files);
            resultsGrid.style.display = 'grid';
        }
    } catch (error) {
        console.error('Erro ao carregar ficheiros:', error);
        loading.style.display = 'none';
        noResults.style.display = 'block';
    }
}

// Realizar pesquisa
async function performSearch() {
    const searchTerm = document.getElementById('search-input').value;
    const category = document.getElementById('category-filter').value;
    
    const resultsGrid = document.getElementById('results-grid');
    const loading = document.getElementById('search-loading');
    const noResults = document.getElementById('no-results');
    
    loading.style.display = 'block';
    resultsGrid.style.display = 'none';
    noResults.style.display = 'none';
    
    try {
        const params = new URLSearchParams();
        if (searchTerm) params.append('search', searchTerm);
        if (category) params.append('category', category);
        
        const response = await fetch(`/api/files/search?${params}`);
        const files = await response.json();
        
        loading.style.display = 'none';
        
        if (files.length === 0) {
            noResults.style.display = 'block';
        } else {
            displayFiles(files);
            resultsGrid.style.display = 'grid';
        }
    } catch (error) {
        console.error('Erro na pesquisa:', error);
        loading.style.display = 'none';
        noResults.style.display = 'block';
    }
}

// Exibir ficheiros
function displayFiles(files) {
    const resultsGrid = document.getElementById('results-grid');
    resultsGrid.innerHTML = '';
    
    files.forEach(file => {
        const fileCard = document.createElement('div');
        fileCard.className = 'result-card';
        
        const uploadDate = new Date(file.upload_date).toLocaleDateString('pt-PT');
        
        fileCard.innerHTML = `
            <div class="result-header">
                <div>
                    <div class="result-title">${file.filename}</div>
                </div>
                <div class="result-category">${file.category}</div>
            </div>
            <div class="result-info">
                <span><i class="fas fa-calendar"></i> ${uploadDate}</span>
                <span><i class="fas fa-hdd"></i> ${formatFileSize(file.size)}</span>
            </div>
            <div class="result-actions">
                <a href="${file.share_link}" target="_blank" class="btn btn-primary btn-small">
                    <i class="fas fa-download"></i> Download
                </a>
                <button class="btn btn-primary btn-small" onclick="copyToClipboard('${file.share_link}')">
                    <i class="fas fa-copy"></i> Copiar Link
                </button>
            </div>
        `;
        
        resultsGrid.appendChild(fileCard);
    });
}

// Funções utilitárias
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showNotification('Link copiado para a área de transferência!', 'success');
    }).catch(function(err) {
        console.error('Erro ao copiar: ', err);
        showNotification('Erro ao copiar link', 'error');
    });
}

function showNotification(message, type = 'info') {
    // Criar elemento de notificação
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Estilos inline para a notificação
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
        max-width: 300px;
        word-wrap: break-word;
    `;
    
    // Cores baseadas no tipo
    const colors = {
        success: '#48bb78',
        error: '#e53e3e',
        info: '#667eea',
        warning: '#ed8936'
    };
    
    notification.style.backgroundColor = colors[type] || colors.info;
    
    // Adicionar ao DOM
    document.body.appendChild(notification);
    
    // Remover após 3 segundos
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Adicionar estilos de animação para notificações
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

