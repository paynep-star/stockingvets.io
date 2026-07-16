function toggleAuthModal() {
    const modal = document.getElementById('authModal');
    modal.style.display = modal.style.display === 'none' ? 'flex' : 'none';
}

function closeAuthModal() {
    document.getElementById('authModal').style.display = 'none';
}

function handleGoogleLogin() {
    if (window.google) {
        google.accounts.id.initialize({
            client_id: 'YOUR_GOOGLE_CLIENT_ID',
            callback: processGoogleLogin
        });
        google.accounts.id.renderButton(
            document.querySelector('.btn-google'),
            { theme: 'outline', size: 'large' }
        );
    }
}

async function processGoogleLogin(response) {
    try {
        const result = await api.googleLogin(response.credential);
        handleLoginSuccess(result);
    } catch (error) {
        alert('Google login failed: ' + error.message);
    }
}

function handleFacebookLogin() {
    alert('Facebook login - implement Facebook SDK');
}

function handleAppleLogin() {
    alert('Apple login - implement Apple Sign In');
}

async function handleEmailLogin() {
    const email = document.getElementById('emailInput').value;
    const password = document.getElementById('passwordInput').value;
    
    if (!email || !password) {
        alert('Please enter email and password');
        return;
    }
    
    try {
        const result = await api.login(email, password);
        handleLoginSuccess(result);
    } catch (error) {
        alert('Login failed: ' + error.message);
    }
}

function handleLoginSuccess(result) {
    localStorage.setItem('authToken', result.token);
    localStorage.setItem('userId', result.userId);
    localStorage.setItem('user', JSON.stringify(result.user));
    
    closeAuthModal();
    updateUIAfterLogin();
    
    if (!result.user.verified) {
        setTimeout(() => {
            document.getElementById('verificationModal').style.display = 'flex';
        }, 500);
    }
}

function showSignUpForm() {
    const modal = document.getElementById('authModal');
    const content = modal.querySelector('.modal-content');
    
    content.innerHTML = `
        <span class="close" onclick="closeAuthModal()">&times;</span>
        <h2>Create Account</h2>
        <input type="text" id="signupName" placeholder="Full Name" class="input-field">
        <input type="email" id="signupEmail" placeholder="Email" class="input-field">
        <input type="password" id="signupPassword" placeholder="Password" class="input-field">
        <input type="password" id="signupConfirm" placeholder="Confirm Password" class="input-field">
        <button class="btn-primary" onclick="handleSignUp()">Create Account</button>
        <button class="btn-secondary" onclick="toggleAuthModal()">Back to Login</button>
    `;
}

async function handleSignUp() {
    const name = document.getElementById('signupName').value;
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;
    const confirm = document.getElementById('signupConfirm').value;
    
    if (!name || !email || !password || !confirm) {
        alert('Please fill all fields');
        return;
    }
    
    if (password !== confirm) {
        alert('Passwords do not match');
        return;
    }
    
    try {
        const result = await api.signup({ name, email, password });
        handleLoginSuccess(result);
    } catch (error) {
        alert('Signup failed: ' + error.message);
    }
}

function updateUIAfterLogin() {
    const user = JSON.parse(localStorage.getItem('user'));
    document.getElementById('loginBtn').style.display = 'none';
    document.getElementById('profileBtn').style.display = 'inline';
}

function showProfile() {
    document.getElementById('profileModal').style.display = 'flex';
    loadProfileData();
}

function closeProfileModal() {
    document.getElementById('profileModal').style.display = 'none';
}

async function loadProfileData() {
    try {
        const user = JSON.parse(localStorage.getItem('user'));
        const verificationStatus = await api.getVerificationStatus();
        
        const profileInfo = document.getElementById('profileInfo');
        profileInfo.innerHTML = `
            <p><strong>Name:</strong> ${user.name}</p>
            <p><strong>Email:</strong> ${user.email}</p>
            <p><strong>Verification Status:</strong> ${verificationStatus.status}</p>
            <p><strong>Member Since:</strong> ${new Date(user.createdAt).toLocaleDateString()}</p>
            <p><strong>Account Balance:</strong> $${user.balance?.toFixed(2) || '0.00'}</p>
        `;
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

function editProfile() {
    alert('Edit profile - implement edit form');
}

function logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userId');
    localStorage.removeItem('user');
    
    document.getElementById('loginBtn').style.display = 'inline';
    document.getElementById('profileBtn').style.display = 'none';
    closeProfileModal();
    location.reload();
}

function closeVerificationModal() {
    document.getElementById('verificationModal').style.display = 'none';
}

async function submitVerification() {
    const idFile = document.getElementById('idUpload').files[0];
    const inputs = document.querySelectorAll('.verification-section input');
    
    const verificationData = {
        fullName: inputs[0].value,
        dateOfBirth: inputs[1].value,
        twitter: inputs[2].value,
        discord: inputs[3].value,
        linkedin: inputs[4].value,
        idFile: idFile
    };
    
    if (!verificationData.fullName || !verificationData.dateOfBirth || !idFile) {
        alert('Please complete all required fields');
        return;
    }
    
    try {
        await api.submitVerification(verificationData);
        alert('Verification submitted! Please wait for approval.');
        closeVerificationModal();
    } catch (error) {
        alert('Verification submission failed: ' + error.message);
    }
}

window.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('authToken');
    if (token) {
        updateUIAfterLogin();
    }
});