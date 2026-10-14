let pollInterval = null;
let currentAppName = 'Plex Token Generator';

function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0;
        var v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}


function handleAppSelect() {
    const select = document.getElementById('app-select');
    const customInput = document.getElementById('custom-app-name');
    if (select.value === 'other') {
        customInput.style.display = 'block';
        customInput.focus();
    } else {
        customInput.style.display = 'none';
    }
}

function getAppName() {
    const select = document.getElementById('app-select');
    const customInput = document.getElementById('custom-app-name');
    if (select.value === 'other') {
        return customInput.value.trim() || 'Plex Token Generator';
    }
    return select.value || 'Plex Token Generator';
}

function startAuth() {
    const btn = document.getElementById('auth-btn');
    const statusMsg = document.getElementById('status-message');
    const select = document.getElementById('app-select');
    const customInput = document.getElementById('custom-app-name');

    // Validate app selection
    if (!select.value) {
        statusMsg.className = 'error-box';
        statusMsg.style.display = 'block';
        statusMsg.textContent = 'Please select an app before continuing.';
        return;
    }
    if (select.value === 'other' && !customInput.value.trim()) {
        statusMsg.className = 'error-box';
        statusMsg.style.display = 'block';
        statusMsg.textContent = 'Please enter an app name.';
        return;
    }

    currentAppName = getAppName();

    const HEADERS = {
        'Accept': 'application/json',
        'X-Plex-Client-Identifier': generateUUID(),
        'X-Plex-Product': currentAppName,
        'X-Plex-Version': '1.2.0',
        'X-Plex-Platform': 'Web',
        'X-Plex-Platform-Version': '1.0',
        'X-Plex-Device': 'Browser',
        'X-Plex-Device-Name': 'Plex Token Generator'
    };

    btn.disabled = true;
    btn.textContent = 'Requesting PIN...';
    statusMsg.style.display = 'none';

    fetch('https://plex.tv/api/v2/pins?strong=true', { method: 'POST', headers: HEADERS })
    .then(function(res) { return res.json(); })
    .then(function(pin) {
        window._plexHeaders = HEADERS;

        const authUrl = 'https://app.plex.tv/auth#?' +
            'clientID=' + encodeURIComponent(HEADERS['X-Plex-Client-Identifier']) +
            '&code=' + encodeURIComponent(pin.code) +
            '&context%5Bdevice%5D%5Bproduct%5D=' + encodeURIComponent(currentAppName) +
            '&context%5Bdevice%5D%5Bplatform%5D=Web' +
            '&context%5Bdevice%5D%5BplatformVersion%5D=1.0' +
            '&context%5Bdevice%5D%5Bdevice%5D=Browser';

        // Show PIN and authorize link instead of auto-opening popup
        document.getElementById('pin-display').textContent = pin.code;
        document.getElementById('authorize-link').href = authUrl;
        document.getElementById('pin-container').style.display = 'block';
        btn.style.display = 'none';

        pollInterval = setInterval(function() { pollForToken(pin.id); }, 2000);

        setTimeout(function() {
            if (pollInterval) {
                clearInterval(pollInterval);
                pollInterval = null;
                document.getElementById('pin-container').style.display = 'none';
                statusMsg.className = 'error-box';
                statusMsg.style.display = 'block';
                statusMsg.textContent = 'Authentication timed out. Please try again.';
                btn.disabled = false;
                btn.style.display = 'inline-block';
                btn.textContent = 'Authenticate with Plex';
            }
        }, 300000);
    })
    .catch(function() {
        statusMsg.className = 'error-box';
        statusMsg.style.display = 'block';
        statusMsg.textContent = 'Failed to contact Plex. Please check your connection and try again.';
        btn.disabled = false;
        btn.textContent = 'Authenticate with Plex';
    });
}

function pollForToken(pinId) {
    fetch('https://plex.tv/api/v2/pins/' + pinId, { headers: window._plexHeaders })
    .then(function(res) { return res.json(); })
    .then(function(data) {
        if (data.authToken) {
            clearInterval(pollInterval);
            pollInterval = null;
            showResult(data.authToken);
        }
    })
    .catch(function(err) { console.error('Polling error:', err); });
}

function showResult(token) {
    document.getElementById('initial-view').style.display = 'none';
    document.getElementById('result-container').style.display = 'block';
    document.getElementById('token-box').textContent = token;
    document.getElementById('app-label').textContent = currentAppName;

    fetch('https://plex.tv/api/v2/user', {
        headers: Object.assign({}, window._plexHeaders, { 'X-Plex-Token': token })
    })
    .then(function(res) { return res.json(); })
    .then(function(user) {
        document.getElementById('username').textContent = user.username || 'N/A';
        document.getElementById('email').textContent = user.email || 'N/A';
        document.getElementById('userid').textContent = user.id || 'N/A';

        var sub = user.subscription || {};
        var plexPass = sub.active ? (user.subscriptionDescription || (sub.plan ? sub.plan.charAt(0).toUpperCase() + sub.plan.slice(1) : 'Active')) + ' ✓' : 'No';
        document.getElementById('plexpass').textContent = plexPass;
        if (sub.active) {
            document.getElementById('plexpass').style.color = '#4caf50';
        }

        if (user.joinedAt) {
            var date = new Date(user.joinedAt * 1000);
            document.getElementById('joinedat').textContent = date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
        } else {
            document.getElementById('joinedat').textContent = 'N/A';
        }

        if (user.thumb) {
            var avatar = document.getElementById('user-avatar');
            avatar.src = user.thumb;
            avatar.style.display = 'block';
        }
    })
    .catch(function() {
        document.getElementById('username').textContent = 'Authenticated';
        document.getElementById('email').textContent = 'N/A';
        document.getElementById('userid').textContent = 'N/A';
        document.getElementById('plexpass').textContent = 'N/A';
        document.getElementById('joinedat').textContent = 'N/A';
    });
}

function copyToken() {
    const token = document.getElementById('token-box').textContent;
    const copyStatus = document.getElementById('copy-status');
    const copyBtn = document.querySelector('.copy-btn');

    navigator.clipboard.writeText(token).then(function() {
        copyStatus.style.display = 'block';
        copyBtn.style.background = '#28a745';
        setTimeout(function() {
            copyStatus.style.display = 'none';
            copyBtn.style.background = '#e5a00d';
        }, 3000);
    }).catch(function() {
        const textarea = document.createElement('textarea');
        textarea.value = token;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        copyStatus.style.display = 'block';
        setTimeout(function() { copyStatus.style.display = 'none'; }, 3000);
    });
}

function resetPage() {
    document.getElementById('initial-view').style.display = 'block';
    document.getElementById('result-container').style.display = 'none';
    document.getElementById('pin-container').style.display = 'none';
    document.getElementById('auth-btn').disabled = false;
    document.getElementById('auth-btn').style.display = 'inline-block';
    document.getElementById('auth-btn').textContent = 'Authenticate with Plex';
    document.getElementById('status-message').style.display = 'none';
    document.getElementById('app-select').value = '';
    document.getElementById('custom-app-name').style.display = 'none';
    document.getElementById('custom-app-name').value = '';
}
