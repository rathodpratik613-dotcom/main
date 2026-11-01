// API Base URL - Use relative path for production, localhost for development
const API_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
    ? 'http://localhost:5000/api'
    : '/api';

// Current user state
let currentUser = null;

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
        currentUser = JSON.parse(savedUser);
        updateUserDisplay();
        showSection('home');
    } else {
        showSection('login');
    }

    // Setup form listeners
    setupFormListeners();
    
    // Setup navigation listeners
    setupNavigationListeners();
});

// Setup form event listeners
function setupFormListeners() {
    // Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    // Register form
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
    
    // Consultation form
    const consultationForm = document.getElementById('consultationForm');
    if (consultationForm) {
        consultationForm.addEventListener('submit', handleConsultation);
    }
    
    // Medicine search on Enter key
    const medicineSearch = document.getElementById('medicineSearch');
    if (medicineSearch) {
        medicineSearch.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                searchMedicines();
            }
        });
    }
}

// Setup navigation listeners
function setupNavigationListeners() {
    // Sidebar navigation
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const section = this.getAttribute('data-section');
            showSection(section);
            
            // Update active state
            navItems.forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');
            
            // Close sidebar on mobile
            if (window.innerWidth <= 768) {
                document.getElementById('sidebar').classList.remove('open');
            }
        });
    });
    
    // Bottom tab bar navigation (mobile)
    const tabItems = document.querySelectorAll('.tab-item');
    tabItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const section = this.getAttribute('data-section');
            showSection(section);
            
            // Update active state
            tabItems.forEach(tab => tab.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

// Toggle between login and register
function toggleAuth(type) {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const toggleBtns = document.querySelectorAll('.toggle-btn');
    
    toggleBtns.forEach(btn => btn.classList.remove('active'));
    
    if (type === 'login') {
        loginForm.classList.remove('hidden');
        registerForm.classList.add('hidden');
        toggleBtns[0].classList.add('active');
    } else {
        loginForm.classList.add('hidden');
        registerForm.classList.remove('hidden');
        toggleBtns[1].classList.add('active');
    }
}

// Handle login
async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        const response = await fetch(`${API_URL}/patients/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentUser = data.patient;
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
            updateUserDisplay();
            showSection('home');
            showToast('Login successful!', 'success');
        } else {
            showToast(data.error || 'Login failed', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showToast('Error connecting to server. Please make sure the backend is running.', 'error');
    }
}

// Handle registration
async function handleRegister(e) {
    e.preventDefault();
    
    const patientData = {
        name: document.getElementById('regName').value,
        email: document.getElementById('regEmail').value,
        phone: document.getElementById('regPhone').value,
        age: parseInt(document.getElementById('regAge').value),
        gender: document.getElementById('regGender').value,
        address: document.getElementById('regAddress').value,
        password: document.getElementById('regPassword').value
    };
    
    try {
        const response = await fetch(`${API_URL}/patients`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(patientData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showToast('Registration successful! Please login.', 'success');
            toggleAuth('login');
            document.getElementById('registerForm').reset();
        } else {
            showToast(data.error || 'Registration failed', 'error');
        }
    } catch (error) {
        console.error('Registration error:', error);
        showToast('Error connecting to server. Please make sure the backend is running.', 'error');
    }
}

// Logout
function logout() {
    currentUser = null;
    localStorage.removeItem('currentUser');
    showSection('login');
    showToast('Logged out successfully', 'info');
}

// Update user display in sidebar
function updateUserDisplay() {
    if (currentUser) {
        const sidebarName = document.getElementById('sidebarName');
        const sidebarAvatar = document.getElementById('sidebarAvatar');
        const welcomeName = document.getElementById('welcomeName');
        
        if (sidebarName) {
            sidebarName.textContent = currentUser.name;
        }
        if (sidebarAvatar) {
            sidebarAvatar.textContent = currentUser.name.charAt(0).toUpperCase();
        }
        if (welcomeName) {
            welcomeName.textContent = currentUser.name.split(' ')[0];
        }
    }
}

// Show section
function showSection(sectionName) {
    // Handle login section
    const loginSection = document.getElementById('loginSection');
    const mainShell = document.getElementById('mainShell');
    
    if (sectionName === 'login') {
        loginSection.classList.remove('hidden');
        loginSection.classList.add('active');
        mainShell.classList.add('hidden');
        return;
    }
    
    // Show main shell
    loginSection.classList.add('hidden');
    loginSection.classList.remove('active');
    mainShell.classList.remove('hidden');
    
    // Hide all sections in content area
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
        section.classList.add('hidden');
    });
    
    // Show selected section
    const section = document.getElementById(`${sectionName}Section`);
    if (section) {
        section.classList.remove('hidden');
        section.classList.add('active');
    }
    
    // Update navigation active state
    updateNavigationActive(sectionName);
    
    // Load section-specific data
    if (sectionName === 'home') {
        loadHealthTip();
        updateDateDisplay();
    } else if (sectionName === 'doctors') {
        loadDoctors();
    } else if (sectionName === 'medicines') {
        loadMedicines();
    } else if (sectionName === 'consultations') {
        loadConsultations();
    } else if (sectionName === 'followups') {
        loadFollowups();
    }
}

// Update navigation active state
function updateNavigationActive(sectionName) {
    // Update sidebar
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('data-section') === sectionName) {
            item.classList.add('active');
        }
    });
    
    // Update bottom tab bar
    const tabItems = document.querySelectorAll('.tab-item');
    tabItems.forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('data-section') === sectionName) {
            item.classList.add('active');
        }
    });
}

// Toggle sidebar (mobile)
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('open');
}

// Handle modal backdrop click
function handleModalBackdrop(event) {
    if (event.target.classList.contains('modal-overlay')) {
        event.target.classList.add('hidden');
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Load health tip
function loadHealthTip() {
    const tips = [
        "Drink at least 8 glasses of water daily to stay hydrated and maintain optimal body function.",
        "Get 7-8 hours of quality sleep every night to support your immune system and mental health.",
        "Exercise for at least 30 minutes daily to improve cardiovascular health and mood.",
        "Eat a balanced diet rich in fruits, vegetables, and whole grains for optimal nutrition.",
        "Take regular breaks from screens to reduce eye strain and improve focus.",
        "Practice mindfulness or meditation for 10 minutes daily to reduce stress.",
        "Wash your hands frequently to prevent the spread of infections.",
        "Get regular health check-ups to catch potential issues early."
    ];
    
    const tipElement = document.getElementById('healthTip');
    if (tipElement) {
        const randomTip = tips[Math.floor(Math.random() * tips.length)];
        tipElement.textContent = randomTip;
    }
}

// Refresh health tip
function refreshHealthTip() {
    loadHealthTip();
}

// Update date display
function updateDateDisplay() {
    const dateElement = document.getElementById('todayDate');
    if (dateElement) {
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        dateElement.textContent = new Date().toLocaleDateString('en-US', options);
    }
}

// Load doctors
async function loadDoctors() {
    try {
        const response = await fetch(`${API_URL}/doctors`);
        const doctors = await response.json();
        
        const doctorsList = document.getElementById('doctorsList');
        if (!doctorsList) return;
        
        doctorsList.innerHTML = '';
        
        if (doctors.length === 0) {
            doctorsList.innerHTML = '<p>No doctors available at the moment.</p>';
            return;
        }
        
        // Populate specialization filter
        const specFilter = document.getElementById('doctorSpecFilter');
        if (specFilter) {
            const specializations = [...new Set(doctors.map(d => d.specialization))];
            specFilter.innerHTML = '<option value="">All Specializations</option>';
            specializations.forEach(spec => {
                specFilter.innerHTML += `<option value="${spec}">${spec}</option>`;
            });
        }
        
        doctors.forEach(doctor => {
            const card = document.createElement('div');
            card.className = 'doctor-card';
            card.innerHTML = `
                <h3>${doctor.name}</h3>
                <p class="specialization">${doctor.specialization}</p>
                <p>Experience: ${doctor.experience_years} years</p>
                <p>Phone: ${doctor.phone}</p>
                <button onclick="openConsultationModal(${doctor.id}, '${doctor.name}')" class="btn btn-primary" style="margin-top: 1rem;">Request Consultation</button>
            `;
            doctorsList.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading doctors:', error);
        const doctorsList = document.getElementById('doctorsList');
        if (doctorsList) {
            doctorsList.innerHTML = '<p>Error loading doctors. Please try again later.</p>';
        }
    }
}

// Filter doctors
function filterDoctors() {
    const searchTerm = document.getElementById('doctorSearchInput').value.toLowerCase();
    const specFilter = document.getElementById('doctorSpecFilter').value;
    
    const cards = document.querySelectorAll('.doctor-card');
    cards.forEach(card => {
        const name = card.querySelector('h3').textContent.toLowerCase();
        const spec = card.querySelector('.specialization').textContent;
        
        const matchesSearch = name.includes(searchTerm) || spec.toLowerCase().includes(searchTerm);
        const matchesSpec = !specFilter || spec === specFilter;
        
        card.style.display = matchesSearch && matchesSpec ? 'block' : 'none';
    });
}

// Open consultation modal
function openConsultationModal(doctorId, doctorName) {
    if (!currentUser) {
        showToast('Please login to request a consultation', 'warning');
        showSection('login');
        return;
    }
    
    document.getElementById('selectedDoctorId').value = doctorId;
    document.getElementById('modalDoctorName').textContent = doctorName;
    document.getElementById('consultationModal').classList.remove('hidden');
}

// Close modal
function closeModal(modalId) {
    document.getElementById(modalId).classList.add('hidden');
}

// Handle consultation
async function handleConsultation(e) {
    e.preventDefault();
    
    const consultationData = {
        patient_id: currentUser.id,
        doctor_id: parseInt(document.getElementById('selectedDoctorId').value),
        symptoms: document.getElementById('symptoms').value
    };
    
    try {
        const response = await fetch(`${API_URL}/consultations`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(consultationData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showToast('Consultation request submitted successfully!', 'success');
            closeModal('consultationModal');
            document.getElementById('consultationForm').reset();
            showSection('consultations');
        } else {
            showToast(data.error || 'Failed to submit consultation request', 'error');
        }
    } catch (error) {
        console.error('Consultation error:', error);
        showToast('Error connecting to server. Please try again.', 'error');
    }
}

// Load medicines
async function loadMedicines() {
    try {
        const response = await fetch(`${API_URL}/pharmacies`);
        const pharmacies = await response.json();
        
        // Load medicines from first pharmacy
        if (pharmacies.length > 0) {
            const medResponse = await fetch(`${API_URL}/pharmacies/${pharmacies[0].id}/medicines`);
            const medicines = await medResponse.json();
            displayMedicines(medicines);
        }
    } catch (error) {
        console.error('Error loading medicines:', error);
        const medicinesList = document.getElementById('medicinesList');
        if (medicinesList) {
            medicinesList.innerHTML = '<p>Error loading medicines. Please try again later.</p>';
        }
    }
}

// Search medicines
async function searchMedicines() {
    const searchTerm = document.getElementById('medicineSearch').value;
    
    if (!searchTerm.trim()) {
        loadMedicines();
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/medicines/search?q=${encodeURIComponent(searchTerm)}`);
        const medicines = await response.json();
        displayMedicines(medicines);
    } catch (error) {
        console.error('Error searching medicines:', error);
        const medicinesList = document.getElementById('medicinesList');
        if (medicinesList) {
            medicinesList.innerHTML = '<p>Error searching medicines. Please try again later.</p>';
        }
    }
}

// Display medicines
function displayMedicines(medicines) {
    const medicinesList = document.getElementById('medicinesList');
    if (!medicinesList) return;
    
    medicinesList.innerHTML = '';
    
    if (medicines.length === 0) {
        medicinesList.innerHTML = '<p>No medicines found.</p>';
        return;
    }
    
    medicines.forEach(medicine => {
        const card = document.createElement('div');
        card.className = 'medicine-card';
        // Convert price to Indian Rupees (assuming $1 = ₹83)
        const priceInINR = (medicine.price * 83).toFixed(2);
        card.innerHTML = `
            <h3>${medicine.name}</h3>
            <p>${medicine.description || 'No description available'}</p>
            <p class="price">₹${priceInINR}</p>
            <p class="pharmacy">Available at: ${medicine.pharmacy_name}</p>
            <p class="pharmacy">📍 ${medicine.pharmacy_address}</p>
            <p class="pharmacy">📞 ${medicine.pharmacy_phone}</p>
            <p class="pharmacy">Stock: ${medicine.stock_quantity} units</p>
        `;
        medicinesList.appendChild(card);
    });
}

// Load consultations
async function loadConsultations() {
    if (!currentUser) {
        showSection('login');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/consultations/patient/${currentUser.id}`);
        const consultations = await response.json();
        
        const consultationsList = document.getElementById('consultationsList');
        if (!consultationsList) return;
        
        consultationsList.innerHTML = '';
        
        if (consultations.length === 0) {
            consultationsList.innerHTML = '<p>No consultations yet. <a href="#" onclick="showSection(\'doctors\')" style="color: #3b82f6;">Find a doctor</a></p>';
            return;
        }
        
        consultations.forEach(consultation => {
            const card = document.createElement('div');
            card.className = 'consultation-card';
            card.innerHTML = `
                <h3>Consultation #${consultation.id}</h3>
                <p><strong>Doctor:</strong> ${consultation.doctor_name} (${consultation.specialization})</p>
                <p><strong>Date:</strong> ${new Date(consultation.created_at).toLocaleString()}</p>
                <p><strong>Symptoms:</strong> ${consultation.symptoms}</p>
                <p><strong>Status:</strong> <span class="status ${consultation.status}">${consultation.status.replace('_', ' ')}</span></p>
                ${consultation.diagnosis ? `<p><strong>Diagnosis:</strong> ${consultation.diagnosis}</p>` : ''}
            `;
            consultationsList.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading consultations:', error);
        const consultationsList = document.getElementById('consultationsList');
        if (consultationsList) {
            consultationsList.innerHTML = '<p>Error loading consultations. Please try again later.</p>';
        }
    }
}

// Load follow-ups
async function loadFollowups() {
    if (!currentUser) {
        showSection('login');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/followups/patient/${currentUser.id}`);
        const followups = await response.json();
        
        const followupsList = document.getElementById('followupsList');
        if (!followupsList) return;
        
        followupsList.innerHTML = '';
        
        if (followups.length === 0) {
            followupsList.innerHTML = '<p>No follow-ups scheduled yet.</p>';
            return;
        }
        
        followups.forEach(followup => {
            const card = document.createElement('div');
            card.className = 'followup-card';
            card.innerHTML = `
                <h3>Follow-up #${followup.id}</h3>
                <p><strong>Doctor:</strong> ${followup.doctor_name}</p>
                <p><strong>Scheduled Date:</strong> ${new Date(followup.scheduled_date).toLocaleDateString()}</p>
                <p><strong>Status:</strong> <span class="status ${followup.status}">${followup.status}</span></p>
                ${followup.notes ? `<p><strong>Notes:</strong> ${followup.notes}</p>` : ''}
                ${followup.status === 'scheduled' ? `<button onclick="completeFollowup(${followup.id})" class="btn btn-success" style="margin-top: 0.5rem;">Mark as Completed</button>` : ''}
            `;
            followupsList.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading follow-ups:', error);
        const followupsList = document.getElementById('followupsList');
        if (followupsList) {
            followupsList.innerHTML = '<p>Error loading follow-ups. Please try again later.</p>';
        }
    }
}

// Complete follow-up
async function completeFollowup(followupId) {
    if (!confirm('Mark this follow-up as completed?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/followups/${followupId}/complete`, {
            method: 'PUT'
        });
        
        if (response.ok) {
            showToast('Follow-up marked as completed', 'success');
            loadFollowups();
        } else {
            showToast('Failed to update follow-up status', 'error');
        }
    } catch (error) {
        console.error('Error completing follow-up:', error);
        showToast('Error updating follow-up. Please try again.', 'error');
    }
}

// Start video call
function startVideoCall() {
    if (!currentUser) {
        showToast('Please login to start a video consultation', 'warning');
        showSection('login');
        return;
    }
    showToast('Video call feature coming soon! This will integrate with WebRTC for real-time video consultations.', 'info');
}

// Book lab test
function bookLabTest(testName, price) {
    if (!currentUser) {
        showToast('Please login to book a lab test', 'warning');
        showSection('login');
        return;
    }
    showToast(`Booking ${testName} for ₹${price}. This feature will be integrated with diagnostic centers.`, 'info');
}
